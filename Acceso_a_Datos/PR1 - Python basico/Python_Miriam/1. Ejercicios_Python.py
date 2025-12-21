# 1- Escribe un programa que llame 2 veces a la función print() para mostrar en líneas separadas tu nombre completo. En la 1ra línea aparecerá el nombre y en la siguiente los apellidos.

print("Miriam")
print("Hernández Navarro")

# 2- Modifica el programa anterior para que el nombre y los apellidos se muestren en la misma línea. Sigue llamando 2 veces a la función print(). Usa el parámetro end.

print("Miriam", end=' ')
print("Hernández Navarro")
#  end es un argumento que se usa para definir qué carácter se usará al final de la impresión. Por defecto es un salto de línea (\n).

# 3- Con un solo print() muestra tu nombre completo de forma que entre cada palabra aparezca un guión bajo o underscore ("_"). Usa el parámetro sep.

print("Miriam", "Hernández", "Navarro", sep='_')
# sep es un argumento que se usa para separar los elementos que se pasan a print. Por defecto es un espacio en blanco.

# 4- Modifica el programa anterior para que usando algún código de escape se muestre una palabra por línea. Sólo debes usar un print()

print("Miriam\n Hernández\n Navarro")

# Modifica el programa anterior para añadir tu número de teléfono en una nueva línea. Sólo debes usar un print().

print("Miriam\nHernández\nNavarro\n", 680331932)

# Escribe en 2 columnas una lista de elementos. En la columna de la izquierda aparecerá el nombre de un producto y en la de la derecha su precio en euros (con decimales). Las palabras deben estar alineadas a la izquierda. Usa colores diferentes para los títulos de columna, para las frutas y para los importes.

colorTitulo = "\033[1;34m" # Código ANSI para el azul
colorTexto = "\033[1;32m" # verde

# mini-lenguaje de formato de Python dentro de f-strings, que te deja fijar ancho y alineado por columna: {valor: [relleno][alineado][ancho][.precisión][tipo]}
# alineado: < izquierda, > derecha, ^ centrado
# ancho: número de caracteres a reservar
# relleno (opcional): un carácter para rellenar espacios (por defecto espacio)
# .precisión / tipo: para números (.2f = 2 decimales, , separador miles, etc.)

# lista de tuplas. Aunque también se podría hacer con un diccionario o lista de objetos y tal
# diccionario: precios = dict(items)  # {"Manzana": 1.2, "Plátano": 0.8, ...}

productos = [
    ("Manzana", 0.50), 
    ("Plátano", 0.30), 
    ("Naranja", 0.40), 
    ("Pera", 0.60), 
    ("Mango", 1.60)
]

print(f"{colorTitulo}{'Producto':<15}{'Precio':>10}")
print("-" * 25)
for producto, precio in productos:
    print(f"{colorTexto}{producto:<15} | {precio:>5.2f} €")

# También se puede hacer así, definiendo una variable para el espacio entre columnas
# espacioEntreValores = 15
# for producto, precio in productos:
#     print(f"{colorTexto}{producto:<{espacioEntreValores}} | {precio:>5.2f} €")

#  7- Escribe un programa que calcule el precio final de un producto según:
    # • La base imponible (precio antes de impuestos)
    # • El tipo de IVA aplicado. Puede ser: general (21%), reducido (10%) o superreducido (4%).
    # • El código promocional. Los códigos promocionales pueden ser: sinpromo (no se aplica promoción), mitad (el precio se reduce a la mitad), descfijo (se descuentan 5 euros) o porcentaje (se descuenta el 5%).

base= float(input("Introduce la base imponible (precio antes de impuestos): "))
tipoIVA = input("Introduce el tipo de IVA (general, reducido, superreducido): ").lower()
codigoPromo = input("Introduce el código promocional (sinpromo, mitad, descfijo, porcentaje): ").lower()

if tipoIVA == "general":
    iva = 0.21
elif tipoIVA == "reducido":
    iva = 0.10
elif tipoIVA == "superreducido":
    iva = 0.04
else:
    print("Tipo de IVA no válido. Se aplicará el tipo general (21%).")
    iva = 0.21
    
precioConIVA = base * (1 + iva) # al hacer 1+iva, se suma el 100% del precio más el porcentaje del IVA es como multiplicar por 1.21, 1.10 o 1.04

if codigoPromo == "sinpromo":
    total = precioConIVA
