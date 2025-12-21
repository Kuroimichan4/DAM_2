# pip install requests 

import requests #librería de peticiones HTTP get/post/put...
import xml.etree.ElementTree as ElementTree
import tkinter as tk
# la diferencia entre tk y ttk simplemente es que el ttk tiene widgets mas nuevos y/o mejorados creo
from tkinter import ttk

url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"

# def cargar_XML(url):
try:
    response = requests.get(url)
    if response.status_code == 200:
        print("Conexión exitosa")
        #print(response.content.decode('utf-8')[:500]) # supongo que también puede ser así: print(response.text[:500])
        # guardo el XML por si hay que tratar datos después o yo que sé
        xml_divisas = response.content

        # el objeto que contiene el xml
        raiz_tree = ElementTree.fromstring(xml_divisas)

        #print("hola gente",raiz_tree.tag)

        #print(raiz_tree)
        #print(raiz_tree.tag)
        #print(raiz_tree.attrib)
        #print(raiz_tree.text)
        #num = 1

        # Todas esas url's se les llama name
        #print("\n ver arbol de mierda del XML ")
        #for hijo in raiz_tree:
        #    print("\nHijos / submodulos de la raíz", hijo.tag)
        #    for nietos in hijo:
        #        print(num)
        #        print("  Nieto:", nietos.tag, "| Atributos:", nietos.attrib)
        #        num = num + 1

        direcciones_XML = {
            "gesmes": "http://www.gesmes.org/xml/2002-08-01",
            "euro": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"
        }

        cube_data = raiz_tree.find(".//euro:Cube[@time]", direcciones_XML) #aquí le mando a buscar dentro de euro, la etiqueta cube, con el atributo time

        #print("prueba fecha",cube_data)
        #print("prueba fecha atributo", cube_data.attrib)

        if cube_data is not None:
            fecha = cube_data.attrib["time"]
            #print("Fecha:", fecha)

            #print("************* Monedas? ***********")
            cambio_divisas = {}

            for cube in cube_data:
                #print(cube.attrib) #se ven los atributos así: {'currency': 'USD', 'rate': '1.1566'}
                moneda = cube.attrib["currency"]
                tasa = cube.attrib["rate"] #sale en tetxo
                # parseo
                tasa_float = float(tasa)
                # añado al diccionario
                cambio_divisas[moneda] = tasa_float
            cambio_divisas["EUR"] = 1

        else:
            print("No se ha encontrado el atributo time en el nodo de mierda")

        # prueba de que hace el cambio
        #print("Cambio EUR a USD:", cambio_divisas["USD"])
        #print("Cambio EUR a JPY:", cambio_divisas["JPY"])
        #print("Cambio EUR a EUR:", cambio_divisas["EUR"])

    else:
        print("Error al conectar con el servidor")
except Exception as e:
    print(f"Ha ocurrido un error: {e}")

def convertir(cantidad, moneda_origen, moneda_destino, cambio_divisas):
    if moneda_origen == "EUR":
        cantidad_euros = cantidad # euros = a 1
    else:
        tasa_origen = cambio_divisas[moneda_origen] # si es otra moneda...
        cantidad_euros = cantidad / tasa_origen # miro cuantas unidades de esa moneda son 1 euro con una regla de 3
        # si son yenes: 200Y / 180,57Y (que son 1€) = 1,11€

    if moneda_destino == "EUR":
        cantidad_destino = cantidad_euros
    else:
        tasa_destino = cambio_divisas[moneda_destino]
        cantidad_destino = cantidad_euros * tasa_destino #

    return cantidad_destino

#(convertir(100, "EUR", "JPY", cambio_divisas))  # debería ser > 180
#print(convertir(100, "JPY", "EUR", cambio_divisas))  # debería ser  rollo 0,55

def realizar_conversion():
    try:
        # cantidad del input
        texto_cantidad = entrada_cantidad.get()
        cantidad = float(texto_cantidad)

        # selección de divisa origen
        moneda_origen = combo_origen.get()
        moneda_destino = combo_destino.get()

        # llamar a la función convertir
        resultado = convertir(cantidad, moneda_origen, moneda_destino, cambio_divisas)

        # resultado
        lbl_resultado.config(
            text=f"{resultado:.2f} {moneda_destino}"
        )

    except ValueError:
        # Si no es número
        lbl_resultado.config(text="Introduce una cantidad numérica válida")
    except Exception as e:
        lbl_resultado.config(text=f"Error: {e}")

# los widget de ttk no se pueden modificar estéticamente directamente hay que crear un style
# si le pongo styles aquí

# *************** Interfaz **********************

ventana = tk.Tk() # crea la ventana
ventana.title("Conversor de Divisas")
ventana.geometry("400x300")
ventana.configure(bg="#555DA1")

# Campo Cantidad
#Label
lbl_cantidad = tk.Label(ventana, text="Cantidad:", bg="#555DA1", fg="white", font=("Arial", 12, "bold"))
lbl_cantidad.pack(pady=5) # el pack hace un vertical layout como en el android studio y el pady pues el padding vertical entre inputs
# Input
entrada_cantidad = tk.Entry(ventana)
entrada_cantidad.pack(pady=5)

# lista de divisas
lista_monedas = sorted(cambio_divisas.keys()) # sorted ordena alfabéticamente

#select para la divisa de origen o combobox como se le dice aquí
lbl_origen = tk.Label(ventana, text="Moneda origen:", bg="#555DA1", fg="white", font=("Arial", 12, "bold"))
lbl_origen.pack(pady=5)

combo_origen = ttk.Combobox(ventana, values=lista_monedas) # el ttk.combobox solo existe en el nuevo ttk y los values son las option del select
combo_origen.set("EUR")   # valor por defecto
combo_origen.pack(pady=5)

#select para la divisa de destino
lbl_destino = tk.Label(ventana, text="Moneda destino:", bg="#555DA1", fg="white", font=("Arial", 12, "bold"))
lbl_destino.pack(pady=5)

combo_destino = ttk.Combobox(ventana, values=lista_monedas)
combo_destino.set("JPY")  # valor por defecto
combo_destino.pack(pady=5)

# Botón para convertir
btn_convertir = ttk.Button(ventana, text="Convertir", command=realizar_conversion) #el comand es como el listener y llama a la función
btn_convertir.pack(pady=10)

# Etiqueta del resultado
lbl_resultado = tk.Label(ventana, text="0.00", bg="#555DA1", fg="white", font=("Arial", 18, "bold"))
lbl_resultado.pack(pady=10)

#esto genera la ventana y se queda ahí fija, sino se pone el mainloop se cierra y se abre todo el rato xq sí
ventana.mainloop()



