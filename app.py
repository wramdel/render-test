import os
import requests
import streamlit as st

st.set_page_config(page_title="Demo API", layout="centered")
st.title("Streamlit → FastAPI → JSON (sin BD)")

API_BASE_URL = os.getenv("API_BASE_URL", "").rstrip("/")

if not API_BASE_URL:
    st.warning("Falta la variable de entorno API_BASE_URL (en Render). Para local: export API_BASE_URL=http://localhost:8000")
    st.stop()

@st.cache_data(ttl=30)
def get_people():
    r = requests.get(f"{API_BASE_URL}/people", timeout=10)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=30)
def get_person(person_id: str):
    r = requests.get(f"{API_BASE_URL}/person/{person_id}", timeout=10)
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()

datos = get_people()
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
        st.warning("No hay datos (API devolvió vacío).")
    elif id_busqueda and id_busqueda != "(sin datos)":
        encontrado = get_person(id_busqueda)
        if encontrado:
            st.success(f"Nombre: {encontrado.get('nombre')}")
            st.json(encontrado)
        else:
            st.error("ID no encontrado")

st.divider()
st.caption(f"API: {API_BASE_URL}")
