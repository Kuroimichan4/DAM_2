# pàra que funcione colab primero poner esto en una celda:
# !pip install cryptography

# después esto encima del codigo:
# %%writefile keytool_miriam.py 
# %%writefile keytool_miriam.py sirve para guardar el código en un archivo llamado keytool_miriam.py en el entorno de Jupyter Notebook que estés usando. es decir, si ejecutas este código en una celda de google colab o jupyter notebook, se creará un archivo con ese nombre que contendrá todo el código que sigue a esa línea.
# !/usr/bin/env python3 sirve para indicar que este script debe ejecutarse con Python 3
from __future__ import annotations

import argparse
import base64
import getpass
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, List

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography import x509
from cryptography.x509.oid import NameOID

# =-----------------------------
# Parámetros de seguridad
# -------------------+------------------------
PBKDF2_ITERS = 200_000
SALT_BYTES = 16
NONCE_BYTES = 12
MIN_PASS_LEN = 6

#-------------------------------------
# Funciones basicas de parseo y criptografía
#--------------------------------

def bytes64_a_texto(data: bytes) -> str: # esto es para convertir bytes a texto base64. Esto lo usamos para guardar datos binarios en formato texto dentro del keystore JSON,
    return base64.b64encode(data).decode("ascii")

def texto_a_bytes64(text: str) -> bytes: # esto es para convertir texto base64 a bytes
    return base64.b64decode(text.encode("ascii"))

def pedir_password_oculta(prompt: str) -> str: # pide una contraseña sin mostrarla en pantalla para que no se vea ni se quede en el historial
    return getpass.getpass(prompt)

def derivar_clave_desde_password(password: str, salt: bytes, length: int = 32) -> bytes: # genera una clave segura a partir de una contraseña y una salt(es un valor aleatorio que añade seguridad) es como concatenar la contraseña con un randomMath o lo que sea
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=length, salt=salt, iterations=PBKDF2_ITERS) #kdf es un objeto que implementa el algoritmo PBKDF2 con HMAC-SHA256. PB KDF es una función que toma una contraseña y la convierte en una clave segura. HMAC es un método para asegurar la integridad de los datos usando una clave secreta
    return kdf.derive(password.encode("utf-8")) # PBKDF2 y SHA-256 son algoritmos de derivación de claves y hash seguros 

        
def pedir_password_y_verificar(texto1: str, texto2: str, min_len: int = MIN_PASS_LEN) -> str: # pide una contraseña dos veces y verifica que coincidan y que tengan la longitud mínima

    while True:
        pass1 = pedir_password_oculta(texto1)
        pass2 = pedir_password_oculta(texto2)
        if len(pass1) < min_len:
            print(f"[!] La contraseña debe tener al menos {min_len} caracteres.")
            continue
        if pass1 != pass2:
            print("[!] Las contraseñas no coinciden. Inténtalo de nuevo.")
            continue
        return pass1


def encrypta(key: bytes, plaintext: bytes, aad: Optional[bytes] = None) -> Dict[str, str]: #Cifra el contenido del keystore y su contenido. Cifra datos usando AES-GCM(un método seguro de cifrado simétrico que usa la misma clave para cifrar y descifrar) 
    nonce = os.urandom(NONCE_BYTES)
    textoCifrado = AESGCM(key).encrypt(nonce, plaintext, aad)
    return {"nonce": bytes64_a_texto(nonce), "ciphertext": bytes64_a_texto(textoCifrado)}

def desencrypta(key: bytes, nonce_b64: str, ciphertext_b64: str, aad: Optional[bytes] = None) -> bytes: # descifra datos usando AES-GCM( el mismo método que arriba pero a la inversa para recuperar los datos originales)
    return AESGCM(key).decrypt(texto_a_bytes64(nonce_b64), texto_a_bytes64(ciphertext_b64), aad)

# *-------------------------------
# Keystore
# ----------------------------

