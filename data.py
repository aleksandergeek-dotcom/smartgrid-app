"""
GridSense AMR — Moduł danych
Generuje realistyczne dane symulowane dla 60 liczników w 3 stacjach.
W wersji produkcyjnej zastąp funkcje get_* zapytaniami do bazy danych (TimescaleDB/InfluxDB).
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ─── SEED dla powtarzalności ───────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ─── STACJE ───────────────────────────────────────────────────────────────────
STATIONS = [
    {"id": "ST-A", "name": "ST-A Górna",    "meters": 20, "load": 64, "risk": "medium",
     "type": "Mieszkaniowa",           "kva": 250, "color": "#2563eb"},
    {"id": "ST-B", "name": "ST-B Wólka",    "meters": 20, "load": 83, "risk": "high",
     "type": "Przemysłowo-usługowa",   "kva": 400, "color": "#dc2626"},
    {"id": "ST-C", "name": "ST-C Centrum",  "meters": 20, "load": 52, "risk": "low",
     "type": "Usługowo-mieszkaniowa",  "kva": 250, "color": "#16a34a"},
]

# ─── CIĄGI KABLOWE ────────────────────────────────────────────────────────────
CIAGI = [
    {"id": "C1", "st": "ST-A", "label": "ST-A Górna → Wzgórze",    "load": 58, "cable": "YAKY 4×95",
     "n": 10, "pv_indices": [0,2,4,6,8], "asym": 0.6,
     "volt_l1": [232,231,230,229,228,227,228,226,225,224],
     "volt_l2": [231,231,230,230,229,228,229,227,226,225],
     "volt_l3": [230,230,229,228,228,227,226,225,224,223],
     "curr":    [14,18,22,16,20,24,18,22,26,19],
     "addrs":   ["Górna 1","Górna 3","Górna 5","Górna 7","Wzgórze 2","Wzgórze 4","Wzgórze 6","Wzgórze 8","Wzgórze 10","Wzgórze 12"]},
    {"id": "C2", "st": "ST-A", "label": "ST-A Słoneczna → Leśna",  "load": 70, "cable": "YAKY 4×70",
     "n": 10, "pv_indices": [1,3,5,7,9], "asym": 1.4,
     "volt_l1": [231,230,229,228,226,225,224,223,222,220],
     "volt_l2": [232,231,230,229,228,227,226,225,224,222],
     "volt_l3": [230,230,228,227,226,225,223,222,221,219],
     "curr":    [20,26,30,24,28,34,22,26,30,24],
     "addrs":   ["Słoneczna 1","Słoneczna 3","Słoneczna 5","Słoneczna 7","Leśna 2","Leśna 4","Leśna 6","Leśna 8","Leśna 10","Leśna 12"]},
    {"id": "C3", "st": "ST-B", "label": "ST-B Wólka → Fabryczna",  "load": 88, "cable": "YAKY 4×120",
     "n": 10, "pv_indices": [0,4,8], "asym": 5.8,
     "volt_l1": [230,228,226,224,221,219,217,215,213,211],
     "volt_l2": [232,233,231,229,228,227,226,225,224,222],
     "volt_l3": [229,227,225,222,219,217,215,213,211,208],
     "curr":    [80,95,110,120,130,118,142,125,138,148],
     "addrs":   ["Wólka 1","Wólka 3","Wólka 5","Fabryczna 2","Fabryczna 4","Fabryczna 6","Fabryczna 8","Fabryczna 10","Fabryczna 12","Fabryczna 14"]},
    {"id": "C4", "st": "ST-B", "label": "ST-B Przemysłowa",         "load": 78, "cable": "YAKY 4×95",
     "n": 10, "pv_indices": [2,5,9], "asym": 1.2,
     "volt_l1": [231,230,229,228,227,226,225,224,223,222],
     "volt_l2": [230,230,229,228,228,227,226,225,224,223],
     "volt_l3": [231,229,228,227,226,225,224,223,222,221],
     "curr":    [70,85,90,78,94,108,82,88,96,102],
     "addrs":   ["Przemysłowa 2","Przemysłowa 4","Przemysłowa 6","Przemysłowa 8","Przemysłowa 10","Przemysłowa 12","Techniczna 2","Techniczna 4","Techniczna 6","Techniczna 8"]},
    {"id": "C5", "st": "ST-C", "label": "ST-C Centrum → Rynek",     "load": 55, "cable": "YAKY 4×70",
     "n": 10, "pv_indices": [0,1,3,5,7,9], "asym": 0.5,
     "volt_l1": [232,231,230,230,229,229,228,228,227,227],
     "volt_l2": [231,231,230,229,229,228,228,227,227,226],
     "volt_l3": [230,230,229,229,228,228,227,226,226,225],
     "curr":    [32,40,36,44,38,42,30,36,40,34],
     "addrs":   ["Centrum 1","Centrum 3","Rynek 2","Rynek 4","Rynek 6","Rynek 8","Rynek 10","Rynek 12","Rynek 14","Rynek 16"]},
    {"id": "C6", "st": "ST-C", "label": "ST-C Kwiatowa → Długa",    "load": 48, "cable": "YAKY 4×70",
     "n": 10, "pv_indices": [0,2,4,6,7,9], "asym": 0.7,
     "volt_l1": [232,231,231,230,230,229,229,228,228,227],
     "volt_l2": [231,231,230,230,229,229,228,228,227,227],
     "volt_l3": [230,230,230,229,229,228,228,237,226,226],
     "curr":    [28,32,36,30,34,38,26,32,36,30],
     "addrs":   ["Kwiatowa 1","Kwiatowa 3","Długa 2","Długa 4","Długa 6","Długa 8","Długa 10","Długa 12","Długa 14","Długa 16"]},
]

# ─── TRANSFORMATORY ───────────────────────────────────────────────────────────
TRANSFORMERS = [
    {"id": "ST-A", "name": "ST-A Górna",   "kva": 250, "load": 64, "temp_oil": 52, "temp_wind": 61,
     "vibration": 1.2, "thd": 4.1, "isolation": 98, "pf": 0.91, "status": "ok"},
    {"id": "ST-B", "name": "ST-B Wólka",   "kva": 400, "load": 83, "temp_oil": 68, "temp_wind": 79,
     "vibration": 3.8, "thd": 9.4, "isolation": 87, "pf": 0.86, "status": "warn"},
    {"id": "ST-C", "name": "ST-C Centrum", "kva": 250, "load": 52, "temp_oil": 48, "temp_wind": 56,
     "vibration": 0.9, "thd": 3.2, "isolation": 99, "pf": 0.93, "status": "ok"},
]

# ─── ALERTY ───────────────────────────────────────────────────────────────────
ALERTS = [
    {"sev": "error", "icon": "⚡", "title": "Asymetria faz 5.8% — Ciąg C3",
     "meter": "C3", "station": "ST-B", "loc": "Ciąg C3, ST-B Wólka", "time": "15:04",
     "desc": "Asymetria prądów faz 5.8% (norma EN 50160: 2%). L1: 148A, L2: 162A, L3: 131A.",
     "consequences": [
         "Uszkodzenie silników elektrycznych — asymetria 5% skraca żywotność o ~50%",
         "Przegrzanie uzwojeń transformatora — wzrost temperatury oleju o 3–5°C",
         "Wibracje mechaniczne i hałas silników u odbiorców",
         "Ryzyko termicznego uszkodzenia kabla L2 (największy prąd)",
     ],
     "actions": ["Pomiar asymetrii na miejscu — ciąg C3", "Przebilansować odbiorniki 1-fazowe",
                 "Rozważyć przeniesienie odbioru M-021 do ciągu C4"]},
    {"sev": "error", "icon": "🌡", "title": "Temperatura oleju transformatora 68°C",
     "meter": "ST-B", "station": "ST-B", "loc": "Transformator ST-B Wólka 400 kVA", "time": "14:58",
     "desc": "Temperatura oleju 68°C. Norma IEC 60076: max 65°C. Temperatura uzwojeń: 79°C.",
     "consequences": [
         "Przyspieszone starzenie izolacji — każde 6°C powyżej normy skraca żywotność o 50%",
         "Ryzyko przebicia izolacji uzwojenia przy dalszym wzroście",
         "Przy 80°C: wyłączenie ochronne → blackout 20 odbiorców",
         "Degradacja oleju — utrata właściwości dielektrycznych",
     ],
     "actions": ["Natychmiastowe odciążenie o min. 15 kW", "Sprawdzić chłodzenie (wentylatory, poziom oleju)",
                 "Zaplanować inspekcję — badanie DGA"]},
    {"sev": "error", "icon": "⚠", "title": "Przeciążenie transformatora 83%",
     "meter": "ST-B", "station": "ST-B", "loc": "Transformator ST-B Wólka 400 kVA", "time": "14:15",
     "desc": "Obciążenie 83% (332/400 kVA). Prognoza AI: 92% o godz. 18:30.",
     "consequences": [
         "Przekroczenie 90% o 18:30 — ryzyko zadziałania zabezpieczenia nadprądowego",
         "Blackout 20 odbiorców przy zadziałaniu",
         "Utrata żywotności transformatora ~0.3 dnia/godz. przy 100%",
     ],
     "actions": ["Aktywować DSM dla 5 odbiorców — redukcja ~18 kW",
                 "Prewencyjne przełączenie ciągów C3→C4", "Alarmować dyspozytora"]},
    {"sev": "error", "icon": "📊", "title": "THD napięcia 9.4%",
     "meter": "ST-B", "station": "ST-B", "loc": "Transformator ST-B Wólka", "time": "14:00",
     "desc": "Zniekształcenie harmoniczne THD-U = 9.4%. Norma EN 50160: max 8%.",
     "consequences": [
         "Błędy pomiarowe liczników kl. 0.5 — do 2% błędu rozliczeniowego",
         "Zakłócenia EMC — awarie sterowników PLC i urządzeń elektronicznych",
         "Dodatkowe straty w kablach od prądów harmonicznych",
     ],
     "actions": ["Pomiar harmonicznych u głównych odbiorców nielinowych",
                 "Rozważyć instalację filtru aktywnego APF",
                 "Sprawdzić filtry LC przemienników częstotliwości"]},
    {"sev": "warn", "icon": "📉", "title": "Napięcie na końcu ciągu C3 — L3: 208V",
     "meter": "M-030", "station": "ST-B", "loc": "Fabryczna 14, ciąg C3", "time": "14:32",
     "desc": "Napięcie L3 na końcu ciągu C3: 208V. Dolna granica normy EN 50160: 207V.",
     "consequences": [
         "Zanik zasilania urządzeń z zabezpieczeniami podnapięciowymi",
         "Zwiększone prądy silnikowe — większe nagrzewanie uzwojeń",
         "Ryzyko błędnego działania urządzeń elektronicznych",
     ],
     "actions": ["Przełączyć 3–4 ostatnich odbiorców na ciąg C4",
                 "Rozważyć instalację regulatora napięcia (SVR) na ciągu"]},
    {"sev": "warn", "icon": "〰", "title": "Asymetria faz 4.1%",
     "meter": "M-019", "station": "ST-A", "loc": "ST-A, Leśna 10", "time": "14:08",
     "desc": "Asymetria napięć 4.1% — tendencja wzrostowa od 4 godzin.",
     "consequences": [
         "Wzrost temperatur silników o ~10–15%",
         "Przy >5%: ryzyko uszkodzenia sprężarki klimatyzacji",
     ],
     "actions": ["Monitorować przez 2 odczyty (30 min)", "Sprawdzić bilans obciążeń 1-fazowych"]},
    {"sev": "warn", "icon": "📉", "title": "Niski cos φ = 0.83",
     "meter": "M-020", "station": "ST-A", "loc": "ST-A, Leśna 12", "time": "13:40",
     "desc": "Cos φ = 0.83, poniżej minimum 0.90 dla taryfy B23.",
     "consequences": [
         "Narzut za energię bierną — ~12% wartości rachunku",
         "Wyższe prądy — dodatkowe straty cieplne w kablach",
         "Przy cos φ < 0.75: kara umowna z OSD",
     ],
     "actions": ["Sprawdzić kondensatory kompensacyjne M-020", "Poinformować odbiorcę o ryzyku narzutu"]},
    {"sev": "warn", "icon": "🌡", "title": "Temperatura obudowy licznika 61°C",
     "meter": "M-028", "station": "ST-B", "loc": "ST-B, Wólka 5", "time": "13:25",
     "desc": "Temperatura obudowy 61°C. Próg ostrzegawczy: 58°C. Norma: max 70°C.",
     "consequences": [
         "Skrócenie żywotności elektroniki licznika",
         "Ryzyko dryfu pomiarowego przy temp. >60°C",
         "Przy >70°C: samoczynny reset → utrata danych 15-min",
     ],
     "actions": ["Sprawdzić wentylację szafy mierniczej", "Pomiar rezystancji zacisków"]},
    {"sev": "warn", "icon": "⚡", "title": "Napięcie L3 237V na ciągu C6",
     "meter": "M-058", "station": "ST-C", "loc": "Długa 12, ciąg C6 ST-C", "time": "13:10",
     "desc": "Napięcie L3 = 237V (+3.0%). Wartość bliska górnej granicy normy (253V).",
     "consequences": [
         "Skrócenie żywotności urządzeń na L3 — wzrost poboru przez urządzenia grzewcze",
         "Ryzyko uszkodzenia zasilaczy impulsowych",
         "PV na końcu ciągu podbija napięcie — przy dużej produkcji może przekroczyć normę",
     ],
     "actions": ["Monitorować — przy >240V zgłosić do OSD", "Sprawdzić bilans na ST-C"]},
]

# ─── FRAUD ────────────────────────────────────────────────────────────────────
FRAUD_CASES = [
    {"id": "M-041", "addr": "Centrum 1", "station": "ST-C", "score": 86, "trend": "rosnący ↑",
     "evidence": [
         "Zużycie spadło o −71% w 4 dni bez żadnych zgłoszeń technicznych",
         "Brak komunikacji 2h 44min w nocy — 3× w ciągu ostatnich 7 dni",
         "Profil dobowy niezgodny z taryfą G12 (pobór w szczycie nocnym 02–04)",
         "Napięcie L1 zaniżone o 4.2V względem sąsiednich liczników na tym samym ciągu",
         "Ostatni odczyt fizyczny: 14 miesięcy temu",
     ],
     "recommendation": "WYSOKI PRIORYTET — inspekcja techniczna w ciągu 48h. Sprawdzić plombę i cewkę prądową.",
     "priority": "HIGH"},
    {"id": "M-019", "addr": "Leśna 10", "station": "ST-A", "score": 74, "trend": "stabilny →",
     "evidence": [
         "Regularne luki komunikacyjne 00:30–01:30 (4× w ostatnim tygodniu)",
         "L2 pobiera o 38% więcej niż L1 i L3 — możliwy nielegalny odbiór 1-fazowy",
         "Brak korelacji zużycia z temperaturą (r=0.22, oczekiwane r>0.7)",
         "Zużycie niższe o 62% vs. sąsiednie domy o podobnej charakterystyce",
     ],
     "recommendation": "ŚREDNI PRIORYTET — weryfikacja podczas kolejnej wizyty. Analiza historii 12 miesięcy.",
     "priority": "MEDIUM"},
    {"id": "M-038", "addr": "Portowa 15", "station": "ST-B", "score": 71, "trend": "stabilny →",
     "evidence": [
         "Skok odczytu o 840 kWh w jednym interwale 15-min — możliwy reset licznika",
         "Cos φ = 0.61 — niecharakterystyczne dla odbiorcy mieszkaniowego",
         "Zmiana profilu zużycia od 3 tygodni — szczyt w nocy zamiast w dzień",
     ],
     "recommendation": "NISKI-ŚREDNI — obserwacja przez 2 tygodnie. Przy utrzymaniu anomalii: inspekcja.",
     "priority": "LOW"},
]


# ─── GENERATORY SZEREGÓW CZASOWYCH ────────────────────────────────────────────

def get_load_profile_96(station_id: str = "all", ref_date=None) -> pd.DataFrame:
    """
    Profil zużycia — 96 punktów (co 15 min przez 24h).

    Wartości REALISTYCZNE dla Polski (dane GUS/URE):
    - Średnie gosp. domowe: ~3 500 kWh/rok → ~9.6 kWh/dobę → ~0.4 kW średnio
    - Szczyt wieczorny (17-21h): ~0.8–1.2 kW per gosp.
    - 20 gosp. domowych (ST-A/C): szczyt ~20 kW, średnia ~8 kW
    - 20 odbiorców mix przem. (ST-B): szczyt ~200 kW, średnia ~80 kW
    - 60 odbiorców łącznie: szczyt ~350–450 kW
    """
    seed = 42 if ref_date is None else int(str(ref_date).replace("-","")) % 10000
    rng = np.random.default_rng(seed)

    # Bazowy profil znormalizowany 0-1 (typowy profil PL wg PSE)
    # Dwa szczyty: poranny 7-9h i wieczorny 17-21h
    base_norm = np.array([
        0.38, 0.35, 0.32, 0.30, 0.29, 0.28, 0.30, 0.38,   # 0-7h  noc/świt
        0.55, 0.72, 0.78, 0.75, 0.70, 0.68, 0.65, 0.62,   # 8-15h praca
        0.65, 0.72, 0.82, 0.92, 1.00, 0.95, 0.88, 0.80,   # 16-23h wieczór
    ], dtype=float)
    # Rozszerzamy do 96 punktów (każda godzina → 4×15min)
    base_96 = np.repeat(base_norm, 4)
    # Lekkie wygładzenie
    kernel = np.array([0.15, 0.7, 0.15])
    base_96_s = np.convolve(base_96, kernel, mode='same')

    # Skale mocy szczytowej per stacja (kW)
    # ST-A: 20 gosp. mieszkaniowych → szczyt ~18 kW
    # ST-B: 20 odbiorcow mix przemysłowych → szczyt ~220 kW
    # ST-C: 20 usługowo-mieszkaniowych → szczyt ~22 kW
    peak = {"ST-A": 18, "ST-B": 220, "ST-C": 22}.get(station_id, 260)

    load = base_96_s * peak * (1 + rng.normal(0, 0.04, 96))
    load = np.clip(load, 0, None)

    # OZE — aktywna 07:00–17:00 (indeksy 28–68 przy 15-min próbkowaniu)
    # Marzec: świt ~07:30, zmierzch ~17:30
    pv_peak = {"ST-A": 50, "ST-B": 30, "ST-C": 60}.get(station_id, 140)

    # Kształt krzywej PV — gaussowski dla marca
    pv_center = 48  # południe = index 48 (12:00)
    pv_sigma  = 14  # szerokość
    pv_shape  = np.exp(-0.5 * ((np.arange(96) - pv_center) / pv_sigma) ** 2)
    # Wyzeruj przed 7:00 (idx<28) i po 17:00 (idx>68)
    pv_shape[:28] = 0
    pv_shape[69:]  = 0
    # Zachmurzenie o 13h (~idx 52-56)
    cloud_factor = np.ones(96)
    cloud_factor[52:57] = 0.45 + rng.random(5) * 0.2
    oze = pv_shape * pv_peak * cloud_factor * (0.88 + rng.random(96) * 0.18)
    oze = np.clip(oze, 0, pv_peak)

    netto = np.maximum(0, load - oze)

    # Timestamp bazowy
    base_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    if ref_date is not None:
        try:
            base_dt = datetime(ref_date.year, ref_date.month, ref_date.day)
        except Exception:
            base_dt = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    times = [base_dt + timedelta(minutes=15 * i) for i in range(96)]

    return pd.DataFrame({"time": times,
                         "load_kw": load.round(0),
                         "oze_kw": oze.round(0),
                         "netto_kw": netto.round(0)})


def get_voltage_history_48(ciag_id: str = "C1", phase: str = "avg") -> pd.DataFrame:
    """Historia napięć na ciągu — 48 punktów (co 30 min przez 24h)."""
    rng = np.random.default_rng(hash(ciag_id) % (2**31))
    c = next((x for x in CIAGI if x["id"] == ciag_id), CIAGI[0])
    base_v = {
        "L1": np.mean(c["volt_l1"]),
        "L2": np.mean(c["volt_l2"]),
        "L3": np.mean(c["volt_l3"]),
        "avg": np.mean(c["volt_l1"] + c["volt_l2"] + c["volt_l3"]),
    }[phase]

    noise = rng.normal(0, 1.5, 48)
    # Napięcie nieco niższe w godzinach szczytu (17-20h = idx 34-40)
    dip = np.zeros(48)
    dip[34:40] = -2.5
    voltages = base_v + noise + dip

    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    times = [now + timedelta(minutes=30 * i) for i in range(48)]
    return pd.DataFrame({"time": times, "voltage_v": voltages.round(1)})


def get_pv_profile(station_id: str = "all") -> pd.DataFrame:
    """Profil produkcji PV — godzinowy, realny dla marca w Polsce."""
    rng = np.random.default_rng(99)
    pv_peak = {"ST-A": 50, "ST-B": 30, "ST-C": 60}.get(station_id, 140)

    # Marzec: wschód ~06:30, zachód ~17:45, produkcja 07:00–17:00
    shape = [0, 0, 0, 0, 0, 0, 0,
             0.02, 0.12, 0.28, 0.48, 0.65,
             0.78, 0.72, 0.58, 0.40, 0.22,
             0.06, 0, 0, 0, 0, 0, 0]
    forecast = [round(f * pv_peak, 1) for f in shape]
    # Zachmurzenie o 13-14h
    actual = []
    for h, f in enumerate(shape):
        factor = 0.82 + rng.random() * 0.24
        if h in (13, 14):
            factor *= 0.55
        actual.append(round(f * pv_peak * factor, 1))

    hours = [f"{h:02d}:00" for h in range(24)]
    return pd.DataFrame({"hour": hours, "forecast_kw": forecast, "actual_kw": actual})


def get_prediction_monthly(station_id: str = "all", months_ahead: int = 1,
                           start_date=None) -> pd.DataFrame:
    """
    Prognoza zuzycia — od 1 do 12 miesiecy do przodu z uwzglednieniem:
    - sezonowosc (zima +35%, lato -25%)
    - temperatura (korelacja r=0.82 z poborem ogrzewania)
    - weekend vs dzien roboczy (-15%)
    - rosnacc przedzialy ufnosci z horyzontem
    """
    rng = np.random.default_rng(7)
    base_daily = {"sta": 320, "stb": 3800, "stc": 390}.get(station_id, 4510)
    seasonal = {
        1:1.38, 2:1.32, 3:1.12, 4:0.92, 5:0.80, 6:0.73,
        7:0.72, 8:0.75, 9:0.85, 10:1.02, 11:1.22, 12:1.35,
    }
    avg_temp = {
        1:-2, 2:-1, 3:4, 4:10, 5:15, 6:19,
        7:21, 8:20, 9:16, 10:10, 11:4, 12:0,
    }
    today = datetime.now().date()
    if start_date is None:
        start_date = today
    n_days = months_ahead * 31
    rows = []
    for i in range(n_days):
        d = start_date + timedelta(days=i)
        m = d.month
        dow = d.weekday()
        season_factor = seasonal[m]
        temp_factor = 1.0 + max(0, (8 - avg_temp[m]) * 0.015)
        weekend_factor = 0.86 if dow >= 5 else 1.0
        noise = rng.normal(0, 0.035)
        value = base_daily * season_factor * temp_factor * weekend_factor * (1 + noise)
        ci_pct = min(0.32, 0.06 + i * 0.0007)
        is_hist = d <= today
        rows.append({
            "date": d,
            "label": d.strftime("%d.%m"),
            "value": round(value, 0),
            "upper": round(value * (1 + ci_pct), 0) if not is_hist else float("nan"),
            "lower": round(value * (1 - ci_pct), 0) if not is_hist else float("nan"),
            "history": round(value, 0) if is_hist else float("nan"),
            "forecast": round(value, 0) if not is_hist else float("nan"),
            "temp_avg": avg_temp[m],
            "season_factor": season_factor,
            "is_weekend": dow >= 5,
            "month": m,
        })
    return pd.DataFrame(rows)


def get_risk_events_prediction(station_id: str = "ST-B",
                               months_ahead: int = 3) -> pd.DataFrame:
    """Predykcja ryzyka przeciazen na podstawie pogody i sezonowosc."""
    rng = np.random.default_rng(42)
    today = datetime.now().date()
    n_days = months_ahead * 30
    seasonal_risk = {
        1:0.72, 2:0.68, 3:0.55, 4:0.28, 5:0.18, 6:0.12,
        7:0.10, 8:0.12, 9:0.22, 10:0.38, 11:0.58, 12:0.70,
    }
    risk_drivers = {
        1:"Mroz + ogrzewanie el.", 2:"Mroz + ogrzewanie el.",
        3:"Zmienne temperatury",  4:"Normalne warunki",
        5:"Normalne warunki",    6:"Klimatyzacja",
        7:"Klimatyzacja (szczyt)", 8:"Klimatyzacja",
        9:"Zmienne temperatury", 10:"Normalne warunki",
        11:"Deszcz + ogrzewanie", 12:"Mroz + ogrzewanie el.",
    }
    rows = []
    for i in range(n_days):
        d = today + timedelta(days=i)
        m = d.month
        base_risk = seasonal_risk[m]
        risk = float(np.clip(base_risk + rng.normal(0, 0.08), 0.05, 0.97))
        rows.append({
            "date": d, "label": d.strftime("%d.%m"),
            "risk_pct": round(risk * 100, 1),
            "driver": risk_drivers[m],
            "level": "high" if risk > 0.6 else "medium" if risk > 0.35 else "low",
        })
    return pd.DataFrame(rows)
def get_price_forecast() -> pd.DataFrame:
    """Prognoza cen TGE na marzec."""
    rng = np.random.default_rng(13)
    base = [.82,.80,.78,.76,.75,.74,.78,.84,.88,.86,.84,.82,.80,.84,.88,.92,
            .96,1.02,1.10,1.12,1.10,1.05,.98,.92,.88,.84,.82,.80,.78,.76,.74]
    noise = rng.normal(0, 0.02, 31)
    price = np.array(base) + noise
    upper = price + 0.06
    lower = price - 0.06
    days = [f"{d+1:02d}.03" for d in range(31)]
    return pd.DataFrame({"day": days, "price": price.round(3),
                         "upper": upper.round(3), "lower": lower.round(3)})


def get_transformer_temp_history() -> pd.DataFrame:
    """Historia temperatury oleju transformatorów — 48h, co 30 min."""
    rng = np.random.default_rng(55)
    n = 48
    base_stb = np.linspace(60, 68, n) + rng.normal(0, 0.5, n)
    base_sta = np.linspace(50, 52, n) + rng.normal(0, 0.3, n)
    base_stc = np.linspace(47, 48, n) + rng.normal(0, 0.3, n)
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    times = [now + timedelta(minutes=30 * i) for i in range(n)]
    return pd.DataFrame({"time": times,
                         "ST-A": base_sta.round(1),
                         "ST-B": base_stb.round(1),
                         "ST-C": base_stc.round(1)})


def get_vibration_spectrum(station_id: str = "ST-B") -> pd.DataFrame:
    """Widmo drgań FFT transformatora."""
    data = {
        "ST-A": [0.3, 1.2, 0.4, 0.8, 0.3, 0.6, 0.2, 0.4, 0.2, 0.3],
        "ST-B": [0.4, 3.8, 0.6, 2.2, 0.5, 1.8, 0.3, 0.9, 0.2, 0.4],
        "ST-C": [0.2, 0.9, 0.3, 0.5, 0.2, 0.4, 0.1, 0.3, 0.1, 0.2],
    }
    freqs = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    vals = data.get(station_id, data["ST-B"])
    return pd.DataFrame({"freq_hz": freqs, "amplitude_mms": vals})


def get_vibration_history(station_id: str = "ST-B") -> pd.DataFrame:
    """Historia amplitudy drgań 100 Hz — 30 dni (trend detekcji anomalii)."""
    rng = np.random.default_rng(hash(station_id) % (2**31))
    n = 30
    base_vals = {"ST-A": 1.2, "ST-B": 3.2, "ST-C": 0.9}
    base = base_vals.get(station_id, 3.2)
    # ST-B ma lekki trend wzrostowy (sygnał nadchodzącej anomalii)
    trend = 0.018 if station_id == "ST-B" else 0.002
    values = base + trend * np.arange(n) + rng.normal(0, 0.12, n)
    values = np.clip(values, 0.1, 5.0)
    today = datetime.now().date()
    dates = [str(today - timedelta(days=n-1-i)) for i in range(n)]
    return pd.DataFrame({"date": dates, "vib_100hz": values.round(3)})


def get_thd_harmonics() -> pd.DataFrame:
    """Harmoniczne THD per stacja."""
    orders = ["3.", "5.", "7.", "9.", "11.", "13.", "15."]
    return pd.DataFrame({
        "order": orders,
        "ST-A": [1.2, 0.8, 0.5, 0.4, 0.3, 0.2, 0.1],
        "ST-B": [3.4, 2.1, 1.6, 1.0, 0.8, 0.5, 0.3],
        "ST-C": [0.9, 0.6, 0.4, 0.3, 0.2, 0.1, 0.1],
    })


def get_transformer_load_history() -> pd.DataFrame:
    """Historia obciążeń transformatorów — 7 dni."""
    rng = np.random.default_rng(22)
    days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
    return pd.DataFrame({
        "day": days,
        "ST-A": (np.array([58,60,62,63,61,55,64]) + rng.normal(0,1,7)).round(1),
        "ST-B": (np.array([78,80,81,83,82,75,83]) + rng.normal(0,1,7)).round(1),
        "ST-C": (np.array([48,50,49,52,51,44,52]) + rng.normal(0,1,7)).round(1),
    })


def get_asym_prediction() -> pd.DataFrame:
    """Predykcja asymetrii faz — 7 dni."""
    days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
    return pd.DataFrame({
        "day": days,
        "ST-A": [1.2, 1.4, 1.8, 1.5, 1.6, 2.1, 1.9],
        "ST-B": [3.1, 3.4, 4.2, 3.8, 4.5, 3.2, 2.8],
        "ST-C": [0.8, 0.9, 1.1, 1.0, 1.2, 0.8, 0.9],
    })


def get_fraud_anomaly_series() -> pd.DataFrame:
    """Szereg anomalii zużycia dla M-041."""
    rng = np.random.default_rng(77)
    n = 30
    expected = rng.uniform(3.5, 5.2, n).round(2)
    actual = expected.copy()
    # Od dnia 8 zużycie dramatycznie spada
    actual[8:] = rng.uniform(0.2, 0.8, n - 8)
    upper = (expected + 0.9).round(2)
    lower = np.maximum(0, expected - 0.9).round(2)
    days = list(range(1, 31))
    comm_breaks = [9, 15, 22]  # dni z przerwą komunikacyjną
    return pd.DataFrame({"day": days, "expected": expected,
                         "actual": actual, "upper": upper, "lower": lower,
                         "comm_break": [d in comm_breaks for d in days]})


def get_fraud_daily_profile() -> pd.DataFrame:
    """Profil dobowy M-041 vs. grupa odniesienia."""
    hours = list(range(24))
    group_avg = [0.8,0.5,0.4,0.3,0.3,0.4,1.2,2.8,3.4,3.0,2.8,2.6,
                 2.4,2.6,2.8,3.0,3.2,3.6,3.8,3.4,2.8,2.0,1.4,1.0]
    m041 = [3.2,3.8,4.1,3.9,3.6,0.4,0.3,0.4,0.5,0.4,0.3,0.4,
            0.3,0.4,0.3,0.4,0.3,0.4,0.3,0.2,0.3,1.2,2.4,3.0]
    return pd.DataFrame({"hour": hours, "group_avg": group_avg, "m041": m041})


def get_digital_twin_profile() -> pd.DataFrame:
    """Cyfrowy bliźniak — profil dobowy rzeczywisty vs. model."""
    rng = np.random.default_rng(33)
    hours = list(range(24))
    actual = [22,18,15,13,12,11,17,26,34,38,40,42,44,42,40,38,
              42,46,50,52,46,38,30,24]
    twin = [round(v * (1 + rng.normal(0, 0.03)), 1) for v in actual]
    price = [.62,.58,.55,.52,.50,.48,.52,.70,.86,.90,.88,.86,
             .84,.82,.80,.82,.90,.96,1.00,.96,.88,.80,.70,.64]
    return pd.DataFrame({"hour": hours, "actual_kw": actual,
                         "twin_kw": twin, "price_pln": price})


def get_meters_df() -> pd.DataFrame:
    """DataFrame wszystkich 60 liczników."""
    rng = np.random.default_rng(42)
    rows = []
    for c in CIAGI:
        for i, mid in enumerate(range(10)):
            meter_id = f"M-{(CIAGI.index(c)*10 + i + 1):03d}"
            addr = c["addrs"][i]
            st = c["st"]
            ciag = c["id"]
            is_pv = i in c["pv_indices"]
            is_industry = c["st"] == "ST-B" and i < 4
            consumption = round(rng.uniform(18, 35) if is_industry else rng.uniform(2, 9), 1)
            asym = round(rng.uniform(4.5, 8) if (c["id"] == "C3" and i >= 4)
                         else rng.uniform(2.2, 4.5) if (c["id"] == "C3" and i < 4)
                         else rng.uniform(0.2, 1.8), 1)
            temp = int(rng.integers(58, 74) if is_industry else rng.integers(35, 50))
            pf = round(rng.uniform(0.82, 0.97), 2)
            v1, v2, v3 = c["volt_l1"][i], c["volt_l2"][i], c["volt_l3"][i]
            fraud = meter_id in ["M-041", "M-019", "M-038"]
            fraud_score = {"M-041": 86, "M-019": 74, "M-038": 71}.get(meter_id, 0)
            if fraud and meter_id == "M-041":
                consumption = round(rng.uniform(0.2, 0.6), 1)
            status = ("error" if (fraud and meter_id == "M-041") or asym > 5 or temp > 65
                      else "warn" if asym > 3 or temp > 58
                      else "ok")
            rows.append({
                "id": meter_id, "addr": addr, "station": st, "ciag": ciag,
                "consumption_kwh": consumption, "pf": pf,
                "temp_c": temp, "asym_pct": asym,
                "volt_l1": v1, "volt_l2": v2, "volt_l3": v3,
                "current_a": c["curr"][i],
                "is_pv": is_pv, "status": status,
                "fraud": fraud, "fraud_score": fraud_score,
                "dist_m": (i + 1) * 80,
            })
    return pd.DataFrame(rows)


def get_risk_forecast() -> pd.DataFrame:
    """Ryzyko awarii na 12 dni."""
    rng = np.random.default_rng(88)
    days = ["Pon","Wt","Śr","Czw","Pt","Sob","Nd","Pon","Wt","Śr","Czw","Pt"]
    return pd.DataFrame({
        "day": days,
        "ST-B": (np.array([62,65,68,70,72,58,65,74,78,80,83,85]) + rng.normal(0,1,12)).round(1),
        "ST-A": (np.array([50,52,55,54,58,44,52,56,60,62,64,65]) + rng.normal(0,1,12)).round(1),
    })


def get_cost_forecast() -> pd.DataFrame:
    """Prognoza kosztu energii na marzec."""
    rng = np.random.default_rng(44)
    base = np.ones(31) * 820
    peak_days = list(range(16, 22))
    for d in peak_days:
        base[d] += 280
    cost = base + rng.normal(0, 40, 31)
    days = [f"{d+1:02d}.03" for d in range(31)]
    return pd.DataFrame({"day": days, "cost_pln": cost.round(0),
                         "is_peak": [i in peak_days for i in range(31)]})


def get_voltage_map_data(ciag_id: str, phase: str = "avg") -> pd.DataFrame:
    """Dane mapy napięć per licznik na ciągu."""
    c = next((x for x in CIAGI if x["id"] == ciag_id), CIAGI[0])
    rows = []
    for i in range(c["n"]):
        v1, v2, v3 = c["volt_l1"][i], c["volt_l2"][i], c["volt_l3"][i]
        if phase == "avg":
            v = round((v1 + v2 + v3) / 3, 1)
        elif phase == "L1":
            v = v1
        elif phase == "L2":
            v = v2
        else:
            v = v3
        is_pv = i in c["pv_indices"]
        status = ("critical" if v < 207 or v > 246
                  else "warning" if v < 218 or v > 238
                  else "ok")
        rows.append({
            "pos": i + 1,
            "addr": c["addrs"][i] + (" ☀" if is_pv else ""),
            "addr_clean": c["addrs"][i],
            "voltage": v, "v_l1": v1, "v_l2": v2, "v_l3": v3,
            "current": c["curr"][i],
            "is_pv": is_pv,
            "dist_m": (i + 1) * 80,
            "status": status,
        })
    return pd.DataFrame(rows)


# ─── PODSUMOWANIE KPI ─────────────────────────────────────────────────────────
SUMMARY_KPI = [
    {"label": "Dokładność predykcji ML",     "value": "94.7%",      "color": "green"},
    {"label": "Oszczędności DSM (marzec)",   "value": "3 240 PLN",  "color": "blue"},
    {"label": "Przychód VPP (prognoza)",     "value": "4 800 PLN",  "color": "green"},
    {"label": "Emisja CO₂ skompensowana",    "value": "−4.6 t",     "color": "teal"},
    {"label": "Anomalie ML (30 dni)",        "value": "31",         "color": "orange"},
    {"label": "Uptime sieci",                "value": "99.4%",      "color": "green"},
]

CRITICAL_ACTIONS = [
    {"icon": "🔥", "title": "Odciążyć transformator ST-B",
     "desc": "83% → prognoza 92% o 18:30. DSM dla 5 odbiorców (−18 kW). Ryzyko blackout 20 odbiorców."},
    {"icon": "🌡", "title": "Inspekcja chłodzenia ST-B",
     "desc": "Olej 68°C (norma 65°C). Sprawdzić wentylatory i poziom oleju. Zlecić badanie DGA."},
    {"icon": "🔍", "title": "Inspekcja M-041 Centrum 1",
     "desc": "Fraud score 86/100. Brak fizycznego odczytu 14 miesięcy. Sprawdzić plombę i cewkę prądową."},
    {"icon": "⚡", "title": "Redukcja asymetrii na C3",
     "desc": "Asymetria 5.8%, napięcie na końcu L3: 208V. Przebilansować odbiorniki 1-fazowe."},
]

PLANNED_ACTIONS = [
    {"icon": "📊", "title": "Badanie harmonicznych ST-B",
     "desc": "THD 9.4% > norma 8%. Pomiar u odbiorców nielinowych. Rozważyć filtr APF."},
    {"icon": "🔋", "title": "Kompensacja mocy biernej M-020",
     "desc": "Cos φ 0.83 — przegląd kondensatorów. Ryzyko narzutu taryfowego ~12%."},
    {"icon": "☀", "title": "Aktywacja VPP przed szczytem 18–22 marca",
     "desc": "Niska produkcja PV + wysoki popyt. Agregacja 28 prosumentów do rynku bilansującego."},
    {"icon": "📋", "title": "Weryfikacja M-019, M-038",
     "desc": "Fraud score 74 i 71. Zaplanować weryfikację podczas wizyty technicznej."},
    {"icon": "🌿", "title": "Raport ESG — luty",
     "desc": "Generacja raportu CO₂. Offset PV: 4.6 t. Export PDF/XLSX."},
]
