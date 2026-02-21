import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- ΡΥΘΜΙΣΕΙΣ ΣΕΛΙΔΑΣ ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- CUSTOM CSS ΓΙΑ LIQUID GLASS & ΡΕΑΛΙΣΤΙΚΑ ΚΟΥΜΠΙΑ ---
# Εδώ ορίζουμε την εμφάνιση: Glassmorphism εφέ και στυλ για τις κάρτες επιλογής
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    }
    /* Στυλ για την κάρτα επιλογής σύνθεσης */
    .config-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: 0.3s;
        cursor: pointer;
        text-align: center;
    }
    .config-card:hover {
        border-color: #00d2ff;
        background: rgba(255, 255, 255, 0.15);
    }
    /* Στυλ για τα μεγάλα κουμπιά ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ */
    .stButton>button {
        border-radius: 20px;
        font-weight: bold;
        transition: 0.3s;
    }
    h1, h2, h3, p, label { color: white !important; font-family: 'Segoe UI', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- ΔΙΑΧΕΙΡΙΣΗ ΒΑΣΗΣ ΔΕΔΟΜΕΝΩΝ ---
# Δημιουργούμε τον πίνακα αν δεν υπάρχει για να αποθηκεύουμε τις κινήσεις
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movements 
                 (id INTEGER PRIMARY KEY, timestamp TEXT, action TEXT, config TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- ΕΙΚΟΝΕΣ ΦΟΡΤΗΓΩΝ (ΕΥΡΩΠΑΪΚΑ FLAT-NOSE) ---
# Χρησιμοποιούμε σταθερά URLs για ρεαλιστικά εικονίδια
IMG_TRACTOR = "https://img.icons8.com/external-flatart-icons-flat-flatarticons/100/external-truck-transportation-flatart-icons-flat-flatarticons-1.png"
IMG_TRAILER = "https://img.icons8.com/external-flatart-icons-flat-flatarticons/100/external-trailer-transportation-flatart-icons-flat-flatarticons.png"
IMG_CONTAINER = "https://img.icons8.com/external-flatart-icons-flat-flatarticons/100/external-container-shipping-and-delivery-flatart-icons-flat-flatarticons.png"

# --- ΕΛΕΓΧΟΣ ΚΑΤΑΣΤΑΣΗΣ ΕΦΑΡΜΟΓΗΣ (STATE) ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'select_config'
if 'current_config' not in st.session_state:
    st.session_state.current_config = None

st.title("🚛 LogiWork Pass")

# --- ΟΘΟΝΗ 1: ΕΠΙΛΟΓΗ ΣΥΝΘΕΣΗΣ (VISUAL SELECTOR) ---
if st.session_state.stage == 'select_config':
    st.subheader("Επιλογή Σύνθεσης Πρωινού")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image(IMG_TRACTOR, width=80)
        if st.button("Σκέτος\nΤράκτορας"):
            st.session_state.current_config = "Σκέτος Τράκτορας"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col2:
        # Εδώ δείχνουμε τράκτορα + άδεια νταλίκα
        st.image(IMG_TRAILER, width=80)
        if st.button("Τράκτορας +\nΝταλίκα"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα"
            st.session_state.stage = 'actions'
            st.rerun()
            
    with col3:
        # Εδώ δείχνουμε την πλήρη σύνθεση με κοντέινερ
        st.image(IMG_CONTAINER, width=80)
        if st.button("Τράκτορας +\nΝταλίκα + Κουτί"):
            st.session_state.current_config = "Τράκτορας + Νταλίκα + Κουτί"
            st.session_state.stage = 'actions'
            st.rerun()

# --- ΟΘΟΝΗ 2: ΚΟΥΜΠΙΑ ΔΡΑΣΗΣ (ΞΕΚΙΝΗΣΑ / ΕΦΤΑΣΑ) ---
elif st.session_state.stage == 'actions':
    st.info(f"Ενεργή Σύνθεση: **{st.session_state.current_config}**")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # Κουμπί Έναρξης με πράσινο χρώμα μέσω CSS logic (προσομοίωση)
        if st.button("🚀 ΞΕΚΙΝΗΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΞΕΚΙΝΗΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.success("Η έναρξη καταγράφηκε!")

    with col_b:
        # Κουμπί Άφιξης
        if st.button("🏁 ΕΦΤΑΣΑ", use_container_width=True):
            conn = sqlite3.connect('logiwork.db')
            c = conn.cursor()
            now = datetime.now().strftime("%d/%m/%Y %H:%M")
            c.execute("INSERT INTO movements (timestamp, action, config) VALUES (?, ?, ?)", 
                      (now, "ΕΦΤΑΣΑ", st.session_state.current_config))
            conn.commit()
            conn.close()
            st.warning("Η άφιξη καταγράφηκε!")
            
    # Κουμπί για επιστροφή στην αρχική επιλογή αν αλλάξει κάτι στο δρομολόγιο
    if st.button("🔄 Αλλαγή Σύνθεσης"):
        st.session_state.stage = 'select_config'
        st.rerun()

# --- ΙΣΤΟΡΙΚΟ (ΒΙΒΛΙΟ ΔΡΟΜΟΛΟΓΙΩΝ) ---
st.markdown("---")
if st.checkbox("📅 Προβολή Ιστορικού"):
    conn = sqlite3.connect('logiwork.db')
    df = pd.read_sql_query("SELECT timestamp as 'Ώρα', action as 'Ενέργεια', config as 'Σύνθεση' FROM movements ORDER BY id DESC", conn)
    st.table(df) # Χρησιμοποιούμε table για πιο καθαρή εμφάνιση σε κινητό
    conn.close()
