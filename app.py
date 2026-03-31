import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. IMPORTA TU NUEVO ARCHIVO DE ESTILOS
from styles import aplicar_estilos_personalizados

# 1. Configuración de página
st.set_page_config(page_title="Cyber Intelligence Dashboard", layout="wide")

# 2. Aplicar los estilos
aplicar_estilos_personalizados()

# 2. Conexión a la base de datos
def ejecutar_query(query):
    conn = sqlite3.connect('data/ciberseguridad.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- CARGA GLOBAL DE DATOS ---

try:
    df_all = ejecutar_query("SELECT * FROM amenazas")
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")
    df_all = pd.DataFrame() # Crea un dataframe vacío para evitar que la app explote

# =================================================================
# 3. BARRA LATERAL (SIDEBAR) - NAVEGACIÓN
# Crea un menú de radio buttons para navegar entre las diferentes 
# secciones del proyecto integrador.
# =================================================================
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

# =================================================================
# 4. LÓGICA DE VISTAS (BLOQUES DE CONTENIDO)
# Dependiendo de la opción seleccionada en el menú, se renderiza 
# el contenido correspondiente.
# =================================================================

# --- BLOQUE: INICIO ---
# Presentación visual del proyecto, objetivos y contexto estratégico.
if menu == "🏠 Inicio":
    st.title("🛡️ Fortaleciendo la Frontera Digital")
    st.markdown("### Análisis Estratégico de Ciberseguridad 2015-2024")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        # Carga la imagen de portada personalizada del proyecto
        st.image("portada.jpeg", caption="Análisis de Amenazas - Proyecto Integrador")
        
    with col2:
        st.subheader("El Valor de los Datos")
        st.write("""
        En la era de la transformación productiva, la ciberseguridad es una necesidad 
        fundamental para la estabilidad social y económica.
        """)
        st.info("💡 **Objetivo:** Transformar incidentes globales en recomendaciones prácticas.")

# --- BLOQUE: RESUMEN GENERAL ---
# Visualización de KPIs (Métricas clave) y un glosario interactivo de términos.
elif menu == "📊 Resumen General":
    st.markdown("# 📊 Inteligencia de Amenazas")
    
    # Envolvemos las métricas en un contenedor para que el CSS actúe
    with st.container():
        c1, c2, c3 = st.columns(3)
        c1.metric("Impacto Económico", f"${df_all['financial_loss_in_million_'].sum():,.0f}M", "Global")
        c2.metric("Alcance de Víctimas", f"{df_all['number_of_affected_users'].sum():,}", "Usuarios")
        c3.metric("Frecuencia", len(df_all), "Eventos")

    # Gráfico de Industria
    st.divider()
    fig_ind = px.bar(df_all.groupby('target_industry').size().reset_index(name='cuenta'), 
                     x='target_industry', y='cuenta', title="Distribución por Industria",
                     color='target_industry', template="plotly_dark")
    st.plotly_chart(fig_ind, use_container_width=True)

    # --- DICCIONARIO COMPLETO RE-ESTABLECIDO ---
    st.subheader("🕵️ Diccionario de Amenazas Analizadas")
    col_a, col_b = st.columns(2)

    with col_a:
        with st.expander("🌐 **DDoS (Denegación de Servicio)**"):
            st.write("Inunda un servidor con tráfico falso para dejarlo inoperativo.")
        with st.expander("🦠 **Malware (Software Malicioso)**"):
            st.write("Software diseñado para infiltrarse o dañar un dispositivo.")
        with st.expander("👥 **Man-in-the-Middle (MitM)**"):
            st.write("Intercepción de comunicación entre dos partes para robar datos.")

    with col_b:
        with st.expander("🎣 **Phishing (Suplantación)**"):
            st.write("Engaño mediante mensajes falsos para obtener contraseñas.")
        with st.expander("🔒 **Ransomware (Secuestro de Datos)**"):
            st.write("Cifra archivos y exige rescate para devolver el acceso.")
        with st.expander("💉 **SQL Injection (Inyección SQL)**"):
            st.write("Inserción de código malicioso para manipular bases de datos.")
            
# --- BLOQUE: ANÁLISIS DE COSTOS ---
# Uso de Treemaps para identificar qué industrias y ataques son más costosos.
elif menu == "💰 Análisis de Costos":
    st.title("💰 Análisis de Impacto Financiero")
    query_costos = """
    SELECT target_industry, attack_type, ROUND(AVG(financial_loss_in_million_), 2) as perdida_promedio
    FROM amenazas
    GROUP BY 1, 2 ORDER BY perdida_promedio DESC
    """
    df_costos = ejecutar_query(query_costos)
    fig_tree = px.treemap(df_costos, path=['target_industry', 'attack_type'], 
                          values='perdida_promedio', color='perdida_promedio', 
                          color_continuous_scale='RdBu', title="Jerarquía de Pérdidas por Sector")
    st.plotly_chart(fig_tree, use_container_width=True)

# --- BLOQUE: ANÁLISIS GEOGRÁFICO ---
# Mapa interactivo y comparativa de rendimiento (respuesta vs pérdida) por país.
elif menu == "🌍 Análisis Geográfico":
    st.title("🌍 Comparativa Global por Países")
    query_pais = "SELECT country, SUM(financial_loss_in_million_) as perdida_total, AVG(incident_resolution_time_in_hours) as tiempo_avg FROM amenazas GROUP BY country"
    df_pais = ejecutar_query(query_pais)
    
    # Mapa Choropleth: Intensidad de pérdidas económicas por nación
    fig_mapa = px.choropleth(df_pais, locations="country", locationmode='country names',
                             color="perdida_total", title="Impacto Económico Global", color_continuous_scale="Reds")
    st.plotly_chart(fig_mapa, use_container_width=True)
    

    # Rankings: Mejores y peores desempeños geográficos
    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Top 10 Más Afectados ($)")
        st.plotly_chart(px.bar(df_pais.nlargest(10, 'perdida_total'), x='perdida_total', y='country', orientation='h', color='perdida_total', color_continuous_scale='Reds'), use_container_width=True)
    with col_right:
        st.subheader("Top 10 Más Rápidos (Respuesta)")
        st.plotly_chart(px.bar(df_pais.nsmallest(10, 'tiempo_avg'), x='tiempo_avg', y='country', orientation='h', color='tiempo_avg', color_continuous_scale='Greens_r'), use_container_width=True)

# --- BLOQUE: EVOLUCIÓN TEMPORAL ---
# Gráficos de área y barras para visualizar tendencias y crecimiento de ataques en el tiempo.
elif menu == "📈 Evolución Temporal":
    st.title("📈 Análisis de Tendencias Históricas (2015-2024)")
    query_trend = "SELECT year, attack_type, SUM(financial_loss_in_million_) as total_perdida, COUNT(*) as cantidad_incidentes FROM amenazas GROUP BY 1, 2 ORDER BY year ASC"
    df_trend = ejecutar_query(query_trend)

    # Gráfico de área: Muestra cómo se acumula la pérdida año tras año
    fig_area = px.area(df_trend, x="year", y="total_perdida", color="attack_type", template="plotly_dark")
    st.plotly_chart(fig_area, use_container_width=True)

    # Slider interactivo: Permite al usuario filtrar detalles por un año específico
    año_sel = st.slider("Seleccione un año para ver el detalle:", 2015, 2024, 2024)
    st.table(df_trend[df_trend['year'] == año_sel].set_index('attack_type'))

# --- BLOQUE: EFICIENCIA DE DEFENSA ---
# Análisis correlacional entre la tecnología usada, el tiempo de respuesta y el costo final.
elif menu == "⚡ Eficiencia de Defensa":
    st.title("⚡ Análisis de Respuesta y Mitigación")
    query_eficiencia = "SELECT defense_mechanism_used, AVG(incident_resolution_time_in_hours) as tiempo_medio, AVG(financial_loss_in_million_) as perdida_media, COUNT(*) as frecuencia FROM amenazas GROUP BY 1"
    df_ef = ejecutar_query(query_eficiencia)

    # Scatter Plot: Identifica qué tecnologías son más rápidas y baratas de implementar
    fig_scatter = px.scatter(df_ef, x="tiempo_medio", y="perdida_media", size="frecuencia", color="defense_mechanism_used", template="plotly_dark")
    st.plotly_chart(fig_scatter, use_container_width=True)

    with st.expander("📝 ¿Cómo leer este gráfico de eficiencia?"):
     st.write("""
    Este gráfico correlaciona la velocidad de respuesta con el impacto financiero:
    - **Eje X (Tiempo):** Entre más a la izquierda, más rápida fue la defensa.
    - **Eje Y (Pérdida):** Entre más abajo, más efectiva fue la mitigación económica.
    - **Tamaño del punto:** Indica qué tan común es el uso de esa defensa en nuestra base de datos.
    """)

# --- BLOQUE: RECOMENDACIONES ---
# Sección final con la propuesta estratégica basada en los hallazgos de los datos.
elif menu == "💡 Recomendaciones":
    st.title("💡 Hoja de Ruta Estratégica 2024-2030")
    
    # Organización por pestañas (Tabs) para separar lo técnico de lo organizacional
    tab1, tab2, tab3 = st.tabs(["🛡️ Técnica", "🏢 Organizacional", "🌐 Global"])
    with tab1:
        st.info("#### Optimización Tecnológica: Implementar IA y Cifrado Avanzado.")
    with tab2:
        st.warning("#### Cultura: Adoptar el modelo Zero Trust (Confianza Cero).")
    with tab3:
        st.success("#### Global: Fomentar la resiliencia productiva nacional.")

    st.caption("Documento generado para el programa Talento Tech - Nivel Integrador.")