import streamlit as st

def aplicar_estilos_personalizados():
    st.markdown("""
        <style>
        /* 1. Fuentes e Importaciones */
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

        /* 2. Fondo con Gradiente Dinámico */
        .stApp {
            background: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #0f0f1b 100%);
            color: #00f2ff;
            font-family: 'Rajdhani', sans-serif;
        }

        /* 3. Títulos Cyber-Punk */
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #00f2ff !important;
            text-shadow: 2px 2px 10px rgba(0, 242, 255, 0.5), -2px -2px 10px rgba(255, 0, 255, 0.3);
            text-transform: uppercase;
            letter-spacing: 4px;
        }

        /* 4. Tarjetas con Efecto Cristal */
        div[data-testid="stMetric"], .stPlotlyChart {
            background: rgba(26, 26, 46, 0.6) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(0, 242, 255, 0.3) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
            transition: all 0.4s ease;
        }

        div[data-testid="stMetric"]:hover {
            border: 1px solid #ff00ff !important;
            box-shadow: 0 0 25px rgba(255, 0, 255, 0.4);
            transform: scale(1.03);
        }

        /* 5. Sidebar Cyber-Grid */
        [data-testid="stSidebar"] {
            background-color: #0a0a12 !important;
            border-right: 2px solid #00f2ff;
        }

        /* 6. Tabs Futuristas */
        button[data-baseweb="tab"] {
            color: #00f2ff !important;
            font-family: 'Orbitron', sans-serif;
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            border-bottom: 3px solid #ff00ff !important;
            background: rgba(255, 0, 255, 0.1) !important;
        }

                /* 9. Estilo para TABLAS y DATAFRAMES (Data Terminal Look) */
        .stTable, [data-testid="stTable"] {
            background-color: rgba(10, 10, 20, 0.95) !important;
            border: 2px solid #00f2ff !important;
            border-radius: 10px !important;
            color: #ffffff !important;
        }

        /* Color de las celdas y cabeceras */
        .stTable td, .stTable th {
            color: #ffffff !important;
            border-bottom: 1px solid rgba(0, 242, 255, 0.2) !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-size: 1.1rem !important;
        }

        .stTable th {
            background-color: rgba(0, 242, 255, 0.1) !important;
            color: #ff00ff !important; /* Cabeceras en Magenta */
            text-transform: uppercase;
        }

        /* Si usas st.dataframe en lugar de st.table */
        [data-testid="stDataFrame"] {
            background-color: #0f0f1b !important;
            border: 1px solid #00f2ff !important;
        }
                
        </style>
        """, unsafe_allow_html=True) # <-- Aquí era donde faltaba el cierre correcto