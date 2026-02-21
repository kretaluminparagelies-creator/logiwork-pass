import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- [CHECKPOINT 26: BULLETPROOF UI] ---
# Στάδιο: Κατάργηση κάθε γραφικού. Χρήση μόνο Full-Width κουμπιών για 100% λειτουργικότητα.

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ ΚΑΙ ΣΤΑΘΕΡΟ UI ---
st.markdown("""
    <style>
    /* Σκούρο επαγγελματικό φόντο */
    .stApp { background-color: #000000; }
    
    /* Τίτλος Εφαρμογής */
    .app-header {
        color: #00d2ff;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        padding: 20px;
        border-bottom: 1px solid #333;
        margin-bottom: 30px;
    }

    /* Στυλ για τα κουμπιά επιλογής (Τράκτορας κτλ) */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        margin-bottom: 15px !important;
        background-color: #1a1a1a !important;
        color: white !important;
        border: 2px solid #444 !important;
    }
    
    /* Χρώμα όταν επιλεγεί κάτι */
    div.stButton > button:active, div.stButton > button:focus {
        border-color: #00d2ff !important;
        color: #00d2ff !important;
    }

    /* Κουμπιά Δράσης (ΞΕΚΙΝΗΣΑ - Πράσινο / ΕΦΤΑΣΑ - Κόκκινο) */
    .btn-green button {
        background-color: #006400 !important;
        border: none !important;
        height: 120px !important;
        font-size: 26px !important;
    }
    .btn-red button {
        background-color: #8B0000 !important;
        border: none !important;
        height: 120px !important;
        font-size: 26px !important;
    }
    
    h1, h2, h3, p { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ (SQLite) ---
def init_db():
    # Δημιουργούμε τη βάση δεδομένων logiwork.db αν δεν υπάρχει
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Πίνακας movements: Καταγράφει πότε, τι έγινε και με ποιο όχημα
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- APP STATE ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.markdown('<div class="app-header">LOGIWORK PASS v1.0</div>', unsafe_allow_html=True)

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΟΧΗΜΑΤΟΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΒΗΜΑ 1: ΕΠΙΛΕΞΤΕ ΟΧΗΜΑ")
    
    # Μεγάλα κουμπιά - Ένα σε κάθε σειρά για ευκολία στο κινητό
    if st.button("1. ΣΚΕΤΟΣ ΤΡΑΚΤΟΡΑΣ"):
        st.session_state.current_config = "Σκέτος Τράκτορας"
        st.session_state.stage = 'actions'
        st.rerun()

    if st.button("2. ΤΡΑΚΤΟΡΑΣ + ΝΤΑΛΙΚΑ"):
        st.session_state.current_config = "Τράκτορας + Νταλίκα"
        st.session_state.stage = 'actions'
        st.rerun()

    if st.button("3. ΤΡΑΚΤΟΡΑΣ + ΚΟΥΤΙ (Full)"):
        st.session_state.current_config = "Τράκτορας + Κουτί"
        st.session_state.stage = 'actions'
        st.rerun()

# --- ΟΘΟΝΗ 2: ΚΑΤΑΓΡΑΦΗ ΚΙΝΗΣΗΣ ---
elif st.session_state.stage == 'actions':
    st.subheader(f"ΟΧΗΜΑ: {st.session_state.current_config}")
    
    # Δύο μεγάλα κουμπιά δίπλα-δίπλα
    col_start, col_end = st.columns(2)
    
    with col_start:
        st.markdown('<div class="btn-green">', unsafe_allow_html=True)
        if st.button("ΞΕΚΙΝΗΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%H:%M - %d/%m/%Y")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΝΑΡΞΗ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_end:
        st.markdown('<div class="btn-red">', unsafe_allow_html=True)
        if st.button("ΕΦΤΑΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%H:%M - %d/%m/%Y")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΑΦΙΞΗ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.error("ΚΑΤΑΓΡΑΦΗΚΕ")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.write("---")
    if st.button("🔄 ΑΛΛΑΓΗ ΕΠΙΛΟΓΗΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ΔΡΟΜΟΛΟΓΙΩΝ ---
st.write("")
if st.checkbox("🔍 ΕΜΦΑΝΙΣΗ ΙΣΤΟΡΙΚΟΥ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα/Ημερ.', action as 'Ενέργεια', config as 'Όχημα' FROM movements ORDER BY id DESC", conn)
    st.table(df) # Το table είναι πιο σταθερό οπτικά από το dataframe
    conn.close()