@dataclass
class KeyItem: # representa una clave guardada en el keystore en forma de objeto
    algorithm: str
    created_at: float
    public_key_pem: str
    subject_dn: Optional[str]
    enc_private: Dict[str, str]

class StoreFile: # maneja la carga, guardado y manipulación del keystore cifrado en un archivo Json
    def __init__(self, path: str):
        self.path = path
        self._inner: Dict[str, Any] = {"version": 1, "items": {}}

    def exists(self) -> bool: # verifica si el archivo del keystore existe
        return os.path.isfile(self.path)

    def crearKeystore(self, store_password: str) -> None: # crea un nuevo keystore cifrado con la contraseña proporcionada
        if self.exists():
            raise RuntimeError("El keystore ya existe.")
        self.guardarKeystore(store_password)

    def abrir_Keystore(self, store_password: str) -> None: # carga y descifra el keystore desde el archivo usando la contraseña proporcionada
        with open(self.path, "rb") as f:
            wrapper = json.loads(f.read().decode("utf-8"))
        if not all(k in wrapper for k in ("kdf_salt", "nonce", "ciphertext")):
            raise RuntimeError("Keystore inválido o no cifrado.")
        store_salt = texto_a_bytes64(wrapper["kdf_salt"])
        store_key = derivar_clave_desde_password(store_password, store_salt)
        plain = desencrypta(store_key, wrapper["nonce"], wrapper["ciphertext"], aad=b"store")
        self._inner = json.loads(plain.decode("utf-8"))

    def guardarKeystore(self, store_password: str) -> None: # cifra y guarda el keystore en el archivo usando la contraseña proporcionada
        store_salt = os.urandom(SALT_BYTES)
        store_key = derivar_clave_desde_password(store_password, store_salt)
        plain = json.dumps(self._inner).encode("utf-8")
        enc = encrypta(store_key, plain, aad=b"store")
        wrapper = {
            "kdf": "PBKDF2-HMAC-SHA256",
            "iterations": PBKDF2_ITERS,
            "kdf_salt": bytes64_a_texto(store_salt),
            "nonce": enc["nonce"],
            "ciphertext": enc["ciphertext"],
        }
        with open(self.path, "wb") as f:    
            f.write(json.dumps(wrapper, indent=2).encode("utf-8"))

    def add_clave_a_keystore(self, alias: str, item: KeyItem) -> None: # añade una nueva clave al keystore bajo el alias especificado
        items = self._inner["items"]
        if alias in items:
            raise RuntimeError(f"El alias '{alias}' ya existe.")
        items[alias] = {
            "algorithm": item.algorithm,
            "created_at": item.created_at,
            "public_key_pem": item.public_key_pem,
            "subject_dn": item.subject_dn,
            "enc_private": item.enc_private,
        }

    def get_clave_keystore(self, alias: str) -> Dict[str, Any]: # recupera una clave del keystore usando el alias 
        try:
            return self._inner["items"][alias]
        except KeyError:
            raise RuntimeError(f"No existe el alias '{alias}'.")

# ------------------------------------------------------
# DN y SAN son objetos de la librería cryptography que representan la identidad del certificado y los nombres alternativos.
# ----------------------------------------------------- 

def parse_dn_a_texto(dn_text: str) -> x509.Name: # convierte un texto DN (que es todo eso del CN=.. DN=... o=... ) en un objeto que la librería cryptography puede usar
    # mapping traduce los identificadores comunes del DN a los OID que usa la librería cryptography
    mappingDN = {
        "CN": NameOID.COMMON_NAME,
        "OU": NameOID.ORGANIZATIONAL_UNIT_NAME,
        "O": NameOID.ORGANIZATION_NAME,
        "L": NameOID.LOCALITY_NAME,
        "ST": NameOID.STATE_OR_PROVINCE_NAME,
        "C": NameOID.COUNTRY_NAME,
        "EMAIL": NameOID.EMAIL_ADDRESS,
    }
    atributosDN = [] # lista de atributos del DN
    for part in [p.strip() for p in dn_text.split(",") if p.strip()]:
        if "=" not in part:
            continue
        key, value = [x.strip() for x in part.split("=", 1)]
        oid = mappingDN.get(key.upper())
        if oid:
            atributosDN.append(x509.NameAttribute(oid, value))
    if not atributosDN:
        raise ValueError("DN no tiene atributos válidos.")
    return x509.Name(atributosDN)

