import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import base64

# --- [CHECKPOINT 22: INTERNAL IMAGE EMBEDDING] ---
# Στάδιο: Ενσωμάτωση εικόνων σε μορφή κειμένου (Base64) για 100% εμφάνιση.

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΕΝΣΩΜΑΤΩΣΗ ΕΙΚΟΝΩΝ ---
# Μετατρέπουμε τα εικονίδια σε κώδικα για να μην "σπάνε" ποτέ
def get_svg_image(type):
    # Επαγγελματική σιλουέτα Ευρωπαϊκού Τράκτορα
    if type == "tractor":
        return '''<svg viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg"><rect x="10" y="15" width="35" height="30" rx="3" fill="#00D2FF"/><rect x="45" y="35" width="15" height="10" fill="#00D2FF"/><circle cx="20" cy="50" r="6" fill="white"/><circle cx="40" cy="50" r="6" fill="white"/><rect x="15" y="20" width="20" height="12" fill="#1a1a1a"/></svg>'''
    # Επαγγελματική σιλουέτα Τράκτορα με Άδεια Νταλίκα
    elif type == "trailer":
        return '''<svg viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="20" width="25" height="25" rx="2" fill="#00D2FF"/><rect x="30" y="38" width="60" height="4" fill="#888"/><circle cx="12" cy="50" r="5" fill="white"/><circle cx="75" cy="50" r="5" fill="white"/><circle cx="85" cy="50" r="5" fill="white"/></svg>'''
    # Επαγγελματική σιλουέτα με Κοντέινερ (Κουτί)
    else:
        return '''<svg viewBox="0 0 100 60" xmlns="http://www.w3.org/2000/svg"><rect x="5" y="20" width="25" height="25" rx="2" fill="#00D2FF"/><rect x="30" y="38" width="60" height="4" fill="#888"/><rect x="35" y="15" width="55" height="23" rx="1" fill="#FF4B4B"/><circle cx="12" cy="50" r="5" fill="white"/><circle cx="75" cy="50" r="5" fill="white"/><circle cx="85" cy="50" r="5" fill="white"/></svg>'''

# --- CUSTOM CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ LOOK ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .card-ui {
        background: #1f2937;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        border: 1px solid #374151;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    .main-btn-start button { background-color: #10b981 !important; height: 80px !important; font-size: 20px !important; color: white !important; }
    .main-btn-stop button { background-color: #ef4444 !important; height: 80px !important; font-size: 20px !important; color: white !important; }
    h1, h2, h3 { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- APP LOGIC ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΟΧΗΜΑΤΟΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("Τι οδηγείς τώρα;")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="card-ui">{get_svg_image("tractor")}</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with col2:
        st.markdown(f'<div class="card-ui">{get_svg_image("trailer")}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with col3:
        st.markdown(f'<div class="card-ui">{get_svg_image("full")}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΔΡΑΣΗ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### Σύνθεση: **{st.session_state.current_config}**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="main-btn-start">', unsafe_allow_html=True)
        if st.button("🚀 ΞΕΚΙΝΗΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="main-btn-stop">', unsafe_allow_html=True)
        if st.button("🏁 ΕΦΤΑΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Αλλαγή Οχήματος"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΠΡΟΒΟΛΗ ΙΣΤΟΡΙΚΟΥ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.table(df)
    conn.close()
