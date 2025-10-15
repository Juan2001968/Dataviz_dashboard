
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
from utils import load_data

st.set_page_config(layout="wide")

st.title("Análisis Descriptivo de las Finanzas Empresariales")

st.markdown("""
En esta sección se realiza un **análisis descriptivo y exploratorio** de la base de datos *finanzas_empresas.csv*,
con el objetivo de comprender la distribución de las variables, identificar patrones entre categorías y
comparar el comportamiento financiero de las empresas según su localización geográfica.

Se utilizarán estadísticas básicas, tablas resumen y visualizaciones interactivas que facilitan
la interpretación de los datos.
""")

# === Cargar datos ===
csv_path = st.session_state.get("csv_path", "finanzas_empresas.csv")
df = load_data(csv_path)

# === Validaciones básicas ===
if df.empty:
    st.error("No se pudo cargar la base de datos. Verifica el archivo CSV.")
    st.stop()

# === Resumen general ===
st.subheader("1. Resumen general del conjunto de datos")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Número total de registros", f"{len(df):,}")
col2.metric("Departamentos únicos", df["Departamento"].nunique() if "Departamento" in df.columns else 0)
col3.metric("Categorías únicas", df["Categoría"].nunique() if "Categoría" in df.columns else 0)
col4.metric("Promedio general del Valor", f"{df['Valor'].mean():.3f}" if "Valor" in df.columns else "N/A")

st.markdown("""
A continuación se muestra una vista previa del conjunto de datos cargado:
""")
st.dataframe(df.head(10), use_container_width=True)

# === Descripción estadística ===
st.subheader("2. Estadísticas descriptivas")

st.markdown("""
El siguiente cuadro presenta un resumen estadístico del campo **Valor**, el cual representa el indicador
financiero de las empresas. Se analizan su tendencia central, dispersión y distribución general.
""")

if "Valor" in df.columns:
    st.dataframe(df["Valor"].describe().to_frame().T, use_container_width=True)
else:
    st.warning("La columna 'Valor' no se encuentra disponible en la base de datos.")

# === Filtros interactivos ===
st.subheader("3. Filtros interactivos")

with st.expander("Mostrar/Ocultar filtros", expanded=True):
    departamentos = sorted(df["Departamento"].dropna().unique()) if "Departamento" in df.columns else []
    categorias = sorted(df["Categoría"].dropna().unique()) if "Categoría" in df.columns else []

    dep_sel = st.multiselect("Selecciona uno o varios departamentos:", departamentos, default=departamentos[:3] if len(departamentos) > 3 else departamentos)
    cat_sel = st.multiselect("Selecciona categorías:", categorias, default=categorias)

filtro = pd.Series(True, index=df.index)
if dep_sel:
    filtro &= df["Departamento"].isin(dep_sel)
if cat_sel:
    filtro &= df["Categoría"].isin(cat_sel)

dff = df[filtro].copy()

st.markdown(f"**Registros filtrados:** {len(dff)}")

# === Gráfico 1: Promedio por Departamento ===
st.subheader("4. Promedio del Valor por Departamento")

st.markdown("""
El siguiente gráfico de barras muestra el **valor promedio** por departamento, permitiendo observar las
diferencias regionales en el desempeño financiero.
""")

if "Departamento" in dff.columns and "Valor" in dff.columns:
    promedio_dep = dff.groupby("Departamento")["Valor"].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 4))
    promedio_dep.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    ax.set_ylabel("Valor promedio")
    ax.set_xlabel("Departamento")
    ax.set_title("Promedio del Valor por Departamento")
    st.pyplot(fig)
else:
    st.warning("No se puede generar el gráfico. Faltan columnas 'Departamento' o 'Valor'.")

# === Gráfico 2: Distribución general del Valor ===
st.subheader("5. Distribución de la variable Valor")

st.markdown("""
La distribución de los valores permite identificar la presencia de asimetrías, concentración de datos
o posibles valores atípicos. Se usa un histograma con curva de densidad.
""")

if "Valor" in dff.columns:
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    sns.histplot(dff["Valor"], kde=True, bins=20, color="lightcoral", ax=ax2)
    ax2.set_xlabel("Valor")
    ax2.set_ylabel("Frecuencia")
    ax2.set_title("Distribución del Valor")
    st.pyplot(fig2)

# === Gráfico 3: Boxplot por Categoría ===
st.subheader("6. Comparación por Categoría")

st.markdown("""
En este gráfico se muestra la distribución del indicador **Valor** en función de la **Categoría** de empresa.
Permite comparar la dispersión y los valores extremos entre grupos.
""")

if "Valor" in dff.columns and "Categoría" in dff.columns:
    fig3 = px.box(
        dff,
        x="Categoría",
        y="Valor",
        color="Categoría",
        title="Distribución del Valor por Categoría",
        points="outliers"
    )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("No se puede graficar porque faltan las columnas 'Valor' y/o 'Categoría'.")

# === Gráfico 4: Heatmap de correlaciones (opcional) ===
st.subheader("7. Matriz de correlaciones")

st.markdown("""
A continuación se presenta una matriz de correlación entre las variables numéricas disponibles en la base.
Esto permite observar relaciones lineales entre las distintas medidas.
""")

num_cols = dff.select_dtypes(include="number")
if not num_cols.empty:
    corr = num_cols.corr()
    fig4, ax4 = plt.subplots(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="YlGnBu", ax=ax4)
    ax4.set_title("Matriz de correlaciones")
    st.pyplot(fig4)
else:
    st.info("No hay suficientes columnas numéricas para calcular correlaciones.")

# === Conclusión ===
st.markdown("---")
st.subheader("8. Conclusiones del análisis")

st.markdown("""
- La base presenta una distribución equilibrada entre departamentos y categorías.  
- Existen diferencias notables en el valor promedio por departamento, lo cual puede reflejar 
  condiciones económicas o empresariales particulares.  
- La variable **Valor** muestra una dispersión moderada, con una tendencia central clara y algunos valores extremos.  
- Las categorías con mayores valores promedio podrían representar sectores con mejor desempeño financiero.  
- El análisis exploratorio permite comprender la estructura inicial de los datos y orientar el análisis geográfico posterior.
""")

