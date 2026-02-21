import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΚΑΙ ΚΑΘΑΡΟ UI ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    /* Κάρτα για την εικόνα του φορτηγού */
    .truck-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    /* Στυλ κουμπιών επιλογής */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 60px;
        font-weight: bold;
        background: #1f2937;
        color: white;
        border: 1px solid #374151;
    }
    /* Μεγάλα κουμπιά ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ */
    .action-start button { background: #059669 !important; height: 100px !important; font-size: 20px !important; }
    .action-stop button { background: #dc2626 !important; height: 100px !important; font-size: 20px !important; }
    h1, h2, h3, p { color: white !important; text-align: center; font-family: 'Inter', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (SQLite) ---
def init_db():
    # Δημιουργία ή σύνδεση στο logiwork.db
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Αποθήκευση: Ώρα, Ενέργεια, Τύπος Οχήματος
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- ΕΙΚΟΝΕΣ ΠΡΑΓΜΑΤΙΚΟΥ ΣΤΟΛΟΥ (URLs) ---
# Χρησιμοποιούμε ρεαλιστικές απεικονίσεις φορτηγών
URL_TRACTOR = "https://cdn-icons-png.flaticon.com/512/2555/2555013.png" # Flat-nose Τράκτορας
URL_TRAILER = "https://cdn-icons-png.flaticon.com/512/3211/3211116.png" # Τράκτορας με άδεια νταλίκα
URL_CONTAINER = "https://cdn-icons-png.flaticon.com/512/1042/1042331.png" # Πλήρες με κοντέινερ

# --- ΔΙΑΧΕΙΡΙΣΗ ΡΟΗΣ (App State) ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.title("🚛 LogiWork Pass")

# --- ΣΤΑΔΙΟ 1: ΕΠΙΛΟΓΗ ΟΧΗΜΑΤΟΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("Τι οδηγείς τώρα;")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="truck-container">', unsafe_allow_html=True)
        st.image(URL_TRACTOR, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with col2:
        st.markdown('<div class="truck-container">', unsafe_allow_html=True)
        st.image(URL_TRAILER, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with col3:
        st.markdown('<div class="truck-container">', unsafe_allow_html=True)
        st.image(URL_CONTAINER, width=100)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΣΤΑΔΙΟ 2: ΚΑΤΑΓΡΑΦΗ ΔΡΟΜΟΛΟΓΙΟΥ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### Επιλογή: **{st.session_state.current_config}**")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="action-start">', unsafe_allow_html=True)
        if st.button("🚀 ΞΕΚΙΝΗΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("Έναρξη καταγράφηκε!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="action-stop">', unsafe_allow_html=True)
        if st.button("🏁 ΕΦΤΑΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("Άφιξη καταγράφηκε!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("")
    if st.button("🔄 Αλλαγή Οχήματος / Σύνθεσης"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ (TABLE) ---
st.markdown("---")
if st.checkbox("📅 ΠΡΟΒΟΛΗ ΙΣΤΟΡΙΚΟΥ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
