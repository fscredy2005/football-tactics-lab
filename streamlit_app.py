"""Football Tactics Lab — Argentine vs France (StatsBomb Open Data).

Deploy on Streamlit Community Cloud with streamlit_app.py as entrypoint.
The trusted, bundled HTML handles all interactive rendering in the browser.
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import streamlit as st

ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "football_tactics_lab.html"
MATCH_ID = 3869685
DATA_URL = f"https://raw.githubusercontent.com/hudl/open-data/master/data/events/{MATCH_ID}.json"
MAX_JSON_BYTES = 24 * 1024 * 1024

st.set_page_config(
    page_title="Football Tactics Lab | Argentine × France 2022",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data(ttl=6 * 60 * 60, show_spinner=False)
def get_official_events() -> list[dict]:
    """Read the public StatsBomb events with a timeout and a size ceiling."""
    req = Request(
        DATA_URL,
        headers={
            "User-Agent": "FootballTacticsLab/1.0 (educational Streamlit dashboard)",
            "Accept": "application/json",
        },
    )
    with urlopen(req, timeout=18) as response:
        content = response.read(MAX_JSON_BYTES + 1)

    if len(content) > MAX_JSON_BYTES:
        raise ValueError("Official events file exceeds the 24 MiB safety limit")

    parsed = json.loads(content)
    if not isinstance(parsed, list) or not parsed or not all(isinstance(e, dict) for e in parsed):
        raise ValueError("Official data is not a non-empty list of event objects")
    if not any(e.get("type", {}).get("name") == "Pass" for e in parsed):
        raise ValueError("Official data does not contain pass events")
    return parsed


def embed_events(html: str, events: list[dict]) -> str:
    """Insert trusted JSON for immediate display without a browser cross-origin fetch.

    The browser still supports refreshing from GitHub or manually importing a file.
    JSON is embedded as inert application/json text, with HTML-sensitive chars escaped.
    """
    data = json.dumps(events, ensure_ascii=False, separators=(",", ":"))
    data = data.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    marker = "<script>"
    start_script = f'<script type="application/json" id="streamlit-preloaded-data">{data}</script>\n{marker}'
    boot_old = "render();loadOnline();"
    boot_new = """render();
const preload = document.getElementById('streamlit-preloaded-data');
if (preload && preload.textContent.trim()) {
  try { accept(JSON.parse(preload.textContent), 'GitHub / StatsBomb (cache Streamlit)'); }
  catch (err) { loadOnline(); }
} else { loadOnline(); }"""
    if html.count(marker) != 1 or html.count(boot_old) != 1:
        raise RuntimeError("Unexpected HTML structure; refusing to inject into an unknown template")
    return html.replace(marker, start_script, 1).replace(boot_old, boot_new, 1)


if not HTML_FILE.is_file():
    st.error("Fichier manquant : football_tactics_lab.html. Ajoute-le à la racine du dépôt GitHub.")
    st.stop()

trusted_html = HTML_FILE.read_text(encoding="utf-8")
try:
    official_events = get_official_events()
    dashboard_html = embed_events(trusted_html, official_events)
except (HTTPError, URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError) as error:
    dashboard_html = trusted_html
    st.info(
        "Chargement serveur de StatsBomb indisponible : "
        "l'application essaiera de récupérer le fichier directement depuis GitHub. "
        "Tu peux aussi utiliser « Importer un JSON »."
    )

# Official StatsBomb wordmark supplied in the public Hudl brand-assets repository.
# Display the attribution prominently before the interactive dashboard.
logo_path = ROOT / "statsbomb_logo.png"
if logo_path.is_file():
    st.image(str(logo_path), width=185)
    st.caption("Données : StatsBomb Open Data · Visualisation pédagogique indépendante")
else:
    st.warning("Logo StatsBomb manquant : ajoute statsbomb_logo.png à la racine du dépôt.")

# The bundled HTML is trusted, and Streamlit 1.66 provides st.iframe for local/HTML content.
st.iframe(
    dashboard_html,
    width="stretch",
    height="content",
    alt="Football Tactics Lab, carte interactive des passes et des tirs Argentine–France 2022",
)

st.caption(
    "Source : StatsBomb Open Data · "
    "[Données officielles](https://github.com/hudl/open-data) · "
    "[Logo issu du dépôt public officiel Hudl](https://github.com/hudl/public-images/blob/master/SB%20-%20Core%20Wordmark%20-%20Colour%20positive.svg) · "
    "Outil indépendant, non affilié à Hudl/StatsBomb."
)
