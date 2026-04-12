# lo relacionado con MediaPipe y landmarks

import cv2 # librería para trabajar con la cámara, imagenes y detección visual de cosas
import mediapipe as mp # lo que va a detectar la mano

class HandDetector: # configura el mediapipe una sola vez
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mp_Hands = mp.solutions.hands
        self.hands = self.mp_Hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mp_Draw = mp.solutions.drawing_utils

    def detectorManos(self, img, draw=True): # procesa la imagen, detecta la mano y dibuja los puntos y las líneas de la mano
        # - modifica la imagen de pantalla para mostrar el control del volumen - #
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # esto traduce los colores de la imagen del CV al MediaPipe
        # se ve que CV pilla los colores en BGR y MediaPipe los lee normal en RGB

        self.results = self.hands.process(imgRGB)  # esto procesa la imagen buscando los patrones de una mano y guarda los datos en results

        if self.results.multi_hand_landmarks:  # si se detecta una mano o varias...
            for mano in self.results.multi_hand_landmarks:  # pilla la primera mano que detecte y la mete en la variable
                if draw:
                    self.mp_Draw.draw_landmarks(img, mano, self.mp_Hands.HAND_CONNECTIONS)
                    # esto pinta sobre la imagen los puntos de las articulaciones de los dedos y con mp_hands.HAND_CONNECTIONS une los puntos con líneas

        return img

    def posicionPuntos(self, img, handNo=0, draw=True): # devuelve una lista con los landmarks que son los puntitos de la mano
        landMarksList = []

        if self.results.multi_hand_landmarks:
            mano = self.results.multi_hand_landmarks[handNo]
            h, w, _ = img.shape

            for id, landMark in enumerate(
                    mano.landmark):  # pilla los 21 puntos, enumerate te los numera y los pone en el ID y el landMark contiene las coordenadas
                x, y = int(landMark.x * w), int(landMark.y * h) # las coordenadas se pasan a pixeles para que openCV lo entienda. para ello se multiplica x ancho y alto

                landMarksList.append((id, x, y))

                if draw:
                    cv2.circle(img, (x, y), 10, (0, 255, 0), -1)

        return landMarksList