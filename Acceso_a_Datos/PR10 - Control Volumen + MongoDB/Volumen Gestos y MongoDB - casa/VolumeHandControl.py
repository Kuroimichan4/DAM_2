import numpy as np
from pycaw.pycaw import AudioUtilities


class VolumeControl:
    def __init__(self):
        self.device = AudioUtilities.GetSpeakers() # pilla el dispositivo de audio
        self.volume = self.device.EndpointVolume # convierte la interfaz al tipo correcto para poder usarla
        self.min_vol, self.max_vol, _ = self.volume.GetVolumeRange()  # Devuelve esto en monlau y en casa: (-96.0, 0.0, 1.5)

    def distanciaPorcentaje(self, length, min_length=20, max_length=200):
        return np.interp(length, [min_length, max_length], [0, 100]) #porcentaje visual, interp es de numPy y básicamente traduce escalas. 20, 200 de arriba es el rango mínimo y máximo de los dedos y lo otro es el porcentaje del volumen del 0 al 100

    def distancia_a_Volumen(self, length, min_length=20, max_length=200):
        return np.interp(length, [min_length, max_length], [self.min_vol, self.max_vol])  #valor real que entiende windows (mirar cuanto es en cada pc que va cambiando)

    def setVolumen(self, length, min_length=20, max_length=200):
        vol_sys = self.distancia_a_Volumen(length, min_length, max_length) #valor real que entiende windows (mirar cuanto es en cada pc que va cambiando)
        self.volume.SetMasterVolumeLevel(vol_sys, None)
        return vol_sys