import folium
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
            f"<div style='font-family:Arial,sans-serif;min-width:220px;'>",
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
            <div style='font-family:Arial;'>
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
