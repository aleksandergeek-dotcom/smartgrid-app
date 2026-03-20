"""
GridSense AMR v1.0 — Streamlit
Uruchomienie:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime

import data as D

# ─── KONFIGURACJA STRONY ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="GridSense AMR",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Główne kolory */
:root { --blue: #2563eb; --green: #16a34a; --red: #dc2626; --amber: #d97706; --purple: #9333ea; }

/* Kompaktowy sidebar */
[data-testid="stSidebar"] { min-width: 220px !important; max-width: 220px !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 13px; padding: 4px 0; }

/* Metryki */
[data-testid="stMetric"] { background: white; border: 1px solid #e2e6ed;
    border-radius: 10px; padding: 12px 16px; }
[data-testid="stMetricValue"] { font-size: 24px !important; font-weight: 700; }
[data-testid="stMetricLabel"] { font-size: 11px !important; text-transform: uppercase;
    letter-spacing: .05em; color: #9aa3b0; }

/* Expander dla alertów */
.stExpander { border: 1px solid #e2e6ed !important; border-radius: 8px !important;
    margin-bottom: 8px !important; }

/* Usunięcie nadmiarowych marginesów */
.block-container { padding-top: 1.5rem !important; }

/* Tabela liczników */
.meter-ok    { background-color: #f0fdf4; border-left: 4px solid #22c55e; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; }
.meter-warn  { background-color: #fffbeb; border-left: 4px solid #f59e0b; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; }
.meter-error { background-color: #fef2f2; border-left: 4px solid #ef4444; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; }

/* Nagłówek aplikacji */
.app-header { display:flex; align-items:center; gap:10px; margin-bottom:18px; }
.app-logo   { background:#2563eb; color:white; font-weight:700; font-size:14px;
    padding:6px 12px; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

# ─── STAŁE KOLORÓW PLOTLY ────────────────────────────────────────────────────
BLUE   = "#2563eb"
GREEN  = "#16a34a"
RED    = "#dc2626"
AMBER  = "#d97706"
PURPLE = "#9333ea"
GRAY   = "#9aa3b0"
TEAL   = "#0d9488"

PLOTLY_LAYOUT = dict(
    margin=dict(l=40, r=20, t=30, b=40),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter, system-ui, sans-serif", size=11, color="#2d3748"),
    xaxis=dict(showgrid=False, linecolor="#e2e6ed", linewidth=1),
    yaxis=dict(gridcolor="rgba(0,0,0,.05)", linecolor="#e2e6ed"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                font=dict(size=10)),
    hovermode="x unified",
)


def fig_style(fig, height=220):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:8px;margin-bottom:18px">
      <div style="background:#2563eb;color:white;font-weight:700;font-size:13px;
          padding:6px 10px;border-radius:7px">⚡</div>
      <div><div style="font-weight:700;font-size:14px">GridSense AMR</div>
        <div style="font-size:10px;color:#9aa3b0">System zarządzania licznikami</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    view = st.radio("Nawigacja", [
        "📊 Przegląd",
        "📈 Profile & Ciągi",
        "🔌 Transformator",
        "🔮 Predykcja AI",
        "🚨 Alerty & Skutki",
        "🔍 Detekcja Fraudów",
        "📋 Podsumowanie",
        "🔢 Liczniki",
    ], label_visibility="hidden")

    st.divider()

    # Live status
    now = datetime.now()
    st.markdown(f"""
    <div style="font-size:11px;color:#6b7585">
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:6px">
      <div style="width:7px;height:7px;border-radius:50%;background:#22c55e"></div>
      <strong>LIVE</strong> — {now.strftime('%H:%M:%S')}
    </div>
    <div>TGE: <strong style="color:#1a202c">0.84 PLN/kWh</strong></div>
    <div>Alerty: <strong style="color:#dc2626">9 aktywnych</strong></div>
    <div>Stacje: <strong style="color:#16a34a">3/3 online</strong></div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("GridSense AMR v1.0 · Python + Streamlit\nDane: symulowane (prototyp)")


# ═══════════════════════════════════════════════════════════════════════════════
#  WIDOKI
# ═══════════════════════════════════════════════════════════════════════════════

