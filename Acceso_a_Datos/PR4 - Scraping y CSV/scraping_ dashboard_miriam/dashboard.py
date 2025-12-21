 # para runear, escribir en terminal: streamlit run dashboard.py
 # Imports + Config
 # Carga de datos (con cache)
 # Panel de filtros (sidebar)
 # Resultados: métricas, tabla, gráficos, extras

import streamlit as st
import pandas as pands

st.set_page_config(page_title="scraping_dashboard_miriam", layout="wide") # con esto se configura la página con su titulo y el ancho
st.title("Scraping_dashboard_miriam") #titulo que se verá en la pestaña del navegador
st.caption("analisis y visualización de los datos de una página") # texto pequeño bajo el titulo

def carga_datos():
    dataFrame = pands.read_csv("datos.csv", sep=";", encoding="utf-8-sig")

    if "precio" in dataFrame.columns:
        dataFrame["precio"] = (
            dataFrame["precio"]
            .astype(str)
            .str.replace("Â", "", regex=False)  # por si viniera “Â£…”
            .str.replace("£", "", regex=False)  # quita el símbolo
            .str.replace(",", ".", regex=False)  # por si hubiera coma decimal
            .str.strip()
        )
        dataFrame["precio"] = pands.to_numeric(dataFrame["precio"], errors="coerce")

    if "rating" in dataFrame.columns:
        dataFrame["rating"] = pands.to_numeric(dataFrame["rating"], errors="coerce")

    return dataFrame

dataFrame = carga_datos() #se cargan los datos

# ----------- filtro del usuario
st.sidebar.header("Filtros") # titulo dentro del panel lateral

op_stock = ["Todos", "In stock", "Out stock"]
sel_stock = st.sidebar.selectbox("Disponibilidad", op_stock) # selectbox muestra un menú desplegable

# filtro precio

precio_min = float(dataFrame["precio"].min())
precio_max = float(dataFrame["precio"].max())

rango_precio = st.sidebar.slider(
    "Selecciona el rango de precios",
    min_value=precio_min,
    max_value=precio_max,
    value=(precio_min, precio_max)
)
# sidebar.slider: crea un control deslizante en la barra lateral
# la primera línea es el titulo que verá el usuario
# el value del final es el rango por defecto y el rango_precio devolverrá una tupla con 2 nums

condición_precio = (dataFrame["precio"] >= rango_precio[0]) & (dataFrame["precio"] <= rango_precio[1])

# rating
tiene_rating = "rating" in dataFrame.columns
if tiene_rating:
    ratings_unicos = sorted([int(x) for x in dataFrame["rating"].dropna().unique().tolist()]) # dropna quita los nulos
    sel_rating = st.sidebar.multiselect(
        "Rating", options=ratings_unicos, default=ratings_unicos
    )
else:
    sel_rating = None


# ----------- aplicar filtros

dataFrame_filtrado = dataFrame.copy()

# stock filtro
if sel_stock == "In stock":
    dataFrame_filtrado = dataFrame_filtrado[
        dataFrame_filtrado["stock"].str.contains("In stock", case=False, na=False)
        # el str se pone para aplicar funciones string, case=False ignora mayus y minus y na=False es para los nulos
        # dataFrame_filtrado = ~dataFrame["stock"].str.contains("In stock", case=False, na=False) Al poner ~ delante de una serie de booleans, se invierten los valores
    ]
elif sel_stock == "Out stock":
    dataFrame_filtrado = dataFrame_filtrado[
        ~dataFrame_filtrado["stock"].str.contains("In stock", case=False, na=False)
        # dataFrame_filtrado = ~dataFrame["stock"].str.contains("In stock", case=False, na=False) Al poner ~ delante de una serie de booleans, se invierten los valores
    ]

# filtro precio
dataFrame_filtrado = dataFrame_filtrado[
    (dataFrame_filtrado["precio"] >= rango_precio[0]) &
    (dataFrame_filtrado["precio"] <= rango_precio[1])
]

if tiene_rating and sel_rating:
    df_filtrado = dataFrame_filtrado[dataFrame_filtrado["rating"].isin(sel_rating)]


# --------- tabla result

st.subheader("Estadísticas")

num_libros = len(dataFrame_filtrado)
precio_medio = round(dataFrame_filtrado["precio"].mean(), 2) if num_libros else 0
# .mean calcula la media de la columna que hayamos seleccionado e ignora NaN
# round(valor, 2) redondea a 2 los decimales
rating_medio = (
    round(df_filtrado["rating"].mean(), 2) if (num_libros and tiene_rating) else 0
)

col1, col2, col3 = st.columns(3)
col1.metric("Número de libros", num_libros)
col2.metric("Precio medio (£)", precio_medio)
if tiene_rating:
    col3.metric("Rating medio", rating_medio)

st.subheader("📋 Tabla de resultados")
st.dataframe(dataFrame_filtrado, use_container_width=True)

# if num_libros and "portada" in dataFrame_filtrado.columns:
#    st.image(dataFrame_filtrado["portada"].iloc[0])

if num_libros and "portada" in dataFrame_filtrado.columns:
    st.subheader("Portada de muestra")
    # Evita error si la URL está vacía o NaN
    primera_portada = dataFrame_filtrado["portada"].dropna().astype(str).head(1)
    if not primera_portada.empty:
        st.image(primera_portada.iloc[0], width=180)

# Botón de descarga del CSV filtrado
st.download_button(
    label="Descargar CSV filtrado",
    data=dataFrame_filtrado.to_csv(index=False, sep=";", encoding="utf-8-sig"),
    file_name="datos_filtrados.csv",
    mime="text/csv",
)