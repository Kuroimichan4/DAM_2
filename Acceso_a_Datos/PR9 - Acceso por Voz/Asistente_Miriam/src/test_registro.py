from src.auth_dao import AuthDAO

dao = AuthDAO()

usuario = input("Nombre de usuario: ")
frase = input("Frase secreta: ")

dao.registrar_usuario(usuario, frase)