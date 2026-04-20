import folium
import json
from datetime import datetime
from html import escape as html_escape
from folium.plugins import MarkerCluster, HeatMap


DISASTER_COLORS = {
    "Earthquake": "#ff4444",
    "Volcanic Eruption": "#ff6600",
    "Wildfire": "#ff8800",
    "Storm": "#4488ff",
    "Flood": "#0066cc",
    "Tsunami": "#003399",
    "Drought": "#cc8800",
    "Extreme Temperature": "#cc0000",
    "Landslide": "#885500",
    "Snow/Ice": "#88ccff",
    "Dust/Haze": "#999966",
    "Water Quality": "#669999",
    "Sea/Lake Ice": "#aaddee",
    "Abandoned Mine": "#8B4513",
    "Active Mine": "#ff6b35",
    "Rare Earth Mine": "#9b59b6",
}

DISASTER_ICONS = {
    "Earthquake": "globe",
    "Volcanic Eruption": "fire",
    "Wildfire": "fire",
    "Storm": "cloud",
    "Flood": "tint",
    "Tsunami": "exclamation-sign",
    "Drought": "grain",
    "Extreme Temperature": "certificate",
    "Landslide": "download",
    "Snow/Ice": "asterisk",
    "Dust/Haze": "eye-close",
    "Water Quality": "tint",
    "Sea/Lake Ice": "asterisk",
    "Abandoned Mine": "warning-sign",
    "Active Mine": "cog",
    "Rare Earth Mine": "star",
}


def _folium_color(hex_color):
    cmap = {
        "#ff4444": "red", "#ff6600": "orange", "#ff8800": "orange",
        "#4488ff": "blue", "#0066cc": "blue", "#003399": "darkblue",
        "#cc8800": "orange", "#cc0000": "darkred", "#885500": "beige",
        "#88ccff": "lightblue", "#999966": "gray", "#669999": "cadetblue",
        "#aaddee": "lightblue",
        "#8B4513": "darkred", "#ff6b35": "orange", "#9b59b6": "purple",
    }
    return cmap.get(hex_color, "blue")


def _severity_radius(event):
    mag = event.get("magnitude", 0) or 0
    sev = event.get("severity", "Moderate")
    if mag > 0:
        return max(5, min(20, mag * 2.5))
    sev_map = {"Critical": 14, "High": 10, "Moderate": 7, "Low": 5}
    return sev_map.get(sev, 7)


def create_global_map(events, selected_types=None, height=600):
    m = folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles=None,
        control_scale=True,
        prefer_canvas=True
    )

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://carto.com/">CARTO</a>',
        name="Dark",
        control=False
    ).add_to(m)

    popup_css = """
    <style>
    .leaflet-popup-content-wrapper {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        border-radius: 12px !important;
    }
    .leaflet-popup-content {
        margin: 0 !important;
        border-radius: 12px !important;
    }
    .leaflet-popup-tip-container { display: none !important; }
    .leaflet-popup-close-button {
        color: #a8aab1 !important;
        font-size: 18px !important;
        top: 6px !important;
        right: 8px !important;
        z-index: 10;
    }
    .leaflet-popup-close-button:hover { color: #ff4444 !important; }
    .leaflet-tooltip {
        background: rgba(0,20,40,0.92) !important;
        border: 1px solid rgba(95,184,255,0.4) !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-size: 0.78rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.6) !important;
    }
    .leaflet-tooltip-top:before,
    .leaflet-tooltip-bottom:before,
    .leaflet-tooltip-left:before,
    .leaflet-tooltip-right:before { display: none !important; }
    </style>
    """
    m.get_root().html.add_child(folium.Element(popup_css))

    heat_data = []
    severity_order = {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1}

    sorted_events = sorted(events, key=lambda e: severity_order.get(e.get("severity", "Low"), 0))

    for event in sorted_events:
        if selected_types and event.get("type") not in selected_types:
            continue
        lat = event.get("lat", 0)
        lon = event.get("lon", 0)
        if lat == 0 and lon == 0:
            continue

        color = DISASTER_COLORS.get(event.get("type", ""), "#ffffff")
        radius = _severity_radius(event)

        sev = event.get("severity", "N/A")
        sev_colors = {"Critical": "#ff4444", "High": "#ff8800", "Moderate": "#ffcc00", "Low": "#88dd44"}
        sev_color = sev_colors.get(sev, "#aaaaaa")
        dtype = event.get("type", "Unknown")
        title = event.get("title", "")
        source = event.get("source", "")
        country = event.get("country", "")

        rows = ""
        if event.get("magnitude"):
            rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Magnitude</td><td style='color:#fff;font-weight:600;'>{event['magnitude']}</td></tr>"
        if event.get("depth"):
            rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Depth</td><td style='color:#fff;'>{event['depth']:.1f} km</td></tr>"
        if event.get("time"):
            t = event["time"]
            tstr = t.strftime("%Y-%m-%d %H:%M UTC") if hasattr(t, "strftime") else str(t)[:16]
            rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Time</td><td style='color:#fff;'>{tstr}</td></tr>"
        if country:
            rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Location</td><td style='color:#9be8a8;'>{country}</td></tr>"
        rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Coords</td><td style='color:#a8aab1;font-size:0.78rem;'>{lat:.2f}°, {lon:.2f}°</td></tr>"
        if source:
            rows += f"<tr><td style='color:#a8aab1;padding:3px 8px 3px 0;'>Source</td><td style='color:#5fb8ff;font-size:0.78rem;'>{source}</td></tr>"

        popup_html = f"""
<div style="
  font-family:'Inter',Arial,sans-serif;
  background:rgba(0,20,40,0.97);
  border:1px solid {color};
  border-radius:12px;
  min-width:240px;
  max-width:300px;
  padding:0;
  overflow:hidden;
  box-shadow:0 8px 32px rgba(0,0,0,0.7);
">
  <div style="background:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.18);padding:10px 14px 8px 14px;border-bottom:1px solid rgba(255,255,255,0.08);">
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">
      <span style="
        display:inline-block;width:10px;height:10px;border-radius:50%;
        background:{color};box-shadow:0 0 8px {color};flex-shrink:0;
      "></span>
      <span style="color:{color};font-size:0.72rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">{dtype}</span>
      <span style="
        margin-left:auto;background:{sev_color}22;color:{sev_color};
        border:1px solid {sev_color};border-radius:4px;
        font-size:0.65rem;font-weight:700;padding:1px 6px;letter-spacing:0.08em;
      ">{sev}</span>
    </div>
    <div style="color:#ffffff;font-size:0.84rem;font-weight:600;line-height:1.35;">{title[:90]}{"…" if len(title)>90 else ""}</div>
  </div>
  <div style="padding:8px 14px 10px 14px;">
    <table style="width:100%;border-collapse:collapse;font-size:0.78rem;">
      {rows}
    </table>
  </div>
</div>"""

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.65,
            weight=1.5,
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=folium.Tooltip(
                f"<span style='font-family:Inter,Arial,sans-serif;font-size:0.8rem;'>"
                f"<b style='color:{color};'>{dtype}</b> — {title[:55]}{'…' if len(title)>55 else ''}</span>",
                sticky=False
            )
        ).add_to(m)

        weight = 1
        if event.get("magnitude"):
            weight = (event["magnitude"] or 1) / 2
        elif sev == "Critical":
            weight = 3
        elif sev == "High":
            weight = 2
        heat_data.append([lat, lon, weight])

    if heat_data:
        HeatMap(
            heat_data, radius=25, blur=20, max_zoom=8,
            gradient={0.2: '#0000ff', 0.4: '#00ff00', 0.6: '#ffff00', 0.8: '#ff8800', 1.0: '#ff0000'}
        ).add_to(m)

    return m


