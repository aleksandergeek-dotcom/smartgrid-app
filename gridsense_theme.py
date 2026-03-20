"""
GridSense AMR — Nowy design system
Inspiracja: Garnaco (clean cards), Team Management (hierarchy), Equa (AI-forward)
Estetyka: Premium Energy Intelligence Dashboard
Font: Plus Jakarta Sans (display) + JetBrains Mono (data)
Akcent: Electric Blue #0A84FF (jak Apple blue, energia)
"""

THEME_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ─── ROOT ─────────────────────────────────────────────────── */
:root {
  --bg:        #F2F4F7;
  --surface:   #FFFFFF;
  --surface2:  #F8F9FB;
  --surface3:  #EEF0F5;
  --border:    rgba(0,0,0,.07);
  --border2:   rgba(0,0,0,.12);

  --ink1:  #0D1117;
  --ink2:  #3D4452;
  --ink3:  #7C8499;
  --ink4:  #A8AEBB;

  --blue:   #0A84FF;
  --blue-l: #EBF4FF;
  --blue-d: #0060D0;

  --green:  #30D158;
  --green-l:#E8FAF0;
  --green-d:#1A9E3C;

  --red:    #FF3B30;
  --red-l:  #FFF0EF;
  --red-d:  #CC1F16;

  --amber:  #FF9F0A;
  --amber-l:#FFF5E6;
  --amber-d:#CC7A00;

  --purple: #7B61FF;
  --purple-l:#F0EDFF;

  --r-card: 18px;
  --r-inner:10px;
  --r-pill: 99px;
  --r-btn:  10px;

  --sh-card:  0 1px 3px rgba(0,0,0,.04), 0 4px 16px rgba(0,0,0,.06);
  --sh-hover: 0 2px 6px rgba(0,0,0,.06), 0 8px 24px rgba(0,0,0,.10);
  --sh-blue:  0 4px 16px rgba(10,132,255,.25);

  --fn: 'Plus Jakarta Sans', system-ui, sans-serif;
  --mo: 'JetBrains Mono', monospace;
}

/* ─── GLOBAL RESET ─────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  font-family: var(--fn) !important;
  color: var(--ink1) !important;
}

/* ─── SIDEBAR ──────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border) !important;
  min-width: 230px !important;
  max-width: 230px !important;
  box-shadow: 2px 0 12px rgba(0,0,0,.04) !important;
}

[data-testid="stSidebar"] > div:first-child {
  padding: 20px 14px !important;
}

/* Radio nav items */
[data-testid="stSidebar"] .stRadio > div {
  gap: 2px !important;
}
[data-testid="stSidebar"] .stRadio label {
  display: flex !important;
  align-items: center !important;
  padding: 9px 12px !important;
  border-radius: var(--r-inner) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: var(--ink2) !important;
  cursor: pointer !important;
  transition: background .12s, color .12s !important;
  margin: 0 !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
  background: var(--surface2) !important;
  color: var(--ink1) !important;
}
[data-testid="stSidebar"] .stRadio [data-checked="true"] label,
[data-testid="stSidebar"] .stRadio input:checked + div label {
  background: var(--blue-l) !important;
  color: var(--blue) !important;
  font-weight: 600 !important;
}
/* Hide radio circles */
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] span:first-child {
  display: none !important;
}

/* ─── MAIN CONTENT AREA ────────────────────────────────────── */
.block-container {
  padding: 24px 28px 40px !important;
  max-width: 1440px !important;
}

/* ─── CARDS (metric boxes) ─────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-card) !important;
  padding: 18px 20px !important;
  box-shadow: var(--sh-card) !important;
  transition: box-shadow .18s, transform .18s !important;
}
[data-testid="stMetric"]:hover {
  box-shadow: var(--sh-hover) !important;
  transform: translateY(-1px) !important;
}
[data-testid="stMetricLabel"] {
  font-family: var(--fn) !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: .07em !important;
  color: var(--ink3) !important;
}
[data-testid="stMetricValue"] {
  font-family: var(--fn) !important;
  font-size: 26px !important;
  font-weight: 800 !important;
  letter-spacing: -.5px !important;
  color: var(--ink1) !important;
  line-height: 1.1 !important;
}
[data-testid="stMetricDelta"] {
  font-family: var(--mo) !important;
  font-size: 11px !important;
  font-weight: 500 !important;
}

/* ─── EXPANDERS (alerts) ───────────────────────────────────── */
[data-testid="stExpander"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-card) !important;
  box-shadow: var(--sh-card) !important;
  margin-bottom: 8px !important;
  overflow: hidden !important;
  transition: box-shadow .18s !important;
}
[data-testid="stExpander"]:hover {
  box-shadow: var(--sh-hover) !important;
}
[data-testid="stExpander"] summary {
  padding: 14px 18px !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}

/* ─── SELECT BOXES ─────────────────────────────────────────── */
[data-baseweb="select"] {
  border-radius: var(--r-inner) !important;
}
[data-baseweb="select"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r-inner) !important;
  font-family: var(--fn) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  box-shadow: none !important;
  transition: border-color .12s, box-shadow .12s !important;
}
[data-baseweb="select"] > div:hover {
  border-color: var(--blue) !important;
  box-shadow: 0 0 0 3px rgba(10,132,255,.12) !important;
}

