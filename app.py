# ============================================================
# 📊 CYBER INTELLIGENCE DASHBOARD
# Descripción:
# Aplicación interactiva desarrollada en Streamlit para el análisis
# de amenazas de ciberseguridad, enfocada en impacto económico,
# tendencias temporales y eficiencia de defensa.
# ============================================================


# =========================
# 📦 IMPORTACIÓN DE LIBRERÍAS
# =========================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from streamlit_option_menu import option_menu

# =========================
# ⚙️ CONFIGURACIÓN INICIAL
# =========================
# Debe ser la primera instrucción de Streamlit

st.set_page_config(page_title="Cyber Intelligence Dashboard", layout="wide")

# =========================
# 🎨 ANIMACION INICIAL
# =========================

import time

def pantalla_carga():
    placeholder = st.empty()

    mensajes = [
        "Inicializando sistema...",
        "Cargando módulos de inteligencia...",
        "Conectando a base de datos...",
        "Analizando amenazas globales...",
        "Acceso concedido ✔"
    ]

    for msg in mensajes:
        placeholder.markdown(f"### 🟢 {msg}")
        time.sleep(0.9)

    placeholder.empty()

# Ejecutar una sola vez
if "loaded" not in st.session_state:
    pantalla_carga()
    st.session_state.loaded = True

# =========================
# 🎨 ESTILOS PERSONALIZADOS
# =========================
# Carga opcional de estilos externos para mejorar UI

try:
    from styles import aplicar_estilos_personalizados
    aplicar_estilos_personalizados()
except ImportError:
    pass

# =========================
# 🗄️ FUNCIÓN DE ACCESO A LA BASE DE DATOS
# =========================
def ejecutar_query(query):
    # Asegúrate de que la ruta 'data/ciberseguridad.db' sea correcta en tu PC
    conn = sqlite3.connect('data/ciberseguridad.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# =========================
# 📥 CARGA GLOBAL DE DATOS
# =========================
# Se realiza una carga inicial para evitar múltiples consultas repetidas
try:
    df_all = ejecutar_query("SELECT * FROM amenazas")
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    df_all = pd.DataFrame() 



# =========================
# ⚙️ BARRA LATERAL PROFESIONAL
# =========================
with st.sidebar:
    # Título del dashboard
    st.title("🚀 Cyber Intelligence")
    
    # Imagen opcional en la barra lateral (descomentar si tienes logo)
    # st.image("logo.png", use_column_width=True)

    st.markdown("---")  # Separador visual

    # Navegación con estilo pro
    menu = option_menu(
        menu_title=None,  # Sin título
        options=[
            "🏠 Inicio", 
            "📊 Resumen General", 
            "💰 Análisis de Costos", 
            "🌍 Análisis Geográfico", 
            "📈 Evolución Temporal", 
            "⚡ Eficiencia de Defensa", 
            "💡 Recomendaciones"
        ],
       
        menu_icon="cast",  # Icono general del menú
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#0a0f1c"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "left",
                "margin": "5px",
                "color": "#e6f1ff",
                "font-weight": "bold",
                "border-radius": "10px",
            },
            "nav-link-selected": {
                "background-color": "#00f2ff",
                "color": "black",
                "border-radius": "10px",
            },
        }
    )

    



# ============================================================
# 🏠 BLOQUE 1: INICIO
# ============================================================
if menu == "🏠 Inicio":
    st.markdown("""
<h1 style='color:#00f2ff; font-family: Orbitron;'>
🛡️ Analisis Estrategico De Ciberseguridad Global
</h1>
<p style='color:#00ffcc;'>Sistema de monitoreo avanzado de amenazas globales</p>
""", unsafe_allow_html=True)
    st.markdown("### *Un Enfoque Analítico para la Mitigación del Impacto Económico en Incidentes Digitales*")
    
    col1, col2 = st.columns([1.2, 0.8])
    with col1:
        # Verifica que 'portada.jpeg' esté en la misma carpeta
        try:
            st.image("portada.jpeg", caption="Análisis de Amenazas - Proyecto Integrador")
        except:
            st.warning("Imagen 'portada.jpeg' no encontrada.")
        
    with col2:
        st.subheader("Resumen Ejecutivo")
        st.write("""
        En la era de la transformación productiva, la ciberseguridad es una necesidad 
        fundamental para la estabilidad social y económica. Este proyecto analiza 
        una década de incidentes globales para proponer estrategias basadas en datos.
        """)
        st.info("💡 **Línea de Investigación:** Ciber-Resiliencia e Impacto Financiero.")

