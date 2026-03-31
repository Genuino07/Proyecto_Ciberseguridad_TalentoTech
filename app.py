import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Configuración de página (Debe ser lo primero)
st.set_page_config(page_title="Cyber Intelligence Dashboard", layout="wide")

# Intentar importar estilos (si el archivo styles.py existe)
try:
    from styles import aplicar_estilos_personalizados
    aplicar_estilos_personalizados()
except ImportError:
    pass

# 2. Función de conexión a la base de datos
def ejecutar_query(query):
    # Asegúrate de que la ruta 'data/ciberseguridad.db' sea correcta en tu PC
    conn = sqlite3.connect('data/ciberseguridad.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- CARGA GLOBAL DE DATOS ---
try:
    df_all = ejecutar_query("SELECT * FROM amenazas")
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    df_all = pd.DataFrame() 

# 3. BARRA LATERAL (SIDEBAR)
st.sidebar.header("Navegación del Proyecto")
menu = st.sidebar.radio(
    "Seleccione una sección:",
    [
        "🏠 Inicio", 
        "📊 Resumen General", 
        "💰 Análisis de Costos", 
        "🌍 Análisis Geográfico", 
        "📈 Evolución Temporal", 
        "⚡ Eficiencia de Defensa", 
        "💡 Recomendaciones"
    ]
)

# --- BLOQUE: INICIO ---
if menu == "🏠 Inicio":
    st.title("🛡️ Inteligencia de Amenazas y Visualización Geoespacial")
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

# --- BLOQUE: RESUMEN GENERAL ---
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

        # --- RE-ESTABLECIENDO EL DICCIONARIO DE ATAQUES ---
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

# --- BLOQUE: ANÁLISIS DE COSTOS ---
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

# --- BLOQUE: ANÁLISIS GEOGRÁFICO ---
elif menu == "🌍 Análisis Geográfico":
    st.title("🌍 Comparativa Global por Países")
    df_pais = ejecutar_query("SELECT country, SUM(financial_loss_in_million_) as perdida_total, AVG(incident_resolution_time_in_hours) as tiempo_avg FROM amenazas GROUP BY country")
    
    fig_mapa = px.choropleth(df_pais, locations="country", locationmode='country names',
                             color="perdida_total", title="Impacto Económico Global", color_continuous_scale="Reds")
    st.plotly_chart(fig_mapa, use_container_width=True)

# --- BLOQUE: EVOLUCIÓN TEMPORAL ---
elif menu == "📈 Evolución Temporal":
    st.title("📈 Análisis de Tendencias Históricas")
    df_trend = ejecutar_query("SELECT year, attack_type, SUM(financial_loss_in_million_) as total_perdida FROM amenazas GROUP BY 1, 2 ORDER BY year ASC")
    fig_area = px.area(df_trend, x="year", y="total_perdida", color="attack_type", template="plotly_dark")
    st.plotly_chart(fig_area, use_container_width=True)

# --- BLOQUE: EFICIENCIA DE DEFENSA ---
elif menu == "⚡ Eficiencia de Defensa":
    st.title("⚡ Análisis de Respuesta y Mitigación")
    df_ef = ejecutar_query("SELECT defense_mechanism_used, AVG(incident_resolution_time_in_hours) as tiempo_medio, AVG(financial_loss_in_million_) as perdida_media, COUNT(*) as frecuencia FROM amenazas GROUP BY 1")

    fig_scatter = px.scatter(df_ef, x="tiempo_medio", y="perdida_media", size="frecuencia", color="defense_mechanism_used", template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # CORRECCIÓN DE INDENTACIÓN AQUÍ:
    with st.expander("📝 ¿Cómo leer este gráfico de eficiencia?"):
        st.write("""
        Este gráfico correlaciona la velocidad de respuesta con el impacto financiero:
        - **Eje X (Tiempo):** Entre más a la izquierda, más rápida fue la defensa.
        - **Eje Y (Pérdida):** Entre más abajo, más efectiva fue la mitigación económica.
        """)

# --- BLOQUE: RECOMENDACIONES ---
elif menu == "💡 Recomendaciones":
    st.title("💡 Hoja de Ruta Estratégica")
    tab1, tab2, tab3 = st.tabs(["🛡️ Técnica", "🏢 Organizacional", "🌐 Global"])
    with tab1:
        st.info("#### Optimización Tecnológica: Implementar IA y Cifrado Avanzado.")
    with tab2:
        st.warning("#### Cultura: Adoptar el modelo Zero Trust.")
    with tab3:
        st.success("#### Global: Fomentar la resiliencia productiva nacional.")