def create_country_map(lat, lon, events=None, zoom=5):
    m = folium.Map(
        location=[lat, lon],
        zoom_start=zoom,
        tiles=None,
        control_scale=True
    )

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; CARTO',
        name="Dark",
        control=False
    ).add_to(m)

    _dark_popup_css = """
    <style>
    .leaflet-popup-content-wrapper {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        border-radius: 12px !important;
    }
    .leaflet-popup-content { margin: 0 !important; border-radius: 12px !important; }
    .leaflet-popup-tip-container { display: none !important; }
    .leaflet-popup-close-button { color: #a8aab1 !important; font-size: 18px !important; top: 6px !important; right: 8px !important; }
    .leaflet-popup-close-button:hover { color: #ff4444 !important; }
    .leaflet-tooltip {
        background: rgba(0,20,40,0.92) !important;
        border: 1px solid rgba(95,184,255,0.4) !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-size: 0.78rem !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.6) !important;
    }
    .leaflet-tooltip-top:before, .leaflet-tooltip-bottom:before,
    .leaflet-tooltip-left:before, .leaflet-tooltip-right:before { display: none !important; }
    </style>
    """
    m.get_root().html.add_child(folium.Element(_dark_popup_css))

    if events:
        for event in events:
            elat = event.get("lat", 0)
            elon = event.get("lon", 0)
            if elat == 0 and elon == 0:
                continue
            color = DISASTER_COLORS.get(event.get("type", ""), "#ffffff")
            radius = _severity_radius(event)
            sev = event.get("severity", "N/A")
            sev_colors = {"Critical": "#ff4444", "High": "#ff8800", "Moderate": "#ffcc00", "Low": "#88dd44"}
            sev_color = sev_colors.get(sev, "#aaaaaa")
            dtype = event.get("type", "Unknown")
            title = event.get("title", "")
            country = event.get("country", "")
            source = event.get("source", "")

            rows = ""
            if event.get("magnitude"):
                rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.76rem;'>Magnitude</td><td style='color:#fff;font-weight:600;font-size:0.76rem;'>{event['magnitude']}</td></tr>"
            if event.get("depth"):
                rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.76rem;'>Depth</td><td style='color:#fff;font-size:0.76rem;'>{event['depth']:.1f} km</td></tr>"
            if event.get("time"):
                t = event["time"]
                tstr = t.strftime("%Y-%m-%d %H:%M UTC") if hasattr(t, "strftime") else str(t)[:16]
                rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.76rem;'>Time</td><td style='color:#fff;font-size:0.76rem;'>{tstr}</td></tr>"
            if country:
                rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.76rem;'>Country</td><td style='color:#9be8a8;font-size:0.76rem;'>{country}</td></tr>"
            rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.72rem;'>Coords</td><td style='color:#a8aab1;font-size:0.72rem;'>{elat:.2f}°, {elon:.2f}°</td></tr>"
            if source:
                rows += f"<tr><td style='color:#a8aab1;padding:2px 8px 2px 0;font-size:0.72rem;'>Source</td><td style='color:#5fb8ff;font-size:0.72rem;'>{source}</td></tr>"

            popup_html = f"""<div style="font-family:'Inter',Arial,sans-serif;background:rgba(0,20,40,0.97);border:1px solid {color};border-radius:12px;min-width:220px;max-width:280px;padding:0;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.7);">
  <div style="background:rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.18);padding:9px 13px 7px 13px;border-bottom:1px solid rgba(255,255,255,0.08);">
    <div style="display:flex;align-items:center;gap:7px;margin-bottom:3px;">
      <span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{color};box-shadow:0 0 7px {color};flex-shrink:0;"></span>
      <span style="color:{color};font-size:0.7rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;">{dtype}</span>
      <span style="margin-left:auto;background:{sev_color}22;color:{sev_color};border:1px solid {sev_color};border-radius:4px;font-size:0.62rem;font-weight:700;padding:1px 5px;">{sev}</span>
    </div>
    <div style="color:#fff;font-size:0.82rem;font-weight:600;line-height:1.3;">{title[:80]}{"…" if len(title)>80 else ""}</div>
  </div>
  <div style="padding:7px 13px 9px 13px;"><table style="width:100%;border-collapse:collapse;">{rows}</table></div>
</div>"""

            folium.CircleMarker(
                location=[elat, elon],
                radius=radius,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=1.5,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=folium.Tooltip(
                    f"<span style='font-family:Inter,Arial,sans-serif;font-size:0.78rem;'><b style='color:{color};'>{dtype}</b> — {title[:50]}{'…' if len(title)>50 else ''}</span>",
                    sticky=False
                )
            ).add_to(m)

    return m


def get_disaster_color(disaster_type):
    return DISASTER_COLORS.get(disaster_type, "#ffffff")


