# captura audio del micro y lo convierte a texto. Si no pilla nada da None o la excepción que sea
from tkinter import messagebox

import speech_recognition as sr


class VoiceService:

    def escuchar_frase(self) -> str | None:

        recognizer = sr.Recognizer()

        # abre el micro y se apaga al acabar como con la conexión de la BBDD
        with sr.Microphone() as source: # señor micro? XD
            print("Habla ahora...")

            # Ajusta al ruido ambiente así igual funciona en clase XD
            recognizer.adjust_for_ambient_noise(source, duration=0.6) # lo de la duración es cuanto tarda en calibrar, cuanto mas tarda en calibrar mejor pero parece que el micro tarda en reaccionar

            try :
                # el timeout: si no hablas, a los 5 segundos se corta; phrase_time_limit: máximo de segundos que puede surar la frase
                audio = recognizer.listen(source, timeout=6, phrase_time_limit=6)

            except sr.WaitTimeoutError:
                print("Tiempo para hablar expirado")
                return None

        try:
            # Google Speech para reconocer la voz. Como es de google se necesita internete
            texto = recognizer.recognize_google(audio, language="es-ES")
            print("Has dicho:", texto)
            return texto

        except sr.UnknownValueError: # cuando el audio llega bien, pero google no entendió una mierda pòr x
            print("No se entendió el audio")
            return None

        except sr.RequestError as e: # por fallo de internet
            print("Error con el servicio de reconocimiento:", e)
            return None






        """
        Por si los micros se vuelven locos y detecta otro
        import speech_recognition as sr
        
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f'Microfono {index}: {name}')
        """