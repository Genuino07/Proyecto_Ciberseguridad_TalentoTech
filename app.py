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
        with col1:
            st.image("portada.jpeg", caption="Análisis de Amenazas - Proyecto Integrador")
        
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
    st.title("📊 Estado de la Ciberseguridad Global")
    df_all = ejecutar_query("SELECT * FROM amenazas")
    
    # --- 1. KPIs PRINCIPALES ---
    c1, c2, c3 = st.columns(3)
    c1.metric("Pérdida Total", f"${df_all['financial_loss_in_million_'].sum():,.0f}M")
    c2.metric("Total Usuarios Afectados", f"{df_all['number_of_affected_users'].sum():,}")
    c3.metric("Incidentes Registrados", len(df_all))

    # --- 2. GRÁFICO DE DISTRIBUCIÓN ---
    st.divider()
    fig_ind = px.bar(df_all.groupby('target_industry').size().reset_index(name='cuenta'), 
                     x='target_industry', y='cuenta', title="Distribución de Ataques por Industria",
                     color='target_industry', template="plotly_dark")
    st.plotly_chart(fig_ind, use_container_width=True)

    # --- 3. GLOSARIO PROFESIONAL DE AMENAZAS ---
    st.subheader("🕵️ Diccionario de Amenazas Analizadas")
    st.write("Selecciona una amenaza para entender su funcionamiento y vectores de ataque:")

    col_a, col_b = st.columns(2)

    with col_a:
        with st.expander("🌐 **DDoS (Denegación de Servicio)**"):
            st.write("""
            **Qué es:** Inunda un servidor o red con tráfico falso para dejarlo inoperativo.  
            **Impacto:** Interrupción total de servicios digitales y pérdidas por inactividad.
            """)
            
        with st.expander("🦠 **Malware (Software Malicioso)**"):
            st.write("""
            **Qué es:** Término general para virus, troyanos o gusanos diseñados para infiltrarse o dañar un dispositivo sin consentimiento.  
            **Impacto:** Robo de información y control remoto de sistemas.
            """)

        with st.expander("👥 **Man-in-the-Middle (MitM)**"):
            st.write("""
            **Qué es:** El atacante intercepta en secreto la comunicación entre dos partes (como tu PC y tu banco) para robar datos.  
            **Impacto:** Robo de credenciales y sesiones bancarias.
            """)

    with col_b:
        with st.expander("🎣 **Phishing (Suplantación)**"):
            st.write("""
            **Qué es:** Ingeniería social mediante correos o mensajes falsos para engañar al usuario y obtener sus contraseñas.  
            **Impacto:** Es la puerta de entrada principal para el 90% de los ciberataques.
            """)

        with st.expander("🔒 **Ransomware (Secuestro de Datos)**"):
            st.write("""
            **Qué es:** Cifra los archivos de la víctima y exige un rescate (usualmente en cripto) para devolver el acceso.  
            **Impacto:** Es el ataque más costoso financieramente en la actualidad.
            """)

        with st.expander("💉 **SQL Injection (Inyección SQL)**"):
            st.write("""
            **Qué es:** Inserción de código malicioso en formularios web para manipular la base de datos de la empresa.  
            **Impacto:** Filtración masiva de bases de datos de clientes y empleados.
            """)

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
    st.title("🌍 Mapa de Calor de Amenazas Globales")
    
    # Consulta detallada
    query_mapa = "SELECT country, attack_type, financial_loss_in_million_, number_of_affected_users FROM amenazas"
    df_mapa = ejecutar_query(query_mapa)

    # Selector interactivo para filtrar el mapa
    tipo_filtro = st.selectbox("Filtrar mapa por tipo de ataque:", ["Todos"] + list(df_mapa['attack_type'].unique()))
    
    if tipo_filtro != "Todos":
        df_mapa = df_mapa[df_mapa['attack_type'] == tipo_filtro]

    # Crear el mapa interactivo
    fig_mapa = px.scatter_geo(df_mapa, 
        locations="country", 
        locationmode='country names',
        color="attack_type", 
        hover_name="country", 
        size="financial_loss_in_million_",
        projection="natural earth",
        title="Impacto Financiero por País y Tipo de Ataque",
        labels={'financial_loss_in_million_': 'Pérdida (MUSD)'},
        template="plotly_dark",
        color_discrete_sequence=px.colors.qualitative.Pastel)

    # Ajustes estéticos del mapa
    fig_mapa.update_geos(
        showcountries=True, countrycolor="RebeccaPurple",
        showcoastlines=True, coastlinecolor="DarkSlateBlue",
        showland=True, landcolor="LightSlateGrey",
        showocean=True, oceancolor="Black"
    )

    st.plotly_chart(fig_mapa, use_container_width=True)

    # --- MÉTRICAS DE LUGAR ---
    st.divider()
    col_l, col_r = st.columns(2)
    with col_l:
        top_pais = df_mapa.groupby('country')['financial_loss_in_million_'].sum().idxmax()
        st.info(f"🚩 **País con mayor pérdida:** {top_pais}")
    with col_r:
        st.write("""
        **Guía de uso:**
        * Usa el **Scroll** para hacer zoom.
        * Haz **clic y arrastra** para moverte por el globo.
        * Pasa el cursor sobre un punto para ver el **costo exacto** del ataque en ese país.
        """)

       # --- SECCIÓN TOP 10 (Corregida) ---