# ─── 1. PRZEGLĄD ─────────────────────────────────────────────────────────────
if view == "📊 Przegląd":
    st.markdown("## Dashboard operacyjny")
    st.caption("3 stacje nN/SN · 60 liczników AMR · odczyt co 15 minut")

    # KPI row
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Pobór chwilowy", "241 kW",   "+6.4% vs plan",  delta_color="inverse")
    c2.metric("Produkcja OZE",  "41 kW",    "-9% vs wczoraj", delta_color="off")
    c3.metric("Zużycie dziś",   "1 916 kWh","-2.8%",          delta_color="normal")
    c4.metric("Alerty aktywne", "9",         "4 krytyczne",    delta_color="inverse")
    c5.metric("ST-B obciążenie","83%",       "⚠ Ryzyko 18:30", delta_color="inverse")

    st.divider()

    col1, col2 = st.columns(2)

    # Profil zużycia 24h
    with col1:
        st.markdown("**Profil zużycia — ostatnie 24h**")
        df = D.get_load_profile_96("all")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"], y=df["load_kw"], name="Pobór",
                                 fill="tozeroy", fillcolor="rgba(37,99,235,.1)",
                                 line=dict(color=BLUE, width=1.5),
                                 hovertemplate="%{y:.1f} kW"))
        fig.add_trace(go.Scatter(x=df["time"], y=df["oze_kw"], name="OZE",
                                 fill="tozeroy", fillcolor="rgba(22,163,74,.1)",
                                 line=dict(color=GREEN, width=1.5),
                                 hovertemplate="%{y:.1f} kW"))
        fig.add_trace(go.Scatter(x=df["time"], y=df["netto_kw"], name="Netto",
                                 line=dict(color=GRAY, width=1, dash="dot"),
                                 hovertemplate="%{y:.1f} kW"))
        fig.update_layout(**PLOTLY_LAYOUT, height=230,
                          yaxis_title="kW", xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

    # Napięcia na ciągach
    with col2:
        st.markdown("**Napięcie na ciągach — aktualny odczyt (koniec ciągu)**")
        ciag_ids = [c["id"] for c in D.CIAGI]
        v_l1 = [c["volt_l1"][-1] for c in D.CIAGI]
        v_l2 = [c["volt_l2"][-1] for c in D.CIAGI]
        v_l3 = [c["volt_l3"][-1] for c in D.CIAGI]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="L1", x=ciag_ids, y=v_l1,
                              marker_color="rgba(239,68,68,.75)", marker_cornerradius=3))
        fig2.add_trace(go.Bar(name="L2", x=ciag_ids, y=v_l2,
                              marker_color="rgba(245,158,11,.75)", marker_cornerradius=3))
        fig2.add_trace(go.Bar(name="L3", x=ciag_ids, y=v_l3,
                              marker_color="rgba(37,99,235,.75)", marker_cornerradius=3))
        # Linie normy
        fig2.add_hline(y=207, line_dash="dot", line_color=RED, line_width=1,
                       annotation_text="min 207V", annotation_position="bottom right")
        fig2.add_hline(y=253, line_dash="dot", line_color=RED, line_width=1,
                       annotation_text="max 253V", annotation_position="top right")
        fig2.update_layout(**PLOTLY_LAYOUT, height=230, barmode="group",
                           yaxis=dict(range=[200, 250], title="V"),
                           xaxis_title=None)
        st.plotly_chart(fig2, use_container_width=True)

    # Status stacji + obciążenie ciągów
    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("**Status stacji nN/SN**")
        for s in D.STATIONS:
            color = RED if s["risk"]=="high" else AMBER if s["risk"]=="medium" else GREEN
            badge = "🔴 Ryzyko" if s["risk"]=="high" else "🟡 Uwaga" if s["risk"]=="medium" else "🟢 OK"
            st.markdown(f"""
            <div style="border:1px solid #e2e6ed;border-radius:8px;padding:10px 12px;
                margin-bottom:6px;background:white">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div>
                  <div style="font-weight:600;font-size:13px">{s['name']}</div>
                  <div style="font-size:11px;color:#9aa3b0">{s['meters']} liczn. · {s['type']}</div>
                </div>
                <div style="text-align:right">
                  <div style="font-weight:700;font-size:15px;color:{color}">{s['load']}%</div>
                  <div style="font-size:11px">{badge}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown("**Ostatnie zdarzenia**")
        for a in D.ALERTS[:4]:
            icon_bg = "#fef2f2" if a["sev"]=="error" else "#fffbeb"
            badge_color = RED if a["sev"]=="error" else AMBER
            st.markdown(f"""
            <div style="display:flex;align-items:flex-start;gap:8px;padding:8px 0;
                border-bottom:1px solid #f0f2f5">
              <div style="background:{icon_bg};padding:5px 7px;border-radius:6px;font-size:13px;
                  flex-shrink:0">{a['icon']}</div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:600;font-size:12px">{a['title'][:40]}</div>
                <div style="font-size:11px;color:#9aa3b0">{a['meter']} · {a['time']}</div>
              </div>
              <div style="background:{badge_color}22;color:{badge_color};font-size:10px;
                  font-weight:600;padding:2px 7px;border-radius:99px;flex-shrink:0">
                {'Krit.' if a['sev']=='error' else 'Ostrzeż.'}
              </div>
            </div>
            """, unsafe_allow_html=True)

    with col5:
        st.markdown("**Obciążenie ciągów**")
        for c in D.CIAGI:
            color = RED if c["load"]>85 else AMBER if c["load"]>70 else BLUE
            st.markdown(f"""
            <div style="margin-bottom:9px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                <span style="font-weight:600">{c['id']} — {c['label'].split('→')[0].strip()}</span>
                <span style="font-weight:700;color:{color}">{c['load']}%</span>
              </div>
              <div style="height:5px;background:#f0f2f5;border-radius:3px;overflow:hidden">
                <div style="height:100%;width:{c['load']}%;background:{color};border-radius:3px"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ─── 2. PROFILE & CIĄGI ──────────────────────────────────────────────────────
elif view == "📈 Profile & Ciągi":
    st.markdown("## Profile zużycia, OZE i mapa napięć na ciągach")

    station_sel = st.selectbox("Stacja", ["all","ST-A","ST-B","ST-C"],
                               format_func=lambda x: {"all":"Wszystkie stacje",
                                                       "ST-A":"ST-A Górna",
                                                       "ST-B":"ST-B Wólka",
                                                       "ST-C":"ST-C Centrum"}[x])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Skumulowany profil zużycia odbiorców**")
        df = D.get_load_profile_96(station_sel)
        # Tydzień temu — lekko zmodyfikowane dane
        rng2 = np.random.default_rng(11)
        last_week = df["load_kw"] * (1 + rng2.normal(0, 0.05, len(df)))

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["load_kw"], name="Dziś",
            fill="tozeroy", fillcolor="rgba(37,99,235,.1)",
            line=dict(color=BLUE, width=2),
            hovertemplate="%{y:.1f} kW"))
        fig.add_trace(go.Scatter(
            x=df["time"], y=last_week.round(1), name="Tydzień temu",
            line=dict(color=GRAY, width=1.5, dash="dot"),
            hovertemplate="%{y:.1f} kW"))
        fig.update_layout(**PLOTLY_LAYOUT, height=240,
                          yaxis_title="kW", xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

        total_today = df["load_kw"].sum() * 0.25  # kWh (15-min intervals)
        total_last  = last_week.sum() * 0.25
        c1, c2, c3 = st.columns(3)
        c1.metric("Łącznie dziś", f"{total_today:.0f} kWh")
        c2.metric("Tydzień temu", f"{total_last:.0f} kWh")
        c3.metric("Zmiana", f"{((total_today/total_last)-1)*100:+.1f}%",
                  delta_color="inverse")

    with col2:
        st.markdown("**Profil produkcji PV — prosumenci (marzec)**")
        pv_peak = {"ST-A": 50, "ST-B": 30, "ST-C": 60}.get(station_sel, 140)
        pv_count = {"ST-A": 10, "ST-B": 6, "ST-C": 12}.get(station_sel, 28)
        df_pv = D.get_pv_profile(station_sel)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df_pv["hour"], y=df_pv["forecast_kw"],
            name=f"Prognoza PV (szczyt {pv_peak} kW)",
            fill="tozeroy", fillcolor="rgba(245,158,11,.12)",
            line=dict(color=AMBER, width=1.5),
            hovertemplate="%{y:.1f} kW"))
        fig2.add_trace(go.Scatter(
            x=df_pv["hour"], y=df_pv["actual_kw"],
            name="Produkcja rzeczywista",
            fill="tozeroy", fillcolor="rgba(22,163,74,.1)",
            line=dict(color=GREEN, width=2),
            mode="lines+markers", marker=dict(size=4, color=GREEN),
            hovertemplate="%{y:.1f} kW"))
        fig2.update_layout(**PLOTLY_LAYOUT, height=240,
                           yaxis_title="kW", xaxis_title=None,
                           yaxis_range=[0, pv_peak * 1.1])
        st.plotly_chart(fig2, use_container_width=True)

        actual_peak = df_pv["actual_kw"].max()
        actual_total = df_pv["actual_kw"].sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Szczyt dziś", f"{actual_peak:.1f} kW")
        c2.metric(f"Prosumenci ({pv_count}×5kW)", f"{pv_peak} kW inst.")
        c3.metric("Prod. łącznie", f"{actual_total:.0f} kWh")

    st.divider()

    # Mapa napięć na ciągu
    st.markdown("### Mapa napięć wzdłuż ciągu — każdy licznik jako punkt pomiarowy")
    st.caption("Napięcie spada z odległością od transformatora (pobór) i rośnie przy instalacjach PV (backfeed). "
               "Punkt ☀ = prosument PV.")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        ciag_sel = st.selectbox("Ciąg", [c["id"] for c in D.CIAGI],
                                format_func=lambda x: next(
                                    c["id"] + " — " + c["label"] for c in D.CIAGI if c["id"]==x))
    with col_b:
        phase_sel = st.selectbox("Faza", ["avg","L1","L2","L3"],
                                 format_func=lambda x: "Średnia L1+L2+L3" if x=="avg" else x)

    df_vm = D.get_voltage_map_data(ciag_sel, phase_sel)
    ciag_obj = next(c for c in D.CIAGI if c["id"] == ciag_sel)

    # Kolory punktów
    def pt_color(row):
        v, pv = row["voltage"], row["is_pv"]
        if v < 207 or v > 246: return RED
        if v < 218: return AMBER
        if v > 238: return PURPLE if pv else AMBER
        return BLUE if pv else GREEN

    colors = df_vm.apply(pt_color, axis=1).tolist()
    sizes  = [14 if r else 10 for r in df_vm["is_pv"]]

    fig3 = go.Figure()
    # Strefa normy
    fig3.add_hrect(y0=207, y1=253, fillcolor="rgba(22,163,74,.06)",
                   line_width=0, annotation_text="Norma EN 50160", annotation_position="top right")
    # Linie graniczne
    fig3.add_hline(y=253, line_dash="dot", line_color=RED, line_width=1,
                   annotation_text="max 253V")
    fig3.add_hline(y=207, line_dash="dot", line_color=RED, line_width=1,
                   annotation_text="min 207V")
    # Linia napięcia
    fig3.add_trace(go.Scatter(
        x=df_vm["addr"], y=df_vm["voltage"],
        mode="lines", name="Linia napięcia",
        line=dict(color=GRAY, width=1.5),
        hoverinfo="skip"))
    # Punkty per licznik
    for _, row in df_vm.iterrows():
        c_pt = pt_color(row)
        pv_txt = " ☀ PV (5kW)" if row["is_pv"] else " brak PV"
        status_txt = {"ok":"✓ Norma","warning":"⚠ Ostrzeżenie","critical":"❌ Poza normą"}[row["status"]]
        pv_effect = (" → podbija napięcie o ok. 1–3V" if row["is_pv"] else " → obniża napięcie")
        fig3.add_trace(go.Scatter(
            x=[row["addr"]], y=[row["voltage"]],
            mode="markers",
            marker=dict(color=c_pt, size=14 if row["is_pv"] else 10,
                        line=dict(color="white", width=1.5)),
            name=row["addr_clean"],
            hovertemplate=(
                f"<b>{row['addr_clean']}</b><br>"
                f"Napięcie: <b>{row['voltage']} V</b> — {status_txt}<br>"
                f"Faza wybrana: {phase_sel}<br>"
                f"L1: {row['v_l1']}V · L2: {row['v_l2']}V · L3: {row['v_l3']}V<br>"
                f"Prąd: {row['current']} A<br>"
                f"Odległość od stacji: ~{row['dist_m']} m<br>"
                f"Instalacja:{pv_txt}{pv_effect}<br>"
                "<extra></extra>"
            ),
            showlegend=False))

    drop = df_vm["voltage"].iloc[0] - df_vm["voltage"].iloc[-1]
    fig3.update_layout(**PLOTLY_LAYOUT, height=280,
                       yaxis=dict(range=[200, 258], title="Napięcie [V]",
                                  gridcolor="rgba(0,0,0,.05)"),
                       xaxis_title=f"Kolejne liczniki wzdłuż ciągu {ciag_sel} (od transformatora)",
                       title=dict(
                           text=f"Ciąg {ciag_sel} · {ciag_obj['label']} · "
                                f"Spadek napięcia: {abs(drop):.1f}V · "
                                f"PV: {len(ciag_obj['pv_indices'])}×5kW={len(ciag_obj['pv_indices'])*5}kW",
                           font=dict(size=12), x=0))
    st.plotly_chart(fig3, use_container_width=True)

    # Legenda kolorów
    st.markdown("""
    <div style="font-size:11px;color:#6b7585;display:flex;gap:16px;flex-wrap:wrap;margin-top:-8px">
      <span><span style="color:#16a34a;font-weight:700">●</span> Norma, brak PV</span>
      <span><span style="color:#2563eb;font-weight:700">●</span> Norma + <strong>☀ PV</strong> (podbija napięcie)</span>
      <span><span style="color:#d97706;font-weight:700">●</span> Ostrzeżenie</span>
      <span><span style="color:#9333ea;font-weight:700">●</span> Ostrzeżenie — PV za wysoko podbija napięcie</span>
      <span><span style="color:#dc2626;font-weight:700">●</span> Poza normą EN 50160</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Karty zbiorcze ciągów
    st.markdown("### Ciągi kablowe — parametry zbiorcze")
    visible = D.CIAGI if station_sel == "all" else [c for c in D.CIAGI if c["st"] == station_sel]
    cols = st.columns(min(len(visible), 3))
    for idx, c in enumerate(visible):
        with cols[idx % 3]:
            load_color = RED if c["load"]>85 else AMBER if c["load"]>70 else BLUE
            v1e, v2e, v3e = c["volt_l1"][-1], c["volt_l2"][-1], c["volt_l3"][-1]
            pv_n = len(c["pv_indices"])
            st.markdown(f"""
            <div style="border:1px solid #e2e6ed;border-radius:10px;padding:13px;
                background:white;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <div>
                  <span style="font-weight:700;font-size:13px;color:{load_color}">{c['id']}</span>
                  <span style="font-size:11px;color:#9aa3b0;margin-left:6px">{c['cable']}</span>
                </div>
                <span style="background:{load_color}22;color:{load_color};font-size:11px;
                    font-weight:600;padding:2px 8px;border-radius:99px">{c['load']}%</span>
              </div>
              <div style="font-size:11px;color:#6b7585;margin-bottom:8px">{c['label']}</div>
              <div style="display:flex;gap:5px;margin-bottom:8px">
                <div style="flex:1;text-align:center;background:#f8f9fb;border-radius:6px;padding:6px 4px">
                  <div style="font-size:9px;color:#9aa3b0;font-weight:600">L1</div>
                  <div style="font-weight:700;font-size:13px;
                      color:{'#dc2626' if v1e<218 else '#16a34a'}">{v1e}V</div>
                </div>
                <div style="flex:1;text-align:center;background:#f8f9fb;border-radius:6px;padding:6px 4px">
                  <div style="font-size:9px;color:#9aa3b0;font-weight:600">L2</div>
                  <div style="font-weight:700;font-size:13px;
                      color:{'#dc2626' if v2e<218 else '#16a34a'}">{v2e}V</div>
                </div>
                <div style="flex:1;text-align:center;background:#f8f9fb;border-radius:6px;padding:6px 4px">
                  <div style="font-size:9px;color:#9aa3b0;font-weight:600">L3</div>
                  <div style="font-weight:700;font-size:13px;
                      color:{'#dc2626' if v3e<218 or v3e>238 else '#16a34a'}">{v3e}V</div>
                </div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#6b7585">
                <span>Asymetria: <strong>{c['asym']}%</strong></span>
                <span>☀ {pv_n}×5kW = {pv_n*5}kW PV</span>
              </div>
              <div style="height:4px;background:#f0f2f5;border-radius:2px;
                  overflow:hidden;margin-top:8px">
                <div style="height:100%;width:{c['load']}%;background:{load_color};
                    border-radius:2px"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ─── 3. TRANSFORMATOR ────────────────────────────────────────────────────────
elif view == "🔌 Transformator":
    st.markdown("## Diagnostyka transformatorów")
    st.caption("Temperatura oleju i uzwojeń · drgania FFT · harmoniczne THD · izolacja")

    # Karty transformatorów
    cols = st.columns(3)
    for i, t in enumerate(D.TRANSFORMERS):
        with cols[i]:
            oil_c  = RED if t["temp_oil"]>65  else AMBER if t["temp_oil"]>58  else "inherit"
            vib_c  = AMBER if t["vibration"]>3  else "inherit"
            thd_c  = AMBER if t["thd"]>8        else "inherit"
            iso_c  = AMBER if t["isolation"]<90 else GREEN
            load_c = RED if t["load"]>80 else AMBER if t["load"]>65 else BLUE
            badge  = "🟡 Monitoruj" if t["status"]=="warn" else "🟢 OK"
            st.markdown(f"""
            <div style="border:1px solid #e2e6ed;border-radius:10px;padding:14px;background:white">
              <div style="display:flex;justify-content:space-between;margin-bottom:10px">
                <div>
                  <div style="font-weight:700;font-size:14px">{t['name']}</div>
                  <div style="font-size:11px;color:#9aa3b0">{t['kva']} kVA · Dyn11</div>
                </div>
                <span>{badge}</span>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                {"".join([
                  f'<div style="background:#f8f9fb;border-radius:6px;padding:8px">'
                  f'<div style="font-size:9px;color:#9aa3b0;font-weight:600;text-transform:uppercase;margin-bottom:3px">{label}</div>'
                  f'<div style="font-family:monospace;font-weight:700;font-size:15px;color:{color}">{value}</div>'
                  f'<div style="font-size:10px;color:#9aa3b0">{norm}</div></div>'
                  for label, value, color, norm in [
                      ("Obciążenie", f"{t['load']}%", load_c, "maks. 100%"),
                      ("Temp. oleju", f"{t['temp_oil']}°C", oil_c, "≤ 65°C"),
                      ("Temp. uzwojeń", f"{t['temp_wind']}°C",
                       AMBER if t['temp_wind']>75 else "inherit", "≤ 80°C"),
                      ("Drgania", f"{t['vibration']} mm/s", vib_c, "≤ 3.5 mm/s"),
                      ("THD-U", f"{t['thd']}%", thd_c, "≤ 8%"),
                      ("Izolacja", f"{t['isolation']}%", iso_c, ""),
                  ]
                ])}
              </div>
              <div style="height:4px;background:#f0f2f5;border-radius:2px;overflow:hidden;margin-top:10px">
                <div style="height:100%;width:{t['load']}%;
                    background:{load_c if load_c!='inherit' else BLUE};border-radius:2px"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Temperatura oleju transformatorów — 48h**")
        df_t = D.get_transformer_temp_history()
        fig = go.Figure()
        for st_id, color, name in [("ST-A", BLUE, "ST-A Górna"),
                                    ("ST-B", RED,  "ST-B Wólka"),
                                    ("ST-C", GREEN,"ST-C Centrum")]:
            fig.add_trace(go.Scatter(x=df_t["time"], y=df_t[st_id], name=name,
                                     line=dict(color=color, width=1.8),
                                     hovertemplate="%{y:.1f}°C"))
        fig.add_hline(y=65, line_dash="dot", line_color=AMBER, line_width=1.5,
                      annotation_text="Norma 65°C", annotation_position="top right")
        fig.update_layout(**PLOTLY_LAYOUT, height=230, yaxis_title="°C",
                          yaxis=dict(range=[44, 75]))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Drgania — widmo FFT (mm/s)**")
        st_vib = st.selectbox("Stacja", ["ST-A","ST-B","ST-C"], index=1)
        df_v = D.get_vibration_spectrum(st_vib)
        colors_vib = [RED if v > 3 else AMBER if v > 1.5 else BLUE for v in df_v["amplitude_mms"]]
        fig2 = go.Figure(go.Bar(x=df_v["freq_hz"].astype(str) + " Hz",
                                y=df_v["amplitude_mms"],
                                marker_color=colors_vib, marker_cornerradius=3))
        fig2.add_hline(y=3.5, line_dash="dot", line_color=RED, line_width=1,
                       annotation_text="Norma 3.5 mm/s")
        fig2.update_layout(**PLOTLY_LAYOUT, height=230,
                           yaxis_title="mm/s", xaxis_title="Częstotliwość",
                           yaxis_range=[0, 5])
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Harmoniczne THD — podział na rzędy**")
        df_thd = D.get_thd_harmonics()
        fig3 = go.Figure()
        for st_id, color in [("ST-A", BLUE), ("ST-B", RED), ("ST-C", GREEN)]:
            fig3.add_trace(go.Bar(name=st_id, x=df_thd["order"],
                                  y=df_thd[st_id], marker_color=color,
                                  marker_opacity=0.75, marker_cornerradius=3))
        fig3.add_hline(y=8, line_dash="dot", line_color=RED, line_width=1,
                       annotation_text="Norma 8%")
        fig3.update_layout(**PLOTLY_LAYOUT, height=215, barmode="group",
                           yaxis_title="%", xaxis_title="Rząd harmoniczny")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("**Historia obciążeń transformatorów — 7 dni (%)**")
        df_hl = D.get_transformer_load_history()
        fig4 = go.Figure()
        for st_id, color in [("ST-A", BLUE), ("ST-B", RED), ("ST-C", GREEN)]:
            fig4.add_trace(go.Scatter(x=df_hl["day"], y=df_hl[st_id], name=st_id,
                                      mode="lines+markers", line=dict(color=color, width=1.8),
                                      marker=dict(size=5), hovertemplate="%{y:.1f}%"))
        fig4.add_hline(y=80, line_dash="dot", line_color=AMBER, line_width=1,
                       annotation_text="Próg ostrzegawczy 80%")
        fig4.update_layout(**PLOTLY_LAYOUT, height=215,
                           yaxis_title="%", yaxis_range=[0, 100])
        st.plotly_chart(fig4, use_container_width=True)


# ─── 4. PREDYKCJA AI ─────────────────────────────────────────────────────────
elif view == "🔮 Predykcja AI":
    st.markdown("## Predykcja AI — zużycie & zagrożenia")
    st.caption("Model ML · dane pogodowe IMGW · ceny TGE · historia 18 miesięcy")

    st.info("📌 Szczyt zużycia prognozowany w dniach **18–22 marca (+26% vs. średnia)** — "
            "temperatury nocne −5°C. ST-B Wólka: **ryzyko przeciążenia 82%** o 17–20. "
            "Koszt energii w szczycie: ~**1.12 PLN/kWh**. Rekomendacja: DSM dla 12 odbiorców taryfy G12.")

    pred_st = st.selectbox("Stacja", ["all","sta","stb","stc"],
                           format_func=lambda x: {"all":"Wszystkie","sta":"ST-A Górna",
                                                   "stb":"ST-B Wólka","stc":"ST-C Centrum"}[x])

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("**Prognoza zużycia — marzec 2025 (kWh)**")
        df_pred = D.get_prediction_monthly(pred_st)
        fig = go.Figure()
        # Przedział ufności
        fig.add_trace(go.Scatter(x=df_pred["day"], y=df_pred["upper"],
                                 fill=None, mode="lines",
                                 line=dict(color="transparent"), showlegend=False))
        fig.add_trace(go.Scatter(x=df_pred["day"], y=df_pred["lower"],
                                 fill="tonexty", mode="lines",
                                 fillcolor="rgba(37,99,235,.1)",
                                 line=dict(color="transparent"),
                                 name="Przedział ufności"))
        # Historia
        fig.add_trace(go.Scatter(x=df_pred["day"], y=df_pred["history"],
                                 name="Historia", line=dict(color=BLUE, width=2),
                                 hovertemplate="%{y:.0f} kWh", connectgaps=False))
        # Prognoza
        fig.add_trace(go.Scatter(x=df_pred["day"], y=df_pred["forecast"],
                                 name="Prognoza", line=dict(color="#93c5fd", width=2, dash="dash"),
                                 hovertemplate="%{y:.0f} kWh", connectgaps=False))
        # Zaznaczenie szczytu
        fig.add_vrect(x0="18.03", x1="22.03", fillcolor=RED, opacity=0.05,
                      line_width=0, annotation_text="Szczyt", annotation_position="top left")
        fig.update_layout(**PLOTLY_LAYOUT, height=270, yaxis_title="kWh")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Ryzyko przeciążeń — stacje**")
        for x in [("ST-B Wólka", 83, "error", "17–20"), ("ST-A Górna", 64, "warn", "18–20"),
                  ("ST-C Centrum", 52, "ok", "—")]:
            name, risk, sev, peak = x
            color = RED if sev=="error" else AMBER if sev=="warn" else GREEN
            label = "Krytyczne" if sev=="error" else "Uwaga" if sev=="warn" else "Normalne"
            st.markdown(f"""
            <div style="margin-bottom:12px">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px;font-size:12px">
                <strong>{name}</strong>
                <span style="font-weight:700;color:{color}">{risk}%</span>
              </div>
              <div style="height:7px;background:#f0f2f5;border-radius:3px;overflow:hidden;margin-bottom:4px">
                <div style="height:100%;width:{risk}%;background:{color};border-radius:3px"></div>
              </div>
              <div style="font-size:11px;color:#6b7585">Szczyt: godz. {peak} ·
                <span style="color:{color};font-weight:600">{label}</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("**Predykcja asymetrii faz — 7 dni (%)**")
        df_asym = D.get_asym_prediction()
        fig2 = go.Figure()
        for st_id, color in [("ST-A", BLUE), ("ST-B", RED), ("ST-C", GREEN)]:
            fig2.add_trace(go.Bar(name=st_id, x=df_asym["day"], y=df_asym[st_id],
                                  marker_color=color, marker_opacity=0.7,
                                  marker_cornerradius=3))
        fig2.add_hline(y=2, line_dash="dot", line_color=AMBER, line_width=1,
                       annotation_text="Norma 2%")
        fig2.update_layout(**PLOTLY_LAYOUT, height=180, barmode="group",
                           yaxis_title="%", yaxis_range=[0, 8],
                           margin=dict(l=30, r=10, t=10, b=30))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Prognoza cen energii TGE — marzec (PLN/kWh)**")
        df_price = D.get_price_forecast()
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df_price["day"], y=df_price["upper"],
                                  fill=None, mode="lines",
                                  line=dict(color="transparent"), showlegend=False))
        fig3.add_trace(go.Scatter(x=df_price["day"], y=df_price["lower"],
                                  fill="tonexty", fillcolor="rgba(245,158,11,.15)",
                                  mode="lines", line=dict(color="transparent"),
                                  name="Przedział ufności"))
        fig3.add_trace(go.Scatter(x=df_price["day"], y=df_price["price"],
                                  name="Cena SPOT", line=dict(color=AMBER, width=2),
                                  hovertemplate="%{y:.3f} PLN/kWh"))
        fig3.add_vrect(x0="18.03", x1="22.03", fillcolor=RED, opacity=0.06, line_width=0)
        fig3.update_layout(**PLOTLY_LAYOUT, height=200, yaxis_title="PLN/kWh")
        st.plotly_chart(fig3, use_container_width=True)
        st.caption("Szczyt cenowy 18–22 marca +34% powyżej średniej. "
                   "Optymalne okno taniego poboru: **00:00–06:00**")

    with col4:
        st.markdown("**Prognozy zużycia — top liczniki (kWh/dzień)**")
        df_meters = D.get_meters_df()
        top = df_meters.nlargest(12, "consumption_kwh")[["id","addr","consumption_kwh","station"]].copy()
        rng = np.random.default_rng(5)
        top["pred_kwh"] = (top["consumption_kwh"] * (1.05 + rng.random(len(top)) * 0.17)).round(1)
        fig4 = go.Figure(go.Bar(
            x=top["pred_kwh"], y=top["id"] + " " + top["addr"],
            orientation="h",
            marker_color=[RED if v>25 else AMBER if v>10 else BLUE for v in top["pred_kwh"]],
            marker_cornerradius=3,
            hovertemplate="%{x:.1f} kWh<extra>%{y}</extra>"))
        fig4.update_layout(**PLOTLY_LAYOUT, height=300,
                           xaxis_title="kWh / dzień",
                           yaxis=dict(autorange="reversed"),
                           margin=dict(l=110, r=20, t=10, b=30))
        st.plotly_chart(fig4, use_container_width=True)


