"""
GridSense AMR v2.0 — Streamlit
Uruchomienie:  streamlit run app.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date

import data as D
import gridsense_theme as T

st.set_page_config(page_title="GridSense AMR", page_icon="⚡",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown(f"<style>{T.THEME_CSS}</style>", unsafe_allow_html=True)

# ─── KOLORY (z theme) ─────────────────────────────────────────────────────────
BLUE=T.BLUE; GREEN=T.GREEN; RED=T.RED; AMBER=T.AMBER
PURPLE=T.PURPLE; GRAY=T.GRAY; TEAL=T.TEAL

# ─── LAYOUT HELPER (deleguje do theme) ───────────────────────────────────────
def fl(fig, height=220, xkw=None, ykw=None, y2kw=None, extra=None):
    return T.chart_layout(fig, height, xkw, ykw, y2kw, extra)


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
now = datetime.now()
with st.sidebar:
    st.markdown(f"""
    <div>
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;
          padding-bottom:16px;border-bottom:1px solid rgba(0,0,0,.07)">
        <div style="width:36px;height:36px;background:#0A84FF;border-radius:10px;
            display:flex;align-items:center;justify-content:center;font-size:18px;
            flex-shrink:0">⚡</div>
        <div>
          <div style="font-weight:800;font-size:15px;letter-spacing:-.4px;">GridSense</div>
          <div style="font-size:10px;color:#A8AEBB;font-weight:500;letter-spacing:.02em">AMR Platform</div>
        </div>
      </div>
      <div style="padding:12px 14px;background:#F8F9FB;border-radius:12px;
          border:1px solid rgba(0,0,0,.07);margin-bottom:16px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
          <div style="display:flex;align-items:center;gap:6px">
            <div style="width:7px;height:7px;border-radius:50%;background:#30D158"></div>
            <span style="font-size:11px;font-weight:700">LIVE</span>
          </div>
          <span style="font-family:"JetBrains Mono",monospace;font-size:11px;color:#A8AEBB">{now.strftime('%H:%M:%S')}</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px">
          <span style="font-size:11px;color:#7C8499">TGE</span>
          <span style="font-family:"JetBrains Mono",monospace;font-size:12px;font-weight:700">0.84 PLN/kWh</span>
        </div>
        <div style="display:flex;justify-content:space-between;margin-bottom:6px">
          <span style="font-size:11px;color:#7C8499">Alerty</span>
          <span style="background:#FFF0EF;color:#FF3B30;font-size:11px;font-weight:700;
              padding:2px 8px;border-radius:99px">9 aktywnych</span>
        </div>
        <div style="display:flex;justify-content:space-between">
          <span style="font-size:11px;color:#7C8499">Stacje</span>
          <span style="background:#E8FAF0;color:#1A9E3C;font-size:11px;font-weight:700;
              padding:2px 8px;border-radius:99px">3/3 online</span>
        </div>
      </div>
      <div style="font-size:10px;font-weight:700;text-transform:uppercase;
          letter-spacing:.08em;color:#A8AEBB;padding:0 2px;margin-bottom:4px">Menu</div>
    </div>""", unsafe_allow_html=True)

    view = st.radio("", [
        "📊  Przegląd",
        "📈  Profile & Ciągi",
        "🔌  Transformator",
        "🔮  Predykcja AI",
        "🚨  Alerty & Skutki",
        "🔍  Detekcja Fraudów",
        "📋  Podsumowanie",
        "🔢  Liczniki",
    ], label_visibility="hidden")

    st.markdown("""
    <div style="margin-top:24px;padding-top:16px;border-top:1px solid rgba(0,0,0,.07)">
      <div style="font-size:10px;color:#A8AEBB;line-height:1.7">
        GridSense AMR v2.0<br>Python + Streamlit<br>Dane: symulowane
      </div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