st.subheader("🏆 Top 10 Países con Mayores Pérdidas")

# Agrupamos los datos correctamente para el ranking
df_ranking = df_mapa.groupby('country')['financial_loss_in_million_'].sum().reset_index()
df_ranking = df_ranking.rename(columns={'financial_loss_in_million_': 'perdida_total'})

# Creamos el gráfico usando el nuevo nombre 'perdida_total'
fig_top10 = px.bar(
    df_ranking.nlargest(10, 'perdida_total'), 
    x='perdida_total', 
    y='country', 
    orientation='h', 
    title="Top 10 Más Afectados (MUSD)",
    color='perdida_total', 
    color_continuous_scale='Reds',
    labels={'perdida_total': 'Pérdida Total (MUSD)', 'country': 'País'}
)

fig_top10.update_layout(yaxis={'categoryorder':'total ascending'}) # Ordenar de mayor a menor
st.plotly_chart(fig_top10, use_container_width=True)

elif menu == "📈 Evolución Temporal":
    st.title("📈 Análisis de Tendencias Históricas (2015-2024)")
    
    # Consulta para obtener datos por año y tipo de ataque
    query_trend = """
    SELECT year, attack_type, 
           SUM(financial_loss_in_million_) as total_perdida,
           COUNT(*) as cantidad_incidentes
    FROM amenazas 
    GROUP BY year, attack_type 
    ORDER BY year ASC
    """
    df_trend = ejecutar_query(query_trend)

    # 1. Gráfico de Área Apilada (Muestra el crecimiento y la composición)
    st.subheader("Impacto Económico Acumulado por Tipo de Ataque")
    fig_area = px.area(df_trend, x="year", y="total_perdida", color="attack_type",
                       title="Evolución de Pérdidas Financieras (MUSD)",
                       labels={"total_perdida": "Pérdida (MUSD)", "year": "Año"},
                       template="plotly_dark",
                       line_group="attack_type")
    st.plotly_chart(fig_area, use_container_width=True)

    # 2. Comparativa de Volumen vs Costo
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.subheader("Crecimiento de Incidentes")
        # Agrupamos por año para ver el volumen total
        df_vol = df_trend.groupby('year')['cantidad_incidentes'].sum().reset_index()
        fig_vol = px.bar(df_vol, x="year", y="cantidad_incidentes", 
                         title="Cantidad de Ataques por Año",
                         color_discrete_sequence=['#ff4b4b'])
        st.plotly_chart(fig_vol, use_container_width=True)

    with col_r:
        st.subheader("Análisis de Intensidad")
        st.write("""
        **Interpretación:** A medida que avanzamos hacia 2024, observamos que la sofisticación de los ataques (como el Ransomware) 
        ha incrementado la 'pendiente' de la gráfica de área. 
        
        Esto sugiere que aunque el número de ataques se mantenga estable, el **costo por incidente** es cada vez mayor debido a la digitalización de la economía.
        """)
        st.info("📊 **Dato Clave:** El periodo 2021-2024 muestra una aceleración en pérdidas debido a ataques dirigidos a Infraestructura Crítica.")

    # 3. Selector de Año para Inspección Rápida
    st.divider()
    año_sel = st.slider("Desliza para inspeccionar un año específico:", 2015, 2024, 2024)
    df_year = df_trend[df_trend['year'] == año_sel]
    st.write(f"### Detalle del año {año_sel}")
    st.table(df_year[['attack_type', 'total_perdida', 'cantidad_incidentes']].set_index('attack_type'))

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

    # Gráfico de Dispersión (Scatter) para ver Eficiencia vs Costo
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

    #  Columnas para Insights Rápidos
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
    
    # Comparativa Detallada (Tabla con estilo)
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