# ─── 5. ALERTY ───────────────────────────────────────────────────────────────
elif view == "🚨 Alerty & Skutki":
    st.markdown("## Alerty, anomalie i skutki")
    st.caption("Kliknij alert aby rozwinąć opis konsekwencji i zalecanych działań")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Krytyczne",        "4",   delta_color="off")
    c2.metric("Ostrzeżenia",      "5",   delta_color="off")
    c3.metric("Rozwiązane (7d)", "28",   delta_color="off")
    c4.metric("Dostępność sieci", "94%", delta_color="off")

    st.divider()

    col_f1, col_f2 = st.columns(2)
    sev_f = col_f1.selectbox("Priorytet", ["Wszystkie","Krytyczne","Ostrzeżenia"])
    st_f  = col_f2.selectbox("Stacja", ["Wszystkie","ST-A","ST-B","ST-C"])

    alerts = D.ALERTS
    if sev_f == "Krytyczne":
        alerts = [a for a in alerts if a["sev"] == "error"]
    elif sev_f == "Ostrzeżenia":
        alerts = [a for a in alerts if a["sev"] == "warn"]
    if st_f != "Wszystkie":
        alerts = [a for a in alerts if a["station"] == st_f]

    for a in alerts:
        border = "#ef4444" if a["sev"]=="error" else "#f59e0b"
        badge  = "🔴 KRYTYCZNY" if a["sev"]=="error" else "🟡 OSTRZEŻENIE"
        with st.expander(f"{a['icon']} {a['title']}  —  {badge}  ·  {a['loc']}  ·  {a['time']}"):
            st.markdown(f"**Opis:** {a['desc']}")
            bg_color    = "#fef2f2" if a["sev"]=="error" else "#fffbeb"
            border_color= "#fee2e2" if a["sev"]=="error" else "#fef3c7"
            text_color  = "#dc2626" if a["sev"]=="error" else "#d97706"
            arrow_color = "#dc2626" if a["sev"]=="error" else "#d97706"
            cons_html = "".join(
                f"<div style='font-size:12px;color:#374151;padding:3px 0;"
                f"display:flex;gap:8px'>"
                f"<span style='color:{arrow_color};font-weight:700'>→</span>"
                f"{c}</div>"
                for c in a["consequences"]
            )
            st.markdown(f"""
            <div style="background:{bg_color};border:1px solid {border_color};
                border-radius:8px;padding:12px 14px;margin:10px 0">
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                  letter-spacing:.05em;color:{text_color};margin-bottom:8px">
                ⚠ Możliwe konsekwencje jeśli nie podjęto działań
              </div>
              {cons_html}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("**Zalecane działania:**")
            for i, ac in enumerate(a["actions"]):
                st.markdown(f"**{i+1}.** {ac}")
            c1, c2, c3 = st.columns(3)
            c1.button("🚨 Zgłoś do dyspozytora", key=f"disp_{a['meter']}")
            c2.button("📋 Utwórz zlecenie",       key=f"order_{a['meter']}")
            c3.button("📈 Analiza trendu",         key=f"trend_{a['meter']}")


# ─── 6. FRAUD ────────────────────────────────────────────────────────────────
elif view == "🔍 Detekcja Fraudów":
    st.markdown("## Detekcja nieuczciwego poboru energii")
    st.caption("Analiza ML · anomalie statystyczne · wzorce czasowe · korelacja z siecią")

    st.info("🤖 Algorytm analizuje **6 wymiarów danych** per licznik: profil dobowy/tygodniowy, "
            "sezonowość, korelacja z pogodą, przerwy komunikacyjne, napięcia sieciowe. "
            "Trzy liczniki przekroczyły próg **Score > 70/100**.")

    # Karty fraudów
    cols = st.columns(3)
    for i, f in enumerate(D.FRAUD_CASES):
        with cols[i]:
            s = f["score"]
            color = RED if s>=80 else AMBER if s>=70 else PURPLE
            priority_label = {"HIGH":"🔴 WYSOKI","MEDIUM":"🟡 ŚREDNI","LOW":"🟠 NISKI"}[f["priority"]]
            st.markdown(f"""
            <div style="border:1px solid #e2e6ed;border-left:4px solid {color};
                border-radius:10px;padding:14px;background:white;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <div>
                  <div style="font-family:monospace;font-weight:700;color:{color}">{f['id']} · {f['addr']}</div>
                  <div style="font-size:11px;color:#9aa3b0">{f['station']} · trend: {f['trend']}</div>
                </div>
                <div style="text-align:right">
                  <div style="font-size:24px;font-weight:700;font-family:monospace;
                      color:{color}">{s}</div>
                  <div style="font-size:10px;font-weight:700;color:{color}">{priority_label}</div>
                </div>
              </div>
              {''.join([f"<div style='font-size:11px;color:#4a5568;padding:2px 0;display:flex;gap:6px'>"
                        f"<span style='color:{color};font-size:8px;margin-top:4px'>◆</span>{ev}</div>"
                        for ev in f['evidence']])}
              <div style="background:#f5f3ff;border:1px solid #e9d5ff;border-radius:6px;
                  padding:9px;margin-top:10px">
                <div style="font-size:10px;font-weight:700;color:#9333ea;margin-bottom:3px;
                    text-transform:uppercase">Rekomendacja</div>
                <div style="font-size:12px;color:#374151">{f['recommendation']}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)
            st.button("📋 Zlecenie inspekcji", key=f"fraud_insp_{f['id']}", use_container_width=True)

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Anomalia zużycia — M-041 (30 dni)**")
        df_fa = D.get_fraud_anomaly_series()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_fa["day"], y=df_fa["upper"],
                                 fill=None, mode="lines",
                                 line=dict(color="transparent"), showlegend=False))
        fig.add_trace(go.Scatter(x=df_fa["day"], y=df_fa["lower"],
                                 fill="tonexty", fillcolor="rgba(139,92,246,.15)",
                                 mode="lines", line=dict(color="transparent"),
                                 name="Oczekiwany zakres"))
        fig.add_trace(go.Scatter(x=df_fa["day"], y=df_fa["expected"],
                                 name="Wzorzec oczekiwany",
                                 line=dict(color=GRAY, width=1.5, dash="dot"),
                                 hovertemplate="%{y:.2f} kWh"))
        fig.add_trace(go.Scatter(x=df_fa["day"], y=df_fa["actual"],
                                 name="Odczyty M-041",
                                 line=dict(color=RED, width=2),
                                 hovertemplate="%{y:.2f} kWh"))
        # Przerwy komunikacyjne
        breaks = df_fa[df_fa["comm_break"]]
        fig.add_trace(go.Scatter(x=breaks["day"], y=breaks["actual"],
                                 mode="markers", name="Przerwa komunikacyjna",
                                 marker=dict(symbol="triangle-down", size=12, color=RED)))
        fig.add_vline(x=8.5, line_dash="dash", line_color=RED, line_width=1,
                      annotation_text="Początek anomalii")
        fig.update_layout(**PLOTLY_LAYOUT, height=250, yaxis_title="kWh",
                          xaxis_title="Dzień miesiąca")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Profil dobowy M-041 vs. grupa odniesienia**")
        df_fp = D.get_fraud_daily_profile()
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_fp["hour"], y=df_fp["group_avg"],
                                  name="Grupa odniesienia",
                                  fill="tozeroy", fillcolor="rgba(37,99,235,.1)",
                                  line=dict(color=BLUE, width=1.5),
                                  hovertemplate="%{y:.2f} kWh"))
        fig2.add_trace(go.Scatter(x=df_fp["hour"], y=df_fp["m041"],
                                  name="M-041 (podejrzany)",
                                  fill="tozeroy", fillcolor="rgba(220,38,38,.1)",
                                  line=dict(color=RED, width=2),
                                  hovertemplate="%{y:.2f} kWh"))
        fig2.add_vrect(x0=2, x1=4, fillcolor=RED, opacity=0.08, line_width=0,
                       annotation_text="Pobór nocny 02–04", annotation_position="top left")
        fig2.update_layout(**PLOTLY_LAYOUT, height=250, yaxis_title="kWh",
                           xaxis_title="Godzina doby")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("M-041 pobiera energię o 02–04 gdy sąsiedzi mają prawie zero — "
                   "klasyczny wzorzec omijania taryfy nocnej")


