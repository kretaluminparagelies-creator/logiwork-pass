import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- CONFIG & STYLE ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        font-weight: bold;
        width: 100%;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border-color: #00d2ff;
        box-shadow: 0 0 10px #00d2ff;
    }
    h1, h2, h3, p, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE LOGIC ---
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Πίνακας Οχημάτων
    c.execute('CREATE TABLE IF NOT EXISTS vehicles (id INTEGER PRIMARY KEY, plate TEXT, type TEXT)')
    # Πίνακας Κινήσεων
    c.execute('''CREATE TABLE IF NOT EXISTS movements 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, 
                  tractor TEXT, trailer TEXT, cargo TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- SIDEBAR: ΔΙΑΧΕΙΡΙΣΗ ΣΤΟΛΟΥ ---
with st.sidebar:
    st.header("⚙️ Ρυθμίσεις Στόλου")
    new_plate = st.text_input("Προσθήκη Πινακίδας")
    v_type = st.selectbox("Τύπος", ["Τράκτορας", "Νταλίκα"])
    if st.button("➕ Προσθήκη"):
        if new_plate:
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            c.execute("INSERT INTO vehicles (plate, type) VALUES (?, ?)", (new_plate.upper(), v_type))
            conn.commit()
            conn.close()
            st.success(f"Προστέθηκε: {new_plate}")

# --- MAIN UI ---
st.title("🚛 LogiWork Pass")

# Ανάκτηση οχημάτων για τα μενού
conn = sqlite3.connect('logiwork.db')
tractors = pd.read_sql_query("SELECT plate FROM vehicles WHERE type='Τράκτορας'", conn)['plate'].tolist()
trailers = pd.read_sql_query("SELECT plate FROM vehicles WHERE type='Νταλίκα'", conn)['plate'].tolist()
conn.close()

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        selected_tractor = st.selectbox("🚜 Τράκτορας", ["-"] + tractors)
    with col2:
        selected_trailer = st.selectbox("📦 Νταλίκα", ["-"] + trailers)
    
    cargo_status = st.select_slider("Κατάσταση Φορτίου", options=["ΧΩΡΙΣ ΚΟΥΤΙ", "ΚΕΝΟ", "ΕΜΦΟΡΤΟ"])
    st.markdown('</div>', unsafe_allow_html=True)

# Κουμπιά Δράσης
col_a, col_b = st.columns(2)
with col_a:
    if st.button("🚀\nΞΕΚΙΝΗΣΑ"):
        if selected_tractor == "-":
            st.error("Διάλεξε Τράκτορα!")
        else:
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, tractor, trailer, cargo) VALUES (?, ?, ?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", selected_tractor, selected_trailer, cargo_status))
            conn.commit()
            conn.close()
            st.toast("Η εκκίνηση καταγράφηκε!")

with col_b:
    if st.button("🏁\nΕΦΤΑΣΑ"):
        conn = sqlite3.connect('logiwork.db')
        c = conn.cursor()
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        c.execute("INSERT INTO movements (timestamp, action, tractor, trailer, cargo) VALUES (?, ?, ?, ?, ?)", 
                  (now, "ΕΦΤΑΣΑ", selected_tractor, selected_trailer, cargo_status))
        conn.commit()
        conn.close()
        st.toast("Η άφιξη καταγράφηκε!")

# Ιστορικό
st.markdown("---")
if st.checkbox("📅 Προβολή Βιβλίου Δρομολογίων"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', tractor as 'Τράκτορας', trailer as 'Νταλίκα', cargo as 'Φορτίο' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
