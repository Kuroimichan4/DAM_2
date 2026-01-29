from src.usuario_dao import UsuarioDAO

if __name__ == "__main__":
    dao = UsuarioDAO()

    dao.registrar_usuario(
        "UsuarioPrueba",
        b"foto_falsa",
        b"cara_falsa"
    )

    usuarios = dao.obtener_todos()
    print("Usuarios en BD:", usuarios)