# ─── 7. PODSUMOWANIE ─────────────────────────────────────────────────────────
elif view == "📋 Podsumowanie":
    st.markdown("## Podsumowanie operacyjne & predykcja problemów")
    st.caption("Synteza wszystkich danych · AI rekomendacje · priorytety działań")

    st.info("🤖 **AI Synthesis:** Analiza 60 liczników, 3 transformatorów, 6 ciągów i danych pogodowych: "
            "**4 priorytety krytyczne** na najbliższe 24h. "
            "Ryzyko awarii bez interwencji: **67%**. Po realizacji rekomendacji: **<8%**.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔴 Działania krytyczne — dziś**")
        for ac in D.CRITICAL_ACTIONS:
            with st.container():
                st.markdown(f"""
                <div style="border:1px solid #fee2e2;border-left:4px solid #ef4444;
                    border-radius:8px;padding:12px 14px;background:white;margin-bottom:8px">
                  <div style="display:flex;gap:8px;align-items:flex-start">
                    <span style="font-size:18px;flex-shrink:0">{ac['icon']}</span>
                    <div>
                      <div style="font-weight:700;font-size:13px">{ac['title']}</div>
                      <div style="font-size:12px;color:#6b7585;margin-top:3px">{ac['desc']}</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    with col2:
        st.markdown("**🟡 Działania planowe — ten tydzień**")
        for ac in D.PLANNED_ACTIONS:
            st.markdown(f"""
            <div style="border:1px solid #fef3c7;border-left:4px solid #f59e0b;
                border-radius:8px;padding:11px 13px;background:white;margin-bottom:7px">
              <div style="display:flex;gap:8px;align-items:flex-start">
                <span style="font-size:16px;flex-shrink:0">{ac['icon']}</span>
                <div>
                  <div style="font-weight:600;font-size:12px">{ac['title']}</div>
                  <div style="font-size:11px;color:#6b7585;margin-top:2px">{ac['desc']}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    col3, col4, col5 = st.columns(3)
    with col3:
        st.markdown("**Ryzyko awarii — 12 dni (%)**")
        df_r = D.get_risk_forecast()
        fig = go.Figure()
        for st_id, color in [("ST-B", RED), ("ST-A", AMBER)]:
            fig.add_trace(go.Scatter(x=df_r["day"], y=df_r[st_id], name=st_id,
                                     mode="lines+markers", line=dict(color=color, width=2),
                                     marker=dict(size=5)))
        fig.add_hline(y=80, line_dash="dot", line_color=RED, line_width=1,
                      annotation_text="Próg krytyczny 80%")
        fig.update_layout(**PLOTLY_LAYOUT, height=210, yaxis_title="%",
                          yaxis_range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.markdown("**Koszt energii — prognoza marzec (PLN/dzień)**")
        df_cost = D.get_cost_forecast()
        colors_cost = [RED if p else "rgba(37,99,235,.6)" for p in df_cost["is_peak"]]
        fig2 = go.Figure(go.Bar(x=df_cost["day"], y=df_cost["cost_pln"],
                                marker_color=colors_cost, marker_cornerradius=2))
        fig2.update_layout(**PLOTLY_LAYOUT, height=210, yaxis_title="PLN",
                           xaxis=dict(tickangle=45, nticks=10))
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("🔴 Czerwone = szczyty cenowe (18–22 marca)")

    with col5:
        st.markdown("**Wskaźniki KPI sieci**")
        for k in D.SUMMARY_KPI:
            col_map = {"green": GREEN, "blue": BLUE, "orange": AMBER,
                       "teal": TEAL, "red": RED}
            c = col_map.get(k["color"], GRAY)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                padding:8px 10px;background:#f8f9fb;border-radius:6px;
                border:1px solid #e2e6ed;margin-bottom:5px">
              <span style="font-size:11px;color:#6b7585">{k['label']}</span>
              <span style="font-family:monospace;font-weight:700;font-size:13px;
                  color:{c}">{k['value']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("**Cyfrowy bliźniak — profil dobowy + cena TGE**")
    df_twin = D.get_digital_twin_profile()
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df_twin["hour"], y=df_twin["actual_kw"], name="Rzeczywiste",
                              line=dict(color=BLUE, width=2.5),
                              hovertemplate="%{y:.1f} kW"))
    fig3.add_trace(go.Scatter(x=df_twin["hour"], y=df_twin["twin_kw"], name="Bliźniak cyfrowy",
                              line=dict(color=PURPLE, width=1.5, dash="dash"),
                              hovertemplate="%{y:.1f} kW"))
    fig3.add_trace(go.Scatter(x=df_twin["hour"], y=df_twin["price_pln"], name="Cena TGE (PLN)",
                              line=dict(color=AMBER, width=1.5),
                              yaxis="y2", hovertemplate="%{y:.2f} PLN"))
    fig3.update_layout(**PLOTLY_LAYOUT, height=230,
                       yaxis=dict(title="kW", gridcolor="rgba(0,0,0,.05)"),
                       yaxis2=dict(title="PLN/kWh", overlaying="y", side="right",
                                   gridcolor=None, showgrid=False))
    st.plotly_chart(fig3, use_container_width=True)


