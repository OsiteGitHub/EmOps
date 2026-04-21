# EmOps®

**Real-time global disaster management intelligence — built for analysts, responders, and decision-makers tracking how the planet moves, shakes, and rebuilds.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red)](https://streamlit.io/)

---

## Overview

EmOps is an open-source Streamlit web application that aggregates and visualises live and historical disaster data from multiple authoritative global sources. It covers natural hazards, mining disasters, drought and heatwave monitoring, regional intelligence, and community reporting — all rendered on interactive CARTO dark-mode maps with a glass-morphism UI.

---

## Features

| Module | What it does |
|---|---|
| **Dashboard** | Live global CARTO map with clickable event popups, severity metrics, latest-alerts grid, and event-distribution chart |
| **Country Analysis** | Per-country risk profiles, historical disaster timelines, and AI-generated situation summaries |
| **Live Alerts** | Real-time feed from USGS, NASA EONET, and GDACS with severity filtering |
| **Drought & Heatwave** | Open-Meteo powered temperature and precipitation monitoring with anomaly detection |
| **Mining Disasters** | Abandoned mines, active mine incidents, and rare-earth extraction risks — globally mapped |
| **Resource Hub** | Evacuation guides, shelter locators, and emergency contact directories |

---

## Data Sources

- **USGS Earthquake Hazards Program** — real-time seismic feeds
- **NASA EONET** — natural event tracking (wildfires, storms, floods, volcanoes)
- **GDACS** — Global Disaster Alert and Coordination System
- **Open-Meteo** — free open-source weather and climate API
- **CARTO** — dark basemap tiles

---

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — Python web framework
- **[Folium](https://python-visualization.github.io/folium/)** — Leaflet.js map rendering
- **[Plotly](https://plotly.com/python/)** — interactive charts
- **[Pandas](https://pandas.pydata.org/)** — data handling
- **CARTO Dark Matter** — map tile layer

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

```bash
git clone https://github.com/your-org/emops.git
cd emops
pip install -r requirements.txt
```

### Run locally

```bash
streamlit run app.py --server.port 5000
```

Then open `http://localhost:5000` in your browser.

---

## Project Structure

```
emops/
├── app.py              # Main application — all pages and UI
├── api_clients.py      # Live data fetchers (USGS, EONET, GDACS, Open-Meteo)
├── map_utils.py        # Folium/CARTO map builders and popup styles
├── disaster_data.py    # Historical disaster records and situation reports
├── regional_data.py    # Africa, Asia, and Middle-East regional datasets
├── mine_data.py        # Abandoned, active, and rare-earth mine datasets
├── .streamlit/
│   └── config.toml     # Streamlit server configuration
├── LICENSE             # Apache 2.0 licence
├── NOTICE              # Third-party attributions
└── CONTRIBUTING.md     # Contributor guide
```

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

---

## Licence

Copyright 2026 EmOps.
Licensed under the [Apache License, Version 2.0](LICENSE).

---

## Disclaimer

EmOps aggregates data from third-party sources for informational purposes only.
Always consult official emergency management authorities in life-threatening situations.
