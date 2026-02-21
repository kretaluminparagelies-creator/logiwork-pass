import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- ΣΧΕΔΙΑΣΜΟΣ ΡΕΑΛΙΣΤΙΚΩΝ ΕΙΚΟΝΙΔΙΩΝ (SVG) ---
# Σχεδιάζουμε τον ευρωπαϊκό τράκτορα, την πλατφόρμα και το κοντέινερ με κώδικα
# για να μην εξαρτόμαστε από εξωτερικά sites και να φαίνονται σωστά.

# 1. Ευρωπαϊκός Τράκτορας (Flat-nose)
tractor_svg = '''<svg viewBox="0 0 100 50" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="10" y="10" width="30" height="30" rx="2" fill="#00D2FF"/>
<rect x="40" y="30" width="10" height="10" fill="#00D2FF"/>
<circle cx="18" cy="42" r="5" fill="white"/>
<circle cx="35" cy="42" r="5" fill="white"/>
<rect x="15" y="15" width="15" height="10" fill="#1a1a1a"/>
</svg>'''

# 2. Τράκτορας με Άδεια Νταλίκα (Πλατφόρμα)
trailer_svg = '''<svg viewBox="0 0 100 50" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="5" y="15" width="25" height="25" rx="2" fill="#00D2FF"/>
<rect x="30" y="32" width="60" height="5" fill="silver"/>
<circle cx="12" cy="42" r="4" fill="white"/>
<circle cx="23" cy="42" r="4" fill="white"/>
<circle cx="75" cy="42" r="4" fill="white"/>
<circle cx="85" cy="42" r="4" fill="white"/>
</svg>'''

# 3. Τράκτορας με Νταλίκα και Κοντέινερ (Κουτί)
full_svg = '''<svg viewBox="0 0 100 50" fill="none" xmlns="http://www.w3.org/2000/svg">
<rect x="5" y="15" width="25" height="25" rx="2" fill="#00D2FF"/>
<rect x="30" y="32" width="60" height="5" fill="silver"/>
<rect x="35" y="12" width="55" height="20" rx="1" fill="#FF4B4B"/>
<path d="M40 12V32M45 12V32M50 12V32" stroke="rgba(255,255,255,0.3)"/>
<circle cx="12" cy="42" r="4" fill="white"/>
<circle cx="75" cy="42" r="4" fill="white"/>
<circle cx="85" cy="42" r="4" fill="white"/>
</svg>'''

# --- ΕΜΦΑΝΙΣΗ (CSS) ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; }
    .card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    h1, h2, h3 { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ ---
def init_db():
    # Δημιουργία σύνδεσης με το αρχείο logiwork.db
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Πίνακας για τις κινήσεις (Ώρα, Τι έκανα, Ποιο όχημα)
    c.execute('CREATE TABLE IF NOT EXISTS movements (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- ΕΛΕΓΧΟΣ ΣΤΑΔΙΟΥ (STATE) ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ ---
if st.session_state.stage == 'select_config':
    st.subheader("Τι οδηγείς τώρα;")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown(f'<div class="card">{tractor_svg}</div>', unsafe_allow_html=True)
        if st.button("ΣΚΕΤΟΣ\nΤΡΑΚΤΟΡΑΣ"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()

    with c2:
        st.markdown(f'<div class="card">{trailer_svg}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΝΤΑΛΙΚΑ"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()

    with c3:
        st.markdown(f'<div class="card">{full_svg}</div>', unsafe_allow_html=True)
        if st.button("ΤΡΑΚΤΟΡΑΣ\n+\nΚΟΥΤΙ"):
            st.session_state.current_config = "Τράκτορας + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΚΟΥΜΠΙΑ ΔΡΑΣΗΣ ---
elif st.session_state.stage == 'actions':
    st.markdown(f"### Επιλογή: {st.session_state.current_config}")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Κουμπί για έναρξη δρομολογίου
        if st.button("🚀 ΞΕΚΙΝΗΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("Έναρξη!")

    with col_b:
        # Κουμπί για ολοκλήρωση
        if st.button("🏁 ΕΦΤΑΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.info("Άφιξη!")
        
    if st.button("🔄 Αλλαγή Οχήματος"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ ---
st.markdown("---")
if st.checkbox("📅 ΒΙΒΛΙΟ ΔΡΟΜΟΛΟΓΙΩΝ"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.dataframe(df, use_container_width=True)
    conn.close()