# ============================================================
# 📊 BLOQUE 2: RESUMEN GENERAL
# ============================================================
elif menu == "📊 Resumen General":
    st.markdown("# 📊 Inteligencia de Amenazas")
    st.write("Visión general del panorama de riesgo global y métricas críticas de impacto.")
    
    if not df_all.empty:
        # Contenedor de KPIs
        with st.container():
            c1, c2, c3 = st.columns(3)
            c1.metric("Impacto Económico", f"${df_all['financial_loss_in_million_'].sum():,.0f}M", "Global")
            c2.metric("Alcance de Víctimas", f"{df_all['number_of_affected_users'].sum():,}", "Usuarios")
            c3.metric("Frecuencia", len(df_all), "Eventos")

        st.divider()
        
        # Gráfico de Distribución por Industria
        fig_ind = px.bar(df_all.groupby('target_industry').size().reset_index(name='cuenta'), 
                         x='target_industry', y='cuenta', title="Frecuencia de Ataques por Sector Industrial",
                         labels={'target_industry': 'Sector', 'cuenta': 'Número de Incidentes'},
                         color='target_industry', template="plotly_dark")
        
        
        
        # Estilo neón para el gráfico
        fig_ind.update_traces(marker_line_color='#00f2ff', marker_line_width=1.5, opacity=0.8)
        st.plotly_chart(fig_ind, use_container_width=True)

        

        st.info("""
**🎯 Objetivo de este gráfico:** Identificar qué sectores industriales son los objetivos principales. 
Al analizar la frecuencia, podemos determinar dónde se concentra el mayor riesgo sistémico y 
priorizar las políticas de protección en las industrias más vulnerables.
""")

# -------- GLOSARIO DE ATAQUES --------
        # Explicación conceptual para usuarios no técnicos

        st.divider()
        st.subheader("🕵️ Glosario Técnico de Vectores de Ataque")
        st.write("Haga clic en cada categoría para entender la naturaleza de la amenaza analizada:")
        
        col_a, col_b = st.columns(2)

        with col_a:
            with st.expander("🌐 **DDoS (Distributed Denial of Service)**"):
                st.write("Inundación de servidores con tráfico masivo para interrumpir servicios críticos.")
            with st.expander("🦠 **Malware & Virus**"):
                st.write("Software hostil diseñado para infiltrarse, dañar o deshabilitar sistemas informáticos.")
            with st.expander("👥 **Man-in-the-Middle (MitM)**"):
                st.write("Intercepción secreta de comunicaciones entre dos partes para el robo de credenciales.")

        with col_b:
            with st.expander("🎣 **Phishing e Ingeniería Social**"):
                st.write("Uso de engaños psicológicos para obtener información confidencial de los usuarios.")
            with st.expander("🔒 **Ransomware**"):
                st.write("Secuestro de activos digitales mediante cifrado, exigiendo un rescate económico.")
            with st.expander("💉 **SQL Injection**"):
                st.write("Manipulación de bases de datos mediante la inserción de código malicioso en formularios.")
    
    else:
        st.warning("⚠️ No hay datos disponibles para mostrar el resumen.")