# ─── 8. LICZNIKI ─────────────────────────────────────────────────────────────
elif view == "🔢 Liczniki":
    st.markdown("## Liczniki AMR — 60 punktów pomiarowych")

    df_m = D.get_meters_df()

    col1, col2, col3 = st.columns(3)
    f_st  = col1.selectbox("Stacja",  ["Wszystkie","ST-A","ST-B","ST-C"])
    f_ss  = col2.selectbox("Status",  ["Wszystkie","ok","warn","error"])
    f_pv  = col3.selectbox("Typ", ["Wszyscy","Prosumenci PV","Tylko odbiorcy"])

    filtered = df_m.copy()
    if f_st  != "Wszystkie": filtered = filtered[filtered["station"]==f_st]
    if f_ss  != "Wszystkie": filtered = filtered[filtered["status"]==f_ss]
    if f_pv  == "Prosumenci PV":  filtered = filtered[filtered["is_pv"]==True]
    if f_pv  == "Tylko odbiorcy": filtered = filtered[filtered["is_pv"]==False]

    st.caption(f"Wyświetlane: **{len(filtered)}** z 60 liczników")

    # Tabela z kolorowanymi wierszami
    st.dataframe(
        filtered[["id","addr","station","ciag","consumption_kwh","pf","temp_c",
                   "asym_pct","volt_l1","volt_l2","volt_l3","current_a","is_pv","status","fraud_score"]].rename(
            columns={"id":"Licznik","addr":"Adres","station":"Stacja","ciag":"Ciąg",
                     "consumption_kwh":"Zużycie [kWh]","pf":"cos φ","temp_c":"Temp [°C]",
                     "asym_pct":"Asymetria [%]","volt_l1":"U L1 [V]","volt_l2":"U L2 [V]",
                     "volt_l3":"U L3 [V]","current_a":"I [A]","is_pv":"PV",
                     "status":"Status","fraud_score":"Fraud score"}),
        use_container_width=True, height=500,
        column_config={
            "Status": st.column_config.TextColumn("Status"),
            "PV": st.column_config.CheckboxColumn("☀ PV"),
            "Fraud score": st.column_config.ProgressColumn(
                "Fraud score", min_value=0, max_value=100, format="%d"),
            "Zużycie [kWh]": st.column_config.NumberColumn(format="%.1f"),
            "Asymetria [%]": st.column_config.NumberColumn(format="%.1f"),
        })

    # Wykresy zbiorcze
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Rozkład statusów**")
        status_counts = filtered["status"].value_counts().reset_index()
        status_counts.columns = ["status","count"]
        color_map = {"ok": GREEN, "warn": AMBER, "error": RED}
        fig = px.pie(status_counts, names="status", values="count",
                     color="status", color_discrete_map=color_map,
                     hole=0.55)
        fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0),
                          legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("**Zużycie per stacja (top 20 liczników)**")
        top20 = filtered.nlargest(20, "consumption_kwh")
        fig2 = px.bar(top20, x="consumption_kwh", y="id",
                      color="station",
                      color_discrete_map={"ST-A": BLUE, "ST-B": RED, "ST-C": GREEN},
                      orientation="h", labels={"consumption_kwh":"kWh","id":""})
        fig2.update_layout(height=300, margin=dict(l=70,r=10,t=10,b=30),
                           plot_bgcolor="white", paper_bgcolor="white",
                           legend_title="Stacja",
                           xaxis=dict(showgrid=True, gridcolor="rgba(0,0,0,.05)"),
                           yaxis=dict(showgrid=False, autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)
