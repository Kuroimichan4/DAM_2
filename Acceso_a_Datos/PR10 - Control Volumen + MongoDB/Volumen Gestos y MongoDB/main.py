# camara y volumen

import cv2 # librería para trabajar con la cámara, imagenes y detección visual de cosas
import math # para hacer los cálculos
import numpy as np
# de la librería de pycaw #
from HandTrackingModule import HandDetector
from VolumeHandControl import VolumeControl
from dao.mongodb_dao import MongoDAO

from pycaw.pycaw import AudioUtilities # audioUtilities para obtener el dispositivo de audio

# -------- pyhron 3.11.9 y mediapipe 0.10.13  recuerfdda para ponerlo en casa igual --------- #
# pip install -r requirements.txt

#solo para ver si responde
# print(volume_control.volume.GetVolumeRange()) debería de devolver algo rollo esto: (-65.25, 0.0, 0.75) -

cap = cv2.VideoCapture(1) # cap representará el objeto para conectarse a la camara predeterminada ( 0 de monlau, la de casa 1)

detector = HandDetector()
volume_control = VolumeControl()

# BBDD
mongo = MongoDAO() # instancia el mongoDAO de mongodb_dao
session_id = mongo.start_session() # crea la sesión con su ID y los cambios que se hayan hecho durante la sesión


while True: # mientras sea succes porque se conecta a la cámara se ejecuta el while infinitamente para ir pillando los fotogramas
    success, img = cap.read() # si se captura, pilla la imagen

    if not success:
        print("No se pudo leer la cámara")
        break

    img = detector.detectorManos(img)
    landMarksList = detector.posicionPuntos(img, draw=False)

    if landMarksList: # si la lista no está vacía
        x1, y1 = landMarksList[4][1], landMarksList[4][2]  # pulgar - mediapipe siempre asigna el ID 4 al pulgar- pilla la cordenada x e y del pulgar
        x2, y2 = landMarksList[8][1], landMarksList[8][2]  # índice - mediapipe siempre asigna el ID 8 al índice

        # el seguro del meñique
        peque_punta = landMarksList[20][2]
        peque_base = landMarksList[18][2]

        peque_abajo = peque_punta > peque_base

        # dibujar puntos
        cv2.circle(img, (x1, y1), 10, (255, 0, 0), -1)
        cv2.circle(img, (x2, y2), 10, (0, 255, 0), -1)

        # dibujar línea entre ellos
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

        # - calcular la distancia entre dedos - #
        length = math.hypot(x2 - x1, y2 - y1) # math.hypot Calcula la distancia en línea recta (la hipotenusa) entre el punto del pulgar (x1, y1) y el del índice (x2, y2)

        vol_bar = np.interp(length, [20, 200], [400, 150]) #para una barra visual
        vol_per = volume_control.distanciaPorcentaje(length) #porcentaje visual, interp es de numPy y básicamente traduce escalas


        if peque_abajo:

            volume_control.setVolumen(length)
            # volume.SetMasterVolumeLevel(vol_sys, None) # le dice que ponga el volumen maestro de win a lo que le pasamos

            #guardar el volumen de la sessión
            mongo.save_event(session_id, 0, int(vol_per), length)


        estado = "ACTIVO" if peque_abajo else "BLOQUEADO"

        cv2.putText(img, f"Distancia: {int(length)}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(img, f"Volumen: {int(vol_per)} %", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(img, f"Control: {estado}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0) if peque_abajo else (0, 0, 255), 2)



    cv2.imshow("Camara", img) # esto muestra la imagen que está detectando en una ventana

    if cv2.waitKey(1) & 0xFF == ord('q'): # cada milisegundo con waitKey comprueba si se ha pulsado la q para salir
        break

mongo.end_session(session_id) #cerrar sesión de mongo
cap.release() # libera la cámara
cv2.destroyAllWindows() #destruye las ventanas abiertas