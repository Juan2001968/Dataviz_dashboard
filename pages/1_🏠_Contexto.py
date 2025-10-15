
import streamlit as st
from utils import load_data

st.title("Contexto de la Base de Datos")

csv_path = st.session_state.get("csv_path", "finanzas_empresas.csv")
df = load_data(csv_path)

st.subheader("Descripción")
st.markdown("""
Esta base contiene registros de **empresas** con su **Departamento** y coordenadas (**Latitud**, **Longitud**),
además de variables de interés como **Categoría** y **Valor**. Es ideal para:
- **Análisis descriptivo** (tablas, conteos, medias).
- **Visualizaciones** (matplotlib / plotly).
- **Georreferenciación** por departamento usando un mapa interactivo (folium).
""")

col1, col2, col3 = st.columns(3)
col1.metric("Filas", f"{len(df):,}")
col2.metric("Columnas", f"{df.shape[1]}")
col3.metric("Departamentos", df["Departamento"].nunique() if "Departamento" in df.columns else 0)

st.subheader("Vista previa")
st.dataframe(df.head(50), use_container_width=True)