elif codigoPromo == "mitad":
    total = precioConIVA / 2
elif codigoPromo == "descfijo":
    total = precioConIVA - 5
elif codigoPromo == "porcentaje":
    total = precioConIVA * 0.95  # equivalente a restar el 5%
else:
    print("Código promocional no válido. No se aplicará promoción.")
    total = precioConIVA
    
print('El precio final es: ', total)


# Tambien se puede hacer mas compactro el código usando diccionarios para los tipos de IVA y códigos promocionales:
# tiposIVA = {"general": 0.21, "reducido": 0.10, "superreducido": 0.04}
# iva = tiposIVA.get(tipoIVA, 0.21)  # si no está el tipo, se aplica el general (21%)
# códigosPromo = {"sinpromo": lambda x: x, "mitad": lambda x: x / 2, "descfijo": lambda x: x - 5, "porcentaje": lambda x: x * 0.95}
    # if tipoIVA not in tipos:
    #     print("Tipo de IVA no válido. Se aplicará el tipo general (21%).")

    # precioConIVA = base * (1 + iva)

    # promos = {
    #     "sinpromo": lambda x: x,
    #     "mitad":    lambda x: x / 2,
    #     "descfijo": lambda x: x - 5,
    #     "porcentaje": lambda x: x * 0.95,
    # }
    # f = promos.get(codigoPromo)
    # if f is None:
    #     print("Código promocional no válido. No se aplicará promoción.")
    #     total = precioConIVA
    # else:
    #     total = f(precioConIVA)

    # return max(total, 0.0) 

# 8- Realiza un programa que:
    # Pida números hasta que se introduzca un numero negativo
    # Tras introducir un número negativo el programa deberá mostrar:
        # Cuantos números se han introducido,
        # la media de los impares y
        # el mayor de los pares.
        # El número negativo sólo se utiliza para indicar el final de la introducción de datos pero no se incluye en los cálculos.
contador = 0
contadorImpares = 0
sumaImpares = 0
MayorPar = 0  
num = 0 
        
print("Introduce los números que quieras (negativo para terminar):")

while num >= 0:
    num = int(input())
    if num >= 0:  # para no contar el negativo
        contador += 1
        if num % 2 == 0: # si el resto da 0 al dividirlo por 2, es par
            if num > MayorPar:  # si el número es mayor que el mayor par actual
                MayorPar = num
        else:  # es impar
            sumaImpares += num  # suma de los impares
            contadorImpares += 1  # cuenta de los impares
            
# Como python va por identación y no hace falta nada para indicar el fin del while

if contadorImpares > 0:
    mediaImpares = sumaImpares / contadorImpares

print("Has introducido", contador, "números.")
print('La media de los impares introducidos es: ', mediaImpares)
print('El mayor de los pares introducidos es: ', MayorPar)

# 9- Realiza un programa que intente adivinar una contraseña que el sistema conoce (la que tu decidas). 
# Hay 3 oportunidades para conseguirlo. En cada intento fallido, el programa debe preguntar si quieres continuar o abandonar. 
# Al finalizar los 3 intentos, si no se ha adivinado la contraseña debe aparecer un mensaje que indique que la cuenta se ha bloqueado, y que se debe contactar con el administrador para reactivarla.

password = 'kaladin'

for intento in range(1, 4):   #intentos  1,2,3
    respuesta = input("Introduce la contraseña: ").lower()
    if respuesta == password:
        print("Contraseña correcta. Has accedido al sistema.")
        break
    print("Contraseña incorrecta.")
        
else:
    # Este else se ejecuta si no se hizo break (es decir, se agotaron los intentos)
    print("Has agotado los 3 intentos. La cuenta se ha bloqueado. Contacta con el administrador para reactivarla.")
    
    
    
# 10- Escribe un programa que pida 8 palabras y las almacene en un array. A continuación, las palabras correspondientes a colores se deben almacenar al comienzo y las que no son colores a continuación.
# Los colores que conoce el programa deben estar en otro array y son los siguientes: verde, rojo, azul, amarillo, naranja, rosa, negro, blanco y morado.

print("Dime 8 palablas (pueden ser colores, objetos o cualquier cosa): ")

coloresBase = ['verde', 'rojo', 'azul', 'amarillo', 'naranja', 'rosa', 'negro', 'blanco', 'morado']

palabrasArray = []
coloresArray = []

ordenArray = []

