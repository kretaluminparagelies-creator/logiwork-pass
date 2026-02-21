import streamlit as st
import sqlite3
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="LogiWork Pass", layout="centered")

# --- LIQUID GLASS STYLING ---
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
    }
    .stButton>button {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 15px;
        color: white;
        height: 100px;
        width: 100%;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    .stButton>button:hover {
        border: 1px solid #00d2ff;
        color: #00d2ff;
    }
    h1 {
        color: white;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('logiwork.db')
    c = conn.cursor()
    # Πίνακας Κινήσεων
    c.execute('''CREATE TABLE IF NOT EXISTS movements 
                 (id INTEGER PRIMARY KEY, 
                  timestamp TEXT, 
                  action TEXT, 
                  location TEXT)''')
    conn.commit()
    conn.close()

init_db()

# --- APP INTERFACE ---
st.title("🚛 LogiWork Pass")
st.markdown("### MVP Driver-Only")

col1, col2 = st.columns(2)

with col1:
    if st.button("🚀\nΞΕΚΙΝΗΣΑ"):
        conn = sqlite3.connect('logiwork.db')
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO movements (timestamp, action, location) VALUES (?, ?, ?)", 
                  (now, "ΞΕΚΙΝΗΣΑ", "Αφετηρία"))
        conn.commit()
        conn.close()
        st.success("Η κίνηση καταγράφηκε!")

with col2:
    if st.button("🏁\nΕΦΤΑΣΑ"):
        conn = sqlite3.connect('logiwork.db')
        c = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO movements (timestamp, action, location) VALUES (?, ?, ?)", 
                  (now, "ΕΦΤΑΣΑ", "Προορισμός"))
        conn.commit()
        conn.close()
        st.info("Η άφιξη καταγράφηκε!")

st.markdown("---")
if st.checkbox("Εμφάνιση Ιστορικού"):
    conn = sqlite3.connect('logiwork.db')
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM movements ORDER BY id DESC", conn)
    st.write(df)
    conn.close()