def parse_san_text(san_text: Optional[str]) -> Optional[x509.SubjectAlternativeName]: # convierte un texto SAN en un objeto que la librería cryptography puede usar. El san es una lista de nombres alternativos para el certificado
    if not san_text:
        return None
    # Separar por comas y limpiar espacios; ignorar entradas vacías
    nombresDNS = [s.strip() for s in san_text.split(",") if s.strip()]
    if not nombresDNS:
        return None
    # Construir la extensión SAN con DNSName para cada nombre
    return x509.SubjectAlternativeName([x509.DNSName(nombre) for nombre in nombresDNS])

# --------------------------------------------------------------------
# Comandos 
# ----------------------------------------------------------------------------

def generar_genkey(args: argparse.Namespace) -> None: # genera un par de claves RSA y las guarda en el keystore cifrado
    if args.keyalg.upper() != "RSA":
        raise SystemExit("Esta versión sólo soporta RSA.")
    store = StoreFile(args.keystore)
    if not store.exists():
        print(f"[i] No existe keystore: {args.keystore}. Se creará uno nuevo.")
        # Pide y verifica contraseña del almacén (mínimo 6, debe coincidir)
        store_pass = pedir_password_y_verificar(
            "Contraseña del almacén (store password): ",
            "Repite la contraseña del almacén: "
        )
        store.crearKeystore(store_pass)
    else:
        for _ in range(3):
            store_pass = pedir_password_oculta("Contraseña del almacén: ")
            try:
                store.abrir_Keystore(store_pass)
                break
            except Exception:
                print("[!] Contraseña del almacén incorrecta. Inténtalo de nuevo.\n")
        else:
            raise SystemExit("Demasiados intentos fallidos al abrir el almacén.")
    print("[i] Generando par de claves RSA…")
    clave_priv = rsa.generate_private_key(public_exponent=65537, key_size=args.keysize)
    clave_pub = clave_priv.public_key()
    # Validación y análisis del DN y SAN
    _ = parse_dn_a_texto(args.dname)
    _ = parse_san_text(args.san)
    
    pub_pem = clave_pub.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8") # convierte la clave pública a formato PEM (un formato de texto legible para claves)
    priv_pem_clear = clave_priv.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    key_pass = pedir_password_y_verificar(
        "Contraseña de la clave (key password): ",
        "Repite la contraseña de la clave: "
    )
    key_salt = os.urandom(SALT_BYTES)
    key_key = derivar_clave_desde_password(key_pass, key_salt) # genera una clave segura a partir de la contraseña de la clave y la salt
    enc = encrypta(key_key, priv_pem_clear, aad=f"alias:{args.alias}".encode("utf-8")) # cifra la clave privada usando la clave derivada y el alias como datos adicionales
    item = KeyItem("RSA", time.time(), pub_pem, args.dname, {"salt": bytes64_a_texto(key_salt), "nonce": enc["nonce"], "ciphertext": enc["ciphertext"]}) # crea un objeto KeyItem con los datos de la clave
    store.add_clave_a_keystore(args.alias, item) # añade la clave al keystore bajo el alias especificado
    store.guardarKeystore(store_pass)
    print(f"[ok] Clave guardada con alias '{args.alias}' en '{args.keystore}'.")