for i in range(1, 9):
    word = input(f"{i}. ").lower()
    if word in coloresBase:
        coloresArray.append(word)
    else:
        palabrasArray.append(word)
    

ordenArray.extend(coloresArray)
ordenArray.extend(palabrasArray)

print('La lista ordenada sería: ')
    
for index, w in enumerate(ordenArray):
    print(index + 1, w)
    
# 11- Crea una función para el ejercicio 7. La función deberá recibir los siguientes parámetros (base imponible, tipo de IVA y código promocional) y mostrará por pantalla la información correspondiente.
# Crea una función para el ejercicio 10 que reciba como parámetro la password de sistema (que el usuario deberá intentar adivinar). 
# La función deberá devolver un string que indique si se ha adinidado la contraseña o no, cuántos intentos se han realizado y si se ha bloqueado la cuenta (sólo en caso de que no se acierte la password)
# Crea un programa principal que llame a estas funciones. Hazlo mediante un menú de 2 opciones, más una 3ra para "Salir".
# El programa principal deberá interaccionar con el usuario (si es necesario) para obtener los parámetros de entrada que se necesiten y, 
# en el caso del ejercicio 10, deberá recoger el string retornado y mostrarlo por pantalla.

def calcularPrecioFinal(base, tipoIVA, codigoPromo):
    if tipoIVA == "general":
        iva = 0.21
    elif tipoIVA == "reducido":
        iva = 0.10
    elif tipoIVA == "superreducido":
        iva = 0.04
    else:
        print("Tipo de IVA no válido. Se aplicará el tipo general (21%).")
        iva = 0.21
        
    precioConIVA = base * (1 + iva) # al hacer 1+iva, se suma el 100% del precio más el porcentaje del IVA es como multiplicar por 1.21, 1.10 o 1.04

    if codigoPromo == "sinpromo":
        total = precioConIVA
    elif codigoPromo == "mitad":
        total = precioConIVA / 2
    elif codigoPromo == "descfijo":
        total = precioConIVA - 5
    elif codigoPromo == "porcentaje":
        total = precioConIVA * 0.95  # equivalente a restar el 5%
    else:
        print("Código promocional no válido. No se aplicará promoción.")
        total = precioConIVA
        
    return total

def adivinanza(password):

    for intento in range(1, 4):   #intentos  1,2,3
        respuesta = input("Introduce la contraseña: ").lower()
        if respuesta == password.lower():
            # print("Contraseña correcta. Has accedido al sistema.")
            return f"Contraseña correcta. Has accedido al sistema en {intento} intento(s)." #también se puede hacer así
        print("Contraseña incorrecta.")
            
    else:
        # Este else se ejecuta si no se hizo break (es decir, se agotaron los intentos)
        return "Has agotado los 3 intentos. La cuenta se ha bloqueado. Contacta con el administrador para reactivarla"
        
def main():
    while True:
        print("\nMenú:")
        print("1. Calcular precio final de un producto")
        print("2. Adivinar la contraseña")
        print("3. Salir")
        
        op = input("Elige una opción (1, 2 o 3): ")
        
        match op:
            case '1':
                base= float(input("Introduce la base imponible (precio antes de impuestos): "))
                tipoIVA = input("Introduce el tipo de IVA (general, reducido, superreducido): ").lower()
                codigoPromo = input("Introduce el código promocional (sinpromo, mitad, descfijo, porcentaje): ").lower()
                
                total= calcularPrecioFinal(base, tipoIVA, codigoPromo)
                print('El precio final es: ',total)
            
            case '2':
                password = 'kaladin'
                resultado = adivinanza(password)
                print(resultado)
                
            case '3':
                print("Saliendo del programa...")
                break   
            
            case _: # este es el default en python
                print("Opción no válida. Por favor, elige 1, 2 o 3.")
        
main()
        
        
        #  en python no hace falta el main() para que funcione, pero es una buena práctica al parecer
        #  Tampoco exixtiía el switch pero en python 3.10 se añadió el match-case que se usa así:
        # match opcion: 
        #     case '1':
        # case _ es el “default”
        
        
# 13- Crea la clase coche de M3 en Python

from enum import Enum # esto es para crear los enum
from datetime import datetime, date # esto es para fechas como java.time.LocalDate, java.time.LocalDateTime, java.time.format.DateTimeFormatter de java

class ColorEnum(Enum):
    ROJO = "rojo"
    AZUL = "azul"
    VERDE = "verde"
    NEGRO = "negro"
    BLANCO = "blanco"


