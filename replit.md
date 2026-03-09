# Global Disaster Resilience Monitor (DisasterWatch)

## Overview
A comprehensive disaster management and resilience web application built with Streamlit. It provides real-time disaster tracking, country and state-level risk assessments, early warnings, evacuation guides, shelter/water locators, community reporting, and drought/heatwave specialized monitoring.

## Architecture
- **Framework**: Streamlit (Python)
- **Maps**: Plotly 3D rotating globe (orthographic projection, auto-rotation, clickable markers with context-aware popups) on Dashboard; Folium + streamlit-folium for country-level maps
- **Charts**: Plotly (interactive visualizations — radar, bar, line, scatter)
- **Data Sources**: USGS Earthquake API, NASA EONET, GDACS, ReliefWeb, Open-Meteo
- **Security**: HTML sanitization via `html.escape` for all external API data rendered in HTML

## File Structure
- `app.py` — Main Streamlit application with all page rendering (Dashboard, Country Analysis, Live Alerts, Drought & Heatwave, Resource Hub)
- `api_clients.py` — API integration layer with caching (USGS earthquakes, NASA events, GDACS, ReliefWeb disasters, Open-Meteo weather)
- `disaster_data.py` — Country risk profiles (70+ countries), state-level coordinates (15 countries), evacuation guides, drought resources, aid organizations, shelter/water locators
- `map_utils.py` — Map utilities: rotating 3D Plotly globe with clickable markers (global dashboard), Folium country maps, color coding, heat overlays
- `.streamlit/config.toml` — Streamlit server configuration

## Key Features
1. **Global Dashboard** — Rotating 3D globe with live disaster markers (clickable with context-aware popups: filtered → event details, all → area summary), event distribution charts, latest alerts feed, ReliefWeb reports
2. **Country Analysis** — Per-country and per-state risk profiles, radar charts, weather forecasts with 7-day outlook, AI-generated resilience summaries, travel safety guides with evacuation protocols
3. **Live Alerts** — Real-time earthquake/event feed with severity filtering, magnitude breakdowns, and comprehensive event tables
4. **Drought & Heatwave Center** — Temperature monitoring with 40°C/35°C alert thresholds, drought risk indices, dry spell detection, drought-resistant crop recommendations, community rainwater harvesting techniques
5. **Resource Hub** — Aid organizations (filterable), shelter & water point locators with map, evacuation guides (before/during/after), emergency preparedness kits, community resilience tips, community disaster reporting form

## Disaster Types Covered
Earthquakes, Floods, Storms, Wildfires, Volcanic Eruptions, Tsunamis, Droughts, Extreme Temperatures, Landslides

## State/Region Support
State-level drill-down with coordinates, weather, and event filtering for: United States (50 states), India, Japan, Indonesia, Philippines, Australia, China, Mexico, Brazil, Canada, Turkey, Italy, Pakistan, Bangladesh, Nepal, Chile

## Design Preferences
- **Font**: Courier New (monospace) throughout all text
- **Text colors**: White (#ffffff) for all body/label text; accent colors (#4fc3f7 cyan) for headers
- **Sidebar background**: #666666 (medium grey)
- **App background**: #0a0e17 (dark navy)
- **Theme**: Dark theme with #4fc3f7 accent

## Dependencies
- streamlit, folium, streamlit-folium, requests, pandas, plotly

## Run Command
```
streamlit run app.py --server.port 5000
```