# ============================================================
# 💰 BLOQUE 3: ANÁLISIS DE COSTOS
# ============================================================
elif menu == "💰 Análisis de Costos":
    st.title("💰 Análisis de Impacto Financiero")
    df_costos = ejecutar_query("""
        SELECT target_industry, attack_type, ROUND(AVG(financial_loss_in_million_), 2) as perdida_promedio
        FROM amenazas GROUP BY 1, 2 ORDER BY perdida_promedio DESC
    """)
    fig_tree = px.treemap(df_costos, path=['target_industry', 'attack_type'], 
                          values='perdida_promedio', color='perdida_promedio', 
                          color_continuous_scale='RdBu', title="Jerarquía de Pérdidas por Sector")
    st.plotly_chart(fig_tree, use_container_width=True)

    # Información adicional debajo del gráfico
    st.markdown("""
### ¿Qué estamos viendo aquí?
Este gráfico muestra la **distribución del impacto económico** global causado por diferentes tipos de ataques de ciberseguridad, clasificados por **industria**. Los **bloques más grandes** indican combinaciones de sector y tipo de ataque con mayores pérdidas económicas.

- **Colores**: La escala de colores va de **amarillo a rojo**, donde el **rojo indica mayores pérdidas**.
- **Tamaño de los bloques**: El tamaño de cada bloque es proporcional al **impacto económico promedio** generado por ese tipo de ataque en ese sector.
""")

# ============================================================
# 🌍 BLOQUE 4: ANÁLISIS GEOGRÁFICO
# ============================================================

elif menu == "🌍 Análisis Geográfico":
    st.title("🌍 Comparativa Global por Países")

    df_map_anim = ejecutar_query("""
    SELECT 
        country,
        year,
        SUM(financial_loss_in_million_) as impacto
    FROM amenazas
    GROUP BY country, year
    ORDER BY year
    """)

    fig_anim = px.choropleth(
        df_map_anim,
        locations="country",
        locationmode="country names",
        color="impacto",
        hover_name="country",
        animation_frame="year",
        color_continuous_scale=["#0a0f1c", "#ff00c8", "#ff0000"],
        title="🌍 Simulación de Ataques Globales en el Tiempo"
    )

    fig_anim.update_layout(
        paper_bgcolor="#0a0f1c",
        plot_bgcolor="#0a0f1c",
        font=dict(color="#e6f1ff"),
        title_font=dict(size=22, color="#00f2ff")
    )

    st.plotly_chart(fig_anim, use_container_width=True)

    import random
    import time

    def live_feed(df):
        placeholder = st.empty()
        ataques = df.sample(min(20, len(df)))

        for _, row in ataques.iterrows():
            placeholder.markdown(f"""
            🔴 **ATAQUE DETECTADO**
            
            🌍 País: {row['country']}  
            📅 Año: {row['year']}  
            💰 Impacto: ${row['impacto']}M  
            """)
            time.sleep(0.9)

    st.subheader("📡 Feed de Ataques en Tiempo Real")
    live_feed(df_map_anim)

# ============================================================
# 📈 BLOQUE 5: EVOLUCIÓN TEMPORAL
# ============================================================
elif menu == "📈 Evolución Temporal":
    st.title("📈 Análisis de Tendencias Históricas")

    # Consulta
    df_trend = ejecutar_query("""
        SELECT year, attack_type, SUM(financial_loss_in_million_) as total_perdida 
        FROM amenazas 
        GROUP BY year, attack_type 
        ORDER BY year ASC
    """)

    # Filtro interactivo por tipo de ataque
    tipos = df_trend["attack_type"].unique()
    seleccion = st.multiselect("🎯 Filtrar tipo de ataque", tipos, default=tipos)
    df_filtrado = df_trend[df_trend["attack_type"].isin(seleccion)]

    # Gráfico con animación por año
    fig_area = px.area(
        df_filtrado,
        x="year",
        y="total_perdida",
        color="attack_type",
        template="plotly_dark",
        animation_frame="year",  # 🔥 Animación por año
        color_discrete_sequence=["#00f2ff", "#ff00c8", "#00ff88", "#ffaa00"],
        title="🌍 Evolución de los Ataques Cibernéticos"
    )

    # Línea total global (agregamos la línea total por año)
    df_total = df_filtrado.groupby("year")["total_perdida"].sum().reset_index()
    fig_area.add_scatter(
        x=df_total["year"],
        y=df_total["total_perdida"],
        mode="lines+markers",
        name="Total Global",
        line=dict(color="#ffffff", width=3, dash="dash")
    )

    # Pico de ataques (añadir anotación)
    max_row = df_total.loc[df_total["total_perdida"].idxmax()]
    fig_area.add_annotation(
        x=max_row["year"],
        y=max_row["total_perdida"],
        text="🚨 Pico de ataques",
        showarrow=True,
        arrowhead=2,
        font=dict(color="#ff4d4d", size=12)
    )

    # Estilo final para el gráfico (ambiente cyber)
    fig_area.update_layout(
        paper_bgcolor="#0a0f1c",
        plot_bgcolor="#0a0f1c",
        font=dict(color="#e6f1ff"),
        title_font=dict(size=22, color="#00f2ff"),
        hovermode="x unified",  # Mostrar detalles al pasar por encima
        showlegend=True,  # Mostrar leyenda de tipos de ataque
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[dict(label="Reproducir",
                          method="animate", args=[None, dict(frame=dict(duration=1000, redraw=True), fromcurrent=True)])]
        )]
    )

    # Mostrar gráfico interactivo
    st.plotly_chart(fig_area, use_container_width=True)

    # Análisis automático
    st.markdown("""
    🧠 **Análisis automático:**  
    Se observa una tendencia creciente en el impacto económico de los ciberataques, 
    con picos asociados a ataques de alta sofisticación como ransomware y exploits avanzados.
    """)


