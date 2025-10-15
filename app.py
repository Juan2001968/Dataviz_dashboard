import streamlit as st

# Configuración general
st.set_page_config(
    page_title="Dashboard de Finanzas Empresariales",
    page_icon="💼",
    layout="wide"
)

# Título e introducción general
st.title("Dashboard de Finanzas Empresariales")

st.markdown("""
## Contexto de la Base de Datos

La base de datos **finanzas_empresas.csv** contiene información simulada sobre distintas empresas colombianas,
clasificadas por **departamento** y **categoría**. Cada registro incluye:
- El **departamento** donde se ubica la empresa.
- Las **coordenadas geográficas** (latitud y longitud) asociadas.
- Una **categoría** que representa el tipo o grupo de empresa.
- Una variable **Valor**, que simboliza un indicador económico o financiero estimado.

El objetivo principal es analizar el comportamiento de esta variable en función del territorio y del tipo
de empresa, identificando diferencias o concentraciones significativas entre departamentos.
            """)