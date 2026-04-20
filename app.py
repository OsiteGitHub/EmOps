import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta, timezone
from html import escape as html_escape
from streamlit_folium import st_folium
import streamlit.components.v1 as components
from api_clients import (
    fetch_earthquakes, fetch_nasa_events, fetch_reliefweb_disasters,
    fetch_weather_data, fetch_historical_weather, get_all_live_events,
    decode_weather, fetch_gdacs_events
)
from disaster_data import (
    COUNTRIES, RISK_PROFILES, COUNTRY_STATES, DISASTER_TYPES,
    AID_ORGANIZATIONS, EVACUATION_GUIDES, DROUGHT_RESOURCES,
    STATE_COORDS, SHELTER_RESOURCES,
    get_risk_profile, get_overall_risk, get_top_risks,
    generate_country_summary, generate_disaster_analysis
)
from map_utils import (
    create_global_map, create_country_map, create_rotating_globe_html,
    DISASTER_COLORS, get_disaster_color
)
from disaster_reports import (
    HISTORICAL_DISASTERS, RESEARCH_ARTICLES,
    get_country_disasters, get_country_research,
    get_disasters_by_type, get_research_by_type,
    get_tropical_disasters
)
from mine_data import (
    ABANDONED_MINES, RARE_EARTH_MINES,
    get_mine_events, get_rare_earth_events,
    get_mines_by_country, get_critical_mines
)


def _safe(text):
    if text is None:
        return ""
    return html_escape(str(text))


def _sort_time(e):
    t = e.get("time")
    if t is None:
        return datetime.min
    if isinstance(t, datetime):
        if t.tzinfo is not None:
            return t.replace(tzinfo=None)
        return t
    return datetime.min


