import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import time


@st.cache_data(ttl=300)
def fetch_earthquakes(min_magnitude=2.5, days=7):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "starttime": start.strftime("%Y-%m-%d"),
        "endtime": end.strftime("%Y-%m-%d"),
        "minmagnitude": min_magnitude,
        "orderby": "time",
        "limit": 500
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        events = []
        for f in data.get("features", []):
            p = f["properties"]
            c = f["geometry"]["coordinates"]
            mag = p.get("mag", 0) or 0
            if mag >= 6:
                sev = "Critical"
            elif mag >= 5:
                sev = "High"
            elif mag >= 4:
                sev = "Moderate"
            else:
                sev = "Low"
            events.append({
                "id": f["id"],
                "type": "Earthquake",
                "title": p.get("title", ""),
                "magnitude": mag,
                "place": p.get("place", ""),
                "time": datetime.utcfromtimestamp(p["time"] / 1000),
                "lat": c[1],
                "lon": c[0],
                "depth": c[2],
                "url": p.get("url", ""),
                "tsunami": p.get("tsunami", 0),
                "alert": p.get("alert", ""),
                "severity": sev
            })
        return events
    except Exception:
        return []


@st.cache_data(ttl=600)
def fetch_nasa_events():
    url = "https://eonet.gsfc.nasa.gov/api/v3/events"
    params = {"status": "open", "limit": 300}
    cat_map = {
        "wildfires": "Wildfire",
        "volcanoes": "Volcanic Eruption",
        "severeStorms": "Storm",
        "floods": "Flood",
        "earthquakes": "Earthquake",
        "drought": "Drought",
        "dustHaze": "Dust/Haze",
        "landslides": "Landslide",
        "snow": "Snow/Ice",
        "tempExtremes": "Extreme Temperature",
        "waterColor": "Water Quality",
        "seaLakeIce": "Sea/Lake Ice"
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        events = []
        for ev in data.get("events", []):
            cat_id = ev["categories"][0]["id"] if ev.get("categories") else "unknown"
            dtype = cat_map.get(cat_id, cat_id.replace("_", " ").title())
            geom = ev.get("geometry", [])
            if geom:
                latest = geom[-1]
                coords = latest.get("coordinates", [0, 0])
                try:
                    t = datetime.fromisoformat(latest.get("date", "").replace("Z", "+00:00"))
                except Exception:
                    t = datetime.utcnow()
                events.append({
                    "id": ev.get("id", ""),
                    "type": dtype,
                    "title": ev.get("title", ""),
                    "lat": coords[1] if len(coords) > 1 else 0,
                    "lon": coords[0] if len(coords) > 0 else 0,
                    "time": t,
                    "source": "NASA EONET",
                    "severity": "Moderate",
                    "url": ev.get("link", "")
                })
        return events
    except Exception:
        return []


@st.cache_data(ttl=600)
def fetch_reliefweb_disasters(limit=50):
    url = "https://api.reliefweb.int/v1/disasters"
    params = {
        "appname": "disaster-resilience-app",
        "limit": limit,
        "sort[]": "date:desc",
        "fields[include][]": ["name", "date", "type", "country", "status", "url"]
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        disasters = []
        for item in data.get("data", []):
            f = item.get("fields", {})
            countries = [c.get("name", "") for c in f.get("country", [])]
            types = [t.get("name", "") for t in f.get("type", [])]
            disasters.append({
                "id": item.get("id", ""),
                "name": f.get("name", ""),
                "date": f.get("date", {}).get("created", ""),
                "countries": countries,
                "types": types,
                "status": f.get("status", ""),
                "url": f.get("url", "")
            })
        return disasters
    except Exception:
        return []


@st.cache_data(ttl=900)
def fetch_weather_data(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_gusts_10m",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,weather_code,uv_index_max",
        "forecast_days": 7,
        "timezone": "auto"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


@st.cache_data(ttl=3600)
def fetch_historical_weather(lat, lon, start_date, end_date):
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "auto"
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


@st.cache_data(ttl=1800)
def fetch_gdacs_events():
    url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH"
    params = {"eventlist": "", "fromDate": (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"), "toDate": datetime.utcnow().strftime("%Y-%m-%d"), "alertlevel": ""}
    try:
        resp = requests.get(url, params=params, timeout=15, headers={"Accept": "application/json"})
        resp.raise_for_status()
        data = resp.json()
        events = []
        type_map = {"EQ": "Earthquake", "TC": "Storm", "FL": "Flood", "VO": "Volcanic Eruption", "DR": "Drought", "WF": "Wildfire", "TS": "Tsunami"}
        for feat in data.get("features", []):
            p = feat.get("properties", {})
            c = feat.get("geometry", {}).get("coordinates", [0, 0])
            al = p.get("alertlevel", "Green")
            sev_map = {"Red": "Critical", "Orange": "High", "Yellow": "Moderate", "Green": "Low"}
            events.append({
                "id": p.get("eventid", ""),
                "type": type_map.get(p.get("eventtype", ""), p.get("eventtype", "Unknown")),
                "title": p.get("name", p.get("eventtype", "")),
                "lat": c[1] if len(c) > 1 else 0,
                "lon": c[0] if len(c) > 0 else 0,
                "time": datetime.utcnow(),
                "severity": sev_map.get(al, "Moderate"),
                "alert_level": al,
                "source": "GDACS",
                "country": p.get("country", ""),
                "url": p.get("url", {}).get("report", "") if isinstance(p.get("url"), dict) else ""
            })
        return events
    except Exception:
        return []


def get_all_live_events():
    earthquakes = fetch_earthquakes(min_magnitude=2.5, days=7)
    nasa = fetch_nasa_events()
    gdacs = fetch_gdacs_events()
    all_events = earthquakes + nasa + gdacs
    seen = set()
    unique = []
    for e in all_events:
        key = (round(e.get("lat", 0), 1), round(e.get("lon", 0), 1), e.get("type", ""))
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


WMO_WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
    55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    66: "Light freezing rain", 67: "Heavy freezing rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
    82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
    95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
}


def decode_weather(code):
    return WMO_WEATHER_CODES.get(code, "Unknown")