def create_rotating_globe_html(events, selected_types=None, height=600):
    filtered = list(events)
    if selected_types:
        filtered = [e for e in filtered if e.get("type") in selected_types]
    filtered = [e for e in filtered if not (e.get("lat", 0) == 0 and e.get("lon", 0) == 0)]

    if not filtered:
        return f'<div style="height:{height}px;background:#000010;display:flex;align-items:center;justify-content:center;color:#ffffff;font-family:Courier New;">No events to display</div>'

    # Cap at 800 points for performance; prioritise critical/high severity
    sev_order = {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1}
    filtered = sorted(filtered, key=lambda e: sev_order.get(e.get("severity", "Low"), 0), reverse=True)[:800]

    points = []
    for e in filtered:
        mag = e.get("magnitude", 0) or 0
        if mag > 0:
            radius = max(0.3, min(1.2, mag * 0.15))
            altitude = max(0.01, min(0.12, mag * 0.012))
        else:
            sev_map = {"Critical": (0.9, 0.09), "High": (0.7, 0.06), "Moderate": (0.5, 0.04), "Low": (0.3, 0.02)}
            radius, altitude = sev_map.get(e.get("severity", "Moderate"), (0.5, 0.04))

        title = str(e.get("title", "") or "").replace("\n", " ")
        dtype = str(e.get("type", "Unknown") or "")
        sev = str(e.get("severity", "N/A") or "N/A")

        if not selected_types:
            nearby = [ev for ev in filtered
                      if abs(ev.get("lat", 0) - e.get("lat", 0)) < 5
                      and abs(ev.get("lon", 0) - e.get("lon", 0)) < 5]
            tc = {}
            for ne in nearby:
                t = ne.get("type", "Unknown")
                tc[t] = tc.get(t, 0) + 1
            lines = [
                f"<b style='color:#4fc3f7;font-size:13px;'>{html_escape(dtype)}</b>",
                f"<b>{html_escape(title[:80])}</b>",
                "<hr style='border-color:#333;margin:5px 0;'>",
                "<span style='color:#4fc3f7;'>Area Summary:</span>"
            ]
            for t, c in sorted(tc.items(), key=lambda x: x[1], reverse=True):
                tcolor = DISASTER_COLORS.get(t, "#fff")
                lines.append(f"<span style='color:{tcolor};'>&#9679;</span> {html_escape(t)}: <b>{c}</b>")
            lines.append(f"<hr style='border-color:#333;margin:5px 0;'>Total: <b>{len(nearby)}</b> events nearby")
            popup = "<br>".join(lines)
        else:
            sev_colors_map = {"Critical": "#ff0000", "High": "#ff6600", "Moderate": "#ffaa00", "Low": "#88cc00"}
            sc = sev_colors_map.get(sev, "#fff")
            lines = [
                f"<b style='color:#4fc3f7;font-size:13px;'>{html_escape(dtype)}</b>",
                f"<b>{html_escape(title[:80])}</b>",
                f"Severity: <b style='color:{sc};'>{html_escape(sev)}</b>"
            ]
            if e.get("magnitude"):
                lines.append(f"Magnitude: <b>{html_escape(str(e['magnitude']))}</b>")
            if e.get("depth"):
                lines.append(f"Depth: <b>{e['depth']:.1f} km</b>")
            if e.get("time") and isinstance(e["time"], datetime):
                lines.append(f"Time: {e['time'].strftime('%Y-%m-%d %H:%M UTC')}")
            popup = "<br>".join(lines)

        points.append({
            "lat": e.get("lat", 0),
            "lng": e.get("lon", 0),
            "color": DISASTER_COLORS.get(e.get("type", ""), "#ffffff"),
            "radius": radius,
            "altitude": altitude,
            "label": html_escape(f"{dtype}: {title[:60]}"),
            "popup": popup
        })

    points_js = json.dumps(points)

    # Pulsing rings on top severity events (max 35 for performance)
    ring_points = []
    for p in points[:35]:
        ring_points.append({
            'lat': p['lat'],
            'lng': p['lng'],
            'color': p['color']
        })
    rings_js = json.dumps(ring_points)

    html = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:{height}px;overflow:hidden;background:#000010;font-family:'Courier New',Courier,monospace}}
