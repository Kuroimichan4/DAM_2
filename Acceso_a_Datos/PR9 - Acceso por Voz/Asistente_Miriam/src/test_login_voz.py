from src.auth_dao import AuthDAO
from src.voice_service import VoiceService

dao = AuthDAO()
voz = VoiceService()

username = input("Username: ")

print("Di tu frase secreta cuando te avise")
passphrase = voz.escuchar_frase()

if passphrase is None:
    print("No se pudo reconocer la voz. Inténtalo de nuevo.")
else:
    ok = dao.validar_login(username, passphrase)

    if ok:
        print("Acceso concedido")
    else:
        print("Acceso denegado")



