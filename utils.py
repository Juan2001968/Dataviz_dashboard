
import pandas as pd
from pathlib import Path
import streamlit as st

@st.cache_data(show_spinner=False)
def load_data(csv_path: str):
    df = pd.read_csv(csv_path)
    # Normalize column names for robustness
    rename_map = {}
    for col in df.columns:
        low = col.lower()
        if low.startswith("depa"):
            rename_map[col] = "Departamento"
        elif "lat" in low:
            rename_map[col] = "Latitud"
        elif "lon" in low or "lng" in low:
            rename_map[col] = "Longitud"
        elif low in ("valor","monto","amount","value"):
            rename_map[col] = "Valor"
    df = df.rename(columns=rename_map)
    # Basic types
    if "Latitud" in df.columns: df["Latitud"] = pd.to_numeric(df["Latitud"], errors="coerce")
    if "Longitud" in df.columns: df["Longitud"] = pd.to_numeric(df["Longitud"], errors="coerce")
    return df
