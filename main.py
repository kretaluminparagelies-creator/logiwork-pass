import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- [CHECKPOINT 21: FINAL RECTIFICATION] ---
# Στάδιο: Οριστική διόρθωση εμφάνισης με επαγγελματικά εικονίδια

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- ΕΠΑΓΓΕΛΜΑΤΙΚΟ UI (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    /* Κάρτα για την εικόνα */
    .img-box {
        background: #1f2937;
        border-radius: 20px;
        padding: 10px;
        border: 2px solid #374151;
        margin-bottom: 10px;
        display: flex;
        justify-content: center;
    }
    /* Κουμπιά Επιλογής */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 55px;
        font-weight: bold;
        text-transform: uppercase;
    }
    /* Κουμπιά Δράσης */
    .action-start button { background-color: #10b981 !important; height: 90px !important; font-size: 20px !important; }
    .action-stop button { background-color: #ef4444 !important; height: 90px !important; font-size: 20px !important; }
    h1, h2, h3, p { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- ΕΓΓΥΗΜΕΝΑ ΕΠΑΓΓΕΛΜΑΤΙΚΑ ΕΙΚΟΝΙΔΙΑ ---
# Χρήση σταθερών πηγών για Ευρωπαϊκά Φορτηγά
IMG_TRACTOR = "https://img.icons8.com/external-flat-icons-inmotus-design/200/external-Tractor-truck-flat-icons-inmotus-design.png"
IMG_TRAILER = "https://img.icons8.com/external-flat-icons-inmotus-design/200/external-Trailer-truck-flat-icons-inmotus-design.png"
IMG_FULL = "https://img.icons8.com/external-flat-icons-inmotus-design/200/external-Container-truck-flat-icons-inmotus-design.png"

# --- ΕΛΕΓΧΟΣ ΡΟΗΣ ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΤΙ ΟΔΗΓΕΙΣ ΤΩΡΑ;")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="img-box">', unsafe_allow_html=True)
        st.image(IMG_TRACTOR, width=120)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with col2:
        st.markdown('<div class="img-box">', unsafe_allow_html=True)
        st.image(IMG_TRAILER, width=120)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with col3:
        st.markdown('<div class="img-box">', unsafe_allow_html=True)
        st.image(IMG_FULL, width=120)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΔΡΑΣΗ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### ΣΥΝΘΕΣΗ: **{st.session_state.current_config}**")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="action-start">', unsafe_allow_html=True)
        if st.button("ΞΕΚΙΝΗΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.toast("ΚΑΤΑΓΡΑΦΗΚΕ!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="action-stop">', unsafe_allow_html=True)
        if st.button("ΕΦΤΑΣΑ"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.toast("ΚΑΤΑΓΡΑΦΗΚΕ!")
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 ΑΛΛΑΓΗ ΟΧΗΜΑΤΟΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΠΡΟΒΟΛΗ ΒΙΒΛΙΟΥ ΔΡΟΜΟΛΟΓΙΩΝ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
