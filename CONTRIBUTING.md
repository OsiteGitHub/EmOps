# Contributing to EmOps

Thank you for your interest in contributing to EmOps — the global disaster management platform.
All contributions are welcome and are released under the Apache 2.0 licence.

## Getting started

1. Fork the repository and create a feature branch from `main`.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app locally:
   ```bash
   streamlit run app.py --server.port 5000
   ```

## Project structure

| File | Purpose |
|---|---|
| `app.py` | Main Streamlit application — all pages and UI |
| `api_clients.py` | Fetches live data from USGS, NASA EONET, GDACS, Open-Meteo |
| `map_utils.py` | Folium / CARTO map builders and popup styles |
| `disaster_data.py` | Historical disaster records and situation reports |
| `regional_data.py` | Africa, Asia, and Middle-East regional datasets |
| `mine_data.py` | Abandoned, active, and rare-earth mine datasets |
| `.streamlit/config.toml` | Streamlit server configuration |

## Contribution guidelines

- Keep pull requests focused — one feature or fix per PR.
- Follow the existing code style (Python 3, f-strings, no unused imports).
- Do not commit secrets, API keys, or personal data.
- Add a brief description of your change in the PR body.
- For significant new features, open an issue first to discuss the approach.

## Reporting bugs

Open a GitHub issue with:
- A clear title and description
- Steps to reproduce
- Expected vs actual behaviour
- Python and Streamlit version

## Licence

By contributing you agree that your submissions will be licensed under the
[Apache License 2.0](LICENSE).
