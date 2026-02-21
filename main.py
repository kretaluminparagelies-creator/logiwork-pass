import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- [CHECKPOINT 23: BOOTSTRAP ICON SYSTEM] ---
# Στάδιο: Χρήση εξωτερικής βιβλιοθήκης εικονιδίων (Bootstrap) για εγγυημένη εμφάνιση.

st.set_page_config(page_title="LogiWork Pass", layout="centered")

# Εισαγωγή της βιβλιοθήκης εικονιδίων Bootstrap μέσω HTML
st.markdown('<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">', unsafe_allow_html=True)

# --- CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ UI ---
st.markdown("""
    <style>
    .stApp { background-color: #111827; }
    
    /* Το κουτί που περιέχει το εικονίδιο */
    .icon-box {
        background: #1f2937;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        border: 2px solid #374151;
        margin-bottom: 10px;
        color: #60a5fa;
    }
    
    /* Μέγεθος εικονιδίων */
    .icon-box i {
        font-size: 60px;
    }
    
    /* Στυλ κουμπιών */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-weight: bold;
    }
    
    .action-start button { background: #059669 !important; height: 100px !important; font-size: 22px !important; }
    .action-stop button { background: #dc2626 !important; height: 100px !important; font-size: 22px !important; }
    
    h1, h2, h3 { color: white !important; text-align: center; }
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

# --- APP LOGIC ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.title("🚜 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΤΙ ΟΔΗΓΕΙΣ ΤΩΡΑ;")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Εικονίδιο για Σκέτο Τράκτορα (Truck Front)
        st.markdown('<div class="icon-box"><i class="bi bi-truck-flatbed"></i></div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with col2:
        # Εικονίδιο για Τράκτορα + Νταλίκα (Truck Profile)
        st.markdown('<div class="icon-box"><i class="bi bi-truck"></i></div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with col3:
        # Εικονίδιο για Τράκτορα + Κουτί (Box/Frontier)
        st.markdown('<div class="icon-box"><i class="bi bi-archive-fill"></i></div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΔΡΑΣΗ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### ΕΠΙΛΟΓΗ: **{st.session_state.current_config}**")
    
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
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ!")
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
            st.info("ΚΑΤΑΓΡΑΦΗΚΕ!")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 ΑΛΛΑΓΗ ΟΧΗΜΑΤΟΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΒΙΒΛΙΟ ΔΡΟΜΟΛΟΓΙΩΝ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.table(df)
    conn.close()
