import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CUSTOM CSS ΓΙΑ LIQUID GLASS & ΜΕΓΑΛΑ ΕΙΚΟΝΙΔΙΑ ---
# Εδώ φτιάχνουμε την αισθητική για να φαίνονται όλα "πλούσια" και επαγγελματικά
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #12100E 0%, #2B4162 100%);
    }
    /* Στυλ για τα κουμπιά επιλογής σύνθεσης */
    div.stButton > button:first-child {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        height: 180px;
        width: 100%;
        border-radius: 20px;
        font-size: 18px;
        backdrop-filter: blur(10px);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #00d2ff;
        background-color: rgba(0, 210, 255, 0.1);
        box-shadow: 0 0 20px rgba(0, 210, 255, 0.2);
    }
    /* Ειδικό στυλ για τα κουμπιά ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ */
    .action-btn-start button {
        background-color: rgba(46, 204, 113, 0.2) !important;
        border: 2px solid #2ecc71 !important;
        height: 120px !important;
        font-size: 24px !important;
    }
    .action-btn-stop button {
        background-color: rgba(231, 76, 60, 0.2) !important;
        border: 2px solid #e74c3c !important;
        height: 120px !important;
        font-size: 24px !important;
    }
    h1, h2, h3, p { color: white !important; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
# Καταγραφή των κινήσεων στην SQLite
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movements 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- ΕΛΕΓΧΟΣ ΚΑΤΑΣΤΑΣΗΣ (STATE) ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'
if 'current_config' not in st.session_state:
    st.session_state.current_config = None

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("Ποια είναι η σύνθεσή σου τώρα;")
    
    # Χρησιμοποιούμε Columns για να είναι δίπλα-δίπλα
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Επιλογή 1: Σκέτος Τράκτορας
        if st.button("🚜\n\nΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col2:
        # Επιλογή 2: Τράκτορας + Νταλίκα
        if st.button("🚛\n\nΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col3:
        # Επιλογή 3: Πλήρης σύνθεση
        if st.button("📦\n\nΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΚΟΥΜΠΙΑ ΔΡΑΣΗΣ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### Σύνθεση: {st.session_state.current_config}")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="action-btn-start">', unsafe_allow_html=True)
        if st.button("ΞΕΚΙΝΗΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("Καταγράφηκε!")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="action-btn-stop">', unsafe_allow_html=True)
        if st.button("ΕΦΤΑΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("Καταγράφηκε!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 Αλλαγή Σύνθεσης"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 Προβολή Βιβλίου Δρομολογίων"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
