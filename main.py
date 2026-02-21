import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- LIQUID GLASS STYLE (CSS) ---
# Εφαρμογή της αισθητικής Glassmorphism [cite: 164, 287]
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        color: white;
        height: 120px;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        border: 1px solid #00d2ff;
        box-shadow: 0 0 15px #00d2ff;
    }
    h1, h2, h3 { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ (ΣΚΕΛΕΤΟΣ) ---
# Υλοποίηση του Min DB [cite: 189, 281]
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movements 
                 (id INTEGER PRIMARY KEY, 
                  timestamp TEXT, 
                  action TEXT, 
                  origin TEXT, 
                  destination TEXT,
                  vehicle_state TEXT,
                  cargo_state TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- ΚΕΝΤΡΙΚΗ ΟΘΟΝΗ (SCREEN 1) ---
st.title("🚛 LogiWork Pass")
st.markdown("## Driver MVP")

# Επιλογή Κατάστασης (No Typing [cite: 165, 288])
vehicle_type = st.radio("Τι ρυμουλκώ;", ["Τράκτορας+Νταλίκα", "Σκέτος Τράκτορας"], horizontal=True)
cargo_status = st.select_slider("Φορτίο:", options=["ΧΩΡΙΣ ΚΟΥΤΙ", "ΚΕΝΟ", "ΕΜΦΟΡΤΟ"])

# Ροή Κίνησης [cite: 170, 260]
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀\nΞΕΚΙΝΗΣΑ"):
        conn = sqlite3.connect('logiwork.db')
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO movements (timestamp, action, vehicle_state, cargo_state) VALUES (?, ?, ?, ?)", 
                  (now, "ΞΕΚΙΝΗΣΑ", vehicle_type, cargo_status))
        conn.commit()
        conn.close()
        st.success("Καταγράφηκε!")

with col2:
    if st.button("🏁\nΕΦΤΑΣΑ"):
        conn = sqlite3.connect('logiwork.db')
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO movements (timestamp, action, vehicle_state, cargo_state) VALUES (?, ?, ?, ?)", 
                  (now, "ΕΦΤΑΣΑ", vehicle_type, cargo_status))
        conn.commit()
        conn.close()
        st.info("Εφτασες!")

# --- ΙΣΤΟΡΙΚΟ (SCREEN 5) ---
st.markdown("---")
if st.checkbox("📅 Προβολή Ιστορικού [cite: 184, 292]"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT * FROM movements ORDER BY id DESC", conn)
    st.dataframe(df)
    conn.close()
