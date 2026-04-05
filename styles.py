def aplicar_estilos_personalizados():
    import streamlit as st

    st.markdown("""
    <style>
    /* ===== FONDO GENERAL ===== */
    .stApp {
        background-color: #0a0f1c;
        color: #e6f1ff;
        font-family: 'Roboto', sans-serif;
    }

    /* ===== IMPORTAR FUENTES ===== */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Roboto:wght@300;400;500&display=swap');

    /* ===== TÍTULOS ===== */
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        letter-spacing: 1px;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background-color: #050a14;
        border-right: 1px solid #00f2ff33;
    }

    /* ===== BOTONES ===== */
    .stButton>button {
        background-color: #00f2ff;
        color: black;
        border-radius: 8px;
        border: none;
    }

    .stButton>button:hover {
        background-color: #00c8cc;
        color: white;
    }

    /* ===== MÉTRICAS (KPIs) ===== */
    div[data-testid="stMetric"] {
        background-color: #111827;
        border: 1px solid #00f2ff55;
        padding: 15px;
        border-radius: 10px;
    }

    /* ===== EXPANDERS ===== */
    .streamlit-expanderHeader {
        color: #00ffcc;
        font-weight: bold;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-thumb {
        background: #00f2ff;
        border-radius: 10px;
    }

    </style>
    """, unsafe_allow_html=True)