def generar_certreq_csr(args: argparse.Namespace) -> None: # crea una CSR usando una clave privada guardada en el keystore. CSR es una solicitud de firma de certificado
    store = StoreFile(args.keystore)
    if not store.exists():
        raise SystemExit("El keystore indicado no existe.")
    store_pass = pedir_password_oculta("Contraseña del almacén: ")
    store.abrir_Keystore(store_pass) 
    item = store.get_clave_keystore(args.alias) 
    key_pass = pedir_password_oculta("Contraseña de la clave (key password): ")
    key_key = derivar_clave_desde_password(key_pass, texto_a_bytes64(item["enc_private"]["salt"]))
    try:
        priv_pem = desencrypta(key_key, item["enc_private"]["nonce"], item["enc_private"]["ciphertext"], aad=f"alias:{args.alias}".encode("utf-8"))
    except Exception:
        raise SystemExit("Contraseña de clave incorrecta o datos corruptos.")
    private_key = serialization.load_pem_private_key(priv_pem, password=None)
    dn_text = args.dname or item.get("subject_dn") # obtiene el DN del argumento o del keystore si no se proporciona
    if not dn_text:
        raise SystemExit("No hay DN. Pasa --dname.")
    subject = parse_dn_a_texto(dn_text) 
    san_ext = parse_san_text(args.san) # obtiene la extensión SAN del argumento si se proporciona
    builder = x509.CertificateSigningRequestBuilder().subject_name(subject)
    if san_ext is not None:
        builder = builder.add_extension(san_ext, critical=False) # añade la extensión SAN si se proporciona
    csr = builder.sign(private_key, hashes.SHA256())
    out_path = args.out or f"{args.alias}.csr"
    with open(out_path, "wb") as f: # guarda la CSR en un archivo
        f.write(csr.public_bytes(serialization.Encoding.PEM)) # escribe la CSR en formato PEM
    print(f"[ok] CSR generado en '{out_path}'.")

# ------------------------------
# menú del CMD/powershell  
# --------------------------------

def build_interfaz_cmd() -> argparse.ArgumentParser: # es lo que te permite usar el programa desde el terminal opciones como --genkey, --alias, etc
# ArgumentParser es una clase que te permite definir y manejar argumentos de línea de comandos
#  formatter_class=argparse.RawTextHelpFormatter, significa que el texto de ayuda se muestra tal cual, sin formateo automático
# add_help=False, significa que no se añade automáticamente la opción --help porque la definimos manualmente
    p = argparse.ArgumentParser(
        description="keytool_miriam: genera claves RSA y CSR usando un keystore cifrado.",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False,
    )
    p.add_argument("--help", action="help", help="Mostrar esta ayuda y salir.")
    mode = p.add_mutually_exclusive_group(required=True) # mode es un grupo de opciones mutuamente excluyentes, es decir, sólo puedes usar una de ellas a la vez
    mode.add_argument("--genkey", action="store_true", help="Generar un par de claves y guardarlo en el keystore.")
    mode.add_argument("--certreq", action="store_true", help="Crear una CSR usando una clave guardada.")
    p.add_argument("--alias", required=True, help="Alias dentro del keystore.") # p.add_argument es para añadir una opción o argumento al parser
    p.add_argument("--keystore", required=True, help="Ruta del keystore.")
    p.add_argument("--dname", help="DN: 'CN=..., OU=..., O=..., L=..., ST=..., C=ES'.") #el dn es la identidad del certificado el CN es el nombre común, OU es la unidad organizativa, O es la organización, L es la localidad, ST es el estado o provincia y C es el país
    p.add_argument("--san", help="SAN DNS separados por coma: 'example.com,www.example.com'.") # el san son los nombres alternativos del certificado. Es una lista de nombres DNS separados por comas que el certificado también protegerá y validará
    p.add_argument("--keyalg", default="RSA", help="Algoritmo de clave (sólo RSA).") # RSA es un algoritmo de clave pública muy común y seguro
    p.add_argument("--keysize", type=int, default=2048, help="Tamaño de clave RSA (por defecto 2048).") # el tamaño de clave es la longitud en bits de la clave RSA. 2048 es un tamaño seguro y comúnmente usado
    p.add_argument("--out", help="Archivo CSR de salida (por defecto <alias>.csr).") # el archivo de salida es donde se guardará la CSR generada. Si no se especifica, se usará el nombre del alias con extensión .csr
    return p