st.set_page_config(
    page_title="EmOps – Global Disaster Resilience Monitor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
  <style>
      @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

      :root {
          --bg: #003047;
          --bg-deeper: #00202f;
          --bg-card: rgba(255, 255, 255, 0.04);
          --fg: #ffffff;
          --muted: #a8aab1;
          --border-soft: rgba(255, 255, 255, 0.10);
          --border-mid: rgba(255, 255, 255, 0.18);
          --accent: #5fb8ff;
          --accent-soft: rgba(95, 184, 255, 0.18);
      }

      * {
          font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
      }

      h1, h2, h3, h4, h5, h6,
      .display-serif {
          font-family: 'Instrument Serif', Georgia, serif !important;
          font-weight: 400 !important;
          letter-spacing: -0.01em;
          color: var(--fg);
      }

      .material-icons,
      .material-icons-round,
      .material-icons-outlined,
      [data-testid="collapsedControl"] span,
      [data-testid="collapsedControl"] svg,
      button[kind="header"] span,
      span[class*="material"] {
          font-family: 'Material Icons' !important;
      }

      body, .stApp {
          background: var(--bg) !important;
          color: var(--fg) !important;
      }

      /* Reduce default top padding of main content area */
      .stMainBlockContainer,
      div[data-testid="stMainBlockContainer"],
      .block-container {
          padding-top: 1.5rem !important;
          max-width: 1400px;
      }

      /* ── Sidebar (dark glass) ──────────────────────────────── */
      section[data-testid="stSidebar"] {
          background: rgba(0, 20, 30, 0.85) !important;
          border-right: 1px solid var(--border-soft) !important;
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
      }

      section[data-testid="stSidebar"] .stMarkdown h1,
      section[data-testid="stSidebar"] .stMarkdown h2,
      section[data-testid="stSidebar"] .stMarkdown h3,
      section[data-testid="stSidebar"] .stMarkdown h4 {
          color: var(--fg) !important;
          font-family: 'Instrument Serif', Georgia, serif !important;
      }

      section[data-testid="stSidebar"] .stRadio label,
      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label,
      section[data-testid="stSidebar"] .stRadio label p,
      section[data-testid="stSidebar"] .stRadio label span,
      section[data-testid="stSidebar"] .stRadio label div,
      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label p,
      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span,
      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label div,
      section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
      section[data-testid="stSidebar"] p,
      section[data-testid="stSidebar"] span,
      section[data-testid="stSidebar"] label {
          color: var(--fg) !important;
          font-weight: 500 !important;
          font-size: 0.92rem !important;
      }

      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
          padding: 8px 12px !important;
          border-radius: 10px;
          margin: 2px 0;
          transition: background 0.18s ease;
      }
      section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
          background: rgba(255, 255, 255, 0.05);
      }

      section[data-testid="stSidebar"] hr {
          border-color: var(--border-soft) !important;
          opacity: 1;
      }

      /* Hide native sidebar toggle arrows */
      [data-testid="stSidebarCollapseButton"],
      [data-testid="collapsedControl"] {
          opacity: 0 !important;
          pointer-events: none !important;
      }

      #MainMenu,
      [data-testid="stMainMenu"],
      header [data-testid="stToolbar"],
      header button[aria-label="Open Settings"],
      header button[title="Open Settings"] {
          display: none !important;
          visibility: hidden !important;
      }

      header[data-testid="stHeader"] {
          background: transparent !important;
      }

      /* ── Liquid glass utility ──────────────────────────────── */
      .liquid-glass {
          background: rgba(255, 255, 255, 0.04);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          border: 1px solid var(--border-soft);
          border-radius: 14px;
          box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.06),
                      0 4px 20px rgba(0, 0, 0, 0.18);
      }

      /* ── Brand header (above nav) ──────────────────────────── */
        .brand-header {
            text-align: center;
            padding: 1.2rem 0 0.4rem 0;
            margin-bottom: 0.6rem;
        }
        .brand-header .hero-title {
            font-size: clamp(2.6rem, 6.5vw, 5rem) !important;
            margin: 0 !important;
            line-height: 1 !important;
        }
        .brand-header .brand-tagline {
            color: var(--muted) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important;
            font-weight: 400 !important;
            line-height: 1.55 !important;
            max-width: 640px;
            margin: 0.7rem auto 0 auto !important;
            text-align: center;
        }

        /* ── Hero section ──────────────────────────────────────── */
        .hero-wrap {
          text-align: center;
          padding: 2.5rem 1rem 1.5rem 1rem;
          animation: fade-rise 0.9s ease-out both;
      }
      .hero-title {
          font-family: 'Instrument Serif', Georgia, serif !important;
          font-size: clamp(3.5rem, 9vw, 7rem) !important;
          line-height: 0.95 !important;
          letter-spacing: -0.04em !important;
          color: var(--fg);
          margin: 0;
          font-weight: 400;
      }
      .hero-title em {
          font-style: italic;
          color: var(--muted);
      }
      .hero-sub {
          color: var(--muted);
          font-size: 1.05rem;
          max-width: 640px;
          margin: 1.4rem auto 0 auto;
          line-height: 1.65;
          font-weight: 400;
          font-family: 'Inter', sans-serif !important;
      }

      /* ── Metric cards (glass) ──────────────────────────────── */
      .metric-card {
          background: rgba(255, 255, 255, 0.04);
          backdrop-filter: blur(10px);
          -webkit-backdrop-filter: blur(10px);
          border: 1px solid var(--border-soft);
          border-radius: 14px;
          padding: 22px 18px;
          text-align: center;
          margin-bottom: 10px;
          min-height: 120px;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          box-sizing: border-box;
          transition: transform 0.25s ease, border-color 0.25s ease;
      }
      .metric-card:hover {
          transform: translateY(-2px);
          border-color: var(--border-mid);
      }
      .metric-card h3 {
          color: var(--muted);
          font-size: 0.68rem;
          text-transform: uppercase;
          letter-spacing: 0.18em;
          margin: 0;
          font-family: 'Inter', sans-serif !important;
          font-weight: 500;
      }
      .metric-card .value {
          font-size: 2.4rem;
          font-weight: 400;
          margin: 6px 0 0 0;
          font-family: 'Instrument Serif', Georgia, serif !important;
          letter-spacing: -0.02em;
      }
      .metric-card .value.red { color: #ff7a85; }
      .metric-card .value.orange { color: #ffb168; }
      .metric-card .value.blue { color: #5fb8ff; }
      .metric-card .value.green { color: #6fd9a8; }
      .metric-card .value.yellow { color: #ffd86b; }
      .metric-card .value.brown { color: #d8a878; }

      /* ── Alert cards (glass) ───────────────────────────────── */
      .alert-card {
          background: rgba(255, 255, 255, 0.03);
          border-left: 3px solid;
          border-radius: 10px;
          padding: 12px 16px;
          margin-bottom: 8px;
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
      }
      .alert-critical { border-color: #ff5566; }
      .alert-high { border-color: #ff9944; }
      .alert-moderate { border-color: #ffd86b; }
      .alert-low { border-color: #6fd9a8; }
      .alert-card .alert-type {
          font-size: 0.7rem;
          text-transform: uppercase;
          letter-spacing: 0.16em;
          font-weight: 600;
      }
      .alert-card .alert-title {
          font-size: 0.95rem;
          color: var(--fg);
          margin: 4px 0;
      }
      .alert-card .alert-time {
          font-size: 0.72rem;
          color: var(--muted);
      }

      /* ── Section headers (minimal) ─────────────────────────── */
    /* Section headers (prominent glass) */
      .section-header {
          background: rgba(255, 255, 255, 0.07);
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
          border: 1px solid rgba(255, 255, 255, 0.18);
          padding: 16px 22px;
          margin: 28px 0 16px 0;
          border-radius: 14px;
          box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.10), 0 6px 24px rgba(0, 0, 0, 0.22);
          position: relative;
          overflow: hidden;
      }
      .section-header::before {
          content: '';
          position: absolute;
          left: 0; top: 0; bottom: 0;
          width: 3px;
          background: linear-gradient(180deg, var(--accent), rgba(95,184,255,0));
      }
      .section-header h2 {
          color: var(--fg) !important;
          margin: 0;
          font-family: 'Instrument Serif', Georgia, serif !important;
          font-size: 1.75rem;
          font-weight: 400;
          letter-spacing: -0.01em;
      }
      /* Top navigation glass pills */
      .top-nav-wrap {
          margin: 0 0 22px 0;
          padding: 10px 14px;
          background: rgba(255, 255, 255, 0.06);
          backdrop-filter: blur(14px);
          -webkit-backdrop-filter: blur(14px);
          border: 1px solid var(--border-soft);
          border-radius: 999px;
          box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.10), 0 6px 24px rgba(0, 0, 0, 0.25);
      }
      .top-nav-wrap div[role="radiogroup"] {
          gap: 6px !important;
          flex-wrap: wrap;
          justify-content: center;
      }
      .top-nav-wrap div[role="radiogroup"] label {
          background: transparent !important;
          border: 1px solid transparent !important;
          border-radius: 999px !important;
          padding: 8px 18px !important;
          margin: 0 !important;
          cursor: pointer;
          transition: background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
      }
      .top-nav-wrap div[role="radiogroup"] label:hover {
          background: rgba(255, 255, 255, 0.07) !important;
          border-color: var(--border-soft) !important;
      }
      .top-nav-wrap div[role="radiogroup"] label:has(input:checked) {
          background: rgba(255, 255, 255, 0.14) !important;
          border-color: rgba(255, 255, 255, 0.28) !important;
      }
      .top-nav-wrap div[role="radiogroup"] label > div:first-child,
      .top-nav-wrap div[role="radiogroup"] label input {
          display: none !important;
      }
      .top-nav-wrap div[role="radiogroup"] label p,
      .top-nav-wrap div[role="radiogroup"] label span {
          color: var(--fg) !important;
          font-family: 'Inter', sans-serif !important;
          font-weight: 500 !important;
          font-size: 0.86rem !important;
          margin: 0 !important;
      }

      /* ── Resource cards ────────────────────────────────────── */
      .resource-card {
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid var(--border-soft);
          border-radius: 12px;
          padding: 18px;
          margin-bottom: 12px;
          backdrop-filter: blur(8px);
          -webkit-backdrop-filter: blur(8px);
      }
      .resource-card h4 {
          color: var(--accent);
          margin: 0 0 8px 0;
          font-family: 'Instrument Serif', Georgia, serif !important;
          font-weight: 400;
          font-size: 1.15rem;
      }
      .resource-card p {
          color: var(--fg);
          font-size: 0.86rem;
          margin: 3px 0;
          opacity: 0.9;
      }

      /* ── Risk bars ─────────────────────────────────────────── */
      .risk-bar {
          background: rgba(255, 255, 255, 0.08);
          border-radius: 6px;
          height: 12px;
          overflow: hidden;
          margin: 4px 0;
      }
      .risk-fill {
          height: 100%;
          border-radius: 6px;
          transition: width 0.5s ease;
      }

      /* ── Expanders ─────────────────────────────────────────── */
      div[data-testid="stExpander"] {
          background: rgba(255, 255, 255, 0.03) !important;
          border: 1px solid var(--border-soft) !important;
          border-radius: 12px !important;
      }
      div[data-testid="stExpander"] summary,
      div[data-testid="stExpander"] p,
      div[data-testid="stExpander"] span {
          color: var(--fg) !important;
      }

      /* ── Tabs (glass pills) ────────────────────────────────── */
      .stTabs [data-baseweb="tab-list"] {
          gap: 6px;
          background: transparent;
          border-bottom: 1px solid var(--border-soft);
      }
      .stTabs [data-baseweb="tab"] {
          background: transparent !important;
          border: none !important;
          border-radius: 0 !important;
          color: var(--muted) !important;
          padding: 10px 18px !important;
          font-family: 'Inter', sans-serif !important;
          font-size: 0.88rem !important;
          font-weight: 500 !important;
          transition: color 0.2s ease;
      }
      .stTabs [data-baseweb="tab"]:hover {
          color: var(--fg) !important;
      }
      .stTabs [aria-selected="true"] {
          background: transparent !important;
          color: var(--fg) !important;
          border-bottom: 2px solid var(--accent) !important;
      }

      /* ── Evac steps ────────────────────────────────────────── */
      .evac-step {
          background: rgba(255, 255, 255, 0.04);
          border-radius: 10px;
          padding: 11px 14px;
          margin: 4px 0;
          border-left: 3px solid var(--accent);
          color: var(--fg);
      }

      /* ── Streamlit metric ──────────────────────────────────── */
      div[data-testid="stMetric"] {
          background: rgba(255, 255, 255, 0.04) !important;
          border: 1px solid var(--border-soft) !important;
          border-radius: 12px !important;
          padding: 16px !important;
      }
      div[data-testid="stMetric"] label {
          color: var(--muted) !important;
      }
      div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
          color: var(--fg) !important;
          font-family: 'Instrument Serif', Georgia, serif !important;
      }

      /* ── Inputs ────────────────────────────────────────────── */
      .stSelectbox > div > div,
      .stMultiSelect > div > div,
      .stTextInput > div > div > input,
      .stNumberInput > div > div > input,
      div[data-baseweb="select"] > div {
          background: rgba(255, 255, 255, 0.05) !important;
          border-color: var(--border-mid) !important;
          color: var(--fg) !important;
          border-radius: 10px !important;
      }
      .stSelectbox label,
      .stMultiSelect label,
      .stTextInput label,
      .stNumberInput label,
      .stRadio label,
      .stCheckbox label {
          color: var(--fg) !important;
      }

      /* ── Buttons ───────────────────────────────────────────── */
      .stButton > button,
      .stDownloadButton > button {
          background: rgba(255, 255, 255, 0.04) !important;
          border: 1px solid var(--border-mid) !important;
          color: var(--fg) !important;
          border-radius: 999px !important;
          padding: 8px 22px !important;
          font-family: 'Inter', sans-serif !important;
          font-weight: 500 !important;
          transition: transform 0.18s ease, background 0.18s ease;
      }
      .stButton > button:hover {
          background: rgba(255, 255, 255, 0.10) !important;
          transform: scale(1.03);
      }

      /* ── Plotly charts (transparent bg) ───────────────────── */
      .js-plotly-plot, .plotly {
          background: transparent !important;
      }

      /* ── Legend chips ──────────────────────────────────────── */
      .legend-item {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          margin: 4px 8px 4px 0;
          padding: 5px 12px;
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid var(--border-soft);
          border-radius: 999px;
          font-size: 0.78rem;
          color: var(--fg);
      }
      .legend-dot {
          display: inline-block;
          width: 8px;
          height: 8px;
          border-radius: 50%;
          vertical-align: middle;
      }

      /* ── General text ──────────────────────────────────────── */
      p, span, div, li {
          color: var(--fg);
      }
      .stApp a {
          color: var(--accent);
      }

      /* ── Animations ───────────────────────────────────────── */
      @keyframes fade-rise {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
      }
      .animate-fade-rise { animation: fade-rise 0.85s ease-out both; }
      .animate-fade-rise-delay { animation: fade-rise 0.85s ease-out 0.18s both; }
      .animate-fade-rise-delay-2 { animation: fade-rise 0.85s ease-out 0.36s both; }

      /* ── Menu popover (kept dark-themed) ──────────────────── */
      [data-baseweb="popover"] {
          min-width: 240px !important;
          border-radius: 12px !important;
          box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
          overflow: hidden !important;
      }
      [data-baseweb="popover"] [data-baseweb="menu"],
      [data-baseweb="popover"] ul {
          background: #001f2e !important;
          border: 1px solid var(--border-mid) !important;
      }
      [data-baseweb="popover"] li,
      [data-baseweb="popover"] [role="option"] {
          color: var(--fg) !important;
          padding: 12px 20px !important;
          font-family: 'Inter', sans-serif !important;
      }
      [data-baseweb="popover"] li:hover {
          background: rgba(255, 255, 255, 0.06) !important;
          color: var(--accent) !important;
      }
  </style>
  """

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_metric(label, value, color="blue"):
    return f"""
    <div class="metric-card">
        <h3>{label}</h3>
        <div class="value {color}">{value}</div>
    </div>
    """


def render_alert_card(event):
    sev = _safe(event.get("severity", "Moderate")).lower()
    dtype = _safe(event.get("type", "Unknown"))
    title = _safe(event.get("title", ""))
    time_str = ""
    if event.get("time"):
        if isinstance(event["time"], datetime):
            time_str = event["time"].strftime("%Y-%m-%d %H:%M UTC")
        else:
            time_str = _safe(str(event["time"]))
    color = DISASTER_COLORS.get(event.get("type", ""), "#ffffff")
    return f"""
    <div class="alert-card alert-{sev}">
        <div class="alert-type" style="color: {color};">● {dtype}</div>
        <div class="alert-title">{title}</div>
        <div class="alert-time">{time_str}</div>
    </div>
    """


def render_risk_bar(name, score, max_score=10):
    pct = (score / max_score) * 100
    if score >= 8:
        color = "#ff4444"
    elif score >= 6:
        color = "#ff8800"
    elif score >= 4:
        color = "#ffcc00"
    else:
        color = "#44cc88"
    return f"""
    <div style="display:flex; align-items:center; margin:6px 0;">
        <span style="width:160px; color:#9be8a8; font-size:0.85rem;">{name}</span>
        <div class="risk-bar" style="flex:1;">
            <div class="risk-fill" style="width:{pct}%; background:{color};"></div>
        </div>
        <span style="width:40px; text-align:right; color:{color}; font-weight:600; font-size:0.85rem;">{score}/10</span>
    </div>
    """


def page_dashboard():
    st.markdown("""
    """, unsafe_allow_html=True)

    with st.spinner("Loading live disaster data..."):
        events = get_all_live_events()

    mine_events = get_mine_events()
    ree_events = get_rare_earth_events()
    all_events = events + mine_events + ree_events

    type_counts = {}
    severity_counts = {"Critical": 0, "High": 0, "Moderate": 0, "Low": 0}
    for e in all_events:
        t = e.get("type", "Other")
        type_counts[t] = type_counts.get(t, 0) + 1
        s = e.get("severity", "Moderate")
        severity_counts[s] = severity_counts.get(s, 0) + 1

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(render_metric("Live Events", len(events), "red"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_metric("Critical", severity_counts.get("Critical", 0), "red"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_metric("High Severity", severity_counts.get("High", 0), "orange"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_metric("Disaster Types", len(type_counts), "blue"), unsafe_allow_html=True)
    with c5:
        st.markdown(render_metric("Mine Sites", len(mine_events) + len(ree_events), "brown"), unsafe_allow_html=True)

    st.markdown('<div class="section-header"><h2>🗺️ Global Disaster + Mining Map</h2></div>', unsafe_allow_html=True)

    all_types = sorted(type_counts.keys())
    filter_types = st.multiselect(
        "Filter by disaster/mine type (leave empty to show all)",
        options=all_types,
        default=None,
        key="dash_filter"
    )

    legend_html = '<div style="margin-bottom:10px;">'
    for dtype, color in sorted(DISASTER_COLORS.items()):
        if dtype in type_counts:
            legend_html += f'<span class="legend-item"><span class="legend-dot" style="background:{color};"></span>{dtype} ({type_counts.get(dtype, 0)})</span>'
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    gmap = create_global_map(all_events, selected_types=filter_types if filter_types else None, height=580)
    st_folium(gmap, width=None, height=560, returned_objects=[])

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown('<div class="section-header"><h2>📊 Event Distribution</h2></div>', unsafe_allow_html=True)
        if type_counts:
            df_types = pd.DataFrame(list(type_counts.items()), columns=["Type", "Count"])
            df_types = df_types.sort_values("Count", ascending=True)
            colors = [DISASTER_COLORS.get(t, "#4488ff") for t in df_types["Type"]]
            fig = go.Figure(go.Bar(
                x=df_types["Count"], y=df_types["Type"],
                orientation='h', marker_color=colors,
                text=df_types["Count"], textposition="auto",
                textfont=dict(color="#ffffff", family="Inter"),
                insidetextfont=dict(color="#ffffff"),
                outsidetextfont=dict(color="#ffffff")
            ))
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ffffff", family="Inter"), height=350,
                margin=dict(l=0, r=20, t=10, b=10),
                xaxis=dict(gridcolor="rgba(255,255,255,0.10)", tickfont=dict(color="#a8aab1")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.10)", tickfont=dict(color="#a8aab1"))
            )
            st.plotly_chart(fig, width="stretch")

    with col_right:
        st.markdown('<div class="section-header"><h2>🚨 Latest Alerts</h2></div>', unsafe_allow_html=True)
        sev_rank = {"Critical": 0, "High": 1, "Moderate": 2, "Low": 3}
        sorted_events = sorted(
            all_events,
            key=lambda e: (
                -(_sort_time(e) - datetime.min).total_seconds(),
                sev_rank.get(e.get("severity", "Low"), 4)
            )
        )
        alert_container = st.container()
        with alert_container:
            for event in sorted_events[:12]:
                st.markdown(render_alert_card(event), unsafe_allow_html=True)

    st.markdown('<div class="section-header"><h2>📋 Global Disaster History & Situation Reports</h2></div>', unsafe_allow_html=True)

    dr_tab1, dr_tab2, dr_tab3 = st.tabs(["📰 News & Situation Reports", "📚 Research Publications", "🌴 Tropical Focus"])

    with dr_tab1:
        dr_filter = st.selectbox("Filter by disaster type", ["All Types", "Flood", "Extreme Temperature", "Landslide", "Tropical Cyclone", "Wildfire", "Drought", "Earthquake", "Coastal Pollution", "Volcanic Eruption", "Storm"], key="dash_dr_filter")
        if dr_filter == "All Types":
            display_disasters = sorted(HISTORICAL_DISASTERS, key=lambda x: x.get("date", ""), reverse=True)
        else:
            display_disasters = get_disasters_by_type(dr_filter, limit=100)
        st.markdown(f"**Showing {len(display_disasters)} situation reports**")
        dr_cols = st.columns(3)
        for idx, d in enumerate(display_disasters[:30]):
            with dr_cols[idx % 3]:
                sev = d.get("severity", "Moderate")
                sev_class = {"Critical": "alert-critical", "High": "alert-high", "Moderate": "alert-moderate", "Low": "alert-low"}.get(sev, "alert-moderate")
                casualties_str = f" | ☠️ {d['casualties']:,}" if d.get("casualties") else ""
                displaced_str = f" | 👥 {d['displaced']:,} displaced" if d.get("displaced") else ""
                st.markdown(f"""
                <div class="alert-card {sev_class}">
                    <div class="alert-type" style="color:{DISASTER_COLORS.get(d.get('type', ''), '#4488ff')};">{_safe(d.get('type', ''))}</div>
                    <div class="alert-title">{_safe(d.get('title', ''))}</div>
                    <div class="alert-time">📅 {_safe(d.get('date', ''))} | 📍 {_safe(d.get('country', ''))}{casualties_str}{displaced_str}</div>
                    <div style="color:#9be8a8;margin-top:5px;font-size:0.8rem;line-height:1.4;">{_safe(d.get('description', '')[:180])}...</div>
                    <div style="margin-top:4px;font-size:0.7rem;color:#1a66cc;">Source: {_safe(d.get('source', ''))}</div>
                </div>
                """, unsafe_allow_html=True)

    with dr_tab2:
        ra_filter = st.selectbox("Filter by disaster type", ["All Types", "Flood", "Extreme Temperature", "Landslide", "Storm", "Wildfire", "Drought", "Earthquake", "Coastal Pollution", "Volcanic Eruption"], key="dash_ra_filter")
        if ra_filter == "All Types":
            display_research = sorted(RESEARCH_ARTICLES, key=lambda x: x.get("year", 0), reverse=True)
        else:
            display_research = get_research_by_type(ra_filter, limit=50)
        st.markdown(f"**Showing {len(display_research)} research publications**")
        for r in display_research:
            countries_str = ", ".join(r.get("countries", [])[:5])
            types_str = ", ".join(r.get("types", [])[:3])
            st.markdown(f"""
            <div class="resource-card">
                <h4>📄 {_safe(r.get('title', ''))}</h4>
                <p style="color:#1a66cc;font-size:0.8rem;">{_safe(r.get('authors', ''))} ({r.get('year', '')}) — <i>{_safe(r.get('journal', ''))}</i></p>
                <p>📍 {_safe(countries_str)} | ⚠️ {_safe(types_str)}</p>
                <p style="font-size:0.82rem;line-height:1.4;">{_safe(r.get('summary', ''))}</p>
            </div>
            """, unsafe_allow_html=True)

    with dr_tab3:
        tropical_disasters = get_tropical_disasters(limit=50)
        st.markdown(f"**{len(tropical_disasters)} disaster reports from tropical nations** — floods, heatwaves, landslides, coastal events, and more")
        tr_cols = st.columns(3)
        for idx, d in enumerate(tropical_disasters[:30]):
            with tr_cols[idx % 3]:
                sev = d.get("severity", "Moderate")
                sev_class = {"Critical": "alert-critical", "High": "alert-high", "Moderate": "alert-moderate", "Low": "alert-low"}.get(sev, "alert-moderate")
                casualties_str = f" | ☠️ {d['casualties']:,}" if d.get("casualties") else ""
                displaced_str = f" | 👥 {d['displaced']:,} displaced" if d.get("displaced") else ""
                st.markdown(f"""
                <div class="alert-card {sev_class}">
                    <div class="alert-type" style="color:{DISASTER_COLORS.get(d.get('type', ''), '#4488ff')};">{_safe(d.get('type', ''))}</div>
                    <div class="alert-title">{_safe(d.get('title', ''))}</div>
                    <div class="alert-time">📅 {_safe(d.get('date', ''))} | 📍 {_safe(d.get('country', ''))}{casualties_str}{displaced_str}</div>
                    <div style="color:#9be8a8;margin-top:5px;font-size:0.8rem;line-height:1.4;">{_safe(d.get('description', '')[:180])}...</div>
                    <div style="margin-top:4px;font-size:0.7rem;color:#1a66cc;">Source: {_safe(d.get('source', ''))}</div>
                </div>
                """, unsafe_allow_html=True)


def page_country_analysis():
    st.markdown('<h1 style="color:#1a66cc;">🏳️ Country Disaster Analysis</h1>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        country = st.selectbox("Select Country", sorted(COUNTRIES.keys()), index=sorted(COUNTRIES.keys()).index("United States"), key="country_select")
    with col2:
        if country in COUNTRY_STATES:
            state = st.selectbox("Select State/Region (optional)", ["All"] + COUNTRY_STATES[country], key="state_select")
        else:
            state = st.selectbox("Select State/Region (optional)", ["All"], key="state_select")

    info = COUNTRIES.get(country, {})
    base_lat, base_lon = info.get("lat", 0), info.get("lon", 0)
    region = info.get("region", "Unknown")

    state_coords = STATE_COORDS.get(country, {})
    if state and state != "All" and state in state_coords:
        lat, lon = state_coords[state]
        zoom = 7
        filter_radius = 5
        location_label = f"{state}, {country}"
    else:
        lat, lon = base_lat, base_lon
        zoom = 5
        filter_radius = 15
        location_label = country

    overall = get_overall_risk(country)
    top_risks = get_top_risks(country, 3)
    risk_label = "VERY HIGH" if overall >= 7 else "HIGH" if overall >= 5.5 else "MODERATE" if overall >= 4 else "LOW"
    risk_color = "red" if overall >= 7 else "orange" if overall >= 5.5 else "yellow" if overall >= 4 else "green"

    mc1, mc2, mc3, mc4 = st.columns(4)
    with mc1:
        st.markdown(render_metric("Overall Risk", f"{overall}/10", risk_color), unsafe_allow_html=True)
    with mc2:
        st.markdown(render_metric("Risk Level", risk_label, risk_color), unsafe_allow_html=True)
    with mc3:
        st.markdown(render_metric("Location", location_label, "blue"), unsafe_allow_html=True)
    with mc4:
        st.markdown(render_metric("Top Threat", top_risks[0][0] if top_risks else "N/A", "orange"), unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Map & Overview", "📊 Risk Profile", "🤖 AI Summary", "🌡️ Weather", "🎒 Travel Safety"])

    with tab1:
        events = get_all_live_events()
        country_events = []
        for e in events:
            elat, elon = e.get("lat", 0), e.get("lon", 0)
            if abs(elat - lat) < filter_radius and abs(elon - lon) < filter_radius:
                country_events.append(e)

        c_left, c_right = st.columns([2, 1])
        with c_left:
            cmap = create_country_map(lat, lon, events=country_events, zoom=zoom)
            st_folium(cmap, width=None, height=450, returned_objects=[])
        with c_right:
            st.markdown(f"### Active Events Near {_safe(location_label)}")
            if country_events:
                for ev in country_events[:8]:
                    st.markdown(render_alert_card(ev), unsafe_allow_html=True)
            else:
                st.info(f"No active disaster events currently detected near {location_label}.")

    with tab2:
        st.markdown('<div class="section-header"><h2>Disaster Risk Profile</h2></div>', unsafe_allow_html=True)
        profile = get_risk_profile(country)
        sorted_profile = sorted(profile.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_profile:
            st.markdown(render_risk_bar(name, score), unsafe_allow_html=True)

        st.markdown('<div class="section-header"><h2>Risk Distribution</h2></div>', unsafe_allow_html=True)
        df_risk = pd.DataFrame(sorted_profile, columns=["Disaster", "Risk Score"])
        colors = [DISASTER_COLORS.get(d, "#4488ff") for d in df_risk["Disaster"]]
        fig = go.Figure(go.Scatterpolar(
            r=df_risk["Risk Score"].tolist() + [df_risk["Risk Score"].iloc[0]],
            theta=df_risk["Disaster"].tolist() + [df_risk["Disaster"].iloc[0]],
            fill='toself',
            fillcolor='rgba(79, 195, 247, 0.2)',
            line=dict(color='#4fc3f7', width=2),
        ))
        fig.update_layout(
            polar=dict(
                bgcolor="#f8f9fa",
                radialaxis=dict(visible=True, range=[0, 10], gridcolor="rgba(255,255,255,0.15)", color="#a8aab1"),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.15)", color="#a8aab1")
            ),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ffffff", font_family="Inter", height=400,
            margin=dict(l=60, r=60, t=30, b=30),
            showlegend=False
        )
        st.plotly_chart(fig, width="stretch")

        st.markdown('<div class="section-header"><h2>Detailed Analysis by Type</h2></div>', unsafe_allow_html=True)
        selected_disaster = st.selectbox("Select disaster type for detailed analysis", DISASTER_TYPES, key="detail_disaster")
        st.markdown(generate_disaster_analysis(country, selected_disaster))

    with tab3:
        st.markdown('<div class="section-header"><h2>AI Resilience Summary</h2></div>', unsafe_allow_html=True)
        summary = generate_country_summary(country)
        st.markdown(summary)

        st.markdown('<div class="section-header"><h2>Historical Context</h2></div>', unsafe_allow_html=True)
        reliefweb = fetch_reliefweb_disasters(50)
        country_disasters_rw = [d for d in reliefweb if country in d.get("countries", [])]
        if country_disasters_rw:
            st.markdown(f"**Recent ReliefWeb reports involving {country}:**")
            for d in country_disasters_rw[:5]:
                st.markdown(f"""
                <div class="alert-card alert-moderate">
                    <div class="alert-title">{_safe(d.get('name', ''))}</div>
                    <div class="alert-time">{_safe(', '.join(d.get('types', [])))} — {_safe(d.get('date', '')[:10])}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f'<div class="section-header"><h2>📰 Disaster History — {_safe(country)}</h2></div>', unsafe_allow_html=True)
        country_hist = get_country_disasters(country, limit=20)
        if country_hist:
            st.markdown(f"**{len(country_hist)} historical disaster situation reports for {country}:**")
            for d in country_hist:
                sev = d.get("severity", "Moderate")
                sev_class = {"Critical": "alert-critical", "High": "alert-high", "Moderate": "alert-moderate", "Low": "alert-low"}.get(sev, "alert-moderate")
                casualties_str = f" | Casualties: {d['casualties']:,}" if d.get("casualties") else ""
                displaced_str = f" | Displaced: {d['displaced']:,}" if d.get("displaced") else ""
                st.markdown(f"""
                <div class="alert-card {sev_class}">
                    <div class="alert-type" style="color:{DISASTER_COLORS.get(d.get('type', ''), '#4488ff')};">{_safe(d.get('type', ''))}</div>
                    <div class="alert-title">{_safe(d.get('title', ''))}</div>
                    <div class="alert-time">📅 {_safe(d.get('date', ''))}{casualties_str}{displaced_str}</div>
                    <div style="color:#9be8a8;margin-top:5px;font-size:0.82rem;line-height:1.4;">{_safe(d.get('description', ''))}</div>
                    <div style="margin-top:4px;font-size:0.7rem;color:#1a66cc;">Source: {_safe(d.get('source', ''))}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No historical disaster situation reports available for {country}.")

        st.markdown(f'<div class="section-header"><h2>📚 Research Publications — {_safe(country)}</h2></div>', unsafe_allow_html=True)
        country_research = get_country_research(country, limit=10)
        if country_research:
            st.markdown(f"**{len(country_research)} academic publications referencing {country}:**")
            for r in country_research:
                types_str = ", ".join(r.get("types", [])[:3])
                st.markdown(f"""
                <div class="resource-card">
                    <h4>📄 {_safe(r.get('title', ''))}</h4>
                    <p style="color:#1a66cc;font-size:0.8rem;">{_safe(r.get('authors', ''))} ({r.get('year', '')}) — <i>{_safe(r.get('journal', ''))}</i></p>
                    <p>⚠️ {_safe(types_str)}</p>
                    <p style="font-size:0.82rem;line-height:1.4;">{_safe(r.get('summary', ''))}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(f"No research publications found referencing {country}.")

    with tab4:
        st.markdown(f'<div class="section-header"><h2>Current Weather & Forecast — {_safe(location_label)}</h2></div>', unsafe_allow_html=True)
        weather = fetch_weather_data(lat, lon)
        if weather:
            current = weather.get("current", {})
            temp = current.get("temperature_2m", "N/A")
            humidity = current.get("relative_humidity_2m", "N/A")
            wind = current.get("wind_speed_10m", "N/A")
            precip = current.get("precipitation", 0)
            code = current.get("weather_code", 0)
            apparent = current.get("apparent_temperature", "N/A")

            wc1, wc2, wc3, wc4, wc5 = st.columns(5)
            with wc1:
                st.metric("Temperature", f"{temp}°C")
            with wc2:
                st.metric("Feels Like", f"{apparent}°C")
            with wc3:
                st.metric("Humidity", f"{humidity}%")
            with wc4:
                st.metric("Wind Speed", f"{wind} km/h")
            with wc5:
                st.metric("Condition", decode_weather(code))

            heat_alert = False
            cold_alert = False
            if isinstance(temp, (int, float)):
                if temp >= 40:
                    heat_alert = True
                    st.error(f"🔥 **EXTREME HEAT ALERT**: Temperature of {temp}°C exceeds 40°C threshold. Take immediate precautions — stay hydrated, avoid outdoor activity, seek shade or air conditioning.")
                elif temp >= 35:
                    st.warning(f"🌡️ **Heat Advisory**: Temperature of {temp}°C is dangerously high. Limit outdoor exposure and ensure adequate hydration.")
                if temp <= -20:
                    cold_alert = True
                    st.error(f"❄️ **EXTREME COLD ALERT**: Temperature of {temp}°C is dangerously low. Risk of hypothermia and frostbite — stay indoors and dress in layers.")

            daily = weather.get("daily", {})
            if daily.get("time"):
                df_forecast = pd.DataFrame({
                    "Date": daily["time"],
                    "Max Temp (°C)": daily.get("temperature_2m_max", []),
                    "Min Temp (°C)": daily.get("temperature_2m_min", []),
                    "Precipitation (mm)": daily.get("precipitation_sum", []),
                    "Max Wind (km/h)": daily.get("wind_speed_10m_max", []),
                })

                fig_temp = go.Figure()
                fig_temp.add_trace(go.Scatter(
                    x=df_forecast["Date"], y=df_forecast["Max Temp (°C)"],
                    mode="lines+markers", name="Max Temp",
                    line=dict(color="#ff6644", width=2), marker=dict(size=6)
                ))
                fig_temp.add_trace(go.Scatter(
                    x=df_forecast["Date"], y=df_forecast["Min Temp (°C)"],
                    mode="lines+markers", name="Min Temp",
                    line=dict(color="#4488ff", width=2), marker=dict(size=6)
                ))
                fig_temp.add_hline(y=40, line_dash="dash", line_color="#ff0000", annotation_text="Heat Alert (40°C)")
                fig_temp.update_layout(
                    title="7-Day Temperature Forecast",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff", font_family="Inter", height=300,
                    margin=dict(l=40, r=20, t=40, b=30),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.10)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.10)", title="°C"),
                    legend=dict(bgcolor="rgba(255,255,255,0.8)")
                )
                st.plotly_chart(fig_temp, width="stretch")

                fig_precip = go.Figure(go.Bar(
                    x=df_forecast["Date"], y=df_forecast["Precipitation (mm)"],
                    marker_color="#4488ff", text=df_forecast["Precipitation (mm)"],
                    textposition="auto"
                ))
                fig_precip.update_layout(
                    title="7-Day Precipitation Forecast",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff", font_family="Inter", height=250,
                    margin=dict(l=40, r=20, t=40, b=30),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.10)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.10)", title="mm")
                )
                st.plotly_chart(fig_precip, width="stretch")
        else:
            st.warning("Weather data is currently unavailable for this location.")

    with tab5:
        st.markdown(f'<div class="section-header"><h2>Travel Safety Guide — {country}</h2></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="resource-card">
            <h4>⚠️ Key Risks for Travelers to {country}</h4>
            <p>Top threats: <b>{top_risks[0][0]}</b> ({top_risks[0][1]}/10), <b>{top_risks[1][0]}</b> ({top_risks[1][1]}/10), <b>{top_risks[2][0]}</b> ({top_risks[2][1]}/10)</p>
            <p>Overall risk level: <b>{risk_label}</b></p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Evacuation Guides by Disaster Type")
        for risk_name, risk_score in top_risks:
            guide = EVACUATION_GUIDES.get(risk_name, {})
            if guide:
                with st.expander(f"🚨 {risk_name} — Risk: {risk_score}/10"):
                    bcol, dcol, acol = st.columns(3)
                    with bcol:
                        st.markdown("**Before**")
                        for step in guide.get("before", []):
                            st.markdown(f'<div class="evac-step">✅ {step}</div>', unsafe_allow_html=True)
                    with dcol:
                        st.markdown("**During**")
                        for step in guide.get("during", []):
                            st.markdown(f'<div class="evac-step">⚡ {step}</div>', unsafe_allow_html=True)
                    with acol:
                        st.markdown("**After**")
                        for step in guide.get("after", []):
                            st.markdown(f'<div class="evac-step">🔄 {step}</div>', unsafe_allow_html=True)


def page_live_alerts():
    st.markdown('<h1 style="color:#1a66cc;">🚨 Live Disaster Alerts</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#333333;">Real-time feed from USGS, NASA EONET, and GDACS</p>', unsafe_allow_html=True)

    with st.spinner("Fetching live data..."):
        events = get_all_live_events()

    tab_eq, tab_all, tab_sev = st.tabs(["🌍 Earthquakes", "📋 All Events", "⚠️ By Severity"])

    with tab_eq:
        earthquakes = [e for e in events if e.get("type") == "Earthquake"]
        st.markdown(f"**{len(earthquakes)} earthquakes** detected in the last 7 days (M2.5+)")

        eq_col1, eq_col2 = st.columns([2, 1])
        with eq_col1:
            eq_map = create_global_map(earthquakes)
            st_folium(eq_map, width=None, height=400, returned_objects=[])
        with eq_col2:
            if earthquakes:
                mag_groups = {"6+": 0, "5-5.9": 0, "4-4.9": 0, "2.5-3.9": 0}
                for eq in earthquakes:
                    m = eq.get("magnitude", 0) or 0
                    if m >= 6:
                        mag_groups["6+"] += 1
                    elif m >= 5:
                        mag_groups["5-5.9"] += 1
                    elif m >= 4:
                        mag_groups["4-4.9"] += 1
                    else:
                        mag_groups["2.5-3.9"] += 1
                for group, count in mag_groups.items():
                    color = "#ff4444" if "6" in group else "#ff8800" if "5" in group else "#ffcc00" if "4" in group else "#44cc88"
                    st.markdown(f"""<div class="alert-card" style="border-color:{color};">
                        <span style="color:{color};font-weight:bold;">M{group}</span>: {count} events
                    </div>""", unsafe_allow_html=True)

        if earthquakes:
            st.markdown("#### Recent Significant Earthquakes")
            sorted_eq = sorted(earthquakes, key=lambda e: e.get("magnitude", 0) or 0, reverse=True)
            df_eq = pd.DataFrame([{
                "Magnitude": e.get("magnitude", ""),
                "Location": e.get("place", ""),
                "Depth (km)": f"{e.get('depth', 0):.1f}" if e.get("depth") else "",
                "Time (UTC)": e["time"].strftime("%Y-%m-%d %H:%M") if isinstance(e.get("time"), datetime) else "",
                "Severity": e.get("severity", ""),
                "Tsunami": "Yes" if e.get("tsunami") else "No"
            } for e in sorted_eq[:30]])
            st.dataframe(df_eq, use_container_width=True, hide_index=True)

    with tab_all:
        type_filter = st.multiselect("Filter by type", sorted(set(e.get("type", "") for e in events)), key="alert_type_filter")
        filtered = events if not type_filter else [e for e in events if e.get("type") in type_filter]
        st.markdown(f"**{len(filtered)} events** displayed")
        for event in sorted(filtered, key=_sort_time, reverse=True)[:50]:
            st.markdown(render_alert_card(event), unsafe_allow_html=True)

    with tab_sev:
        for sev_level in ["Critical", "High", "Moderate", "Low"]:
            sev_events = [e for e in events if e.get("severity") == sev_level]
            if sev_events:
                sev_colors = {"Critical": "#ff4444", "High": "#ff8800", "Moderate": "#ffcc00", "Low": "#44cc88"}
                st.markdown(f"### <span style='color:{sev_colors[sev_level]};'>{sev_level}</span> — {len(sev_events)} events", unsafe_allow_html=True)
                for ev in sev_events[:10]:
                    st.markdown(render_alert_card(ev), unsafe_allow_html=True)


def page_drought_heatwave():
    st.markdown('<h1 style="color:#1a66cc;">🌡️ Drought & Heatwave Center</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#333333;">Specialized monitoring for extreme heat, drought conditions, and water stress</p>', unsafe_allow_html=True)

    tab_monitor, tab_help, tab_crops, tab_water = st.tabs(["🌡️ Heat Monitor", "💧 Drought Help", "🌾 Crop Advice", "🏗️ Water Harvesting"])

    with tab_monitor:
        st.markdown('<div class="section-header"><h2>Global Heat & Drought Monitor</h2></div>', unsafe_allow_html=True)

        monitor_country = st.selectbox("Select country to monitor", sorted(COUNTRIES.keys()), index=sorted(COUNTRIES.keys()).index("India"), key="heat_country")
        info = COUNTRIES.get(monitor_country, {})
        lat, lon = info.get("lat", 0), info.get("lon", 0)

        weather = fetch_weather_data(lat, lon)

        if weather:
            current = weather.get("current", {})
            temp = current.get("temperature_2m", 0)
            humidity = current.get("relative_humidity_2m", 0)
            apparent = current.get("apparent_temperature", 0)

            hc1, hc2, hc3, hc4 = st.columns(4)
            with hc1:
                st.metric("Current Temp", f"{temp}°C")
            with hc2:
                st.metric("Feels Like", f"{apparent}°C")
            with hc3:
                st.metric("Humidity", f"{humidity}%")
            with hc4:
                heat_index = "EXTREME" if isinstance(temp, (int, float)) and temp >= 45 else "DANGER" if isinstance(temp, (int, float)) and temp >= 40 else "CAUTION" if isinstance(temp, (int, float)) and temp >= 35 else "OK"
                st.metric("Heat Index", heat_index)

            if isinstance(temp, (int, float)):
                if temp >= 40:
                    st.error(f"""
                    🔥 **EXTREME HEAT ALERT — {monitor_country}**

                    Current temperature ({temp}°C) exceeds the 40°C danger threshold.

                    **Immediate Actions:**
                    - Stay indoors in air-conditioned spaces
                    - Drink water every 15-20 minutes even if not thirsty
                    - Avoid outdoor activities between 10 AM - 4 PM
                    - Check on elderly neighbors and vulnerable persons
                    - Watch for heat exhaustion symptoms: heavy sweating, weakness, nausea, dizziness
                    """)
                elif temp >= 35:
                    st.warning(f"""
                    🌡️ **Heat Advisory — {monitor_country}**

                    Temperature of {temp}°C warrants caution. Stay hydrated and limit outdoor exertion.
                    """)

            daily = weather.get("daily", {})
            if daily.get("time"):
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                precip = daily.get("precipitation_sum", [])

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=daily["time"], y=max_temps, mode="lines+markers", name="Max Temp", line=dict(color="#ff4444", width=2)))
                fig.add_trace(go.Scatter(x=daily["time"], y=min_temps, mode="lines+markers", name="Min Temp", line=dict(color="#4488ff", width=2)))
                fig.add_hline(y=40, line_dash="dash", line_color="#ff0000", annotation_text="Danger: 40°C")
                fig.add_hline(y=35, line_dash="dot", line_color="#ff8800", annotation_text="Caution: 35°C")
                fig.update_layout(
                    title=f"7-Day Temperature Forecast — {monitor_country}",
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font_color="#ffffff", font_family="Inter", height=350,
                    xaxis=dict(gridcolor="rgba(255,255,255,0.10)"), yaxis=dict(gridcolor="rgba(255,255,255,0.10)", title="°C"),
                    legend=dict(bgcolor="rgba(255,255,255,0.8)"),
                    margin=dict(l=40, r=20, t=40, b=30)
                )
                st.plotly_chart(fig, width="stretch")

                total_precip = sum(p for p in precip if p is not None)
                avg_max = sum(t for t in max_temps if t is not None) / max(len(max_temps), 1)
                days_above_35 = sum(1 for t in max_temps if t is not None and t >= 35)
                days_above_40 = sum(1 for t in max_temps if t is not None and t >= 40)

                dc1, dc2, dc3, dc4 = st.columns(4)
                with dc1:
                    st.metric("7-Day Total Precip", f"{total_precip:.1f} mm")
                with dc2:
                    st.metric("Avg Max Temp", f"{avg_max:.1f}°C")
                with dc3:
                    st.metric("Days >35°C", str(days_above_35))
                with dc4:
                    st.metric("Days >40°C", str(days_above_40))

                if total_precip < 1:
                    st.warning("⚠️ **Dry Spell Alert**: Less than 1mm total precipitation forecast over the next 7 days. Drought conditions may develop or worsen.")
                if total_precip == 0 and avg_max > 35:
                    st.error("🚨 **Drought + Heat Compound Risk**: Zero precipitation combined with extreme heat significantly increases water stress, crop damage, and wildfire risk.")

        st.markdown('<div class="section-header"><h2>Drought Risk Index</h2></div>', unsafe_allow_html=True)
        profile = get_risk_profile(monitor_country)
        drought_score = profile.get("Drought", 3)
        heat_score = profile.get("Extreme Temperature", 3)
        st.markdown(render_risk_bar("Drought Risk", drought_score), unsafe_allow_html=True)
        st.markdown(render_risk_bar("Extreme Temperature Risk", heat_score), unsafe_allow_html=True)

        combined = (drought_score + heat_score) / 2
        if combined >= 7:
            st.error(f"🔴 {monitor_country} has a **VERY HIGH** combined drought and heat risk ({combined:.1f}/10). Chronic water stress and heat events are frequent concerns.")
        elif combined >= 5:
            st.warning(f"🟠 {monitor_country} has a **HIGH** combined drought and heat risk ({combined:.1f}/10). Seasonal water shortages and heat episodes are expected.")
        else:
            st.info(f"🟢 {monitor_country} has a **MODERATE** combined drought and heat risk ({combined:.1f}/10).")

    with tab_help:
        st.markdown('<div class="section-header"><h2>💧 Water Conservation & Drought Survival</h2></div>', unsafe_allow_html=True)

        st.markdown("### Water-Saving Tips")
        for i, tip in enumerate(DROUGHT_RESOURCES["water_tips"]):
            st.markdown(f'<div class="evac-step">💧 {tip}</div>', unsafe_allow_html=True)

        st.markdown("### Aid Organizations for Drought Relief")
        aid_cols = st.columns(2)
        drought_orgs = [o for o in AID_ORGANIZATIONS if "Drought" in o.get("focus", "") or "Food" in o.get("focus", "") or "Water" in o.get("focus", "") or "All" in o.get("focus", "")]
        for i, org in enumerate(drought_orgs):
            with aid_cols[i % 2]:
                st.markdown(f"""
                <div class="resource-card">
                    <h4>🏥 {org['name']}</h4>
                    <p>Focus: {org['focus']}</p>
                    <p>Type: {org['type']}</p>
                    <p>🔗 <a href="{org['url']}" target="_blank" style="color:#1a66cc;">{org['url']}</a></p>
                </div>
                """, unsafe_allow_html=True)

    with tab_crops:
        st.markdown('<div class="section-header"><h2>🌾 Drought-Resistant Crops</h2></div>', unsafe_allow_html=True)
        st.markdown("These crops are recommended for regions experiencing drought or water scarcity:")

        for crop_info in DROUGHT_RESOURCES["crop_advice"]:
            parts = crop_info.split("—")
            name = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            st.markdown(f"""
            <div class="resource-card">
                <h4>🌱 {name}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_water:
        st.markdown('<div class="section-header"><h2>🏗️ Community Rainwater Harvesting</h2></div>', unsafe_allow_html=True)
        st.markdown("Proven techniques for capturing and storing rainwater:")

        for i, technique in enumerate(DROUGHT_RESOURCES["harvesting_tips"]):
            parts = technique.split(":")
            name = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ""
            st.markdown(f"""
            <div class="alert-card alert-moderate">
                <div class="alert-type" style="color:#1a66cc;">#{i+1} {name}</div>
                <div class="alert-title">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def page_resources():
    st.markdown('<h1 style="color:#1a66cc;">🆘 Resource Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#333333;">Shelters, aid organizations, evacuation guides & community resources</p>', unsafe_allow_html=True)

    tab_orgs, tab_shelters, tab_evac, tab_prep, tab_community, tab_report = st.tabs(["🏥 Aid Organizations", "🏠 Shelter & Water Locator", "🚨 Evacuation Guides", "🎒 Preparedness", "👥 Community", "📝 Report Disaster"])

    with tab_orgs:
        st.markdown('<div class="section-header"><h2>Global Aid & Relief Organizations</h2></div>', unsafe_allow_html=True)

        org_type = st.selectbox("Filter by type", ["All"] + sorted(set(o["type"] for o in AID_ORGANIZATIONS)), key="org_filter")
        filtered_orgs = AID_ORGANIZATIONS if org_type == "All" else [o for o in AID_ORGANIZATIONS if o["type"] == org_type]

        org_cols = st.columns(2)
        for i, org in enumerate(filtered_orgs):
            with org_cols[i % 2]:
                st.markdown(f"""
                <div class="resource-card">
                    <h4>🏥 {org['name']}</h4>
                    <p><b>Focus:</b> {org['focus']}</p>
                    <p><b>Type:</b> {org['type']}</p>
                    <p>🔗 <a href="{org['url']}" target="_blank" style="color:#1a66cc;">{org['url']}</a></p>
                </div>
                """, unsafe_allow_html=True)

    with tab_shelters:
        st.markdown('<div class="section-header"><h2>🏠 Shelter & Water Point Locator</h2></div>', unsafe_allow_html=True)
        st.markdown("Find emergency shelters, water points, and aid resources during disasters.")

        sh_col1, sh_col2 = st.columns(2)
        with sh_col1:
            st.markdown("#### Emergency Shelters")
            for s in SHELTER_RESOURCES.get("global_shelters", []):
                st.markdown(f"""
                <div class="resource-card">
                    <h4>🏠 {_safe(s['name'])}</h4>
                    <p>{_safe(s['description'])}</p>
                    <p>🔗 <a href="{_safe(s['url'])}" target="_blank" style="color:#1a66cc;">Visit Resource</a></p>
                </div>
                """, unsafe_allow_html=True)
        with sh_col2:
            st.markdown("#### Water Access Points")
            for w in SHELTER_RESOURCES.get("water_points", []):
                st.markdown(f"""
                <div class="resource-card">
                    <h4>💧 {_safe(w['name'])}</h4>
                    <p>{_safe(w['description'])}</p>
                    <p>🔗 <a href="{_safe(w['url'])}" target="_blank" style="color:#1a66cc;">Visit Resource</a></p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-header"><h2>📍 Locate Resources on Map</h2></div>', unsafe_allow_html=True)
        shelter_country = st.selectbox("Select your country", sorted(COUNTRIES.keys()), key="shelter_country")
        s_info = COUNTRIES.get(shelter_country, {})
        s_lat, s_lon = s_info.get("lat", 0), s_info.get("lon", 0)
        import folium
        shelter_map = folium.Map(location=[s_lat, s_lon], zoom_start=6, tiles=None)
        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr="CARTO", name="Dark", control=False
        ).add_to(shelter_map)
        folium.Marker(
            location=[s_lat, s_lon],
            popup=f"Central {shelter_country} — Search nearby for shelters and aid centers",
            icon=folium.Icon(color="blue", icon="home", prefix="glyphicon"),
            tooltip=f"{shelter_country} center"
        ).add_to(shelter_map)
        st.markdown(f"Use this map to orient yourself in **{shelter_country}**. For active shelter locations during emergencies, use the shelter finder links above.")
        st_folium(shelter_map, width=None, height=350, returned_objects=[])

    with tab_evac:
        st.markdown('<div class="section-header"><h2>Emergency Evacuation Guides</h2></div>', unsafe_allow_html=True)

        evac_type = st.selectbox("Select disaster type", list(EVACUATION_GUIDES.keys()), key="evac_type")
        guide = EVACUATION_GUIDES.get(evac_type, {})

        if guide:
            st.markdown(f"### {evac_type} Evacuation Protocol")
            bcol, dcol, acol = st.columns(3)

            with bcol:
                st.markdown("#### 📋 Before")
                for step in guide.get("before", []):
                    st.markdown(f'<div class="evac-step">✅ {step}</div>', unsafe_allow_html=True)

            with dcol:
                st.markdown("#### ⚡ During")
                for step in guide.get("during", []):
                    st.markdown(f'<div class="evac-step">⚡ {step}</div>', unsafe_allow_html=True)

            with acol:
                st.markdown("#### 🔄 After")
                for step in guide.get("after", []):
                    st.markdown(f'<div class="evac-step">🔄 {step}</div>', unsafe_allow_html=True)

    with tab_prep:
        st.markdown('<div class="section-header"><h2>Emergency Preparedness Kit</h2></div>', unsafe_allow_html=True)

        kit_items = {
            "Water & Food": ["Water (1 gallon per person per day, 3-day supply)", "Non-perishable food (3-day supply)", "Manual can opener", "Water purification tablets or filter"],
            "First Aid": ["First aid kit with bandages, antiseptic, medications", "Prescription medications (7-day supply)", "Emergency blanket", "Insect repellent and sunscreen"],
            "Communication": ["Battery-powered or hand-crank radio", "Flashlight with extra batteries", "Whistle to signal for help", "Cell phone with chargers and backup battery"],
            "Documents": ["Copies of ID, insurance, and bank documents in waterproof bag", "Emergency contact list", "Local emergency numbers", "Maps of local area"],
            "Tools & Shelter": ["Multi-purpose tool or knife", "Dust masks / N95 respirators", "Plastic sheeting and duct tape", "Warm clothing and rain gear", "Sleeping bag or warm blanket"],
            "Sanitation": ["Moist towelettes, garbage bags, plastic ties", "Wrench or pliers to turn off utilities", "Personal sanitation supplies", "Hand sanitizer"],
        }

        for category, items in kit_items.items():
            with st.expander(f"📦 {category}"):
                for item in items:
                    st.markdown(f'<div class="evac-step">• {item}</div>', unsafe_allow_html=True)

    with tab_community:
        st.markdown('<div class="section-header"><h2>Community Resilience</h2></div>', unsafe_allow_html=True)

        resilience_tips = [
            ("Know Your Neighbors", "Build connections with people nearby. Share skills, resources, and emergency plans. Community bonds are the first line of defense in disasters."),
            ("Map Local Resources", "Identify nearby shelters, hospitals, fire stations, and water sources. Know evacuation routes and meeting points."),
            ("Volunteer with Local Organizations", "Join community emergency response teams (CERT), Red Cross chapters, or local volunteer fire departments."),
            ("Share Skills & Knowledge", "Teach first aid, CPR, and disaster preparedness in your community. Knowledge sharing multiplies resilience."),
            ("Create Neighborhood Emergency Plans", "Develop block-by-block communication chains. Identify vulnerable residents who may need extra help."),
            ("Maintain Communication Trees", "Set up group messaging channels for your neighborhood. Ensure multiple ways to reach each other when infrastructure fails."),
            ("Practice Regular Drills", "Organize community disaster drills. Practice evacuations, shelter-in-place, and communication protocols."),
            ("Support Local Food Systems", "Community gardens, food co-ops, and seed banks increase food security during disruptions."),
        ]

        for title, desc in resilience_tips:
            st.markdown(f"""
            <div class="resource-card">
                <h4>🤝 {title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    with tab_report:
        st.markdown('<div class="section-header"><h2>📝 Community Disaster Reporting</h2></div>', unsafe_allow_html=True)
        st.markdown("Report a disaster event in your area to help the community. Your report helps improve situational awareness and response coordination.")

        with st.form("disaster_report_form", clear_on_submit=True):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                report_type = st.selectbox("Disaster Type", DISASTER_TYPES, key="report_type")
                report_country = st.selectbox("Country", sorted(COUNTRIES.keys()), key="report_country")
                report_severity = st.select_slider("Severity", options=["Low", "Moderate", "High", "Critical"], value="Moderate", key="report_severity")
            with r_col2:
                report_location = st.text_input("Specific Location (city, area)", key="report_location")
                report_date = st.date_input("Date of Event", key="report_date")
                report_contact = st.text_input("Contact Email (optional)", key="report_contact")

            report_description = st.text_area("Description of the event", height=120, placeholder="Describe what happened, the scale of impact, people affected, damage observed, and any immediate needs...", key="report_desc")

            report_needs = st.multiselect("Immediate Needs", [
                "Medical Assistance", "Food & Water", "Shelter", "Search & Rescue",
                "Evacuation Support", "Communication Equipment", "Transportation",
                "Power/Electricity", "Sanitation", "Psychological Support"
            ], key="report_needs")

            submitted = st.form_submit_button("Submit Report", type="primary")
            if submitted:
                if report_description and report_location:
                    if "community_reports" not in st.session_state:
                        st.session_state.community_reports = []
                    st.session_state.community_reports.append({
                        "type": report_type,
                        "country": report_country,
                        "location": report_location,
                        "severity": report_severity,
                        "date": str(report_date),
                        "description": report_description,
                        "needs": report_needs,
                        "submitted_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
                    })
                    st.success("Your disaster report has been submitted. Thank you for contributing to community awareness and response coordination.")
                else:
                    st.error("Please provide at least a location and description of the event.")

        if st.session_state.get("community_reports"):
            st.markdown('<div class="section-header"><h2>Recent Community Reports</h2></div>', unsafe_allow_html=True)
            for report in reversed(st.session_state.community_reports[-10:]):
                sev_class = report.get("severity", "moderate").lower()
                st.markdown(f"""
                <div class="alert-card alert-{_safe(sev_class)}">
                    <div class="alert-type" style="color:#1a66cc;">📝 {_safe(report.get('type', ''))} — {_safe(report.get('severity', ''))}</div>
                    <div class="alert-title">{_safe(report.get('location', ''))}, {_safe(report.get('country', ''))}</div>
                    <div class="alert-time">{_safe(report.get('date', ''))} | Submitted: {_safe(report.get('submitted_at', ''))}</div>
                    <div style="color:#9be8a8;margin-top:5px;font-size:0.85rem;">{_safe(report.get('description', '')[:200])}</div>
                </div>
                """, unsafe_allow_html=True)


def page_mining():
    st.markdown('<h1 style="color:#1a66cc;">⛏️ Mining Disasters & Environmental Impacts</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color:#333333;">Global database of abandoned mines, active mining pits, and rare earth extraction sites causing environmental disasters. Sources: USGS MRDS, AML Inventories, EJAtlas, research literature.</p>', unsafe_allow_html=True)

    tab_abandoned, tab_active, tab_ree, tab_map, tab_country = st.tabs([
        "🏚️ Abandoned Mines", "⚙️ Active Mining Pits", "💎 Rare Earth Mines", "🗺️ Mine Map", "🔍 By Country"
    ])

    sev_order = {"Critical": 4, "High": 3, "Moderate": 2, "Low": 1}
    sev_colors = {"Critical": "#cc0000", "High": "#cc5500", "Moderate": "#cc8800", "Low": "#448800"}

    def render_mine_card(m, show_ree=False):
        sev = m.get("severity", "Moderate")
        sc = sev_colors.get(sev, "#888")
        mineral = _safe(m.get("mineral", ""))
        status = _safe(m.get("status", ""))
        issue = _safe(m.get("issue", ""))
        source = _safe(m.get("source", ""))
        country = _safe(m.get("country", ""))
        state_loc = _safe(m.get("state", ""))
        year = m.get("year_abandoned")
        prod = m.get("production_tpa")
        res = m.get("reserves_mt")
        extras = ""
        if year:
            extras += f" | Abandoned: {year}"
        if prod:
            extras += f" | Production: {prod:,} t/yr"
        if res:
            extras += f" | Reserves: {res} Mt"
        loc_str = f"{state_loc}, {country}" if state_loc else country
        st.markdown(f"""
        <div class="resource-card" style="border-left:4px solid {sc}; margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <h4 style="margin:0 0 4px 0;">{_safe(m.get('name',''))}</h4>
                <span style="color:{sc};font-weight:700;font-size:0.8rem;white-space:nowrap;margin-left:8px;">{sev}</span>
            </div>
            <div style="font-size:0.78rem;color:#555555;margin-bottom:4px;">📍 {loc_str} | 🪨 {mineral} | {status}{extras}</div>
            <div style="font-size:0.83rem;color:#9be8a8;line-height:1.4;margin-bottom:4px;">{issue}</div>
            <div style="font-size:0.7rem;color:#1a66cc;">📚 {source}</div>
        </div>
        """, unsafe_allow_html=True)

    with tab_abandoned:
        st.markdown(f'<div class="section-header"><h2>🏚️ Abandoned Mines — Global Inventory ({sum(1 for m in ABANDONED_MINES if m.get("status")=="Abandoned")} sites)</h2></div>', unsafe_allow_html=True)
        st.markdown("Data compiled from: USEPA Superfund, USGS MRDS, AML national inventories (Australia 50,000+, Canada 5,700+ Ontario, South Africa 6,000+), EJAtlas, research literature.")

        region_filter = st.selectbox("Filter by region/continent", ["All", "North America", "South America", "Africa", "Europe", "Asia", "Oceania", "Middle East"], key="aband_region")
        sev_filter = st.selectbox("Filter by severity", ["All", "Critical", "High", "Moderate", "Low"], key="aband_sev")

        abandoned = [m for m in ABANDONED_MINES if m.get("status") == "Abandoned"]
        if region_filter != "All":
            region_map = {
                "North America": ["United States", "Canada", "Mexico"],
                "South America": ["Brazil", "Peru", "Chile", "Colombia", "Bolivia", "Argentina", "Venezuela", "Ecuador"],
                "Africa": ["South Africa", "Ghana", "DR Congo", "Zambia", "Zimbabwe", "Nigeria", "Tanzania", "Mali", "Burkina Faso", "Morocco", "Malawi"],
                "Europe": ["Romania", "Spain", "United Kingdom", "Germany", "Ukraine", "Poland"],
                "Asia": ["India", "Indonesia", "Philippines", "Kyrgyzstan", "Uzbekistan", "Kazakhstan", "China", "Mongolia", "Myanmar", "Laos", "Vietnam", "Malaysia", "Japan"],
                "Oceania": ["Australia", "Papua New Guinea"],
                "Middle East": ["Oman", "Saudi Arabia", "Iran"],
            }
            allowed = region_map.get(region_filter, [])
            abandoned = [m for m in abandoned if m.get("country") in allowed]
        if sev_filter != "All":
            abandoned = [m for m in abandoned if m.get("severity") == sev_filter]

        abandoned = sorted(abandoned, key=lambda x: sev_order.get(x.get("severity", "Low"), 0), reverse=True)
        st.markdown(f"**Showing {len(abandoned)} abandoned mine sites**")
        for m in abandoned:
            render_mine_card(m)

    with tab_active:
        st.markdown(f'<div class="section-header"><h2>⚙️ Active Mining Pits — Ongoing Environmental Impacts ({sum(1 for m in ABANDONED_MINES if m.get("status")=="Active")} sites)</h2></div>', unsafe_allow_html=True)
        st.markdown("Active mines with documented environmental issues: acid drainage, tailings failures, toxic emissions, water contamination, community displacement.")

        active = [m for m in ABANDONED_MINES if m.get("status") == "Active"]
        active = sorted(active, key=lambda x: sev_order.get(x.get("severity", "Low"), 0), reverse=True)
        st.markdown(f"**Showing {len(active)} active mining sites with environmental concerns**")
        for m in active:
            render_mine_card(m)

    with tab_ree:
        st.markdown(f'<div class="section-header"><h2>💎 Rare Earth Mining Sites — Global ({len(RARE_EARTH_MINES)} sites)</h2></div>', unsafe_allow_html=True)
        st.markdown("""**Rare Earth Elements (REE)** are critical for electronics, EVs, wind turbines, and defense. Mining causes severe environmental impacts:
        radioactive thorium/uranium waste, acid mine drainage, groundwater contamination, and massive land destruction.
        **China dominates ~70% of global production** (Bayan Obo, Jiangxi in-situ leach, Sichuan mines).
        Sources: USGS REE Statistics, IAEA, ScienceDirect, Yale Environment 360, EJAtlas.""")

        ree_sev = st.selectbox("Filter by severity", ["All", "Critical", "High", "Moderate", "Low"], key="ree_sev")
        ree_status = st.selectbox("Filter by status", ["All", "Active", "Abandoned"], key="ree_status")

        ree_display = list(RARE_EARTH_MINES)
        if ree_sev != "All":
            ree_display = [m for m in ree_display if m.get("severity") == ree_sev]
        if ree_status != "All":
            ree_display = [m for m in ree_display if m.get("status") == ree_status]
        ree_display = sorted(ree_display, key=lambda x: sev_order.get(x.get("severity", "Low"), 0), reverse=True)

        col_stats1, col_stats2, col_stats3, col_stats4 = st.columns(4)
        with col_stats1:
            st.metric("Total REE Sites", len(RARE_EARTH_MINES))
        with col_stats2:
            st.metric("Critical Sites", sum(1 for m in RARE_EARTH_MINES if m.get("severity") == "Critical"))
        with col_stats3:
            st.metric("Countries Affected", len(set(m.get("country") for m in RARE_EARTH_MINES)))
        with col_stats4:
            active_ree = sum(1 for m in RARE_EARTH_MINES if m.get("status") == "Active")
            st.metric("Active Sites", active_ree)

        st.markdown(f"**Showing {len(ree_display)} rare earth mine sites**")
        for m in ree_display:
            render_mine_card(m, show_ree=True)

    with tab_map:
        st.markdown('<div class="section-header"><h2>🗺️ Mine Locations on Global Map</h2></div>', unsafe_allow_html=True)
        map_type = st.selectbox("Show mine type", ["All Mines", "Abandoned Mines Only", "Active Mines Only", "Rare Earth Mines Only"], key="mine_map_type")

        all_mine_ev = get_mine_events() + get_rare_earth_events()
        if map_type == "Abandoned Mines Only":
            all_mine_ev = [e for e in all_mine_ev if e.get("type") == "Abandoned Mine"]
        elif map_type == "Active Mines Only":
            all_mine_ev = [e for e in all_mine_ev if e.get("type") == "Active Mine"]
        elif map_type == "Rare Earth Mines Only":
            all_mine_ev = [e for e in all_mine_ev if e.get("type") == "Rare Earth Mine"]

        if all_mine_ev:
            import folium
            mine_map = folium.Map(location=[20, 10], zoom_start=2, tiles=None, prefer_canvas=True)
            folium.TileLayer(
                tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                attr='&copy; CARTO', name="Light", control=False
            ).add_to(mine_map)
            color_map = {"Abandoned Mine": "#8B4513", "Active Mine": "#ff6b35", "Rare Earth Mine": "#9b59b6"}
            icon_map = {"Abandoned Mine": "☠️", "Active Mine": "⚙️", "Rare Earth Mine": "💎"}
            for ev in all_mine_ev:
                lat, lon = ev.get("lat", 0), ev.get("lon", 0)
                if lat == 0 and lon == 0:
                    continue
                mtype = ev.get("type", "")
                mcolor = color_map.get(mtype, "#888888")
                popup_html = f"""
                <div style='font-family:Courier New;min-width:220px;max-width:320px;'>
                    <h4 style='color:{mcolor};margin:0 0 4px 0;'>{icon_map.get(mtype, "⛏️")} {_safe(ev.get('title',''))}</h4>
                    <p style='margin:2px 0;font-size:0.8rem;'><b>{mtype}</b> | {_safe(ev.get('mineral',''))}</p>
                    <p style='margin:2px 0;font-size:0.8rem;'>📍 {_safe(ev.get('country',''))} | Severity: <b style='color:{mcolor};'>{_safe(ev.get('severity',''))}</b></p>
                    <p style='margin:4px 0;font-size:0.78rem;line-height:1.4;'>{_safe(ev.get('description','')[:200])}</p>
                    <p style='margin:2px 0;font-size:0.7rem;color:#1a66cc;'>📚 {_safe(ev.get('source',''))}</p>
                </div>"""
                sev_radius_map = {"Critical": 10, "High": 7, "Moderate": 5, "Low": 3}
                radius = sev_radius_map.get(ev.get("severity", "Moderate"), 5)
                folium.CircleMarker(
                    location=[lat, lon], radius=radius,
                    color=mcolor, fill=True, fillColor=mcolor, fillOpacity=0.75, weight=1.5,
                    popup=folium.Popup(popup_html, max_width=340),
                    tooltip=f"{icon_map.get(mtype,'⛏️')} {ev.get('title','')} [{ev.get('severity','')}]"
                ).add_to(mine_map)
            from streamlit_folium import st_folium
            st_folium(mine_map, width="100%", height=550)
        else:
            st.info("No mine sites to display for selected filter.")

    with tab_country:
        st.markdown('<div class="section-header"><h2>🔍 Mine Sites by Country</h2></div>', unsafe_allow_html=True)
        all_countries = sorted(set(m.get("country", "") for m in ABANDONED_MINES + RARE_EARTH_MINES if m.get("country")))
        sel_country = st.selectbox("Select country", all_countries, key="mine_country_select")
        country_mines = get_mines_by_country(sel_country)
        if country_mines:
            st.markdown(f"**{len(country_mines)} mine sites documented for {sel_country}:**")
            for m in country_mines:
                render_mine_card(m)
        else:
            st.info(f"No mine site data available for {sel_country} in current database.")

        st.markdown('<div class="section-header"><h2>⚠️ Top Critical Mine Sites Globally</h2></div>', unsafe_allow_html=True)
        critical = get_critical_mines(limit=15)
        st.markdown(f"**{len(critical)} critical-severity mine sites across all categories:**")
        for m in critical:
            render_mine_card(m)


st.markdown("""
<div class="brand-header animate-fade-rise">
    <h1 class="hero-title">EmOps<sup style="font-size:0.35em;color:#a8aab1;vertical-align:super;margin-left:4px;">&reg;</sup></h1>
    <p class="brand-tagline">Real-time disaster, mining, and rare-earth intelligence &mdash; built for analysts, responders, and decision-makers tracking how the planet moves, shakes, and rebuilds.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div id="top-nav-anchor"></div>', unsafe_allow_html=True)
page = st.radio(
    "Navigation",
    ["🗺️ Dashboard", "🏳️ Country Analysis", "🚨 Live Alerts", "🌡️ Drought & Heatwave", "⛏️ Mining Disasters", "🆘 Resource Hub"],
    label_visibility="collapsed",
    horizontal=True,
    key="top_nav"
)


components.html("""
<script>
(function(){
  var pd = window.parent.document;
  /* Hide sidebar */
  var s = pd.createElement('style');
  s.textContent = 'section[data-testid="stSidebar"]{display:none !important;width:0 !important;} [data-testid="stSidebarCollapsedControl"]{display:none !important;}';
  pd.head.appendChild(s);

  /* Tag the nav radio so CSS can style it */
  function tagNav(){
    var anchor = pd.getElementById('top-nav-anchor');
    if(!anchor) return false;
    var sib = anchor.parentElement;
    while(sib && sib.nextElementSibling){
      sib = sib.nextElementSibling;
      var radio = sib.querySelector ? sib.querySelector('[data-testid="stRadio"]') : null;
      if(radio){ radio.classList.add('top-nav-wrap'); return true; }
      if(sib.getAttribute && sib.getAttribute('data-testid') === 'stRadio'){
        sib.classList.add('top-nav-wrap'); return true;
      }
    }
    /* Fallback: first stRadio on the page */
    var first = pd.querySelector('[data-testid="stRadio"]');
    if(first){ first.classList.add('top-nav-wrap'); return true; }
    return false;
  }
  var tries = 0;
  var iv = setInterval(function(){
    if(tagNav() || ++tries > 30) clearInterval(iv);
  }, 120);
})();
</script>
""", height=0)



if "🗺️ Dashboard" in page:
    page_dashboard()
elif "🏳️ Country Analysis" in page:
    page_country_analysis()
elif "🚨 Live Alerts" in page:
    page_live_alerts()
elif "🌡️ Drought & Heatwave" in page:
    page_drought_heatwave()
elif "⛏️ Mining Disasters" in page:
    page_mining()
elif "🆘 Resource Hub" in page:
    page_resources()
