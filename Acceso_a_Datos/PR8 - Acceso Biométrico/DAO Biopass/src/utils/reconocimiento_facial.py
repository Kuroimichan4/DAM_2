import cv2
from src.usuario_dao import UsuarioDAO
from src.utils.camera_utils import capturar_foto, recortar_cara, frame_a_bytes, bytes_a_frame, normalizar_cara


# ------------------------------------------------------ mirar all -----------------------------------------------------------------
def reconocer_usuario(threshold=70.0):
   # Captura una cara nueva y la compara con las caras guardadas usando lo del LBPH y si lo pilla da el nombre y el grado de confianza si no pues none y ya

    dao = UsuarioDAO()
    registros = dao.obtener_caras()  # [(id, nombre, cara_bytes), ...]

    if not registros:
        return None, None

    #  Preparara el dataset  de las caras guardadas
    etiquetas = []
    imagenes = []
    id_to_nombre = {}

    for idx, (user_id, nombre, cara_bytes) in enumerate(registros):
        frame = bytes_a_frame(cara_bytes)
        if frame is None:
            continue
        # frame guardado puede estar en color: normalizamos
        cara_norm = normalizar_cara(frame)
        imagenes.append(cara_norm)
        etiquetas.append(idx)
        id_to_nombre[idx] = nombre

    if not imagenes:
        return None, None

    #  Entrena al LBPH para que reconozva las caras
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(imagenes, __import__("numpy").array(etiquetas))

    # captura la cara actual que se muestra en la cámara
    foto_bytes, frame = capturar_foto()
    if frame is None:
        return None, None

    cara_frame = recortar_cara(frame)
    if cara_frame is None:
        return None, None

    cara_norm = normalizar_cara(cara_frame)

    # pongo en una variable el nombre y el grado de confianza con el quie ha reconozido
    label, confidence = recognizer.predict(cara_norm)

    # lo de la confianza va al revés del asistente virtual
    if confidence <= threshold:
        return id_to_nombre[label], confidence
    return None, confidence
