# pip install requests beautifulsoup4 pandas streamlit para instalar las dependencias
# para guardar los datos  recordar guardarlos en data: data/datos.csv o como quiera llamarle
import requests
from bs4 import BeautifulSoup
import requests
import pandas as pandas
from urllib.parse import urljoin # para convertir a url

# BeautifulSoup: Analiza el HTML de páginas estáticas para extraer información
# Pandas: trata los datos del csv
# stramlit: framwork de python para crear dashboards interactivos a partir de datos

respPag = requests.get("https://books.toscrape.com/", headers={"User-Agent": "Miriam - pract_scraping_dashboard"})
# esto manda una petición http a la pag como si se abriera desde el navegador y guarda el texto en la variable
# headers es simplemenmte para identificarnos ante el servidor para indicar quienes somos y que estamos haciendo
soup = BeautifulSoup(respPag.content, "html.parser")
# convierte el texto plano del HTML (resp.text) en una estructura de árbol de objetos que Python puede recorrer. Ahora soup representa toda la página web como una especie de árbol con etiquetas

productos = soup.select(".product_pod") #buscará todos los elementos de la página con ese nombre de clase y devolverá una lista que representará cada producto

lista = []

for producto in productos:
    titulo = producto.select_one("h3").get_text(strip=True)
    # select_one() es como el select pero devuelve el primer resultado que encuentra, usando selectores CSS. En este caso pilla el titulo que es el únoco h3 que veo en cada div de los libros
    # get_text() extrae solo el texto que hay dentro de la etiqueta HTML, eliminando las etiquetas <a>, <p>, etc.
    # strip=True elimina espacios, saltos de línea o tabulaciones al principio y al final del texto
    # también se podría usar otras funciones para hacer lo mismo: it.find("h3", class_="title")
    precio = producto.select_one(".price_color").get_text(strip=True)
    rating = len(producto.select("i.icon-star"))
    stock = producto.select_one(".instock.availability").get_text(strip=True)
    portada = urljoin("https://books.toscrape.com/",producto.select_one("img.thumbnail").get("src"))

    lista.append({"titulo": titulo, "precio": precio, "rating": rating, "stock": stock, "portada": portada})

    pandas.DataFrame(lista).to_csv("datos.csv", index=False, encoding="utf-8-sig", sep=";")
    # Convierte la lista en un DataFrame (una tabla).
    # index=false se pone xq DataFrame pone index autoáticamnete y si no se pone en false, lo añade a la tabla de forma automática en una columna extra
    # utf-8 → codifica bien, pero Excel (Windows) no siempre lo reconoce.
    # utf-8-sig → añade un BOM (Byte Order Mark) al principio del archivo.



