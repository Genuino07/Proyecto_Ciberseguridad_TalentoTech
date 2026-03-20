import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Configuración profesional
st.set_page_config(page_title="CyberSecurity Analytics Pro", layout="wide")

# 2. Conexión a la base de datos
def ejecutar_query(query):
    conn = sqlite3.connect('data/ciberseguridad.db')
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# --- SIDEBAR (Un solo menú para todo) ---
st.sidebar.header("Opciones de Análisis")
menu = st.sidebar.selectbox(
    "Seleccione una Vista:",
    ["Resumen General", "Análisis de Costos", "Análisis Geográfico", "Evolución Temporal", "Eficiencia de Defensa", "Recomendaciones"]
)

# --- LÓGICA DE VISTAS ---

if menu == "Resumen General":
    st.title("🛡️ Estado de la Ciberseguridad Global")
    df_all = ejecutar_query("SELECT * FROM amenazas")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Pérdida Total", f"${df_all['financial_loss_in_million_'].sum():,.0f}M")
    c2.metric("Total Usuarios Afectados", f"{df_all['number_of_affected_users'].sum():,}")
    c3.metric("Incidentes Registrados", len(df_all))

    fig_ind = px.bar(df_all.groupby('target_industry').size().reset_index(name='cuenta'), 
                     x='target_industry', y='cuenta', title="Distribución de Ataques por Industria",
                     color='target_industry', template="plotly_dark")
    st.plotly_chart(fig_ind, use_container_width=True)

elif menu == "Análisis de Costos":
    st.title("💰 Análisis de Impacto Financiero")
    query_costos = """
    SELECT target_industry, attack_type, ROUND(AVG(financial_loss_in_million_), 2) as perdida_promedio
    FROM amenazas
    GROUP BY target_industry, attack_type
    ORDER BY perdida_promedio DESC
    """
    df_costos = ejecutar_query(query_costos)
    fig_tree = px.treemap(df_costos, path=['target_industry', 'attack_type'], 
                          values='perdida_promedio', color='perdida_promedio', 
                          color_continuous_scale='RdBu', title="Mapa de Calor de Pérdidas")
    st.plotly_chart(fig_tree, use_container_width=True)
    st.dataframe(df_costos)

elif menu == "Análisis Geográfico":
    st.title("🌍 Comparativa Global por Países")
    query_pais = "SELECT country, SUM(financial_loss_in_million_) as perdida_total, AVG(incident_resolution_time_in_hours) as tiempo_avg FROM amenazas GROUP BY country"
    df_pais = ejecutar_query(query_pais)

    fig_mapa = px.choropleth(df_pais, locations="country", locationmode='country names',
                             color="perdida_total", title="Impacto Económico Global", color_continuous_scale="Reds")
    st.plotly_chart(fig_mapa, use_container_width=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("Top 10 Más Afectados ($)")
        st.plotly_chart(px.bar(df_pais.nlargest(10, 'perdida_total'), x='perdida_total', y='country', orientation='h', color='perdida_total', color_continuous_scale='Reds'), use_container_width=True)
    with col_right:
        st.subheader("Top 10 Más Rápidos (Respuesta)")
        st.plotly_chart(px.bar(df_pais.nsmallest(10, 'tiempo_avg'), x='tiempo_avg', y='country', orientation='h', color='tiempo_avg', color_continuous_scale='Greens_r'), use_container_width=True)

elif menu == "Evolución Temporal":
    st.title("📈 Tendencias 2015 - 2024")
    query_trend = "SELECT year, SUM(financial_loss_in_million_) as total_perdida FROM amenazas GROUP BY year ORDER BY year ASC"
    df_trend = ejecutar_query(query_trend)
    fig_line = px.line(df_trend, x='year', y='total_perdida', title="Evolución Anual", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

elif menu == "Eficiencia de Defensa":
    st.title("⚡ Análisis de Respuesta y Defensa")
    query_defensa = "SELECT defense_mechanism_used, AVG(incident_resolution_time_in_hours) as tiempo_medio FROM amenazas GROUP BY 1 ORDER BY 2 ASC"
    df_defensa = ejecutar_query(query_defensa)
    fig_def = px.bar(df_defensa, x='tiempo_medio', y='defense_mechanism_used', orientation='h', color='tiempo_medio', color_continuous_scale='Viridis')
    st.plotly_chart(fig_def, use_container_width=True)

elif menu == "Recomendaciones":
    st.title("💡 Recomendaciones Estratégicas")
    st.info("Priorizar la implementación de **IA-based Detection** y **Encryption**, ya que presentan los menores tiempos de resolución en el dataset.")
    st.success("Conclusión: Los sectores de Infraestructura Crítica deben migrar a modelos Zero Trust para mitigar el impacto de ataques de tipo Ransomware.")