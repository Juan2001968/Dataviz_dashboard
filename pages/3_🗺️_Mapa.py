
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from utils import load_data

st.title("🗺️ Georreferenciación por Departamento")

csv_path = st.session_state.get("csv_path", "finanzas_empresas.csv")
df = load_data(csv_path)

# Filtro por categoría y rango de valor
with st.sidebar:
    st.header("Filtros de mapa")
    cats = sorted(df["Categoría"].dropna().unique()) if "Categoría" in df.columns else []
    cat_sel = st.multiselect("Categoría", cats, default=cats)
    min_val, max_val = (float(df["Valor"].min()), float(df["Valor"].max())) if "Valor" in df.columns else (0.0, 1.0)
    val_range = st.slider("Rango de Valor", min_val, max_val, (min_val, max_val))

mask = pd.Series([True]*len(df))
if cat_sel and "Categoría" in df.columns:
    mask &= df["Categoría"].isin(cat_sel)
if "Valor" in df.columns:
    mask &= df["Valor"].between(val_range[0], val_range[1])

dff = df[mask].dropna(subset=["Latitud","Longitud"])

# Agregamos por Departamento para crear un punto promedio por dpto
if all(col in dff.columns for col in ["Departamento","Latitud","Longitud"]):
    agg = dff.groupby("Departamento").agg(
        Lat=("Latitud","mean"),
        Lon=("Longitud","mean"),
        Conteo=("Departamento","size"),
        Valor_prom=("Valor","mean")
    ).reset_index()
else:
    st.error("Faltan columnas necesarias: Departamento, Latitud y Longitud.")
    st.stop()

# Crear el mapa
if len(agg):
    center = [agg["Lat"].mean(), agg["Lon"].mean()]
else:
    center = [4.6, -74.1]

m = folium.Map(location=center, zoom_start=5)
mc = MarkerCluster().add_to(m)

for _, r in agg.iterrows():
    folium.CircleMarker(
        location=[r["Lat"], r["Lon"]],
        radius=6 + (r["Conteo"]/agg["Conteo"].max())*10,
        popup=f"{r['Departamento']}<br>Registros: {int(r['Conteo'])}<br>Valor prom: {r['Valor_prom']:.3f}",
        tooltip=r["Departamento"],
        fill=True
    ).add_to(mc)

map_state = st_folium(m, height=520, use_container_width=True, returned_objects=[])

st.caption("💡 **Interacción:** haz clic en un punto para ver detalles.")

# Mostrar tabla vinculada (ordenada por valor promedio)
st.subheader("Resumen por Departamento")
st.dataframe(agg.sort_values("Valor_prom", ascending=False), use_container_width=True)
