import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(page_title="SmartGrid AI | MDM & ADMS", layout="wide", page_icon="⚡")

st.markdown("""
    <style>
    .stApp { background-color: #0F172A; color: #E2E8F0; }
    .css-1d391kg {background-color: #1E293B;}
    .metric-card {
        background-color: #1E293B;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px; padding: 20px; text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 24px; font-weight: bold; color: #00F0FF; }
    .metric-label { font-size: 14px; color: #94A3B8; }
    .alert-card {
        background-color: #331A1A; border-left: 5px solid #FF3366;
        padding: 15px; margin-bottom: 10px; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_mock_data():
    np.random.seed(42)
    meters = []
    for i in range(1, 61):
        if i <= 20:
            ciag = "Ciąg A (Północ)"
            m_type = np.random.choice(["Gospodarstwo", "Prosument (PV)"], p=[0.7, 0.3])
        elif i <= 40:
            ciag = "Ciąg B (Centrum)"
            m_type = np.random.choice(["Prosument (PV)", "Prosument (PV + Magazyn)"], p=[0.6, 0.4])
        else:
            ciag = "Ciąg C (Południe)"
            m_type = np.random.choice(["Gospodarstwo", "Biznes/Usługi"], p=[0.8, 0.2])

        meters.append({
            "ID": f"METER-{1000+i}", "Ciąg": ciag, "Typ": m_type,
            "Napięcie L1": np.random.normal(231, 2),
            "Napięcie L2": np.random.normal(229, 3),
            "Napięcie L3": np.random.normal(230, 2),
            "THD (%)": round(np.random.uniform(1.0, 5.5), 2),
            "cos_phi": round(np.random.uniform(0.85, 0.99), 2),
            "Temp. Zacisków": round(np.random.normal(35, 5), 1)
        })

    meters[15]['Napięcie L1'] = 205.0
    meters[15]['Napięcie L3'] = 248.0
    meters[45]['THD (%)'] = 9.8
    meters[50]['cos_phi'] = 0.65
    meters[12]['ID'] = "METER-1013 (ZŁODZIEJ)"

    dates = pd.date_range(end=datetime.today(), periods=30).tolist()
    future_dates = pd.date_range(start=datetime.today(), periods=30).tolist()
    hist_consump = np.random.normal(1200, 150, 30)
    hist_pv = np.random.normal(400, 100, 30)
    pred_consump = [hist_consump[-1] + i*5 + np.random.normal(0, 50) for i in range(30)]
    pred_pv = [hist_pv[-1] + np.random.normal(0, 80) for i in range(30)]

    return pd.DataFrame(meters), dates, hist_consump, hist_pv, future_dates, pred_consump, pred_pv

df_meters, dates, hist_consump, hist_pv, future_dates, pred_consump, pred_pv = generate_mock_data()

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Flash_symbol.svg/1200px-Flash_symbol.svg.png", width=50)
st.sidebar.title("SmartGrid AI")
st.sidebar.markdown("Zarządzanie siecią SN/nN")
menu = st.sidebar.radio(
    "Moduły Systemu:",
    ["1. Global Dashboard", "2. Topologia i Liczniki", "3. Predykcje i Symulator EV", "4. Alerty i Diagnostyka"]
)

if menu == "1. Global Dashboard":
    st.header("🌐 Global Command Center - Stacja Transformatorowa TR-442")
    st.markdown("Widok zagregowany dla 60 punktów poboru energii.")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{round(sum(hist_consump[-7:]))} kWh</div><div class="metric-label">Zużycie (Ostatnie 7 dni)</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #00FF66;">{round(sum(hist_pv[-7:]))} kWh</div><div class="metric-label">Generacja PV (Ostatnie 7 dni)</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #B026FF;">64 %</div><div class="metric-label">Wskaźnik Samo-zbilansowania</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color: #FFB000;">78 %</div><div class="metric-label">Obciążenie Transformatora</div></div>', unsafe_allow_html=True)

    st.write("---")
    st.subheader("Profil Skumulowany Odbiorców i Produkcji PV (Historia + 30 Dni Predykcji)")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=hist_consump, mode='lines', name='Zużycie (Historia)',
                             line=dict(color='#00F0FF', width=3), fill='tozeroy', fillcolor='rgba(0, 240, 255, 0.1)'))
    fig.add_trace(go.Scatter(x=dates, y=hist_pv, mode='lines', name='Produkcja PV (Historia)',
                             line=dict(color='#00FF66', width=2), fill='tozeroy', fillcolor='rgba(0, 255, 102, 0.1)'))
    fig.add_trace(go.Scatter(x=future_dates, y=pred_consump, mode='lines', name='Predykcja Zużycia (AI)',
                             line=dict(color='#B026FF', width=3, dash='dash')))
    fig.update_layout(template="plotly_dark", paper_bgcolor='#0F172A', plot_bgcolor='#1E293B',
                      hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

elif menu == "2. Topologia i Liczniki":
    st.header("🔌 Cyfrowy Bliźniak (Digital Twin) - Parametry Węzłów")
    selected_ciag = st.selectbox("Wybierz ciąg (obwód):", ["Wszystkie"] + list(df_meters['Ciąg'].unique()))
    df_filtered = df_meters[df_meters['Ciąg'] == selected_ciag] if selected_ciag != "Wszystkie" else df_meters
    st.dataframe(df_filtered.style.background_gradient(cmap="Blues", subset=['Napięcie L1', 'Napięcie L2', 'Napięcie L3']), height=400)

    st.subheader("Analiza Napięć na Fazy - Identyfikacja Asymetrii")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_filtered['ID'], y=df_filtered['Napięcie L1'], name='Faza L1', marker_color='#00F0FF'))
    fig_bar.add_trace(go.Bar(x=df_filtered['ID'], y=df_filtered['Napięcie L2'], name='Faza L2', marker_color='#B026FF'))
    fig_bar.add_trace(go.Bar(x=df_filtered['ID'], y=df_filtered['Napięcie L3'], name='Faza L3', marker_color='#00FF66'))
    fig_bar.update_layout(template="plotly_dark", barmode='group', paper_bgcolor='#0F172A', plot_bgcolor='#1E293B', yaxis=dict(range=[190, 260]))
    st.plotly_chart(fig_bar, use_container_width=True)

elif menu == "3. Predykcje i Symulator EV":
    st.header("🤖 Analityka Predykcyjna i Symulator \"What-If\"")
    st.markdown("Symuluj przyszłe scenariusze przeciążeń transformatora uwzględniając rozwój elektromobilności i warunki pogodowe.")

    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Parametry Symulacji EV")
        ev_count = st.slider("Ilu odbiorców podłączy dziś EV (11 kW)?", min_value=0, max_value=60, value=5)
        ev_time = st.time_input("O której godzinie uruchomią ładowanie?", value=datetime.strptime("17:00", "%H:%M").time())
        st.info("💡 Model koreluje te dane z taryfami strefowymi oraz profilem zjazdu z pracy.")

    with col2:
        st.subheader("Symulacja Obciążenia Transformatora TR-442 (% Mocy Znamionowej)")
        hours = [f"{h:02d}:00" for h in range(24)]
        base_load = [40, 35, 30, 30, 35, 50, 70, 75, 70, 65, 60, 65, 70, 75, 80, 85, 90, 85, 75, 60, 55, 50, 45, 40]
        ev_impact = [0] * 24
        start_idx = ev_time.hour
        for i in range(start_idx, min(start_idx + 4, 24)):
            ev_impact[i] = ev_count * 2
        simulated_load = [base + ev for base, ev in zip(base_load, ev_impact)]

        fig_ev = go.Figure()
        fig_ev.add_trace(go.Scatter(x=hours, y=base_load, mode='lines', fill='tozeroy', name='Standardowe Obciążenie', line=dict(color='#00F0FF')))
        fig_ev.add_trace(go.Scatter(x=hours, y=simulated_load, mode='lines', fill='tonexty', name='Symulacja (+EV)', line=dict(color='#FF3366', dash='dash')))
        fig_ev.add_hline(y=100, line_dash="dot", line_color="red", annotation_text="Krytyczne przeciążenie (100%)", annotation_position="top right")
        fig_ev.update_layout(template="plotly_dark", paper_bgcolor='#0F172A', plot_bgcolor='#1E293B', yaxis_title="% Obciążenia Transformatora")
        st.plotly_chart(fig_ev, use_container_width=True)

elif menu == "4. Alerty i Diagnostyka":
    st.header("🚨 Centrum Alertów i Kontekst Edukacyjny")
    st.markdown("Inteligentny system wykrywania anomalii klasyfikujący priorytety interwencji sieciowych.")

    alerts = [
        {
            "title": "🔴 KRYTYCZNE: Asymetria Faz na linii 'Ciąg A'",
            "desc": "Zarejestrowano Napięcie L1 = 205V, L3 = 248V u odbiorcy METER-1016.",
            "what_happens": "Ryzyko przepalenia przewodu neutralnego (N). Urządzenia jednofazowe na L1 mogą nie działać prawidłowo lub się wyłączać, a te na L3 są narażone na uszkodzenie izolacji z powodu przepięcia.",
            "action": "Wyślij ekipę w celu weryfikacji zacisków w złączu kablowym oraz przepięcia najbardziej obciążających urządzeń (np. pomp ciepła) u odbiorców na inne fazy."
        },
        {
            "title": "🟣 KRYTYCZNE: Podejrzenie kradzieży (NTL) - METER-1013",
            "desc": "Licznik nie rejestruje poboru mocy czynnej, jednak zbilansowanie na stacji wykazuje przepływ 15A w tym kierunku obwodu.",
            "what_happens": "Generuje to niemonitorowane straty techniczne (Non-Technical Losses) dla OSD i zaburza bilans całej stacji.",
            "action": "Automatycznie wygenerowano zgłoszenie do jednostki kontroli. Wymagana inspekcja wizualna przedlicznikowa."
        },
        {
            "title": "🟡 OSTRZEŻENIE: Bardzo niski współczynnik mocy (cos φ = 0.65)",
            "desc": "Odbiorca METER-1050 generuje znaczną ilość energii biernej indukcyjnej.",
            "what_happens": "Energia bierna zapycha sieci przesyłowe, powodując dodatkowe straty cieplne na transformatorze i ograniczając jego przepustowość dla mocy czynnej.",
            "action": "Powiadom klienta biznesowego o nałożeniu kar umownych. Zalecana instalacja baterii kondensatorów (kompensacja mocy biernej)."
        },
        {
            "title": "🟠 OSTRZEŻENIE: Podwyższone wibracje stacji trafo (Drgania 110 Hz)",
            "desc": "Akcelerometry na rdzeniu TR-442 wykryły wibracje odchylone od standardowych 100 Hz.",
            "what_happens": "Odchylenia w drganiach to wczesny objaw starzenia się rdzenia magnetycznego, obluzowania uzwojeń lub efekt nasycenia spowodowany zbyt dużym wskaźnikiem THD (Harmonicznych) z inwerterów PV.",
            "action": "Zaplanuj prace konserwacyjne w najbliższym oknie technologicznym."
        }
    ]

    for alert in alerts:
        with st.expander(alert["title"]):
            st.markdown(f"**Szczegóły:** {alert['desc']}")
            st.markdown(f"**Co może się stać?** {alert['what_happens']}")
            st.markdown(f"**Zalecenie AI:** {alert['action']}")