if view == "📊  Przegląd":
    st.markdown("## Dashboard operacyjny")
    st.caption("3 stacje nN/SN · 60 liczników AMR · odczyt co 15 minut")

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Pobór chwilowy","412 kW","+5.2% vs plan",delta_color="inverse")
    c2.metric("Produkcja OZE","41 kW","−9% vs wczoraj",delta_color="off")
    c3.metric("Zużycie dziś","3 280 kWh","−2.8%",delta_color="normal")
    c4.metric("Alerty aktywne","9","4 krytyczne",delta_color="inverse")
    c5.metric("ST-B obciążenie","83%","⚠ Ryzyko 18:30",delta_color="inverse")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Profil zużycia — ostatnie 24h (60 odbiorców)**")
        df = D.get_load_profile_96("all")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"],y=df["load_kw"],name="Pobór sieciowy",
            fill="tozeroy",fillcolor="rgba(10,132,255,.10)",
            line=dict(color=BLUE,width=1.8),hovertemplate="%{y:.0f} kW"))
        fig.add_trace(go.Scatter(x=df["time"],y=df["oze_kw"],name="Produkcja OZE",
            fill="tozeroy",fillcolor="rgba(48,209,88,.10)",
            line=dict(color=GREEN,width=1.8),hovertemplate="%{y:.0f} kW"))
        fig.add_trace(go.Scatter(x=df["time"],y=df["netto_kw"],name="Netto",
            line=dict(color=GRAY,width=1.2,dash="dot"),hovertemplate="%{y:.0f} kW"))
        fl(fig, 230, ykw=dict(title="kW"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Napięcie na ciągach — koniec ciągu [V]**")
        ciag_ids = [c["id"] for c in D.CIAGI]
        v_l1=[c["volt_l1"][-1] for c in D.CIAGI]
        v_l2=[c["volt_l2"][-1] for c in D.CIAGI]
        v_l3=[c["volt_l3"][-1] for c in D.CIAGI]
        fig2 = go.Figure()
        for vals,name,color in [(v_l1,"L1","rgba(239,68,68,.75)"),
                                 (v_l2,"L2","rgba(245,158,11,.75)"),
                                 (v_l3,"L3","rgba(37,99,235,.75)")]:
            fig2.add_trace(go.Bar(name=name,x=ciag_ids,y=vals,marker_color=color,
                hovertemplate=f"{name}: %{{y}} V<extra>%{{x}}</extra>"))
        fig2.add_hline(y=207,line_dash="dot",line_color=RED,line_width=1,
            annotation_text="min 207V",annotation_font_size=9)
        fig2.add_hline(y=253,line_dash="dot",line_color=RED,line_width=1,
            annotation_text="max 253V",annotation_font_size=9)
        fl(fig2, 230, ykw=dict(title="V",range=[200,250]), extra=dict(barmode="group"))
        st.plotly_chart(fig2, use_container_width=True)

    col3,col4,col5 = st.columns(3)
    with col3:
        st.markdown("**Status stacji nN/SN**")
        for s in D.STATIONS:
            color=RED if s["risk"]=="high" else AMBER if s["risk"]=="medium" else GREEN
            badge="🔴 Ryzyko" if s["risk"]=="high" else "🟡 Uwaga" if s["risk"]=="medium" else "🟢 OK"
            st.markdown(f"""<div style="border:1px solid rgba(0,0,0,.07);border-radius:14px;
                padding:10px 12px;margin-bottom:6px;background:white">
              <div style="display:flex;justify-content:space-between;align-items:center">
                <div><div style="font-weight:600;font-size:13px">{s['name']}</div>
                  <div style="font-size:11px;color:#A8AEBB">{s['meters']} liczn. · {s['type']}</div></div>
                <div style="text-align:right">
                  <div style="font-weight:700;font-size:15px;color:{color}">{s['load']}%</div>
                  <div style="font-size:11px">{badge}</div>
                </div>
              </div></div>""", unsafe_allow_html=True)

    with col4:
        st.markdown("**Ostatnie zdarzenia**")
        for a in D.ALERTS[:4]:
            bg=RED if a["sev"]=="error" else AMBER
            st.markdown(f"""<div style="display:flex;align-items:flex-start;gap:8px;
                padding:8px 0;border-bottom:1px solid #f0f2f5">
              <div style="background:{bg}15;padding:5px 7px;border-radius:6px;
                  font-size:13px;flex-shrink:0">{a['icon']}</div>
              <div style="flex:1;min-width:0">
                <div style="font-weight:600;font-size:12px">{a['title'][:38]}</div>
                <div style="font-size:11px;color:#A8AEBB">{a['meter']} · {a['time']}</div>
              </div>
              <div style="background:{bg}22;color:{bg};font-size:10px;font-weight:600;
                  padding:2px 7px;border-radius:99px;flex-shrink:0">
                {'Krit.' if a['sev']=='error' else 'Ostrzeż.'}</div>
            </div>""", unsafe_allow_html=True)

    with col5:
        st.markdown("**Obciążenie ciągów**")
        for c in D.CIAGI:
            col_c=RED if c["load"]>85 else AMBER if c["load"]>70 else BLUE
            st.markdown(f"""<div style="margin-bottom:9px">
              <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                <span style="font-weight:600">{c['id']} — {c['label'].split('→')[0].strip()}</span>
                <span style="font-weight:700;color:{col_c}">{c['load']}%</span></div>
              <div style="height:5px;background:#f0f2f5;border-radius:3px;overflow:hidden">
                <div style="height:100%;width:{c['load']}%;background:{col_c};border-radius:3px"></div>
              </div></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
elif view == "📈  Profile & Ciągi":
    st.markdown("## Profile zużycia, OZE i mapa napięć")

    ct1,ct2,ct3 = st.columns([2,1,1])
    with ct1:
        station_sel = st.selectbox("Stacja",["all","ST-A","ST-B","ST-C"],
            format_func=lambda x:{"all":"Wszystkie stacje (60 odbiorców)",
                "ST-A":"ST-A Górna (20 odbiorców)","ST-B":"ST-B Wólka (20 odbiorców)",
                "ST-C":"ST-C Centrum (20 odbiorców)"}[x])
    with ct2:
        sel_date = st.date_input("Dzień", value=date.today(),
            min_value=date.today()-timedelta(days=365), max_value=date.today())
    with ct3:
        st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
        if sel_date != date.today():
            st.info(f"Historyczne: {sel_date.strftime('%d.%m.%Y')}")

    pv_n  = {"all":28,"ST-A":10,"ST-B":6,"ST-C":12}[station_sel]
    pv_pk = {"all":140,"ST-A":50,"ST-B":30,"ST-C":60}[station_sel]
    od_n  = {"all":60,"ST-A":20,"ST-B":20,"ST-C":20}[station_sel]

    df = D.get_load_profile_96(station_sel, ref_date=sel_date)
    total_today = df["load_kw"].sum() * 0.25
    rng2 = np.random.default_rng(42)
    last_week = df["load_kw"] * (1 + rng2.normal(0, 0.04, len(df)))

    m1,m2,m3,m4,m5,m6 = st.columns(6)
    m1.metric("Łącznie dziś", f"{total_today:.0f} kWh")
    m2.metric("Tydzień temu", f"{last_week.sum()*0.25:.0f} kWh")
    m3.metric("Zmiana", f"{((total_today/(last_week.sum()*0.25+0.001))-1)*100:+.1f}%",
              delta_color="inverse")
    m4.metric("Szczyt dziś", f"{df['load_kw'].max():.0f} kW")
    m5.metric(f"PV ({pv_n}×5kW)", f"{pv_pk} kW inst.")
    m6.metric("Prod. OZE dziś", f"{df['oze_kw'].sum()*0.25:.0f} kWh")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**Skumulowany profil zużycia — {od_n} odbiorców**")
        st.caption("Typowy profil mieszkaniowy: dwa szczyty — poranny 7–9h i wieczorny 17–21h. "
                   "Średnie gosp. domowe: ~12 kWh/dobę → 20 gosp. = ~240 kWh/dobę.")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["time"],y=df["load_kw"],
            name=f"Pobór {sel_date.strftime('%d.%m')}",
            fill="tozeroy",fillcolor="rgba(10,132,255,.10)",
            line=dict(color=BLUE,width=2),hovertemplate="%{y:.0f} kW · %{x|%H:%M}"))
        fig.add_trace(go.Scatter(x=df["time"],y=last_week.values,name="Tydzień temu",
            line=dict(color=GRAY,width=1.5,dash="dot"),hovertemplate="%{y:.0f} kW"))
        fig.add_vrect(x0=df["time"].iloc[28],x1=df["time"].iloc[36],
            fillcolor="rgba(10,132,255,.06)",line_width=0,
            annotation_text="szczyt poranny",annotation_font_size=9)
        fig.add_vrect(x0=df["time"].iloc[68],x1=df["time"].iloc[84],
            fillcolor="rgba(220,38,38,.05)",line_width=0,
            annotation_text="szczyt wieczorny",annotation_font_size=9)
        fl(fig, 265, ykw=dict(title="kW"))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"**Produkcja PV — {pv_n} instalacji × 5 kW = {pv_pk} kW łącznie**")
        st.caption("Marzec: produkcja 07:00–17:00, szczyt ~12:00. "
                   "Zachmurzenie może obniżyć produkcję o 30–60%.")
        df_pv = D.get_pv_profile(station_sel)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df_pv["hour"],y=df_pv["forecast_kw"],
            name=f"Prognoza (max {pv_pk} kW)",
            fill="tozeroy",fillcolor="rgba(245,158,11,.12)",
            line=dict(color=AMBER,width=1.5),hovertemplate="%{y:.1f} kW"))
        fig2.add_trace(go.Scatter(x=df_pv["hour"],y=df_pv["actual_kw"],
            name="Produkcja rzeczywista",
            fill="tozeroy",fillcolor="rgba(48,209,88,.10)",
            line=dict(color=GREEN,width=2),mode="lines+markers",
            marker=dict(size=5,color=GREEN),hovertemplate="%{y:.1f} kW"))
        fig2.add_vrect(x0="13:00",x1="14:00",
            fillcolor="rgba(100,100,100,.08)",line_width=0,
            annotation_text="zachmurzenie",annotation_font_size=9)
        fl(fig2, 265, ykw=dict(title="kW", range=[0,pv_pk*1.15]))
        st.plotly_chart(fig2, use_container_width=True)
        p_peak=df_pv["actual_kw"].max(); p_tot=df_pv["actual_kw"].sum()
        cp1,cp2,cp3=st.columns(3)
        cp1.metric("Szczyt real.",f"{p_peak:.1f} kW")
        cp2.metric("Prod. łącznie",f"{p_tot:.0f} kWh")
        cp3.metric("Pokrycie",f"{min(100,p_tot/(total_today+0.001)*100):.0f}%")

    st.divider()
    st.markdown("### Mapa napięć wzdłuż ciągu — każdy licznik jako punkt pomiarowy")
    st.caption("Napięcie spada z odległością od transformatora (pobór ↓). "
               "Instalacje ☀ PV podbijają napięcie w miejscu przyłącza (backfeed ↑).")

    ca,cb = st.columns([2,1])
    with ca:
        ciag_sel = st.selectbox("Ciąg kablowy",[c["id"] for c in D.CIAGI],
            format_func=lambda x: next(
                c["id"]+" — "+c["label"]+f" ({len(c['pv_indices'])} PV)"
                for c in D.CIAGI if c["id"]==x))
    with cb:
        phase_sel = st.selectbox("Faza",["avg","L1","L2","L3"],
            format_func=lambda x:"Średnia L1+L2+L3" if x=="avg" else x)

    df_vm = D.get_voltage_map_data(ciag_sel, phase_sel)
    co = next(c for c in D.CIAGI if c["id"]==ciag_sel)
    pv_in_ciag = len(co["pv_indices"])
    drop = float(df_vm["voltage"].iloc[0]-df_vm["voltage"].iloc[-1])
    v_min = df_vm["voltage"].min(); v_max = df_vm["voltage"].max()

    cs1,cs2,cs3,cs4=st.columns(4)
    cs1.metric("Min napięcie (koniec)",f"{v_min:.1f} V",
               "⚠ Bliskie normy!" if v_min<215 else "✓ OK")
    cs2.metric("Max napięcie",f"{v_max:.1f} V")
    cs3.metric("Spadek wzdłuż ciągu",f"{abs(drop):.1f} V",
               "↑ PV podnosi napięcie" if drop<0 else None)
    cs4.metric("PV na ciągu",f"{pv_in_ciag}×5kW={pv_in_ciag*5}kW")

    def pt_color(row):
        v,pv=row["voltage"],row["is_pv"]
        if v<207 or v>246: return RED
        if v>238: return PURPLE if pv else AMBER
        if v<218: return AMBER
        return BLUE if pv else GREEN

    fig3 = go.Figure()
    fig3.add_hrect(y0=207,y1=253,fillcolor="rgba(22,163,74,.05)",line_width=0)
    fig3.add_hline(y=253,line_dash="dot",line_color=RED,line_width=1,
        annotation_text="max 253V",annotation_font_size=9)
    fig3.add_hline(y=207,line_dash="dot",line_color=RED,line_width=1,
        annotation_text="min 207V",annotation_font_size=9)
    fig3.add_hline(y=230,line_dash="dot",line_color=GRAY,line_width=0.8,
        annotation_text="nominalne 230V",annotation_font_size=9)
    fig3.add_trace(go.Scatter(x=df_vm["addr"],y=df_vm["voltage"],
        mode="lines",line=dict(color=GRAY,width=1.5),
        showlegend=False,hoverinfo="skip"))
    for _,row in df_vm.iterrows():
        c_pt=pt_color(row)
        pv_txt=" ☀ PV 5kW (podbija napięcie)" if row["is_pv"] else " (tylko odbiór)"
        st_txt={"ok":"✓ Norma EN 50160","warning":"⚠ Ostrzeżenie",
                "critical":"❌ POZA NORMĄ"}[row["status"]]
        fig3.add_trace(go.Scatter(x=[row["addr"]],y=[row["voltage"]],
            mode="markers",
            marker=dict(color=c_pt,size=15 if row["is_pv"] else 10,
                symbol="diamond" if row["is_pv"] else "circle",
                line=dict(color="white",width=1.5)),
            hovertemplate=(f"<b>{row['addr_clean']}</b><br>"
                f"Napięcie: <b>{row['voltage']} V</b><br>"
                f"L1:{row['v_l1']}V · L2:{row['v_l2']}V · L3:{row['v_l3']}V<br>"
                f"Prąd: {row['current']} A<br>"
                f"Odległość: ~{row['dist_m']} m<br>"
                f"Instalacja:{pv_txt}<br>{st_txt}<extra></extra>"),
            showlegend=False))
    for lbl,col_l,sym in [("Norma, brak PV",GREEN,"circle"),
                           ("Norma + ☀ PV",BLUE,"diamond"),
                           ("Ostrzeżenie",AMBER,"circle"),
                           ("PV za wysoko",PURPLE,"diamond"),
                           ("Poza normą",RED,"circle")]:
        fig3.add_trace(go.Scatter(x=[None],y=[None],mode="markers",
            marker=dict(color=col_l,size=9,symbol=sym),name=lbl))
    fl(fig3, 300,
       xkw=dict(title=f"Liczniki — ciąg {ciag_sel} od transformatora",tickangle=35),
       ykw=dict(title="Napięcie [V]",range=[200,260]),
       extra=dict(legend=dict(orientation="h",y=-0.38,x=0,font=dict(size=10))))
    st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.markdown("### Ciągi kablowe — parametry zbiorcze")
    visible = D.CIAGI if station_sel=="all" else [c for c in D.CIAGI if c["st"]==station_sel]
    cols_c = st.columns(min(len(visible),3))
    for idx,c in enumerate(visible):
        with cols_c[idx%3]:
            lc=RED if c["load"]>85 else AMBER if c["load"]>70 else BLUE
            v1e,v2e,v3e=c["volt_l1"][-1],c["volt_l2"][-1],c["volt_l3"][-1]
            pv_n2=len(c["pv_indices"])
            def vc(v): return RED if v<215 or v>242 else AMBER if v<220 or v>238 else GREEN
            ph_html="".join(
                f'<div style="flex:1;text-align:center;background:#F8F9FB;border-radius:6px;padding:6px 4px">'
                f'<div style="font-size:9px;color:#A8AEBB;font-weight:600">L{i+1}</div>'
                f'<div style="font-weight:700;font-size:13px;color:{vc(v)}">{v}V</div></div>'
                for i,v in enumerate([v1e,v2e,v3e]))
            st.markdown(f"""<div style="border:1px solid rgba(0,0,0,.07);border-left:4px solid {lc};
                border-radius:16px;padding:15px;background:#FFFFFF;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                <div><span style="font-weight:700;font-size:13px;color:{lc}">{c['id']}</span>
                  <span style="font-size:11px;color:#A8AEBB;margin-left:6px">{c['cable']}</span></div>
                <span style="background:{lc}22;color:{lc};font-size:11px;font-weight:600;
                    padding:2px 8px;border-radius:99px">{c['load']}%</span></div>
              <div style="font-size:11px;color:#7C8499;margin-bottom:8px">{c['label']}</div>
              <div style="display:flex;gap:5px;margin-bottom:8px">{ph_html}</div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#7C8499">
                <span>Asymetria: <strong>{c['asym']}%</strong></span>
                <span>☀ {pv_n2}×5kW={pv_n2*5}kW</span></div>
              <div style="height:4px;background:#f0f2f5;border-radius:2px;overflow:hidden;margin-top:8px">
                <div style="height:100%;width:{c['load']}%;background:{lc};border-radius:2px"></div>
              </div></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
elif view == "🔌  Transformator":
    st.markdown("## Diagnostyka transformatorów")
    st.caption("Temperatura · drgania FFT · harmoniczne · izolacja · wykrywanie anomalii")

    tr_sel = st.radio("Wybierz transformator",
                      ["ST-A Górna","ST-B Wólka","ST-C Centrum"], horizontal=True)
    tr_id = tr_sel.split()[0]
    t = next(x for x in D.TRANSFORMERS if x["id"]==tr_id)

    oil_c = RED if t["temp_oil"]>65 else AMBER if t["temp_oil"]>58 else GREEN
    vib_c = RED if t["vibration"]>3.5 else AMBER if t["vibration"]>2.5 else GREEN
    thd_c = AMBER if t["thd"]>8 else GREEN
    iso_c = AMBER if t["isolation"]<90 else GREEN
    load_c= RED if t["load"]>80 else AMBER if t["load"]>65 else BLUE

    st.markdown(f"### {t['name']} — {t['kva']} kVA · Dyn11")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    c1.metric("Obciążenie",f"{t['load']}%")
    c2.metric("Temp. oleju",f"{t['temp_oil']}°C","norma ≤65°C",delta_color="off")
    c3.metric("Temp. uzwojeń",f"{t['temp_wind']}°C","norma ≤80°C",delta_color="off")
    c4.metric("Drgania",f"{t['vibration']} mm/s","norma ≤3.5",delta_color="off")
    c5.metric("THD-U",f"{t['thd']}%","norma ≤8%",delta_color="off")
    c6.metric("Izolacja",f"{t['isolation']}%")

    issues=[]
    if t["temp_oil"]>65:  issues.append(f"🌡 Temperatura oleju {t['temp_oil']}°C > norma 65°C")
    if t["vibration"]>3.5:issues.append(f"📳 Drgania {t['vibration']} mm/s > norma 3.5 mm/s")
    if t["thd"]>8:        issues.append(f"〰 THD-U {t['thd']}% > norma 8%")
    if t["isolation"]<90: issues.append(f"⚠ Izolacja {t['isolation']}% — monitoruj")
    if t["load"]>80:      issues.append(f"⚡ Obciążenie {t['load']}% — ryzyko przy szczytach")
    if issues:
        st.warning("**Wykryte problemy:**\n"+"\n".join(f"- {i}" for i in issues))
    else:
        st.success("✓ Transformator pracuje w normalnych parametrach")

    st.divider()
    st.markdown("#### 📳 Analiza drgań i detekcja anomalii")
    st.markdown(
        "Drgania transformatora to jeden z najwcześniejszych sygnałów nadchodzącej awarii. "
        "Zdrowy TR 50 Hz drga głównie na **100 Hz** (podwójna częstotliwość sieciowa) i harmonicznych. "
        "Wzrost amplitudy lub nowe składowe częstotliwościowe wskazują na obluzowanie rdzenia, "
        "uszkodzenie uzwojenia lub problemy mechaniczne.")

    df_vib_hist = D.get_vibration_history(tr_id)
    df_vib_fft  = D.get_vibration_spectrum(tr_id)

    cv1,cv2 = st.columns(2)
    with cv1:
        st.markdown("**Widmo FFT drgań — aktualny pomiar**")
        cols_vib=[RED if v>3.5 else AMBER if v>2.5 else BLUE for v in df_vib_fft["amplitude_mms"]]
        fig_vib=go.Figure(go.Bar(x=df_vib_fft["freq_hz"].astype(str)+" Hz",
            y=df_vib_fft["amplitude_mms"],marker_color=cols_vib,
            hovertemplate="%{x}: %{y:.2f} mm/s<extra></extra>"))
        fig_vib.add_hline(y=3.5,line_dash="dot",line_color=RED,line_width=1.5,
            annotation_text="Norma 3.5 mm/s")
        fig_vib.add_hline(y=2.5,line_dash="dot",line_color=AMBER,line_width=1,
            annotation_text="Próg ostrzegawczy")
        fl(fig_vib,240,xkw=dict(title="Częstotliwość [Hz]"),ykw=dict(title="mm/s",range=[0,5.5]))
        st.plotly_chart(fig_vib, use_container_width=True)

    with cv2:
        st.markdown("**Trend drgań — 30 dni (składowa 100 Hz)**")
        x_num=np.arange(len(df_vib_hist))
        slope,intercept=np.polyfit(x_num,df_vib_hist["vib_100hz"],1)
        trend_line=slope*x_num+intercept
        fig_vt=go.Figure()
        fig_vt.add_trace(go.Scatter(x=df_vib_hist["date"],y=df_vib_hist["vib_100hz"],
            name="Amplituda 100 Hz",line=dict(color=BLUE,width=2),
            fill="tozeroy",fillcolor="rgba(10,132,255,.08)",hovertemplate="%{y:.2f} mm/s"))
        trend_col=RED if slope>0.04 else AMBER if slope>0.01 else GREEN
        fig_vt.add_trace(go.Scatter(x=df_vib_hist["date"],y=trend_line,
            name=f"Trend ({slope*7:.3f} mm/s/tydz.)",
            line=dict(color=trend_col,width=1.5,dash="dash")))
        fig_vt.add_hline(y=3.5,line_dash="dot",line_color=RED,line_width=1)
        fl(fig_vt,240,ykw=dict(title="mm/s",range=[0,5]))
        st.plotly_chart(fig_vt, use_container_width=True)
        wg=slope*7
        if wg>0.03: st.warning(f"⚠ Trend wzrostowy: +{wg:.3f} mm/s/tydz. — zalecana inspekcja")
        else:       st.success(f"✓ Trend stabilny: {wg:+.3f} mm/s/tydz.")

    with st.expander("Jak wdrożyć monitoring drgań w praktyce?"):
        st.markdown("""
**1. Czujniki** — accelerometry MEMS (np. ADXL345 ~20 PLN, IoT) lub przemysłowe ICP (PCB 603C01).
Próbkowanie >1 kHz dla spektrum do 500 Hz (twierdzenie Nyquista).

**2. Algorytm detekcji anomalii:**
```python
from scipy.fft import fft
from scipy.signal import welch
import numpy as np

# Zbierz 30 dni jako baseline
baseline_spectrum = np.mean(all_fft_measurements, axis=0)
baseline_std      = np.std(all_fft_measurements, axis=0)

# Każdy nowy pomiar:
current_spectrum = np.abs(fft(new_signal))
z_scores = (current_spectrum - baseline_spectrum) / (baseline_std + 1e-9)

if np.max(z_scores) > 3.0:     # >3 sigma = anomalia
    send_alert("Anomalia drgań transformatora")
```

**3. Reguły ekspertowe (od razu wdrażalne):**
- Amplituda 100 Hz > 3.5 mm/s → ALARM KRYTYCZNY
- Wzrost 100 Hz > 20% w tygodniu → OSTRZEŻENIE
- Nowa składowa 150 Hz (nieparzysty harmoniczny) → badanie izolacji
- Wzrost szerokopasmowy (50–500 Hz) → obluzowanie rdzenia
        """)

    st.divider()
    ct3,ct4=st.columns(2)
    with ct3:
        st.markdown("**Temperatura oleju — 48h**")
        df_th=D.get_transformer_temp_history()
        col_map={"ST-A":BLUE,"ST-B":RED,"ST-C":GREEN}
        fig_th=go.Figure()
        fig_th.add_trace(go.Scatter(x=df_th["time"],y=df_th[tr_id],
            name=f"Temp. oleju — {t['name']}",line=dict(color=col_map[tr_id],width=2.5),
            fill="tozeroy",fillcolor=f"rgba(37,99,235,.08)",
            hovertemplate="%{y:.1f}°C"))
        fig_th.add_hline(y=65,line_dash="dot",line_color=RED,line_width=1.5,
            annotation_text="Norma max 65°C")
        fig_th.add_hline(y=58,line_dash="dot",line_color=AMBER,line_width=1,
            annotation_text="Próg ostrzegawczy 58°C")
        fl(fig_th,230,ykw=dict(title="°C",range=[44,78]))
        st.plotly_chart(fig_th, use_container_width=True)

    with ct4:
        st.markdown("**THD — harmoniczne napięcia (wybrany TR wyróżniony)**")
        df_thd=D.get_thd_harmonics()
        fig_thd=go.Figure()
        for st_id2,col2_ in [("ST-A",BLUE),("ST-B",RED),("ST-C",GREEN)]:
            op=1.0 if st_id2==tr_id else 0.3
            fig_thd.add_trace(go.Bar(name=st_id2,x=df_thd["order"],y=df_thd[st_id2],
                marker_color=col2_,opacity=op))
        fig_thd.add_hline(y=8,line_dash="dot",line_color=RED,line_width=1,
            annotation_text="Norma 8%")
        fl(fig_thd,230,xkw=dict(title="Rząd harmoniczny"),ykw=dict(title="%"),
           extra=dict(barmode="group"))
        st.plotly_chart(fig_thd, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
elif view == "🔮  Predykcja AI":
    st.markdown("## Predykcja AI — zużycie & zagrożenia")
    st.caption("Model uwzgledniajacy: sezonowosc · temperature IMGW · weekendy · rosnace przedzialy ufnosci")

    # Kontrolki gorne
    pc1, pc2, pc3, pc4 = st.columns([2, 1, 1, 1])
    with pc1:
        pred_st = st.selectbox("Stacja", ["all","sta","stb","stc"],
            format_func=lambda x: {"all":"Wszystkie stacje","sta":"ST-A Górna",
                                   "stb":"ST-B Wólka","stc":"ST-C Centrum"}[x])
    with pc2:
        months_ahead = st.selectbox("Horyzont prognozy",
            [1, 3, 6, 12],
            format_func=lambda x: f"{x} miesiąc" if x==1 else f"{x} miesiące" if x<5 else f"{x} miesięcy",
            index=0)
    with pc3:
        from datetime import date as date_type
        pred_start = st.date_input("Od dnia",
            value=date_type.today(),
            min_value=date_type.today() - timedelta(days=365),
            max_value=date_type.today())
    with pc4:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        ci_pct_end = min(32, 6 + months_ahead * 30 * 0.07)
        st.info(f"Przedział ufnosci: ±6% → ±{ci_pct_end:.0f}%")

    df_pred = D.get_prediction_monthly(pred_st, months_ahead=months_ahead, start_date=pred_start)

    # Insight oparty na danych
    peak_month_idx = df_pred.groupby("month")["value"].mean().idxmax()
    peak_month_name = {1:"Styczen",2:"Luty",3:"Marzec",4:"Kwiecien",5:"Maj",6:"Czerwiec",
                       7:"Lipiec",8:"Sierpien",9:"Wrzesien",10:"Pazdziernik",
                       11:"Listopad",12:"Grudzien"}.get(peak_month_idx,"")
    winter_months = df_pred[df_pred["month"].isin([12,1,2])]
    summer_months = df_pred[df_pred["month"].isin([6,7,8])]
    if len(winter_months) > 0 and len(summer_months) > 0:
        w_avg = winter_months["value"].mean()
        s_avg = summer_months["value"].mean()
        diff_pct = (w_avg / s_avg - 1) * 100
        st.info(f"📊 Prognoza na {months_ahead} mies. — zima vs lato: "
                f"**+{diff_pct:.0f}%** wyzsze zuzycie zima (ogrzewanie elektryczne). "
                f"Szczyt sezonowy: **{peak_month_name}**. "
                f"Przedzialy ufnosci rosna z horyzontem: koniec prognozy ±{ci_pct_end:.0f}%.")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown(f"**Prognoza zuzwycia — {months_ahead * 31} dni (kWh/dzien)**")
        fig_p = go.Figure()
        # Przedzialy ufnosci
        fig_p.add_trace(go.Scatter(x=df_pred["label"], y=df_pred["upper"],
            fill="none", mode="lines", line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig_p.add_trace(go.Scatter(x=df_pred["label"], y=df_pred["lower"],
            fill="tonexty", mode="lines", fillcolor="rgba(10,132,255,.10)",
            line=dict(color="rgba(0,0,0,0)"), name="Przedzialy ufnosci"))
        # Historia
        fig_p.add_trace(go.Scatter(x=df_pred["label"], y=df_pred["history"],
            name="Historia", line=dict(color=BLUE, width=2.5),
            hovertemplate="%{y:.0f} kWh · %{x}", connectgaps=False))
        # Prognoza
        fig_p.add_trace(go.Scatter(x=df_pred["label"], y=df_pred["forecast"],
            name="Prognoza AI", line=dict(color="#60a5fa", width=2, dash="dash"),
            hovertemplate="%{y:.0f} kWh · %{x}", connectgaps=False))
        # Oznacz weekendy jako szare tło
        weekends = df_pred[df_pred["is_weekend"]]
        for _, wr in weekends.iloc[::2].iterrows():
            fig_p.add_vrect(x0=wr["label"], x1=wr["label"],
                fillcolor="rgba(0,0,0,.02)", line_width=0)
        # Oznacz szczyty zimowe
        high_load = df_pred[df_pred["season_factor"] > 1.2]
        if len(high_load) > 0:
            # Zaznacz pierwszy i ostatni dzien wysokiego sezonu
            pass

        nticks = min(len(df_pred), 20)
        fl(fig_p, 290,
           xkw=dict(tickangle=45, nticks=nticks),
           ykw=dict(title="kWh/dzien"))
        st.plotly_chart(fig_p, use_container_width=True)

        # Statystyki prognozy
        hist = df_pred[df_pred["history"].notna()]
        fcast = df_pred[df_pred["forecast"].notna()]
        ps1,ps2,ps3,ps4 = st.columns(4)
        if len(hist) > 0:
            ps1.metric("Srednia hist.", f"{hist['value'].mean():.0f} kWh/d")
        if len(fcast) > 0:
            ps2.metric("Srednia prognoza", f"{fcast['value'].mean():.0f} kWh/d")
            ps3.metric("Szczyt prognozy", f"{fcast['value'].max():.0f} kWh/d")
            ps4.metric("Min. prognozy", f"{fcast['value'].min():.0f} kWh/d")

    with col2:
        st.markdown("**Ryzyko przeciazen — nastepne 90 dni**")
        df_risk = D.get_risk_events_prediction(
            "ST-B" if pred_st in ("all","stb") else pred_st.upper().replace("STA","ST-A").replace("STC","ST-C"),
            months_ahead=max(1, months_ahead // 2 + 1))
        # Grupuj po tygodniach
        df_risk["week"] = pd.to_datetime(df_risk["date"]).dt.isocalendar().week.astype(str)
        weekly = df_risk.groupby(["week","driver"])["risk_pct"].mean().reset_index()
        weekly = weekly.head(12)

        fig_risk = go.Figure()
        colors_risk = [RED if r>60 else AMBER if r>35 else GREEN for r in df_risk["risk_pct"]]
        fig_risk.add_trace(go.Bar(
            x=df_risk["label"].iloc[::7],  # co tydzien
            y=df_risk["risk_pct"].iloc[::7],
            marker_color=[RED if r>60 else AMBER if r>35 else GREEN
                         for r in df_risk["risk_pct"].iloc[::7]],
            hovertemplate="Ryzyko: %{y:.1f}%<extra>%{x}</extra>"))
        fig_risk.add_hline(y=60, line_dash="dot", line_color=RED, line_width=1,
            annotation_text="Prog krytyczny 60%")
        fig_risk.add_hline(y=35, line_dash="dot", line_color=AMBER, line_width=1,
            annotation_text="Prog ostrzegawczy 35%")
        fl(fig_risk, 200,
           xkw=dict(title=None, tickangle=45),
           ykw=dict(title="Ryzyko %", range=[0,100]))
        st.plotly_chart(fig_risk, use_container_width=True)

        # Czynniki ryzyka
        st.markdown("**Glowne czynniki ryzyka wg sezonu:**")
        for _, row in df_risk.drop_duplicates("driver").head(4).iterrows():
            col_r = RED if row["risk_pct"]>60 else AMBER if row["risk_pct"]>35 else GREEN
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                padding:6px 10px;background:#F8F9FB;border-radius:6px;
                border-left:3px solid {col_r};margin-bottom:5px">
              <span style="font-size:12px">{row['driver']}</span>
              <span style="font-weight:700;color:{col_r};font-size:12px">{row['risk_pct']:.0f}%</span>
            </div>""", unsafe_allow_html=True)

        st.divider()
        st.markdown("**Predykcja asymetrii faz — 7 dni**")
        df_asym = D.get_asym_prediction()
        fig_a = go.Figure()
        for st_id3, col3_ in [("ST-A",BLUE),("ST-B",RED),("ST-C",GREEN)]:
            fig_a.add_trace(go.Bar(name=st_id3, x=df_asym["day"], y=df_asym[st_id3],
                marker_color=col3_, marker_opacity=0.75))
        fig_a.add_hline(y=2, line_dash="dot", line_color=AMBER, line_width=1,
            annotation_text="Norma 2%")
        fl(fig_a, 195, ykw=dict(title="%", range=[0,8]),
           extra=dict(barmode="group", margin=dict(l=40,r=10,t=20,b=30)))
        st.plotly_chart(fig_a, use_container_width=True)

    # Dolny rzad — ceny TGE + top liczniki
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Prognoza cen TGE — marzec (PLN/kWh)**")
        df_price = D.get_price_forecast()
        fig_pr = go.Figure()
        fig_pr.add_trace(go.Scatter(x=df_price["day"], y=df_price["upper"],
            fill="none", mode="lines", line=dict(color="rgba(0,0,0,0)"), showlegend=False))
        fig_pr.add_trace(go.Scatter(x=df_price["day"], y=df_price["lower"],
            fill="tonexty", mode="lines", fillcolor="rgba(255,159,10,.12)",
            line=dict(color="rgba(0,0,0,0)"), name="Przedzialy"))
        fig_pr.add_trace(go.Scatter(x=df_price["day"], y=df_price["price"],
            name="Cena SPOT TGE", line=dict(color=AMBER, width=2),
            hovertemplate="%{y:.3f} PLN/kWh"))
        fl(fig_pr, 210, xkw=dict(tickangle=45, nticks=10), ykw=dict(title="PLN/kWh"))
        st.plotly_chart(fig_pr, use_container_width=True)

    with col4:
        st.markdown("**Prognozy zuzwycia — top 12 licznikow (kWh/dzien)**")
        df_meters = D.get_meters_df()
        top = df_meters.nlargest(12, "consumption_kwh").copy()
        rng_t = np.random.default_rng(5)
        top["pred"] = (top["consumption_kwh"] * (1.05 + rng_t.random(len(top))*0.17)).round(1)
        col_bars = [RED if v>25 else AMBER if v>10 else BLUE for v in top["pred"]]
        fig_bars = go.Figure(go.Bar(
            x=top["pred"], y=top["id"]+" "+top["addr"],
            orientation="h", marker_color=col_bars,
            hovertemplate="%{x:.1f} kWh<extra>%{y}</extra>"))
        fig_bars.update_layout(
            height=310,
            margin=dict(l=120, r=20, t=20, b=40),
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title="kWh/dzien", showgrid=True, gridcolor="rgba(0,0,0,.05)"),
            yaxis=dict(autorange="reversed", showgrid=False))
        st.plotly_chart(fig_bars, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
elif view == "🚨  Alerty & Skutki":
    st.markdown("## Alerty, anomalie i skutki")
    st.caption("Rozwiń każdy alert aby zobaczyć konsekwencje i zalecane działania")

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Krytyczne","4"); c2.metric("Ostrzeżenia","5")
    c3.metric("Rozwiązane (7d)","28"); c4.metric("Dostępność sieci","94%")
    st.divider()

    cf1,cf2=st.columns(2)
    sev_f=cf1.selectbox("Priorytet",["Wszystkie","Krytyczne","Ostrzeżenia"],key="al_sev")
    st_f =cf2.selectbox("Stacja",["Wszystkie","ST-A","ST-B","ST-C"],key="al_st")

    alerts=D.ALERTS
    if sev_f=="Krytyczne":    alerts=[a for a in alerts if a["sev"]=="error"]
    elif sev_f=="Ostrzeżenia":alerts=[a for a in alerts if a["sev"]=="warn"]
    if st_f!="Wszystkie":     alerts=[a for a in alerts if a["station"]==st_f]

    for idx,a in enumerate(alerts):
        badge="🔴 KRYTYCZNY" if a["sev"]=="error" else "🟡 OSTRZEŻENIE"
        bg_c ="#fef2f2" if a["sev"]=="error" else "#fffbeb"
        bd_c ="#fee2e2" if a["sev"]=="error" else "#fef3c7"
        tx_c ="#dc2626" if a["sev"]=="error" else "#d97706"
        label=f"{a['icon']} {a['title']} — {badge} · {a['loc']} · {a['time']}"
        with st.expander(label,expanded=False):
            st.markdown(f"**Opis:** {a['desc']}")
            cons_items="".join(
                f"<div style='font-size:12px;color:#3D4452;padding:3px 0;"
                f"display:flex;gap:8px'>"
                f"<span style='color:{tx_c};font-weight:700;flex-shrink:0'>→</span>"
                f"{c}</div>" for c in a["consequences"])
            st.markdown(f"""<div style="background:{bg_c};border:1px solid {bd_c};
                border-radius:8px;padding:12px 14px;margin:10px 0">
              <div style="font-size:11px;font-weight:700;text-transform:uppercase;
                  letter-spacing:.05em;color:{tx_c};margin-bottom:8px">
                ⚠ Możliwe konsekwencje jeśli nie podjęto działań</div>
              {cons_items}</div>""", unsafe_allow_html=True)
            st.markdown("**Zalecane działania:**")
            for i,ac in enumerate(a["actions"],1):
                st.markdown(f"**{i}.** {ac}")
            cb1,cb2,cb3=st.columns(3)
            # Unikalne klucze = idx + meter id — eliminuje StreamlitDuplicateElementKey
            cb1.button("🚨 Dyspozytor",  key=f"d_{idx}_{a['meter']}")
            cb2.button("📋 Zlecenie",    key=f"o_{idx}_{a['meter']}")
            cb3.button("📈 Trend",       key=f"t_{idx}_{a['meter']}")


# ─────────────────────────────────────────────────────────────────────────────
elif view == "🔍  Detekcja Fraudów":
    st.markdown("## Detekcja nieuczciwego poboru energii")
    st.caption("Analiza ML · anomalie statystyczne · wzorce czasowe · korelacja z siecią")
    st.info("🤖 Algorytm analizuje **6 wymiarów danych** per licznik. "
            "Trzy liczniki przekroczyły próg **Score > 70/100**.")

    cols_f=st.columns(3)
    for i,f in enumerate(D.FRAUD_CASES):
        with cols_f[i]:
            s=f["score"]
            color=RED if s>=80 else AMBER if s>=70 else PURPLE
            lbl={"HIGH":"🔴 WYSOKI","MEDIUM":"🟡 ŚREDNI","LOW":"🟠 NISKI"}[f["priority"]]
            ev_html="".join(
                f"<div style='font-size:11px;color:#3D4452;padding:2px 0;display:flex;gap:6px'>"
                f"<span style='color:{color};font-size:8px;margin-top:4px;flex-shrink:0'>◆</span>"
                f"{ev}</div>" for ev in f["evidence"])
            st.markdown(f"""<div style="border:1px solid rgba(0,0,0,.07);border-left:4px solid {color};
                border-radius:16px;padding:16px;background:#FFFFFF;margin-bottom:10px">
              <div style="display:flex;justify-content:space-between;margin-bottom:8px">
                <div><div style="font-family:"JetBrains Mono",monospace;font-weight:700;color:{color}">
                    {f['id']} · {f['addr']}</div>
                  <div style="font-size:11px;color:#A8AEBB">{f['station']} · {f['trend']}</div></div>
                <div style="text-align:right">
                  <div style="font-size:24px;font-weight:700;font-family:"JetBrains Mono",monospace;
                      color:{color}">{s}</div>
                  <div style="font-size:10px;font-weight:700;color:{color}">{lbl}</div>
                </div></div>
              {ev_html}
              <div style="background:#f5f3ff;border:1px solid #e9d5ff;border-radius:6px;
                  padding:9px;margin-top:10px">
                <div style="font-size:10px;font-weight:700;color:#9333ea;margin-bottom:3px;
                    text-transform:uppercase">Rekomendacja</div>
                <div style="font-size:12px;color:#3D4452">{f['recommendation']}</div>
              </div></div>""", unsafe_allow_html=True)
            # Unikalne klucze przez i i id
            st.button("📋 Zlecenie inspekcji",key=f"fi_{i}_{f['id']}",use_container_width=True)

    st.divider()
    col1,col2=st.columns(2)
    with col1:
        st.markdown("**Anomalia zużycia — M-041 (30 dni)**")
        df_fa=D.get_fraud_anomaly_series()
        fig_fa=go.Figure()
        fig_fa.add_trace(go.Scatter(x=df_fa["day"],y=df_fa["upper"],
            fill="none",mode="lines",line=dict(color="rgba(0,0,0,0)"),showlegend=False))
        fig_fa.add_trace(go.Scatter(x=df_fa["day"],y=df_fa["lower"],
            fill="tonexty",mode="lines",fillcolor="rgba(123,97,255,.12)",
            line=dict(color="rgba(0,0,0,0)"),name="Oczekiwany zakres"))
        fig_fa.add_trace(go.Scatter(x=df_fa["day"],y=df_fa["expected"],name="Wzorzec",
            line=dict(color=GRAY,width=1.5,dash="dot"),hovertemplate="%{y:.2f} kWh"))
        fig_fa.add_trace(go.Scatter(x=df_fa["day"],y=df_fa["actual"],name="M-041",
            line=dict(color=RED,width=2.5),hovertemplate="%{y:.2f} kWh"))
        brk=df_fa[df_fa["comm_break"]]
        fig_fa.add_trace(go.Scatter(x=brk["day"],y=brk["actual"],mode="markers",
            name="Przerwa komunikacyjna",
            marker=dict(symbol="triangle-down",size=14,color=RED,
                line=dict(color="white",width=1))))
        fig_fa.add_vline(x=8.5,line_dash="dash",line_color=RED,line_width=1.5,
            annotation_text="Początek anomalii",annotation_font_size=9)
        fl(fig_fa,260,xkw=dict(title="Dzień miesiąca"),ykw=dict(title="kWh"))
        st.plotly_chart(fig_fa, use_container_width=True)

    with col2:
        st.markdown("**Profil dobowy M-041 vs. grupa odniesienia**")
        df_fp=D.get_fraud_daily_profile()
        fig_fp=go.Figure()
        fig_fp.add_trace(go.Scatter(x=df_fp["hour"],y=df_fp["group_avg"],
            name="Grupa odniesienia",fill="tozeroy",fillcolor="rgba(10,132,255,.10)",
            line=dict(color=BLUE,width=1.8),hovertemplate="%{y:.2f} kWh"))
        fig_fp.add_trace(go.Scatter(x=df_fp["hour"],y=df_fp["m041"],
            name="M-041 (podejrzany)",fill="tozeroy",fillcolor="rgba(255,59,48,.10)",
            line=dict(color=RED,width=2.2),hovertemplate="%{y:.2f} kWh"))
        fig_fp.add_vrect(x0=2,x1=4,fillcolor="rgba(255,59,48,.06)",line_width=0,
            annotation_text="Anomalny pobór 02–04",annotation_font_size=9)
        fl(fig_fp,260,xkw=dict(title="Godzina doby"),ykw=dict(title="kWh"))
        st.plotly_chart(fig_fp, use_container_width=True)
        st.caption("M-041 pobiera o 02–04 gdy sąsiedzi mają prawie zero — "
                   "klasyczny wzorzec omijania taryfy nocnej")


# ─────────────────────────────────────────────────────────────────────────────
elif view == "📋  Podsumowanie":
    st.markdown("## Podsumowanie operacyjne & predykcja problemów")
    st.info("🤖 **AI Synthesis:** 60 liczników, 3 transformatory, 6 ciągów. "
            "**4 priorytety krytyczne** na 24h. Ryzyko awarii bez interwencji: **67%**. "
            "Po realizacji: **<8%**.")

    col1,col2=st.columns(2)
    with col1:
        st.markdown("**🔴 Działania krytyczne — dziś**")
        for ac in D.CRITICAL_ACTIONS:
            st.markdown(f"""<div style="border:1px solid #fee2e2;border-left:4px solid #ef4444;
                border-radius:8px;padding:12px 14px;background:#FFFFFF;margin-bottom:8px">
              <div style="display:flex;gap:8px;align-items:flex-start">
                <span style="font-size:18px;flex-shrink:0">{ac['icon']}</span>
                <div><div style="font-weight:700;font-size:13px">{ac['title']}</div>
                  <div style="font-size:12px;color:#7C8499;margin-top:3px">{ac['desc']}</div>
                </div></div></div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("**🟡 Działania planowe — ten tydzień**")
        for ac in D.PLANNED_ACTIONS:
            st.markdown(f"""<div style="border:1px solid #fef3c7;border-left:4px solid #f59e0b;
                border-radius:8px;padding:11px 13px;background:#FFFFFF;margin-bottom:7px">
              <div style="display:flex;gap:8px;align-items:flex-start">
                <span style="font-size:16px;flex-shrink:0">{ac['icon']}</span>
                <div><div style="font-weight:600;font-size:12px">{ac['title']}</div>
                  <div style="font-size:11px;color:#7C8499;margin-top:2px">{ac['desc']}</div>
                </div></div></div>""", unsafe_allow_html=True)

    st.divider()
    co3,co4,co5=st.columns(3)
    with co3:
        st.markdown("**Ryzyko awarii — 12 dni (%)**")
        df_r=D.get_risk_forecast()
        fig_r=go.Figure()
        for st4,col4_ in [("ST-B",RED),("ST-A",AMBER)]:
            fig_r.add_trace(go.Scatter(x=df_r["day"],y=df_r[st4],name=st4,
                mode="lines+markers",line=dict(color=col4_,width=2),marker=dict(size=5)))
        fig_r.add_hline(y=80,line_dash="dot",line_color=RED,line_width=1,
            annotation_text="Próg krytyczny 80%")
        fl(fig_r,220,ykw=dict(title="%",range=[0,100]))
        st.plotly_chart(fig_r, use_container_width=True)

    with co4:
        st.markdown("**Koszt energii — prognoza marzec (PLN/dzień)**")
        df_cost=D.get_cost_forecast()
        col_c=[RED if p else "rgba(37,99,235,.6)" for p in df_cost["is_peak"]]
        fig_c=go.Figure(go.Bar(x=df_cost["day"],y=df_cost["cost_pln"],
            marker_color=col_c,hovertemplate="%{y:.0f} PLN<extra>%{x}</extra>"))
        fl(fig_c,220,xkw=dict(tickangle=45,nticks=10),ykw=dict(title="PLN/dzień"))
        st.plotly_chart(fig_c, use_container_width=True)
        st.caption("🔴 = szczyty cenowe 18–22 marca")

    with co5:
        st.markdown("**Wskaźniki KPI sieci**")
        for k in D.SUMMARY_KPI:
            cm={"green":GREEN,"blue":BLUE,"orange":AMBER,"teal":TEAL,"red":RED}
            c5_=cm.get(k["color"],GRAY)
            st.markdown(f"""<div style="display:flex;justify-content:space-between;
                align-items:center;padding:8px 10px;background:#F8F9FB;border-radius:6px;
                border:1px solid #e2e6ed;margin-bottom:5px">
              <span style="font-size:11px;color:#7C8499">{k['label']}</span>
              <span style="font-family:"JetBrains Mono",monospace;font-weight:700;font-size:13px;
                  color:{c5_}">{k['value']}</span>
            </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("**Cyfrowy bliźniak — profil dobowy + cena TGE**")
    df_twin=D.get_digital_twin_profile()
    fig_tw=go.Figure()
    fig_tw.add_trace(go.Scatter(x=df_twin["hour"],y=df_twin["actual_kw"],
        name="Rzeczywiste",line=dict(color=BLUE,width=2.5),hovertemplate="%{y:.1f} kW"))
    fig_tw.add_trace(go.Scatter(x=df_twin["hour"],y=df_twin["twin_kw"],
        name="Bliźniak cyfrowy",line=dict(color=PURPLE,width=1.5,dash="dash"),
        hovertemplate="%{y:.1f} kW"))
    fig_tw.add_trace(go.Scatter(x=df_twin["hour"],y=df_twin["price_pln"],
        name="Cena TGE (PLN/kWh)",line=dict(color=AMBER,width=1.5),
        yaxis="y2",hovertemplate="%{y:.2f} PLN"))
    fl(fig_tw,240,xkw=dict(title="Godzina doby"),ykw=dict(title="kW"),
       y2kw=dict(title="PLN/kWh",overlaying="y",side="right",showgrid=False))
    st.plotly_chart(fig_tw, use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
elif view == "🔢  Liczniki":
    st.markdown("## Liczniki AMR — 60 punktów pomiarowych")
    df_m=D.get_meters_df()
    co1,co2,co3=st.columns(3)
    f_st=co1.selectbox("Stacja",["Wszystkie","ST-A","ST-B","ST-C"],key="m_st")
    f_ss=co2.selectbox("Status",["Wszystkie","ok","warn","error"],key="m_ss")
    f_pv=co3.selectbox("Typ",["Wszyscy","Prosumenci PV","Tylko odbiorcy"],key="m_pv")

    filtered=df_m.copy()
    if f_st!="Wszystkie":      filtered=filtered[filtered["station"]==f_st]
    if f_ss!="Wszystkie":      filtered=filtered[filtered["status"]==f_ss]
    if f_pv=="Prosumenci PV":  filtered=filtered[filtered["is_pv"]==True]
    if f_pv=="Tylko odbiorcy": filtered=filtered[filtered["is_pv"]==False]
    st.caption(f"Wyświetlane: **{len(filtered)}** z 60 liczników")

    st.dataframe(
        filtered[["id","addr","station","ciag","consumption_kwh","pf","temp_c",
                   "asym_pct","volt_l1","volt_l2","volt_l3","current_a",
                   "is_pv","status","fraud_score"]].rename(columns={
            "id":"Licznik","addr":"Adres","station":"Stacja","ciag":"Ciąg",
            "consumption_kwh":"Zużycie [kWh]","pf":"cos φ","temp_c":"Temp [°C]",
            "asym_pct":"Asym [%]","volt_l1":"U L1","volt_l2":"U L2","volt_l3":"U L3",
            "current_a":"I [A]","is_pv":"PV","status":"Status","fraud_score":"Fraud"}),
        use_container_width=True,height=480,
        column_config={
            "PV":st.column_config.CheckboxColumn("☀ PV"),
            "Fraud":st.column_config.ProgressColumn(
                "Fraud score",min_value=0,max_value=100,format="%d"),
            "Zużycie [kWh]":st.column_config.NumberColumn(format="%.1f"),
            "Asym [%]":st.column_config.NumberColumn(format="%.1f"),
        })

    st.divider()
    ca,cb=st.columns(2)
    with ca:
        st.markdown("**Rozkład statusów**")
        sc=filtered["status"].value_counts().reset_index()
        sc.columns=["status","count"]
        fig_pie=px.pie(sc,names="status",values="count",color="status",
            color_discrete_map={"ok":GREEN,"warn":AMBER,"error":RED},hole=0.55)
        fig_pie.update_layout(height=220,margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="white",paper_bgcolor="white",
            legend=dict(orientation="h",y=-0.15))
        st.plotly_chart(fig_pie, use_container_width=True)
    with cb:
        st.markdown("**Zużycie — top 20 liczników**")
        top20=filtered.nlargest(20,"consumption_kwh")
        fig_b=px.bar(top20,x="consumption_kwh",y="id",color="station",
            color_discrete_map={"ST-A":BLUE,"ST-B":RED,"ST-C":GREEN},
            orientation="h",labels={"consumption_kwh":"kWh","id":""})
        fig_b.update_layout(height=310,margin=dict(l=80,r=10,t=10,b=30),
            plot_bgcolor="white",paper_bgcolor="white",
            xaxis=dict(showgrid=True,gridcolor="rgba(0,0,0,.05)"),
            yaxis=dict(autorange="reversed",showgrid=False),legend_title="Stacja")
        st.plotly_chart(fig_b, use_container_width=True)
