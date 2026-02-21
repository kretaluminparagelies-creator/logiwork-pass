import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- [CHECKPOINT 25: MANUAL HTML INTERFACE] ---
# Στάδιο: Πλήρης κατάργηση εικονιδίων. Χρήση χειροκίνητου HTML για 100% αξιοπιστία.

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΚΑΙ ΣΤΑΘΕΡΟ UI ---
st.markdown("""
    <style>
    /* Φόντο εφαρμογής */
    .stApp { background-color: #050505; }
    
    /* Τίτλος */
    .main-title {
        color: #ffffff;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        padding: 20px;
        border-bottom: 2px solid #333;
    }

    /* Στυλ για τα μεγάλα κουμπιά επιλογής */
    .stButton > button {
        background-color: #1a1a1a !important;
        color: #00d2ff !important;
        border: 2px solid #00d2ff !important;
        border-radius: 15px !important;
        height: 120px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
        text-transform: uppercase;
    }
    
    /* Hover εφέ */
    .stButton > button:hover {
        background-color: #00d2ff !important;
        color: #000000 !important;
    }

    /* Κουμπιά Δράσης (ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ) */
    .action-start button {
        background-color: #008000 !important;
        border: none !important;
        color: white !important;
        height: 100px !important;
    }
    .action-stop button {
        background-color: #8B0000 !important;
        border: none !important;
        color: white !important;
        height: 100px !important;
    }
    
    h1, h2, h3 { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΙΑΧΕΙΡΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    # Δημιουργία αρχείου βάσης δεδομένων
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Στήλες: ID, Ημερομηνία/Ώρα, Ενέργεια, Τύπος Φορτηγού
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- ΕΛΕΓΧΟΣ ΚΑΤΑΣΤΑΣΗΣ ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.markdown('<h1 class="main-title">LOGIWORK PASS</h1>', unsafe_allow_html=True)

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΕΠΙΛΕΞΤΕ ΣΥΝΘΕΣΗ")
    
    # Επιλογή 1: Σκέτος Τράκτορας
    if st.button("🚛 ΣΚΕΤΟΣ ΤΡΑΚΤΟΡΑΣ"):
        st.session_state.current_config = "Σκέτος Τράκτορας"
        st.session_state.stage = 'actions'
        st.rerun()

    # Επιλογή 2: Τράκτορας + Νταλίκα
    if st.button("🚚 ΤΡΑΚΤΟΡΑΣ + ΝΤΑΛΙΚΑ"):
        st.session_state.current_config = "Τράκτορας + Νταλίκα"
        st.session_state.stage = 'actions'
        st.rerun()

    # Επιλογή 3: Τράκτορας + Κουτί
    if st.button("📦 ΤΡΑΚΤΟΡΑΣ + ΚΟΥΤΙ"):
        st.session_state.current_config = "Τράκτορας + Κουτί"
        st.session_state.stage = 'actions'
        st.rerun()

# --- ΟΘΟΝΗ 2: ΚΟΥΜΠΙΑ ΔΡΑΣΗΣ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### ΤΩΡΑ: {st.session_state.current_config}")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown('<div class="action-start">', unsafe_allow_html=True)
        if st.button("ΞΕΚΙΝΗΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="action-stop">', unsafe_allow_html=True)
        if st.button("ΕΦΤΑΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 ΑΛΛΑΓΗ ΣΥΝΘΕΣΗΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("ΠΡΟΒΟΛΗ ΙΣΤΟΡΙΚΟΥ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.table(df)
    conn.close()
