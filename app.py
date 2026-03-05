import json
from pathlib import Path
import streamlit as st

DATA_PATH = Path(__file__).with_name("data.json")

@st.cache_data
def cargar_datos():
    if not DATA_PATH.exists():
        return []
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

st.set_page_config(page_title="Demo JSON", layout="centered")
st.title("Demo: Streamlit + JSON (sin BD)")

datos = cargar_datos()
ids = [str(x.get("id")) for x in datos]

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Búsqueda")
    modo = st.radio("Modo", ["Selector", "Escribir ID"], horizontal=False)

    if modo == "Selector":
        id_busqueda = st.selectbox("ID", options=ids if ids else ["(sin datos)"])
    else:
        id_busqueda = st.text_input("ID", value="1").strip()

with col2:
    st.subheader("Resultado")
    if not datos:
        st.warning("No hay datos. Revisa data.json")
    elif id_busqueda and id_busqueda != "(sin datos)":
        encontrado = next((x for x in datos if str(x.get("id")) == id_busqueda), None)
        if encontrado:
            st.success(f"Nombre: {encontrado.get('nombre')}")
            st.json(encontrado)
        else:
            st.error("ID no encontrado")

st.divider()
st.caption(f"Fuente: {DATA_PATH.name}")