def main(argv: Optional[List[str]] = None) -> int: 
    parser = build_interfaz_cmd() #esto lo que hace es construir la interfaz de línea de comandos es decir las opciones y argumentos acepta el programa cuando lo ejecutas desde la terminal
    args = parser.parse_args(argv) # aquí es donde se analizan los argumentos pasados desde la terminal y se almacenan en la variable args para que el programa pueda usarlos
    try:
        if args.genkey: # si se pasa la opción --genkey, se llama a la función generar_genkey para generar un par de claves y guardarlas en el keystore
            if not args.dname: 
                raise SystemExit("--genkey requiere --dname.") 
            generar_genkey(args)
        elif args.certreq: # si se pasa la opción --certreq, se llama a la función generar_certreq_csr para crear una CSR usando una clave guardada en el keystore
            generar_certreq_csr(args) 
        else:
            parser.print_help(); return 1 # si no se pasa ninguna opción válida, se muestra la ayuda
        return 0
    except KeyboardInterrupt: # si el usuario interrumpe la ejecución (Ctrl+C), se maneja la excepción y se muestra un mensaje de cancelación
        print("\n[cancelado]"); return 130
    except Exception as e: # si ocurre cualquier otra excepción, se muestra el error
        print(f"[error] {e}"); return 1

if __name__ == "__main__":
    sys.exit(main()) # ejecuta la función main cuando el script se ejecuta directamente desde la terminal

#cmd --------------------------------------------------------

# # Generar par de claves (crea el keystore si no existe)
# python keytool_miriam.py --genkey --alias michi --keystore mykeys.ks --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com" --keysize 2048
# py .\keytool_miriam.py --genkey --alias michi --keystore mykeys.ks --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com" --keysize 2048


# python keytool_miriam.py --genkey ^
#   --alias michi ^
#   --keystore mykeys.ks ^
#   --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" ^
#   --san "example.com,www.example.com" ^
#   --keysize 2048

# # Crear CSR desde ese alias
# python keytool_miriam.py --certreq --alias michi --keystore mykeys.ks --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com" --keysize 2048
# py .\keytool_miriam.py --certreq --alias michi --keystore mykeys.ks --out michi.csr --dname "CN=Miriam, OU=m, O=m, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com"


# python keytool_miriam.py --certreq --alias server \
#   --keystore mykeys.ks --out server.csr \
#   --dname "CN=example.com, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" \
#   --san "example.com,www.example.com"


#  powershell -------------------------------------------

# # Generar par de claves (crea el keystore si no existe)
# py .\keytool_miriam.py --genkey --alias michi --keystore mykeys.ks --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com" --keysize 2048

# # Crear CSR desde ese alias
# py .\keytool_miriam.py --certreq --alias michi --keystore mykeys.ks --out michi.csr --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" --san "example.com,www.example.com"



# python .\keytool_miriam.py --genkey `
#   --alias michi `
#   --keystore mykeys.ks `
#   --dname "CN=Miriam, OU=monlau, O=monlau, L=Barcelona, ST=Barcelona, C=ES" `
#   --san "example.com,www.example.com" `
#   --keysize 2048


# 1-B
# 2-C
# 3-B
# 4-B
# 5-B
# 6-B
# 7-B
# 8-B
# 9-C
# 10-B
# 11-B
# 12-B
# 13-B
# 14-B
# 15-B
# 16-C
# 17-B
# 18-A
# 19-B
# # 20-A