# Global Disaster Resilience Monitor (DisasterWatch)

## Overview
A comprehensive disaster management and resilience web application built with Streamlit. It provides real-time disaster tracking, country and state-level risk assessments, early warnings, evacuation guides, shelter/water locators, community reporting, and drought/heatwave specialized monitoring.

## Architecture
- **Framework**: Streamlit (Python)
- **Maps**: Folium + streamlit-folium (dark-themed interactive maps with CartoDB dark_matter tiles)
- **Charts**: Plotly (interactive visualizations — radar, bar, line, scatter)
- **Data Sources**: USGS Earthquake API, NASA EONET, GDACS, ReliefWeb, Open-Meteo
- **Security**: HTML sanitization via `html.escape` for all external API data rendered in HTML

## File Structure
- `app.py` — Main Streamlit application with all page rendering (Dashboard, Country Analysis, Live Alerts, Drought & Heatwave, Resource Hub)
- `api_clients.py` — API integration layer with caching (USGS earthquakes, NASA events, GDACS, ReliefWeb disasters, Open-Meteo weather)
- `disaster_data.py` — Country risk profiles (70+ countries), state-level coordinates (15 countries), evacuation guides, drought resources, aid organizations, shelter/water locators
- `map_utils.py` — Folium map creation utilities (global map, country map, color coding, heat overlays)
- `.streamlit/config.toml` — Streamlit server configuration

## Key Features
1. **Global Dashboard** — Interactive dark-themed map with live disaster markers from multiple sources, event distribution charts, latest alerts feed, ReliefWeb reports
2. **Country Analysis** — Per-country and per-state risk profiles, radar charts, weather forecasts with 7-day outlook, AI-generated resilience summaries, travel safety guides with evacuation protocols
3. **Live Alerts** — Real-time earthquake/event feed with severity filtering, magnitude breakdowns, and comprehensive event tables
4. **Drought & Heatwave Center** — Temperature monitoring with 40°C/35°C alert thresholds, drought risk indices, dry spell detection, drought-resistant crop recommendations, community rainwater harvesting techniques
5. **Resource Hub** — Aid organizations (filterable), shelter & water point locators with map, evacuation guides (before/during/after), emergency preparedness kits, community resilience tips, community disaster reporting form

## Disaster Types Covered
Earthquakes, Floods, Storms, Wildfires, Volcanic Eruptions, Tsunamis, Droughts, Extreme Temperatures, Landslides

## State/Region Support
State-level drill-down with coordinates, weather, and event filtering for: United States (50 states), India, Japan, Indonesia, Philippines, Australia, China, Mexico, Brazil, Canada, Turkey, Italy, Pakistan, Bangladesh, Nepal, Chile

## Dependencies
- streamlit, folium, streamlit-folium, requests, pandas, plotly

## Run Command
```
streamlit run app.py --server.port 5000
```
