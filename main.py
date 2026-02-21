import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- [CHECKPOINT 24: SOLID TEXT-BASED UI] ---
# Στάδιο: Κατάργηση όλων των εξωτερικών αρχείων. Χρήση καθαρού κειμένου και χρωμάτων.

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΑ ΚΟΥΜΠΙΑ ΧΩΡΙΣ ΕΙΚΟΝΕΣ ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* Μεγάλα τετράγωνα κουμπιά επιλογής */
    .truck-box {
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #1f2937;
        border: 3px solid #3b82f6;
        border-radius: 20px;
        color: white;
        font-size: 50px;
        margin-bottom: 10px;
    }
    
    /* Κουμπιά Δράσης */
    .action-btn-start button {
        background-color: #059669 !important;
        height: 120px !important;
        font-size: 25px !important;
        border-radius: 25px !important;
        color: white !important;
    }
    .action-btn-stop button {
        background-color: #dc2626 !important;
        height: 120px !important;
        font-size: 25px !important;
        border-radius: 25px !important;
        color: white !important;
    }
    
    h1, h2, h3, p { color: white !important; text-align: center; font-family: 'Arial'; }
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

st.title("🚜 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΤΙ ΟΔΗΓΕΙΣ ΤΩΡΑ;")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Οπτικό πλαίσιο για Τράκτορα
        st.markdown('<div class="truck-box">🚜</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with col2:
        # Οπτικό πλαίσιο για Τράκτορα + Νταλίκα
        st.markdown('<div class="truck-box">🚛</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with col3:
        # Οπτικό πλαίσιο για Τράκτορα + Κουτί
        st.markdown('<div class="truck-box">📦</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΔΡΑΣΗ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### ΕΠΙΛΟΓΗ: **{st.session_state.current_config}**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="action-btn-start">', unsafe_allow_html=True)
        if st.button("🚀 ΞΕΚΙΝΗΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="action-btn-stop">', unsafe_allow_html=True)
        if st.button("🏁 ΕΦΤΑΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("ΚΑΤΑΓΡΑΦΗΚΕ!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 ΑΛΛΑΓΗ ΟΧΗΜΑΤΟΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΒΙΒΛΙΟ ΔΡΟΜΟΛΟΓΙΩΝ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
