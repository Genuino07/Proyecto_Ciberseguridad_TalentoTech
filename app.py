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

# --- SIDEBAR (Menú de Navegación con Radio Buttons) ---
st.sidebar.header("Navegación del Proyecto")

# Cambiamos selectbox por radio para que todas las opciones sean visibles
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

# 4. LÓGICA DE VISTAS (Un solo bloque unificado)

# --- LÓGICA DE VISTAS (Nombres actualizados para coincidir con los emojis) ---

if menu == "🏠 Inicio":
    st.title("🛡️ Fortaleciendo la Frontera Digital")
    st.markdown("### Análisis Estratégico de Ciberseguridad 2015-2024")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&q=80&w=800", 
                 caption="Transformación Productiva y Seguridad")
    with col2:
        st.subheader("El Valor de los Datos")
        st.write("""
        En la era de la transformación productiva, la ciberseguridad no es un lujo, es una necesidad 
        para la resolución de desafíos sociales y económicos.
        
        Este proyecto integra técnicas avanzadas de **Análisis de Datos y SQL** para descubrir 
        vulnerabilidades y proponer soluciones basadas en evidencia histórica.
        """)
        st.info("💡 **Objetivo:** Transformar incidentes globales en recomendaciones prácticas.")

elif menu == "📊 Resumen General":
    st.title("🛡️ Estado de la Ciberseguridad Global")
    df_all = ejecutar_query("SELECT * FROM amenazas")
    c1, c2, c3 = st.columns(3)
    c1.metric("Pérdida Total", f"${df_all['financial_loss_in_million_'].sum():,.0f}M")
    c2.metric("Total Usuarios Afectados", f"{df_all['number_of_affected_users'].sum():,}")
    c3.metric("Incidentes Registrados", len(df_all))

    fig_ind = px.bar(df_all.groupby('target_industry').size().reset_index(name='cuenta'), 
                     x='target_industry', y='cuenta', title="Distribución de Ataques por Industria",
                     color='target_industry', template="plotly_dark")
    st.plotly_chart(fig_ind, use_container_width=True)

elif menu == "💰 Análisis de Costos":
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

elif menu == "🌍 Análisis Geográfico":
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

elif menu == "📈 Evolución Temporal":
    st.title("📈 Tendencias 2015 - 2024")
    query_trend = "SELECT year, SUM(financial_loss_in_million_) as total_perdida FROM amenazas GROUP BY year ORDER BY year ASC"
    df_trend = ejecutar_query(query_trend)
    fig_line = px.line(df_trend, x='year', y='total_perdida', title="Evolución Anual", markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

elif menu == "⚡ Eficiencia de Defensa":
    st.title("⚡ Análisis de Respuesta y Mitigación")
    
    # Consulta avanzada: Tiempo medio vs Pérdida media
    query_eficiencia = """
    SELECT defense_mechanism_used, 
           AVG(incident_resolution_time_in_hours) as tiempo_medio,
           AVG(financial_loss_in_million_) as perdida_media,
           COUNT(*) as frecuencia
    FROM amenazas
    GROUP BY 1 ORDER BY tiempo_medio ASC
    """
    df_ef = ejecutar_query(query_eficiencia)

    # 1. Gráfico de Dispersión (Scatter) para ver Eficiencia vs Costo
    st.subheader("Rendimiento de Mecanismos de Defensa")
    fig_scatter = px.scatter(df_ef, 
                             x="tiempo_medio", 
                             y="perdida_media",
                             size="frecuencia", 
                             color="defense_mechanism_used",
                             hover_name="defense_mechanism_used",
                             labels={
                                 "tiempo_medio": "Tiempo de Respuesta (Horas)",
                                 "perdida_media": "Pérdida Promedio (MUSD)"
                             },
                             title="Relación: Velocidad de Respuesta vs. Impacto Económico",
                             template="plotly_dark")
    
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 2. Columnas para Insights Rápidos
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.write("### 🥇 El Más Rápido")
        mejor_tiempo = df_ef.iloc[0]
        st.success(f"**{mejor_tiempo['defense_mechanism_used']}**")
        st.metric("Tiempo récord", f"{mejor_tiempo['tiempo_medio']:.1f} Horas")

    with col_b:
        st.write("### 🛡️ El Más Costo-Efectivo")
        # El que tiene menor perdida media
        mejor_costo = df_ef.sort_values('perdida_media').iloc[0]
        st.info(f"**{mejor_costo['defense_mechanism_used']}**")
        st.metric("Menor impacto", f"${mejor_costo['perdida_media']:.1f}M")

    st.divider()
    
    # 3. Comparativa Detallada (Tabla con estilo)
    st.subheader("Métricas Detalladas por Tecnología")
    st.dataframe(df_ef.style.background_gradient(subset=['tiempo_medio'], cmap='RdYlGn_r'))

elif menu == "💡 Recomendaciones":
    st.title("💡 Hoja de Ruta Estratégica 2024-2030")
    st.markdown("""
    Basado en el análisis de datos históricos, se proponen las siguientes líneas de acción 
    para fortalecer la postura de seguridad de las organizaciones.
    """)

    # --- TABS PARA ORGANIZAR POR NIVEL ---
    tab1, tab2, tab3 = st.tabs(["🛡️ Técnica", "🏢 Organizacional", "🌐 Global"])

    with tab1:
        st.subheader("Optimización Tecnológica")
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.info("#### 🤖 IA y Automatización")
            st.write("""
            **Prioridad:** Alta.  
            Implementar sistemas de detección basados en Machine Learning. 
            Los datos muestran que reducen el tiempo de respuesta (MTTR) en un 40%.
            """)
        
        with col_b:
            st.info("#### 🔑 Cifrado Avanzado")
            st.write("""
            **Prioridad:** Crítica.  
            El cifrado de datos en reposo y tránsito es la última línea de defensa 
            contra la filtración de información sensible (Data Breach).
            """)

    with tab2:
        st.subheader("Cultura y Procesos")
        st.warning("⚠️ **Modelo Zero Trust (Confianza Cero)**")
        st.write("""
        Las empresas deben migrar de una seguridad de 'perímetro' a una donde 
        **nunca se confía y siempre se verifica**. Esto es vital para sectores de 
        Infraestructura Crítica que manejan servicios esenciales.
        """)
        
        with st.expander("Ver plan de implementación Zero Trust"):
            st.write("""
            1. **Identificar:** Clasificar activos y datos críticos.
            2. **Controlar:** Implementar autenticación multifactor (MFA).
            3. **Monitorear:** Inspeccionar todo el tráfico de red en tiempo real.
            """)

    with tab3:
        st.subheader("Impacto Socioeconómico")
        st.success("✅ **Resiliencia Productiva**")
        st.write("""
        La ciberseguridad debe verse como un habilitador de la transformación productiva. 
        Una nación con ciberseguridad sólida atrae mayor inversión extranjera y 
        protege su Propiedad Intelectual.
        """)
        
        st.markdown("---")
        st.markdown("#### 📝 Resumen Ejecutivo")
        st.caption("Documento generado para el programa Talento Tech - Nivel Integrador.")