import csv
import os

alumnos = {} # Diccionario para almacenar los datos de los alumnos
uf1_y_uf2 = 'Notas_Alumnos_UF1yUF2.csv'
carpeta = 'FicherosCSV_reader_writer'
ruta = os.path.join(os.getcwd(), carpeta) # os.getcwd() obtiene la ruta actual donde estamos ejecutando el script
columnas = ["Id", "Nombre", "Apellidos", "UF1", "UF2"]

def csv_reader_writer():
    with open("Notas_Alumnos_UF1.csv","r") as file:
        contenido = csv.reader(file, delimiter=";")
        next(contenido)
        for fila in contenido:
            # print('ID: ', fila[0], ', Nombre: ', fila[2], ', Apellidos: ', fila[1], 'notas: ', fila[3])
            id = fila[0].strip()
            apellido = fila[1].strip()
            nombre = fila[2].strip()
            uf1 = fila[3].strip()

            alumnos[id] = {
                "Id": id,
                "Nombre": nombre,
                "Apellidos": apellido,
                "UF1": uf1,
                "UF2": ""  
            }
        
    with open("Notas_Alumnos_UF2.csv","r") as file:
        contenido = csv.reader(file, delimiter=";")
        next(contenido)
        for fila in contenido:
            # print(fila[0], ', Nombre: ', fila[2], fila[1], 'notas: ', fila[3])
            id = fila[0].strip()
            uf2 = fila[3].strip()

            if id in alumnos:
                alumnos[id]["UF2"] = uf2
                
            else:
                apellido = fila[1].strip()
                nombre = fila[2].strip()
                alumnos[id] = {
                    "Id": id,
                    "Nombre": nombre,
                    "Apellidos": apellido,
                    "UF1": "",
                    "UF2": uf2  
                }
    
    try:
        if not os.path.exists(ruta):
            os.mkdir(carpeta)
            
        with open(os.path.join(ruta, uf1_y_uf2), "w", newline='') as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(columnas) # primero escribimos la cabecera
                
            for row in alumnos.values():
                writer.writerow([row["Id"], row["Nombre"], row["Apellidos"], row["UF1"], row["UF2"]])
                
        print(f'Fichero creado en: {os.path.join(ruta, uf1_y_uf2)}')
        
    except Exception as e:
        print('Ha ocurrido un error: ', e)
    except FileNotFoundError:
        print('No se ha encontrado el fichero')
    except PermissionError:
        print('No tienes permisos para leer el fichero')
        
alumnos_dict = {}
carpeta_dict = 'FicherosCSV_dictreader_dictwriter'
ruta_dict = os.path.join(os.getcwd(), carpeta_dict) 

def csv_dictreader_dicwriter():
    with open("Notas_Alumnos_UF1.csv","r") as file:
        contenido = csv.DictReader(file, delimiter=";")
        
        for fila in contenido:
            id = fila["Id"].strip()
            apellido = fila["Apellidos"].strip()
            nombre = fila["Nombre"].strip()
            uf1 = fila["UF1"].strip()

            alumnos[id] = {
                "Id": id,
                "Nombre": nombre,
                "Apellidos": apellido,
                    "UF1": uf1,
                    "UF2": "" 
            }
    
    with open("Notas_Alumnos_UF2.csv","r") as file:
        contenido = csv.DictReader(file, delimiter=";")
        
        for fila in contenido:
            id = fila["Id"].strip()
            apellido = fila["Apellidos"].strip()
            nombre = fila["Nombre"].strip()
            uf2 = fila["UF2"].strip()

            if id in alumnos:
                alumnos[id]["UF2"] = uf2
                
            else:
                alumnos[id] = {
                    "Id": id,
                    "Nombre": nombre,
                    "Apellidos": apellido,
                    "UF1": "",
                    "UF2": uf2  
                }
        
        try:
            os.makedirs(ruta_dict, exist_ok=True)
            
            with open(os.path.join(ruta_dict, uf1_y_uf2), "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=columnas, delimiter=";")
                
                if file.tell() == 0: # Si el fichero está vacío, escribimos la cabecera
                    writer.writeheader() # primero escribimos la cabecera
                
                for datos in alumnos.values():
                    writer.writerow(datos) 
            
        except Exception as e:
            print('Ha ocurrido un error: ', e)
        except FileNotFoundError:
            print('No se ha encontrado el fichero')
        except PermissionError:
            print('No tienes permisos para leer el fichero')   
    
if __name__ == "__main__":
    
    csv_reader_writer()
    csv_dictreader_dicwriter()
    print("Ficheros creados correctamente")