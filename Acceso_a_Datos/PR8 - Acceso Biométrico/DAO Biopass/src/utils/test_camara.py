import cv2 # librería openCV es para manejar la cámara y lo relacionado a ella

def main():
    # creo el objeto de la camara en si. El 0 indica que es la cámara por defecto
    cap = cv2.VideoCapture(1)

    # esto es por si la estamos usando en otra app
    if not cap.isOpened():
        print("No se pudo abrir la cámara")
        return

    print("Cámara abierta. Pulsa 'c' para capturar, 'q' para salir.")


    while True:
        # cap.read() le pide a la cámara que tome una foto en ese preciso milisegundo
        # ret es un boolean que si va bien la cam y recive señal da true y si no false
        # frame es el array de pixeles que representa la imagen
        ret, frame = cap.read()
        if not ret:
            print("No se pudo leer frame")
            break

        cv2.imshow("Camara BioPass", frame) # abre una ventana para mostrar la imagen

        key = cv2.waitKey(1) & 0xFF

        if key == ord('c'):
            cv2.imwrite("foto_prueba.jpg", frame)
            print("Foto guardada como foto_prueba.jpg")

        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
