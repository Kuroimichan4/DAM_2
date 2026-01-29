#  Lógica de OpenCV (Detectar y Bytes).

# Opción URL: Guardar la foto en C:/fotos/pepe.jpg y guardar la ruta en la BD. Es rápido, pero si borras la carpeta, la BD se rompe.
# Opción BLOB (La que usaremos): Convertimos la imagen a bytes y la guardamos dentro de la
# tabla. Garantiza que la copia de seguridad de la BD contiene todos los datos necesarios.

import cv2
import numpy as np

def capturar_foto() -> "tuple[bytes, object] | tuple[None, None]":

    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        return None, None

    foto_frame = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("BioPass - Camara (c=capturar, q=salir)", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            foto_frame = frame.copy()
            break
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if foto_frame is None:
        return None, None

    # convierto la imagen frame a bytes JPEG para guardarlo en la BBDD
    ok, buffer = cv2.imencode(".jpg", foto_frame)
    if not ok:
        return None, None

    foto_bytes = buffer.tobytes()
    return foto_bytes, foto_frame

def recortar_cara(frame):


    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detector = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    caras = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(caras) == 0:
        return None

    # coge la primera cara detectada
    x, y, w, h = caras[0]
    return frame[y:y+h, x:x+w]

def frame_a_bytes(frame) -> bytes:
    ok, buffer = cv2.imencode(".jpg", frame)
    if not ok:
        raise ValueError("No se pudo convertir la imagen a bytes")
    return buffer.tobytes()


def bytes_a_frame(img_bytes: bytes):
    # de la BBDD en bytes a jpg

    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return frame

def normalizar_cara(cara_frame, size=(200, 200)):
    # lo paso a escala de grises para normalizar pero creo que eso dificulta el reconocimiento, revisar mas adelante---------------------------------------------

    gray = cv2.cvtColor(cara_frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, size)
    return gray