class MotorEnum(Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    HIBRIDO = "hibrido"
    ELECTRICO = "electrico"

class Coche:
    # aquí van lois atributos
    # ruedas = 4  # atributo de clase, esto lo pondría si todas las instancias van a tener el mismo valor
    
    MAX = 120.0  # velocidad máxima
    
    # __init__ es el constructor en Python (equivalente a public Coche(...) en Java)
    def __init__(this, marca: str, placa: str, modelo: str, power: int, capacity: int, color: ColorEnum, motor: MotorEnum, speed: float, fabricationDate: str, numDors: int, peso: float): 
        # en python se usa self y no this normalmente, pero en pytjon puedes seleccionar la palabra que quieras
        this._marca = marca
        this._placa = placa
        this._modelo = modelo
        this._power = power
        this._capacity = capacity
        this._color = color
        this._motor = motor
        this._speed = 0.0  # velocidad inicial
        this.speed = speed  # usa el setter para validar la velocidad inicial
        this._fabricationDate = fabricationDate
        this._numDors = numDors
        this._peso = peso
        
#  Getters y Setters (en python se usan @property y @atributo.setter)
# @property crea un getter en Python.
# @variable.setter crea un setter.
# El _marca con guion bajo es una convención para decir “atributo privado”. (En Python no existen private/protected, todo es público, pero se usa _ para indicar que no deberías tocarlo directamente).
    @property # getter
    def marca(this): 
        return this._marca
            # esto también se podría hacer así si quisiera poner que acepte nulos
            # def marca(self) -> str | None: return self._marca
    @marca.setter # setter
    def marca(this, value):
        this._marca = value
        
    @property
    def placa(this):
        return this._placa
    @placa.setter
    def placa(this, value):
        this._placa = value
        
    @property
    def modelo(this):
        return this._modelo 
    @modelo.setter
    def modelo(this, value):
        this._modelo = value

    @property
    def power(this):
        return this._power
    @power.setter
    def power(this, value):
        this._power = value

    @property
    def capacity(this):
        return this._capacity
    @capacity.setter
    def capacity(this, value):
        this._capacity = value
        
    @property
    def color(this):
        return this._color
    @color.setter
    def color(this, value):
        this._color = value
        
    @property
    def motor(this):
        return this._motor
    @motor.setter
    def motor(this, value):
        this._motor = value
        
    @property
    def speed(this):
        return this._speed
    @speed.setter
    def speed(this, value: float):
        v = float(value)
        if v >= this.MAX:
            this._speed = this.MAX
        elif v < 0:
            this._speed = 0.0
        else:
            this._speed = v

    @property
    def fabricationDate(this):
        return this._fabricationDate
    @fabricationDate.setter
    def fabricationDate(this, value):
        this._fabricationDate = value
        
    @property
    def numDors(this):
        return this._numDors
    @numDors.setter
    def numDors(this, value):
        this._numDors = value
        
    @property
    def peso(this):
        return this._peso
    @peso.setter
    def peso(this, value):
        this._peso = value
        
    # métodos ------------------------------------------------------------------------
    def acelerar(this):
        this.speed = this.speed + 10
        return this.speed

    def frenar(this):
        this.speed = this.speed - 10
        return this.speed

    # __str__ en Python es lo mismo que toString() en Java ------------------------
    def __str__(this):
        componentes: list[str] = []
        componentes.append("Información del coche: ")
        if this.marca: componentes.append(f"Marca: {this.marca}")
        if this.placa: componentes.append(f"Placa: {this.placa}")
        if this.modelo: componentes.append(f"Modelo: {this.modelo}")
        if this.power: componentes.append(f"Potencia: {this.power} CV")
        if this.capacity: componentes.append(f"Cilindrada: {this.capacity} cc")
        if this.color: componentes.append(f"Color: {this.color.value}")
        if this.motor: componentes.append(f"Motor: {this.motor.value}")
        if this.speed: componentes.append(f"Velocidad actual: {this.speed} km/h")
        if this.fabricationDate: componentes.append(f"Fecha de fabricación: {this.fabricationDate}")
        if this.numDors: componentes.append(f"Número de puertas: {this.numDors}")
        if this.peso: componentes.append(f"Peso: {this.peso} kg")
        componentes.append("Fin de la información del coche.")
        return "\n".join(componentes)  # une los elementos de la lista con saltos de línea