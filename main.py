import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- ΣΧΕΔΙΑΣΜΟΣ SVG (Ρεαλιστικές Σιλουέτες Ευρωπαϊκών Φορτηγών) ---
# Φτιάχνουμε κώδικα για να σχεδιαστούν οι σιλουέτες ώστε να μην είναι emoji
tractor_svg = '<svg viewBox="0 0 24 24" fill="white" width="80"><path d="M20 18h-1c-1.1 0-2-.9-2-2V8c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v7c0 1.1.9 2 2 2H4c-1.1 0-2 .9-2 2h20l-2-3zM5 8h9v5H5V8z"/></svg>'
trailer_svg = '<svg viewBox="0 0 24 24" fill="white" width="100"><path d="M2 15h16v-5H2v5zm18-5v7h2v-7h-2zM2 17h16c0 1.1.9 2 2 2s2-.9 2-2H2z"/></svg>'
full_truck_svg = '<svg viewBox="0 0 24 24" fill="white" width="120"><path d="M2 16h2c0 1.1.9 2 2 2s2-.9 2-2h8c0 1.1.9 2 2 2s2-.9 2-2h2v-5H2v5zm0-6h14V5H2v5zm16 0h4v3h-4v-3z"/></svg>'

# --- CUSTOM CSS ΓΙΑ ΕΠΑΓΓΕΛΜΑΤΙΚΟ UI ---
st.markdown(f"""
    <style>
    .stApp {{
        background: #1a1a1a;
    }}
    /* Καλούπι για τα κουμπιά επιλογής */
    .config-box {{
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        margin-bottom: 10px;
    }}
    .config-box:hover {{
        border-color: #00d2ff;
        background: rgba(0, 210, 255, 0.05);
    }}
    /* Μεγάλα κουμπιά ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ */
    .action-btn button {{
        height: 120px !important;
        font-size: 22px !important;
        border-radius: 25px !important;
    }}
    h1, h2, h3, p {{ color: white !important; font-family: 'Inter', sans-serif; }}
    </style>
    """, unsafe_allow_html=True)

# --- ΔΗΜΙΟΥΡΓΙΑ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- ΕΛΕΓΧΟΣ ΚΑΤΑΣΤΑΣΗΣ ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'
if 'current_config' not in st.session_state:
    st.session_state.current_config = None

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΑΓΓΕΛΜΑΤΙΚΗ ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="config-box">{tractor_svg}</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ", key="btn1"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col2:
        st.markdown(f'<div class="config-box">{trailer_svg}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ", key="btn2"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col3:
        st.markdown(f'<div class="config-box">{full_truck_svg}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ", key="btn3"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΚΟΥΜΠΙΑ ΔΡΑΣΗΣ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### Ενεργή Μονάδα: {st.session_state.current_config}")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if st.button("🚀 ΞΕΚΙΝΗΣΑ", use_container_width=True, type="primary"):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("ΚΑΤΑΓΡΑΦΗΚΕ")

    with col_b:
        if st.button("🏁 ΕΦΤΑΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("ΚΑΤΑΓΡΑΦΗΚΕ")
        
    if st.button("🔄 ΑΛΛΑΓΗ ΣΥΝΘΕΣΗΣ"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΒΙΒΛΙΟ ΔΡΟΜΟΛΟΓΙΩΝ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