#globeViz{{width:100%;height:{height}px}}
#info-popup{{
  display:none;position:absolute;top:16px;right:16px;
  background:rgba(10,14,23,0.96);border:1px solid #4fc3f7;
  border-radius:10px;padding:14px 18px;color:#ffffff;
  font-family:'Courier New',Courier,monospace;font-size:12px;
  max-width:300px;min-width:200px;z-index:1000;
  box-shadow:0 8px 32px rgba(0,0,0,0.8);line-height:1.6;
  max-height:{height - 60}px;overflow-y:auto;
}}
#info-popup::-webkit-scrollbar{{width:4px}}
#info-popup::-webkit-scrollbar-thumb{{background:#4fc3f7;border-radius:2px}}
.close-btn{{position:absolute;top:6px;right:10px;cursor:pointer;color:#4fc3f7;font-size:16px;font-weight:bold;line-height:1}}
.close-btn:hover{{color:#ff4444}}
#rotation-status{{
  position:absolute;bottom:12px;left:12px;color:#ffffff;
  font-size:11px;font-family:'Courier New',monospace;cursor:pointer;
  padding:4px 10px;background:rgba(10,14,23,0.8);border-radius:6px;
  border:1px solid rgba(79,195,247,0.4);user-select:none;
}}
#rotation-status:hover{{color:#4fc3f7;border-color:#4fc3f7}}
</style>
</head><body>
<div style="position:relative;width:100%;height:{height}px;">
  <div id="globeViz"></div>
  <div id="info-popup">
    <span class="close-btn" onclick="document.getElementById('info-popup').style.display='none'">&times;</span>
    <div id="popup-content"></div>
  </div>
  <div id="rotation-status" onclick="toggleRotation()">&#10227; Rotating</div>
</div>
<script src="https://unpkg.com/globe.gl@2.41.6/dist/globe.gl.min.js"></script>
<script>
var pointsData = {points_js};
var ringsData = {rings_js};
var rotating = true;

function hexToRgba(hex, a) {{
  if (!hex) return 'rgba(255,255,255,'+a+')';
  var c = hex.replace('#','');
  if (c.length === 3) c = c[0]+c[0]+c[1]+c[1]+c[2]+c[2];
  var r = parseInt(c.substr(0,2),16);
  var g = parseInt(c.substr(2,2),16);
  var b = parseInt(c.substr(4,2),16);
  return 'rgba('+r+','+g+','+b+','+a+')';
}}

var countryLabels = [
  {{lat:37.1,lng:-95.7,text:"UNITED STATES",tier:"country"}},
  {{lat:-14.2,lng:-51.9,text:"BRAZIL",tier:"country"}},
  {{lat:61.5,lng:105.3,text:"RUSSIA",tier:"country"}},
  {{lat:35.9,lng:104.2,text:"CHINA",tier:"country"}},
  {{lat:20.6,lng:78.9,text:"INDIA",tier:"country"}},
  {{lat:-25.3,lng:133.8,text:"AUSTRALIA",tier:"country"}},
  {{lat:56.1,lng:-106.4,text:"CANADA",tier:"country"}},
  {{lat:23.6,lng:-102.6,text:"MEXICO",tier:"country"}},
  {{lat:-38.4,lng:-63.6,text:"ARGENTINA",tier:"country"}},
  {{lat:9.1,lng:8.7,text:"NIGERIA",tier:"country"}},
  {{lat:26.8,lng:30.8,text:"EGYPT",tier:"country"}},
  {{lat:-30.6,lng:22.9,text:"SOUTH AFRICA",tier:"country"}},
  {{lat:36.2,lng:138.3,text:"JAPAN",tier:"country"}},
  {{lat:-0.8,lng:113.9,text:"INDONESIA",tier:"country"}},
  {{lat:51.2,lng:10.5,text:"GERMANY",tier:"country"}},
  {{lat:46.2,lng:2.2,text:"FRANCE",tier:"country"}},
  {{lat:55.4,lng:-3.4,text:"UK",tier:"country"}},
  {{lat:41.9,lng:12.6,text:"ITALY",tier:"country"}},
  {{lat:40.5,lng:-3.7,text:"SPAIN",tier:"country"}},
  {{lat:39.0,lng:35.2,text:"TURKEY",tier:"country"}},
  {{lat:32.4,lng:53.7,text:"IRAN",tier:"country"}},
  {{lat:23.9,lng:45.1,text:"SAUDI ARABIA",tier:"country"}},
  {{lat:30.4,lng:69.3,text:"PAKISTAN",tier:"country"}},
  {{lat:4.6,lng:-74.3,text:"COLOMBIA",tier:"country"}},
  {{lat:-9.2,lng:-75.0,text:"PERU",tier:"country"}},
  {{lat:-35.7,lng:-71.5,text:"CHILE",tier:"country"}},
  {{lat:-0.02,lng:37.9,text:"KENYA",tier:"country"}},
  {{lat:9.2,lng:40.5,text:"ETHIOPIA",tier:"country"}},
  {{lat:-4.0,lng:21.8,text:"DR CONGO",tier:"country"}},
  {{lat:15.9,lng:100.5,text:"THAILAND",tier:"country"}},
  {{lat:12.9,lng:121.8,text:"PHILIPPINES",tier:"country"}},
  {{lat:14.1,lng:108.3,text:"VIETNAM",tier:"country"}},
  {{lat:4.2,lng:108.0,text:"MALAYSIA",tier:"country"}},
  {{lat:23.7,lng:90.4,text:"BANGLADESH",tier:"country"}},
  {{lat:21.9,lng:96.0,text:"MYANMAR",tier:"country"}},
  {{lat:28.4,lng:84.1,text:"NEPAL",tier:"country"}},
  {{lat:33.9,lng:67.7,text:"AFGHANISTAN",tier:"country"}},
  {{lat:12.9,lng:77.5,text:"SRI LANKA",tier:"country"}},
  {{lat:46.0,lng:14.5,text:"EUROPE",tier:"country"}},
  {{lat:-20.3,lng:57.6,text:"MAURITIUS",tier:"country"}},
  {{lat:-6.3,lng:143.9,text:"PAPUA NEW GUINEA",tier:"country"}},
  {{lat:-17.7,lng:178.0,text:"FIJI",tier:"country"}},
  {{lat:17.2,lng:-61.8,text:"CARIBBEAN",tier:"country"}},
  {{lat:1.4,lng:38.0,text:"SOMALIA",tier:"country"}},
  {{lat:14.6,lng:-14.5,text:"SENEGAL",tier:"country"}},
  {{lat:12.6,lng:-8.0,text:"MALI",tier:"country"}},
  {{lat:15.2,lng:19.0,text:"CHAD",tier:"country"}},
  {{lat:16.0,lng:8.0,text:"NIGER",tier:"country"}},
  {{lat:5.5,lng:-3.0,text:"GHANA",tier:"country"}},
  {{lat:-1.3,lng:36.8,text:"TANZANIA",tier:"country"}},
  {{lat:1.0,lng:32.0,text:"UGANDA",tier:"country"}},
  {{lat:-13.0,lng:34.0,text:"MALAWI",tier:"country"}},
  {{lat:-18.7,lng:35.5,text:"MOZAMBIQUE",tier:"country"}},
  {{lat:-29.0,lng:28.2,text:"LESOTHO",tier:"country"}},
  {{lat:12.1,lng:15.0,text:"CAMEROON",tier:"country"}},
  {{lat:6.4,lng:2.4,text:"BENIN",tier:"country"}},
  {{lat:-15.4,lng:28.3,text:"ZAMBIA",tier:"country"}},
  {{lat:-20.0,lng:23.8,text:"BOTSWANA",tier:"country"}},
  {{lat:52.0,lng:20.0,text:"POLAND",tier:"country"}},
  {{lat:50.1,lng:14.4,text:"CZECHIA",tier:"country"}},
  {{lat:47.2,lng:19.5,text:"HUNGARY",tier:"country"}},
  {{lat:45.9,lng:24.9,text:"ROMANIA",tier:"country"}},
  {{lat:60.5,lng:8.0,text:"NORWAY",tier:"country"}},
  {{lat:60.1,lng:18.6,text:"SWEDEN",tier:"country"}},
  {{lat:64.0,lng:26.0,text:"FINLAND",tier:"country"}},
  {{lat:55.7,lng:12.6,text:"DENMARK",tier:"country"}},
  {{lat:52.1,lng:5.3,text:"NETHERLANDS",tier:"country"}},
  {{lat:50.8,lng:4.5,text:"BELGIUM",tier:"country"}},
  {{lat:47.4,lng:8.5,text:"SWITZERLAND",tier:"country"}},
  {{lat:47.5,lng:14.5,text:"AUSTRIA",tier:"country"}},
  {{lat:55.3,lng:23.9,text:"LITHUANIA",tier:"country"}},
  {{lat:56.9,lng:24.6,text:"LATVIA",tier:"country"}},
  {{lat:59.4,lng:24.8,text:"ESTONIA",tier:"country"}},
  {{lat:53.9,lng:27.6,text:"BELARUS",tier:"country"}},
  {{lat:48.4,lng:31.2,text:"UKRAINE",tier:"country"}},
  {{lat:42.3,lng:43.4,text:"GEORGIA",tier:"country"}},
  {{lat:40.1,lng:47.6,text:"AZERBAIJAN",tier:"country"}},
  {{lat:40.5,lng:45.0,text:"ARMENIA",tier:"country"}},
  {{lat:33.2,lng:43.7,text:"IRAQ",tier:"country"}},
  {{lat:33.9,lng:35.9,text:"LEBANON",tier:"country"}},
  {{lat:31.9,lng:35.9,text:"JORDAN",tier:"country"}},
  {{lat:25.0,lng:51.2,text:"QATAR",tier:"country"}},
  {{lat:24.4,lng:54.4,text:"UAE",tier:"country"}},
  {{lat:22.0,lng:58.0,text:"OMAN",tier:"country"}},
  {{lat:15.6,lng:48.5,text:"YEMEN",tier:"country"}},
  {{lat:26.2,lng:50.6,text:"BAHRAIN",tier:"country"}},
  {{lat:29.3,lng:48.0,text:"KUWAIT",tier:"country"}},
  {{lat:34.0,lng:9.0,text:"TUNISIA",tier:"country"}},
  {{lat:28.0,lng:2.6,text:"ALGERIA",tier:"country"}},
  {{lat:32.0,lng:-5.0,text:"MOROCCO",tier:"country"}},
  {{lat:5.0,lng:-1.0,text:"IVORY COAST",tier:"country"}},
  {{lat:4.0,lng:10.0,text:"EQUATORIAL GUINEA",tier:"country"}},
  {{lat:1.5,lng:10.3,text:"GABON",tier:"country"}},
  {{lat:-4.0,lng:15.3,text:"CONGO",tier:"country"}},
  {{lat:6.4,lng:-9.4,text:"LIBERIA",tier:"country"}},
  {{lat:8.5,lng:-11.8,text:"SIERRA LEONE",tier:"country"}},
  {{lat:11.8,lng:-15.2,text:"GUINEA-BISSAU",tier:"country"}},
  {{lat:11.7,lng:-15.9,text:"GUINEA",tier:"country"}},
  {{lat:12.4,lng:-11.8,text:"GUINEA",tier:"country"}},
  {{lat:15.5,lng:-14.5,text:"MAURITANIA",tier:"country"}},
  {{lat:14.7,lng:-17.4,text:"GAMBIA",tier:"country"}},
];

var stateLabels = [
  {{lat:40.7,lng:-74.0,text:"New York",tier:"state"}},
  {{lat:34.0,lng:-118.2,text:"California",tier:"state"}},
  {{lat:41.8,lng:-87.6,text:"Illinois",tier:"state"}},
  {{lat:29.7,lng:-95.4,text:"Texas",tier:"state"}},
  {{lat:33.4,lng:-112.1,text:"Arizona",tier:"state"}},
  {{lat:47.6,lng:-122.3,text:"Washington",tier:"state"}},
  {{lat:45.5,lng:-122.7,text:"Oregon",tier:"state"}},
  {{lat:39.7,lng:-104.9,text:"Colorado",tier:"state"}},
  {{lat:30.3,lng:-81.7,text:"Florida",tier:"state"}},
  {{lat:33.7,lng:-84.4,text:"Georgia",tier:"state"}},
  {{lat:35.2,lng:-80.8,text:"N Carolina",tier:"state"}},
  {{lat:37.5,lng:-77.4,text:"Virginia",tier:"state"}},
  {{lat:39.3,lng:-76.6,text:"Maryland",tier:"state"}},
  {{lat:42.4,lng:-71.1,text:"Massachusetts",tier:"state"}},
  {{lat:44.3,lng:-89.8,text:"Wisconsin",tier:"state"}},
  {{lat:46.9,lng:-110.4,text:"Montana",tier:"state"}},
  {{lat:44.0,lng:-120.5,text:"Oregon",tier:"state"}},
  {{lat:43.5,lng:-116.2,text:"Idaho",tier:"state"}},
  {{lat:40.7,lng:-111.9,text:"Utah",tier:"state"}},
  {{lat:46.9,lng:-100.8,text:"N Dakota",tier:"state"}},
  {{lat:44.4,lng:-100.3,text:"S Dakota",tier:"state"}},
  {{lat:41.1,lng:-98.3,text:"Nebraska",tier:"state"}},
  {{lat:38.5,lng:-98.4,text:"Kansas",tier:"state"}},
  {{lat:35.5,lng:-97.5,text:"Oklahoma",tier:"state"}},
  {{lat:32.7,lng:-92.8,text:"Louisiana",tier:"state"}},
  {{lat:32.8,lng:-89.4,text:"Mississippi",tier:"state"}},
  {{lat:34.8,lng:-92.7,text:"Arkansas",tier:"state"}},
  {{lat:36.2,lng:-86.7,text:"Tennessee",tier:"state"}},
  {{lat:38.2,lng:-84.9,text:"Kentucky",tier:"state"}},
  {{lat:39.9,lng:-82.7,text:"Ohio",tier:"state"}},
  {{lat:40.3,lng:-86.1,text:"Indiana",tier:"state"}},
  {{lat:44.3,lng:-85.4,text:"Michigan",tier:"state"}},
  {{lat:46.4,lng:-93.1,text:"Minnesota",tier:"state"}},
  {{lat:41.6,lng:-93.6,text:"Iowa",tier:"state"}},
  {{lat:38.6,lng:-90.2,text:"Missouri",tier:"state"}},
  {{lat:39.0,lng:-105.6,text:"Colorado",tier:"state"}},
  {{lat:36.1,lng:-119.7,text:"California",tier:"state"}},
  {{lat:63.0,lng:-153.0,text:"Alaska",tier:"state"}},
  {{lat:20.5,lng:-157.0,text:"Hawaii",tier:"state"}},
  {{lat:27.8,lng:85.3,text:"Kathmandu",tier:"state"}},
  {{lat:28.7,lng:77.1,text:"Delhi",tier:"state"}},
  {{lat:19.1,lng:72.9,text:"Maharashtra",tier:"state"}},
  {{lat:13.1,lng:80.3,text:"Tamil Nadu",tier:"state"}},
  {{lat:22.6,lng:88.4,text:"West Bengal",tier:"state"}},
  {{lat:26.1,lng:85.3,text:"Bihar",tier:"state"}},
  {{lat:26.9,lng:80.9,text:"Uttar Pradesh",tier:"state"}},
  {{lat:23.3,lng:77.4,text:"Madhya Pradesh",tier:"state"}},
  {{lat:17.4,lng:78.5,text:"Telangana",tier:"state"}},
  {{lat:15.3,lng:75.7,text:"Karnataka",tier:"state"}},
  {{lat:10.2,lng:76.0,text:"Kerala",tier:"state"}},
  {{lat:20.3,lng:85.8,text:"Odisha",tier:"state"}},
  {{lat:23.7,lng:86.4,text:"Jharkhand",tier:"state"}},
  {{lat:22.3,lng:84.1,text:"Chhattisgarh",tier:"state"}},
  {{lat:26.2,lng:92.9,text:"Assam",tier:"state"}},
  {{lat:34.1,lng:77.6,text:"Jammu & Kashmir",tier:"state"}},
  {{lat:30.7,lng:76.8,text:"Punjab",tier:"state"}},
  {{lat:29.1,lng:75.7,text:"Haryana",tier:"state"}},
  {{lat:27.0,lng:74.2,text:"Rajasthan",tier:"state"}},
  {{lat:22.3,lng:71.2,text:"Gujarat",tier:"state"}},
  {{lat:39.9,lng:116.4,text:"Beijing",tier:"state"}},
  {{lat:31.2,lng:121.5,text:"Shanghai",tier:"state"}},
  {{lat:23.1,lng:113.3,text:"Guangdong",tier:"state"}},
  {{lat:30.7,lng:104.1,text:"Sichuan",tier:"state"}},
  {{lat:27.6,lng:112.0,text:"Hunan",tier:"state"}},
  {{lat:32.1,lng:119.2,text:"Jiangsu",tier:"state"}},
  {{lat:30.3,lng:120.2,text:"Zhejiang",tier:"state"}},
  {{lat:36.1,lng:117.0,text:"Shandong",tier:"state"}},
  {{lat:34.8,lng:113.7,text:"Henan",tier:"state"}},
  {{lat:38.0,lng:106.3,text:"Ningxia",tier:"state"}},
  {{lat:43.8,lng:87.6,text:"Xinjiang",tier:"state"}},
  {{lat:29.6,lng:91.1,text:"Tibet",tier:"state"}},
  {{lat:-33.9,lng:151.2,text:"New South Wales",tier:"state"}},
  {{lat:-37.8,lng:145.0,text:"Victoria",tier:"state"}},
  {{lat:-27.5,lng:153.0,text:"Queensland",tier:"state"}},
  {{lat:-31.9,lng:115.9,text:"W Australia",tier:"state"}},
  {{lat:-34.9,lng:138.6,text:"S Australia",tier:"state"}},
  {{lat:-42.9,lng:147.3,text:"Tasmania",tier:"state"}},
  {{lat:-12.5,lng:131.0,text:"NT",tier:"state"}},
  {{lat:45.4,lng:-75.7,text:"Ontario",tier:"state"}},
  {{lat:45.5,lng:-73.6,text:"Quebec",tier:"state"}},
  {{lat:51.1,lng:-114.1,text:"Alberta",tier:"state"}},
  {{lat:49.9,lng:-97.1,text:"Manitoba",tier:"state"}},
  {{lat:50.4,lng:-104.6,text:"Saskatchewan",tier:"state"}},
  {{lat:49.3,lng:-123.1,text:"British Columbia",tier:"state"}},
  {{lat:44.7,lng:-63.6,text:"Nova Scotia",tier:"state"}},
  {{lat:-23.5,lng:-46.6,text:"Sao Paulo",tier:"state"}},
  {{lat:-22.9,lng:-43.2,text:"Rio de Janeiro",tier:"state"}},
  {{lat:-15.8,lng:-47.9,text:"Brasilia",tier:"state"}},
  {{lat:-12.0,lng:-77.0,text:"Lima",tier:"state"}},
  {{lat:-34.6,lng:-58.4,text:"Buenos Aires",tier:"state"}},
  {{lat:-33.4,lng:-70.7,text:"Santiago",tier:"state"}},
  {{lat:4.7,lng:-74.1,text:"Bogota",tier:"state"}},
  {{lat:10.5,lng:-66.9,text:"Caracas",tier:"state"}},
  {{lat:-0.2,lng:-78.5,text:"Quito",tier:"state"}},
  {{lat:-16.5,lng:-68.1,text:"La Paz",tier:"state"}},
  {{lat:18.5,lng:-69.9,text:"Santo Domingo",tier:"state"}},
  {{lat:18.1,lng:-77.3,text:"Jamaica",tier:"state"}},
  {{lat:10.5,lng:-61.4,text:"Trinidad",tier:"state"}},
  {{lat:55.8,lng:37.6,text:"Moscow Oblast",tier:"state"}},
  {{lat:59.9,lng:30.3,text:"St Petersburg",tier:"state"}},
  {{lat:56.8,lng:60.6,text:"Sverdlovsk",tier:"state"}},
  {{lat:55.0,lng:82.9,text:"Novosibirsk",tier:"state"}},
  {{lat:53.3,lng:83.8,text:"Altai",tier:"state"}},
  {{lat:43.1,lng:131.9,text:"Primorsky",tier:"state"}},
  {{lat:62.0,lng:129.7,text:"Yakutia",tier:"state"}},
  {{lat:64.5,lng:40.5,text:"Arkhangelsk",tier:"state"}},
  {{lat:68.0,lng:33.1,text:"Murmansk",tier:"state"}},
];

var cityLabels = [
  {{lat:40.7,lng:-74.0,text:"New York",tier:"city"}},
  {{lat:34.1,lng:-118.2,text:"Los Angeles",tier:"city"}},
  {{lat:41.9,lng:-87.6,text:"Chicago",tier:"city"}},
  {{lat:51.5,lng:-0.1,text:"London",tier:"city"}},
  {{lat:48.9,lng:2.3,text:"Paris",tier:"city"}},
  {{lat:55.8,lng:37.6,text:"Moscow",tier:"city"}},
  {{lat:35.7,lng:139.7,text:"Tokyo",tier:"city"}},
  {{lat:39.9,lng:116.4,text:"Beijing",tier:"city"}},
  {{lat:31.2,lng:121.5,text:"Shanghai",tier:"city"}},
  {{lat:19.1,lng:72.9,text:"Mumbai",tier:"city"}},
  {{lat:28.6,lng:77.2,text:"New Delhi",tier:"city"}},
  {{lat:-23.5,lng:-46.6,text:"São Paulo",tier:"city"}},
  {{lat:-33.9,lng:151.2,text:"Sydney",tier:"city"}},
  {{lat:30.0,lng:31.2,text:"Cairo",tier:"city"}},
  {{lat:6.5,lng:3.4,text:"Lagos",tier:"city"}},
  {{lat:-1.3,lng:36.8,text:"Nairobi",tier:"city"}},
  {{lat:-33.9,lng:18.4,text:"Cape Town",tier:"city"}},
  {{lat:25.2,lng:55.3,text:"Dubai",tier:"city"}},
  {{lat:41.0,lng:29.0,text:"Istanbul",tier:"city"}},
  {{lat:13.8,lng:100.5,text:"Bangkok",tier:"city"}},
  {{lat:-6.2,lng:106.8,text:"Jakarta",tier:"city"}},
  {{lat:14.6,lng:121.0,text:"Manila",tier:"city"}},
  {{lat:37.6,lng:127.0,text:"Seoul",tier:"city"}},
  {{lat:19.4,lng:-99.1,text:"Mexico City",tier:"city"}},
  {{lat:-12.0,lng:-77.0,text:"Lima",tier:"city"}},
  {{lat:-34.6,lng:-58.4,text:"Buenos Aires",tier:"city"}},
  {{lat:43.7,lng:-79.4,text:"Toronto",tier:"city"}},
  {{lat:4.7,lng:-74.1,text:"Bogotá",tier:"city"}},
  {{lat:35.7,lng:51.4,text:"Tehran",tier:"city"}},
  {{lat:24.9,lng:67.0,text:"Karachi",tier:"city"}},
  {{lat:24.7,lng:46.7,text:"Riyadh",tier:"city"}},
  {{lat:23.8,lng:90.4,text:"Dhaka",tier:"city"}},
  {{lat:3.1,lng:101.7,text:"Kuala Lumpur",tier:"city"}},
  {{lat:22.3,lng:114.2,text:"Hong Kong",tier:"city"}},
  {{lat:1.4,lng:103.8,text:"Singapore",tier:"city"}},
  {{lat:10.8,lng:106.6,text:"Ho Chi Minh City",tier:"city"}},
  {{lat:5.6,lng:-0.2,text:"Accra",tier:"city"}},
  {{lat:21.0,lng:105.8,text:"Hanoi",tier:"city"}},
  {{lat:9.1,lng:7.5,text:"Abuja",tier:"city"}},
  {{lat:23.1,lng:113.3,text:"Guangzhou",tier:"city"}},
  {{lat:34.7,lng:135.5,text:"Osaka",tier:"city"}},
  {{lat:13.1,lng:80.3,text:"Chennai",tier:"city"}},
  {{lat:31.6,lng:65.0,text:"Lahore",tier:"city"}},
  {{lat:33.6,lng:73.0,text:"Islamabad",tier:"city"}},
  {{lat:52.5,lng:13.4,text:"Berlin",tier:"city"}},
  {{lat:-22.9,lng:-43.2,text:"Rio de Janeiro",tier:"city"}},
  {{lat:-37.8,lng:144.9,text:"Melbourne",tier:"city"}},
  {{lat:15.4,lng:47.1,text:"Aden",tier:"city"}},
  {{lat:5.6,lng:-0.2,text:"Accra",tier:"city"}},
  {{lat:12.4,lng:-1.5,text:"Ouagadougou",tier:"city"}},
  {{lat:12.1,lng:15.0,text:"N'Djamena",tier:"city"}},
  {{lat:13.5,lng:2.1,text:"Niamey",tier:"city"}},
  {{lat:17.4,lng:78.5,text:"Hyderabad",tier:"city"}},
  {{lat:12.9,lng:77.6,text:"Bangalore",tier:"city"}},
  {{lat:11.6,lng:104.9,text:"Phnom Penh",tier:"city"}},
  {{lat:9.0,lng:38.7,text:"Addis Ababa",tier:"city"}},
  {{lat:25.0,lng:121.5,text:"Taipei",tier:"city"}},
  {{lat:6.9,lng:79.9,text:"Colombo",tier:"city"}},
  {{lat:59.9,lng:30.3,text:"St Petersburg",tier:"city"}},
  {{lat:40.2,lng:44.5,text:"Yerevan",tier:"city"}},
  {{lat:40.4,lng:49.9,text:"Baku",tier:"city"}},
  {{lat:41.7,lng:44.8,text:"Tbilisi",tier:"city"}},
  {{lat:50.5,lng:30.5,text:"Kyiv",tier:"city"}},
  {{lat:47.0,lng:28.9,text:"Chisinau",tier:"city"}},
  {{lat:43.8,lng:87.6,text:"Urumqi",tier:"city"}},
  {{lat:30.7,lng:104.1,text:"Chengdu",tier:"city"}},
  {{lat:26.1,lng:119.3,text:"Fuzhou",tier:"city"}},
  {{lat:22.5,lng:88.4,text:"Kolkata",tier:"city"}},
  {{lat:26.9,lng:81.0,text:"Lucknow",tier:"city"}},
  {{lat:17.4,lng:78.5,text:"Hyderabad",tier:"city"}},
  {{lat:33.3,lng:44.4,text:"Baghdad",tier:"city"}},
  {{lat:33.9,lng:35.5,text:"Beirut",tier:"city"}},
  {{lat:31.8,lng:35.2,text:"Jerusalem",tier:"city"}},
  {{lat:32.1,lng:34.8,text:"Tel Aviv",tier:"city"}},
  {{lat:33.5,lng:36.3,text:"Damascus",tier:"city"}},
  {{lat:31.6,lng:65.7,text:"Kandahar",tier:"city"}},
  {{lat:34.5,lng:69.2,text:"Kabul",tier:"city"}},
  {{lat:15.6,lng:32.5,text:"Khartoum",tier:"city"}},
  {{lat:2.0,lng:45.3,text:"Mogadishu",tier:"city"}},
  {{lat:0.3,lng:32.6,text:"Kampala",tier:"city"}},
  {{lat:-4.3,lng:15.3,text:"Kinshasa",tier:"city"}},
  {{lat:-4.3,lng:15.3,text:"Brazzaville",tier:"city"}},
  {{lat:-25.9,lng:32.6,text:"Maputo",tier:"city"}},
  {{lat:-17.8,lng:31.0,text:"Harare",tier:"city"}},
  {{lat:-15.4,lng:28.3,text:"Lusaka",tier:"city"}},
  {{lat:-24.7,lng:25.9,text:"Gaborone",tier:"city"}},
  {{lat:18.1,lng:-15.9,text:"Nouakchott",tier:"city"}},
  {{lat:14.7,lng:-17.4,text:"Dakar",tier:"city"}},
  {{lat:13.5,lng:-2.1,text:"Bamako",tier:"city"}},
  {{lat:10.8,lng:-13.7,text:"Conakry",tier:"city"}},
  {{lat:8.5,lng:-13.2,text:"Freetown",tier:"city"}},
  {{lat:6.4,lng:-10.8,text:"Monrovia",tier:"city"}},
  {{lat:5.4,lng:-4.0,text:"Abidjan",tier:"city"}},
  {{lat:6.4,lng:2.4,text:"Cotonou",tier:"city"}},
  {{lat:6.1,lng:1.2,text:"Lomé",tier:"city"}},
  {{lat:50.1,lng:14.4,text:"Prague",tier:"city"}},
  {{lat:52.2,lng:21.0,text:"Warsaw",tier:"city"}},
  {{lat:47.5,lng:19.1,text:"Budapest",tier:"city"}},
  {{lat:44.8,lng:20.5,text:"Belgrade",tier:"city"}},
  {{lat:42.0,lng:21.4,text:"Skopje",tier:"city"}},
  {{lat:43.9,lng:12.4,text:"San Marino",tier:"city"}},
  {{lat:48.2,lng:16.4,text:"Vienna",tier:"city"}},
  {{lat:47.4,lng:8.5,text:"Zurich",tier:"city"}},
  {{lat:46.9,lng:7.4,text:"Bern",tier:"city"}},
  {{lat:50.8,lng:4.4,text:"Brussels",tier:"city"}},
  {{lat:52.4,lng:4.9,text:"Amsterdam",tier:"city"}},
  {{lat:55.7,lng:12.6,text:"Copenhagen",tier:"city"}},
  {{lat:59.9,lng:10.7,text:"Oslo",tier:"city"}},
  {{lat:59.3,lng:18.1,text:"Stockholm",tier:"city"}},
  {{lat:60.2,lng:25.0,text:"Helsinki",tier:"city"}},
  {{lat:64.1,lng:-21.9,text:"Reykjavik",tier:"city"}},
  {{lat:-34.9,lng:-56.2,text:"Montevideo",tier:"city"}},
  {{lat:-0.2,lng:-78.5,text:"Quito",tier:"city"}},
  {{lat:-16.5,lng:-68.1,text:"La Paz",tier:"city"}},
  {{lat:-25.3,lng:-57.6,text:"Asuncion",tier:"city"}},
  {{lat:8.0,lng:-66.9,text:"Caracas",tier:"city"}},
  {{lat:17.3,lng:-62.7,text:"Basseterre",tier:"city"}},
  {{lat:18.5,lng:-69.9,text:"Santo Domingo",tier:"city"}},
  {{lat:18.5,lng:-72.3,text:"Port-au-Prince",tier:"city"}},
  {{lat:17.1,lng:-61.8,text:"St Johns",tier:"city"}},
  {{lat:32.3,lng:-64.8,text:"Hamilton",tier:"city"}},
  {{lat:43.1,lng:131.9,text:"Vladivostok",tier:"city"}},
  {{lat:55.0,lng:82.9,text:"Novosibirsk",tier:"city"}},
  {{lat:56.8,lng:60.6,text:"Yekaterinburg",tier:"city"}},
  {{lat:51.2,lng:71.4,text:"Astana",tier:"city"}},
  {{lat:43.3,lng:76.9,text:"Almaty",tier:"city"}},
  {{lat:37.9,lng:58.4,text:"Ashgabat",tier:"city"}},
  {{lat:38.6,lng:68.8,text:"Dushanbe",tier:"city"}},
  {{lat:41.3,lng:69.3,text:"Tashkent",tier:"city"}},
  {{lat:42.9,lng:74.6,text:"Bishkek",tier:"city"}},
];

var globe = Globe({{animateIn: false, rendererConfig: {{antialias: true, precision: 'mediump'}}}})
  .backgroundColor('#04080f')
  .showGlobe(true)
  .showAtmosphere(true)
  .atmosphereColor('#5fb8ff')
  .atmosphereAltitude(0.25)
  .pointsData(pointsData)
  .pointLat('lat')
  .pointLng('lng')
  .pointColor('color')
  .pointRadius('radius')
  .pointAltitude('altitude')
  .pointResolution(6)
  .pointsMerge(false)
  .pointLabel(function(d){{
    return '<div style="background:rgba(10,14,23,0.92);border:1px solid #4fc3f7;border-radius:6px;padding:5px 9px;color:#fff;font-family:Courier New;font-size:11px;max-width:200px;">' + d.label + '</div>';
  }})
  .onPointClick(function(d){{
    document.getElementById('popup-content').innerHTML = d.popup;
    document.getElementById('info-popup').style.display = 'block';
  }})
  .ringsData(ringsData)
  .ringLat('lat')
  .ringLng('lng')
  .ringColor(function(d){{ return function(t){{ return hexToRgba(d.color, 1 - t); }}; }})
  .ringMaxRadius(5)
  .ringPropagationSpeed(2.5)
  .ringRepeatPeriod(1500)
  .ringAltitude(0.005)
  .polygonsData([])
  .polygonAltitude(0.008)
  .polygonCapColor(function(){{ return 'rgba(40,80,140,0.55)'; }})
  .polygonSideColor(function(){{ return 'rgba(20,40,80,0.35)'; }})
  .polygonStrokeColor(function(){{ return 'rgba(120,200,255,0.85)'; }})
  .labelsData(countryLabels)
  .labelLat('lat')
  .labelLng('lng')
  .labelText('text')
  .labelSize(function(d){{ return d.tier === 'country' ? 0.7 : d.tier === 'state' ? 0.5 : 0.35; }})
  .labelColor(function(d){{ return d.tier === 'country' ? 'rgba(255,220,100,0.95)' : d.tier === 'state' ? 'rgba(180,220,255,0.9)' : 'rgba(200,200,200,0.85)'; }})
  .labelResolution(1)
  .labelAltitude(0.001)
  .labelDotRadius(0)
  (document.getElementById('globeViz'));

var ctrl = globe.controls();
ctrl.autoRotate = true;
ctrl.autoRotateSpeed = 1.8;
ctrl.enableZoom = true;
ctrl.enableDamping = true;
ctrl.dampingFactor = 0.15;
ctrl.rotateSpeed = 1.4;
ctrl.zoomSpeed = 1.6;
ctrl.minDistance = 110;
ctrl.maxDistance = 580;
globe.pointOfView({{altitude: 2.5}}, 0);

/* Dark navy globe material since we removed the earth texture */
try {{
  var mat = globe.globeMaterial();
  if (mat) {{
    if (mat.color && mat.color.set) mat.color.set('#0a1628');
    if (mat.emissive && mat.emissive.set) mat.emissive.set('#050a14');
    if ('shininess' in mat) mat.shininess = 12;
    mat.needsUpdate = true;
  }}
}} catch(e) {{ /* fallback - sphere stays default */ }}

/* Load country borders for the carto-style map overlay */
fetch('https://raw.githubusercontent.com/vasturiano/globe.gl/master/example/datasets/ne_110m_admin_0_countries.geojson')
  .then(function(r){{ return r.json(); }})
  .then(function(geo){{
    if (geo && geo.features) {{ globe.polygonsData(geo.features); }}
  }})
  .catch(function(e){{ /* silent fallback - globe still works without borders */ }});

var labelUpdateTimer = null;
function updateLabels() {{
  clearTimeout(labelUpdateTimer);
  labelUpdateTimer = setTimeout(function() {{
    var dist = globe.camera().position.length();
    if (dist < 155) {{
      globe.labelsData(countryLabels.concat(stateLabels).concat(cityLabels));
    }} else if (dist < 270) {{
      globe.labelsData(countryLabels.concat(stateLabels));
    }} else {{
      globe.labelsData(countryLabels);
    }}
  }}, 80);
}}

ctrl.addEventListener('change', updateLabels);

function toggleRotation() {{
  rotating = !rotating;
  ctrl.autoRotate = rotating;
  document.getElementById('rotation-status').innerHTML = rotating ? '&#10227; Rotating' : '&#9208; Paused';
}}
</script>
</body></html>"""
    return html