/* ─── DATE INPUT ───────────────────────────────────────────── */
[data-baseweb="input"] input {
  background: var(--surface) !important;
  border-radius: var(--r-inner) !important;
  font-family: var(--fn) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}

/* ─── INFO / WARNING / ERROR BOXES ────────────────────────── */
[data-testid="stAlert"] {
  border-radius: var(--r-card) !important;
  border-width: 1px !important;
  font-family: var(--fn) !important;
  font-size: 13px !important;
}

/* ─── DATAFRAME ────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: var(--r-card) !important;
  overflow: hidden !important;
  border: 1px solid var(--border) !important;
  box-shadow: var(--sh-card) !important;
}

/* ─── DIVIDER ──────────────────────────────────────────────── */
hr {
  border-color: var(--border) !important;
  margin: 18px 0 !important;
}

/* ─── BUTTONS ──────────────────────────────────────────────── */
[data-testid="baseButton-secondary"],
[data-testid="stButton"] button {
  background: var(--surface) !important;
  border: 1px solid var(--border2) !important;
  border-radius: var(--r-btn) !important;
  font-family: var(--fn) !important;
  font-size: 12px !important;
  font-weight: 600 !important;
  color: var(--ink2) !important;
  padding: 6px 14px !important;
  transition: all .15s !important;
}
[data-testid="baseButton-secondary"]:hover,
[data-testid="stButton"] button:hover {
  background: var(--blue-l) !important;
  border-color: var(--blue) !important;
  color: var(--blue) !important;
}

/* ─── SECTION TITLES ───────────────────────────────────────── */
h1, h2, h3 {
  font-family: var(--fn) !important;
  letter-spacing: -.4px !important;
  color: var(--ink1) !important;
}
h2 { font-size: 22px !important; font-weight: 800 !important; }

/* ─── CAPTIONS ─────────────────────────────────────────────── */
[data-testid="stCaptionContainer"] p {
  font-size: 12px !important;
  color: var(--ink3) !important;
}

/* ─── RADIO (sidebar nav cleanup) ─────────────────────────── */
.stRadio {
  gap: 0 !important;
}

/* ─── SCROLLBAR ────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--ink4); }

/* ─── PAGE LOAD ANIMATION ──────────────────────────────────── */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.block-container > div > div {
  animation: fadeUp .3s ease both;
}
.block-container > div > div:nth-child(2) { animation-delay: .04s; }
.block-container > div > div:nth-child(3) { animation-delay: .08s; }
.block-container > div > div:nth-child(4) { animation-delay: .12s; }
.block-container > div > div:nth-child(5) { animation-delay: .16s; }
"""

# Kolory dla Pythona (Plotly charts)
BLUE    = "#0A84FF"
GREEN   = "#30D158"
RED     = "#FF3B30"
AMBER   = "#FF9F0A"
PURPLE  = "#7B61FF"
GRAY    = "#A8AEBB"
TEAL    = "#32ADE6"
INK1    = "#0D1117"
INK2    = "#3D4452"
INK3    = "#7C8499"
BG      = "#F2F4F7"
SURFACE = "#FFFFFF"

# Layout Plotly - spójny ze stylinguem
PLOTLY_BASE = dict(
    plot_bgcolor=SURFACE,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, system-ui, sans-serif",
              size=11, color=INK2),
    margin=dict(l=44, r=16, t=28, b=36),
    hovermode="x unified",
    hoverlabel=dict(
        bgcolor=INK1,
        font=dict(color="white", size=11, family="Plus Jakarta Sans"),
        bordercolor=INK1,
    ),
    legend=dict(
        orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
        font=dict(size=10, color=INK2), bgcolor="rgba(0,0,0,0)",
        borderwidth=0,
    ),
    xaxis=dict(
        showgrid=False,
        linecolor="rgba(0,0,0,.08)",
        linewidth=1,
        tickfont=dict(size=10, color=INK3),
        tickcolor="rgba(0,0,0,0)",
    ),
    yaxis=dict(
        gridcolor="rgba(0,0,0,.05)",
        gridwidth=1,
        linecolor="rgba(0,0,0,0)",
        tickfont=dict(size=10, color=INK3),
        zeroline=False,
    ),
)

def chart_layout(fig, height=220, xkw=None, ykw=None, y2kw=None, extra=None):
    """Aplikuje nowy design system do wykresu Plotly."""
    lo = dict(**PLOTLY_BASE, height=height)
    if xkw:
        lo["xaxis"] = {**PLOTLY_BASE["xaxis"], **xkw}
    if ykw:
        lo["yaxis"] = {**PLOTLY_BASE["yaxis"], **ykw}
    if y2kw:
        lo["yaxis2"] = {**PLOTLY_BASE["yaxis"], **y2kw}
    if extra:
        lo.update(extra)
    fig.update_layout(**lo)
    return fig

