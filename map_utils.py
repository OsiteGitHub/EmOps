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

    lats = [e.get("lat", 0) for e in filtered]
    lons = [e.get("lon", 0) for e in filtered]
    colors = [DISASTER_COLORS.get(e.get("type", ""), "#ffffff") for e in filtered]

    sizes_inner = []
    sizes_halo = []
    for e in filtered:
        mag = e.get("magnitude", 0) or 0
        if mag > 0:
            s = max(5, min(16, mag * 2))
        else:
            sev_s = {"Critical": 12, "High": 9, "Moderate": 7, "Low": 5}
            s = sev_s.get(e.get("severity", "Moderate"), 7)
        sizes_inner.append(s)
        sizes_halo.append(int(s * 2.2))

    popups = []
    for i, e in enumerate(filtered):
        title = html_escape(str(e.get("title", "") or "").replace("\n", " "))
        dtype = html_escape(str(e.get("type", "Unknown") or ""))
        sev = html_escape(str(e.get("severity", "N/A") or "N/A"))

        if not selected_types:
            nearby = [ev for ev in filtered
                      if abs(ev.get("lat", 0) - e.get("lat", 0)) < 5
                      and abs(ev.get("lon", 0) - e.get("lon", 0)) < 5]
            tc = {}
            for ne in nearby:
                t = ne.get("type", "Unknown")
                tc[t] = tc.get(t, 0) + 1
            lines = [
                f"<b style='color:#4fc3f7;font-size:14px;'>{dtype}</b>",
                f"<b>{title}</b>",
                "<hr style='border-color:#333;margin:6px 0;'>",
                "<b style='color:#4fc3f7;'>Area Disaster Summary:</b>"
            ]
            for t, c in sorted(tc.items(), key=lambda x: x[1], reverse=True):
                tcolor = DISASTER_COLORS.get(t, "#fff")
                lines.append(f"<span style='color:{tcolor};'>&#9679;</span> {html_escape(t)}: <b>{c}</b> event(s)")
            lines.append(f"<hr style='border-color:#333;margin:6px 0;'>Total: <b>{len(nearby)}</b> events in area")
            popup = "<br>".join(lines)
        else:
            lines = [
                f"<b style='color:#4fc3f7;font-size:14px;'>{dtype}</b>",
                f"<b>{title}</b>"
            ]
            if e.get("magnitude"):
                lines.append(f"Magnitude: <b>{html_escape(str(e['magnitude']))}</b>")
            if e.get("depth"):
                lines.append(f"Depth: <b>{e['depth']:.1f}</b> km")
            sev_colors_map = {"Critical": "#ff0000", "High": "#ff6600", "Moderate": "#ffaa00", "Low": "#88cc00"}
            sc = sev_colors_map.get(sev, "#fff")
            lines.append(f"Severity: <b style='color:{sc};'>{sev}</b>")
            if e.get("time"):
                if isinstance(e["time"], datetime):
                    lines.append(f"Time: {e['time'].strftime('%Y-%m-%d %H:%M UTC')}")
            popup = "<br>".join(lines)
        popups.append(popup)

    hovers = [f"{html_escape(str(e.get('type', '')))}: {html_escape(str(e.get('title', '')))}" for e in filtered]

    lats_js = json.dumps(lats)
    lons_js = json.dumps(lons)
    colors_js = json.dumps(colors)
    si_js = json.dumps(sizes_inner)
    sh_js = json.dumps(sizes_halo)
    popups_js = json.dumps(popups)
    hovers_js = json.dumps(hovers)

    html = f"""<!DOCTYPE html>
<html><head>
<script src="https://cdn.plot.ly/plotly-2.35.0.min.js"></script>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0e17;font-family:'Courier New',Courier,monospace}}
#globe{{width:100%;height:{height}px}}
#info-popup{{
  display:none;position:absolute;top:20px;right:20px;
  background:rgba(20,27,45,0.95);border:1px solid #4fc3f7;
  border-radius:12px;padding:16px 20px;color:#ffffff;
  font-family:'Courier New',Courier,monospace;font-size:13px;
  max-width:340px;min-width:220px;z-index:1000;
  box-shadow:0 8px 32px rgba(0,0,0,0.6);line-height:1.6;
  max-height:{height - 60}px;overflow-y:auto;
}}
#info-popup::-webkit-scrollbar{{width:4px}}
#info-popup::-webkit-scrollbar-thumb{{background:#4fc3f7;border-radius:2px}}
.close-btn{{position:absolute;top:8px;right:12px;cursor:pointer;color:#4fc3f7;font-size:18px;font-weight:bold}}
.close-btn:hover{{color:#ff4444}}
#rotation-status{{
  position:absolute;bottom:12px;left:12px;color:rgba(255,255,255,0.6);
  font-size:11px;font-family:'Courier New',monospace;cursor:pointer;
  padding:4px 10px;background:rgba(20,27,45,0.7);border-radius:6px;
  border:1px solid rgba(79,195,247,0.3);user-select:none;
}}
#rotation-status:hover{{color:#4fc3f7;border-color:#4fc3f7}}
</style>
</head><body>
<div style="position:relative">
<div id="globe"></div>
<div id="info-popup">
  <span class="close-btn" onclick="document.getElementById('info-popup').style.display='none'">&times;</span>
  <div id="popup-content"></div>
</div>
<div id="rotation-status" onclick="toggleRotation()">&#10227; Rotating</div>
</div>
<script>
var lats={lats_js},lons={lons_js},colors={colors_js};
var sizesI={si_js},sizesH={sh_js};
var popupData={popups_js},hoverTexts={hovers_js};
var haloTrace={{
  type:'scattergeo',lat:lats,lon:lons,mode:'markers',
  marker:{{size:sizesH,color:colors,opacity:0.15,line:{{width:0}}}},
  hoverinfo:'skip',showlegend:false
}};
var mainTrace={{
  type:'scattergeo',lat:lats,lon:lons,mode:'markers',
  marker:{{size:sizesI,color:colors,opacity:0.85,
    line:{{color:'rgba(255,255,255,0.4)',width:1}},sizemode:'diameter'}},
  text:hoverTexts,hoverinfo:'text',
  hoverlabel:{{bgcolor:'#141b2d',bordercolor:'#4fc3f7',
    font:{{family:'Courier New',color:'#ffffff',size:12}}}},
  showlegend:false
}};
var layout={{
  geo:{{
    projection:{{type:'orthographic',rotation:{{lon:0,lat:20,roll:0}}}},
    showland:true,landcolor:'#1a2332',
    showocean:true,oceancolor:'#0a0e17',
    showlakes:true,lakecolor:'#0d1221',
    showcoastlines:true,coastlinecolor:'#2a3a4a',coastlinewidth:0.5,
    showcountries:true,countrycolor:'#2a3a4a',countrywidth:0.3,
    showframe:false,bgcolor:'#0a0e17',
    lonaxis:{{showgrid:true,gridcolor:'#1a2332'}},
    lataxis:{{showgrid:true,gridcolor:'#1a2332'}}
  }},
  paper_bgcolor:'#0a0e17',plot_bgcolor:'#0a0e17',
  margin:{{l:0,r:0,t:0,b:0}},height:{height},
  font:{{family:'Courier New',color:'#ffffff'}}
}};
Plotly.newPlot('globe',[haloTrace,mainTrace],layout,{{responsive:true,displayModeBar:false}});
var rotating=true,angle=0,userInteracting=false;
function rotate(){{
  if(rotating&&!userInteracting){{
    angle=(angle+0.3)%360;
    Plotly.relayout('globe',{{'geo.projection.rotation.lon':angle}});
  }}
  requestAnimationFrame(rotate);
}}
requestAnimationFrame(rotate);
var g=document.getElementById('globe');
g.addEventListener('mousedown',function(){{userInteracting=true}});
g.addEventListener('mouseup',function(){{
  userInteracting=false;
  try{{angle=g._fullLayout.geo._subplot.projection.rotation.lon||angle}}catch(x){{try{{angle=g.layout.geo.projection.rotation.lon||angle}}catch(y){{}}}}
}});
g.addEventListener('touchstart',function(){{userInteracting=true}});
g.addEventListener('touchend',function(){{userInteracting=false}});
function toggleRotation(){{
  rotating=!rotating;
  document.getElementById('rotation-status').innerHTML=rotating?'&#10227; Rotating':'&#9208; Paused';
}}
g.on('plotly_click',function(data){{
  if(data.points&&data.points.length>0){{
    var pt=data.points[0];
    if(pt.curveNumber===1&&pt.pointIndex<popupData.length){{
      document.getElementById('popup-content').innerHTML=popupData[pt.pointIndex];
      document.getElementById('info-popup').style.display='block';
    }}
  }}
}});
</script>
</body></html>"""
    return html