# ============================================================
# ⚡ BLOQUE 6: EFICIENCIA DE DEFENSA
# ============================================================
elif menu == "⚡ Eficiencia de Defensa":
    st.title("⚡ Análisis de Respuesta y Mitigación")
    df_ef = ejecutar_query("SELECT defense_mechanism_used, AVG(incident_resolution_time_in_hours) as tiempo_medio, AVG(financial_loss_in_million_) as perdida_media, COUNT(*) as frecuencia FROM amenazas GROUP BY 1")

    fig_scatter = px.scatter(df_ef, x="tiempo_medio", y="perdida_media", size="frecuencia", color="defense_mechanism_used", template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

    
    with st.expander("📝 ¿Cómo leer este gráfico de eficiencia?"):
        st.write("""
        Este gráfico correlaciona la velocidad de respuesta con el impacto financiero:
        - **Eje X (Tiempo):** Entre más a la izquierda, más rápida fue la defensa.
        - **Eje Y (Pérdida):** Entre más abajo, más efectiva fue la mitigación económica.
        """)

# ============================================================
# 💡 BLOQUE DE RECOMENDACIONES
# ============================================================
#
elif menu == "💡 Recomendaciones":
    st.title("💡 Hoja de Ruta Estratégica ")

    st.markdown("""
    Nuestro objetivo es ofrecer **estrategias claras y visuales** para mitigar riesgos,
    optimizar defensas y aumentar resiliencia.
    """)

    # =========================
    # Tarjetas de Recomendaciones
    # =========================
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color:#0a0f1c; padding:20px; border-radius:15px; text-align:center; box-shadow: 0px 0px 10px #00f2ff;">
            <h3 style="color:#00f2ff;">🛡️ Técnica</h3>
            <p style="color:#e6f1ff; font-size:14px;">
            Implementar IA y cifrado avanzado para detección temprana de amenazas.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background-color:#0a0f1c; padding:18px; border-radius:15px; text-align:center; box-shadow: 0px 0px 10px #ff00c8;">
            <h3 style="color:#ff00c8;">🏢 Organizacional</h3>
            <p style="color:#e6f1ff; font-size:14px;">
            Adoptar modelo Zero Trust y fomentar cultura de ciber-resiliencia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background-color:#0a0f1c; padding:20px; border-radius:15px; text-align:center; box-shadow: 0px 0px 10px #00ff9f;">
            <h3 style="color:#00ff9f;">🌐 Global</h3>
            <p style="color:#e6f1ff; font-size:14px;">
            Fomentar la resiliencia productiva a nivel nacional e internacional.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # Detalle interactivo
    # =========================
    st.markdown("---")
    with st.expander("📌 Ver Detalles de Implementación"):
        st.markdown("""
        - **Monitoreo 24/7**: Sistemas de alerta temprana y dashboards de control.
        - **Simulaciones de ataque**: Red Team & Blue Team para pruebas de resiliencia.
        - **Políticas de capacitación**: Entrenamiento continuo para equipos técnicos y usuarios.
        - **Revisión periódica de protocolos**: Ajuste de controles según evolución de amenazas.
        """)