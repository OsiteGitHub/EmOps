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
}


def _folium_color(hex_color):
    cmap = {
        "#ff4444": "red", "#ff6600": "orange", "#ff8800": "orange",
        "#4488ff": "blue", "#0066cc": "blue", "#003399": "darkblue",
        "#cc8800": "orange", "#cc0000": "darkred", "#885500": "beige",
        "#88ccff": "lightblue", "#999966": "gray", "#669999": "cadetblue",
        "#aaddee": "lightblue",
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

        popup_parts = [
            f'<div style="font-family:Courier New,Courier,monospace;min-width:220px;">',
            f"<h4 style='color:{color};margin:0 0 5px 0;'>{event.get('type', 'Unknown')}</h4>",
            f"<p style='margin:2px 0;'><b>{event.get('title', '')}</b></p>",
        ]
        if event.get("magnitude"):
            popup_parts.append(f"<p style='margin:2px 0;'>Magnitude: <b>{event['magnitude']}</b></p>")
        if event.get("depth"):
            popup_parts.append(f"<p style='margin:2px 0;'>Depth: {event['depth']:.1f} km</p>")
        if event.get("time"):
            popup_parts.append(f"<p style='margin:2px 0;'>Time: {event['time']}</p>")
        sev = event.get("severity", "N/A")
        sev_colors = {"Critical": "#ff0000", "High": "#ff6600", "Moderate": "#ffaa00", "Low": "#88cc00"}
        sev_color = sev_colors.get(sev, "#fff")
        popup_parts.append(f"<p style='margin:2px 0;'>Severity: <span style='color:{sev_color};font-weight:bold;'>{sev}</span></p>")
        popup_parts.append("</div>")

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6,
            weight=1,
            popup=folium.Popup("".join(popup_parts), max_width=300),
            tooltip=f"{event.get('type', '')}: {event.get('title', '')}"
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

    if events:
        for event in events:
            elat = event.get("lat", 0)
            elon = event.get("lon", 0)
            if elat == 0 and elon == 0:
                continue
            color = DISASTER_COLORS.get(event.get("type", ""), "#ffffff")
            radius = _severity_radius(event)
            popup_html = f"""
            <div style='font-family:Courier New,Courier,monospace;'>
                <h4 style='color:{color};margin:0;'>{event.get('type', '')}</h4>
                <p style='margin:3px 0;'><b>{event.get('title', '')}</b></p>
                <p style='margin:3px 0;'>Severity: {event.get('severity', 'N/A')}</p>
            </div>
            """
            folium.CircleMarker(
                location=[elat, elon],
                radius=radius,
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=1,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=event.get("title", "")
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
        return f'<div style="height:{height}px;background:#0a0e17;display:flex;align-items:center;justify-content:center;color:#ffffff;font-family:Courier New;">No events to display</div>'

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
var rotating = true;
var rotationTimer = null;

var globe = Globe({{animateIn: false}})
  .globeImageUrl('https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg')
  .bumpImageUrl('https://unpkg.com/three-globe/example/img/earth-topology.png')
  .backgroundImageUrl('https://unpkg.com/three-globe/example/img/night-sky.png')
  .pointsData(pointsData)
  .pointLat('lat')
  .pointLng('lng')
  .pointColor('color')
  .pointRadius('radius')
  .pointAltitude('altitude')
  .pointsMerge(false)
  .pointLabel(function(d){{
    return '<div style="background:rgba(10,14,23,0.9);border:1px solid #4fc3f7;border-radius:6px;padding:6px 10px;color:#fff;font-family:Courier New;font-size:11px;max-width:220px;">' + d.label + '</div>';
  }})
  .onPointClick(function(d){{
    document.getElementById('popup-content').innerHTML = d.popup;
    document.getElementById('info-popup').style.display = 'block';
  }})
  (document.getElementById('globeViz'));

globe.controls().autoRotate = true;
globe.controls().autoRotateSpeed = 0.4;
globe.controls().enableZoom = true;
globe.controls().minDistance = 120;
globe.controls().maxDistance = 600;
globe.pointOfView({{altitude: 2.5}}, 0);

function toggleRotation() {{
  rotating = !rotating;
  globe.controls().autoRotate = rotating;
  document.getElementById('rotation-status').innerHTML = rotating ? '&#10227; Rotating' : '&#9208; Paused';
}}
</script>
</body></html>"""
    return html
