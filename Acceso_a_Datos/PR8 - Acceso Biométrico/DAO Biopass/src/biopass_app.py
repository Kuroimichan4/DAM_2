# INTERFAZ: Usa el DAO y la Cámara.

import tkinter as tk
from tkinter import messagebox

from src.usuario_dao import UsuarioDAO
from src.utils.camera_utils import capturar_foto, recortar_cara, frame_a_bytes
from src.utils.reconocimiento_facial import reconocer_usuario

class BioPassApp:
    def __init__(self): # init para que se ejecute nada mas arrancar
    # self se refiere a instancia de la clase que estoy creando que el Biopass mismo. Es como el this de java
    # al poner self.root le digo que guarde dentro de la app lo que sea para usarlo en otros metods
        # creación de pantalla
        self.root = tk.Tk()
        self.root.title("Registro")
        self.root.geometry("420x220")

    # creo el dao
        self.dao = UsuarioDAO()

    # 3 los widgets/componentes
        tk.Label(self.root, text="Nombre de usuario: ").pack(pady=(20, 5))
    #  argumento 1 = ponlo en la ventana principal, arg 2 = contenido, pack = empaqueta y muestra en el primer sitio disponible, si no está no se ve nada

        self.entry_nombre = tk.Entry(self.root, width=35)  # crea el input, lo mete en una variable, le dice en qué ventana está y el tamaño
        # pack pone los elementos uno encima de otro normalmente y el pady es el padding de toda la vida
        self.entry_nombre.pack(pady=5)  # esto pinta el input en pantalla y le da el padding

    # ------------------------------------------------ me quedé por aquí ---------------------------------------------------
        tk.Button(self.root, text="Registrar usuario: ", command=self.registrar).pack(pady=15)
        # command es como un listener
       # tk.Button(self.root, text="Ver usuarios", command=self.ver_usuarios).pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)

    def registrar(self):
        # registro sin cámara para ver si funciona
        nombre = self.entry_nombre.get().strip()

        if not nombre:
            messagebox.showwarning("Falta nombre", "Escribe un nombre antes de registrar.")
            return

        try:
            # para testear por si se vuelva a cascar
            # self.dao.registrar_usuario(nombre, b"foto_falsa", b"cara_falsa")
            # la b de delante es para indicar el tipo de dato que es, por defecto es string pero en este caso es un objeto de bytes
            # messagebox.showinfo("OK", f"Usuario '{nombre}' registrado (modo prueba).")
            # self.entry_nombre.delete(0, tk.END)

            foto_bytes, frame = capturar_foto()

            if foto_bytes is None or frame is None:
                messagebox.showwarning("Cancelado", "No se capturó ninguna foto.")
                return

            cara_frame = recortar_cara(frame)
            if cara_frame is None:
                messagebox.showwarning(
                    "Sin cara detectada",
                    "No se detectó ninguna cara. Intenta de nuevo con más luz y mirando a cámara."
                )
                return

            cara_bytes = frame_a_bytes(cara_frame)

                # foto completa + cara recortada
            self.dao.registrar_usuario(nombre, foto_bytes, foto_bytes)

            messagebox.showinfo("OK", f"Usuario '{nombre}' registrado")
            self.entry_nombre.delete(0, tk.END)  # pilla el input del nombre y lo vacía con delete pero hay que decirle de qué posición a qué posición (del 0 hasta el final)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar:\n{e}")


    def ver_usuarios(self):
        try:
            filas = self.dao.obtener_todos()
            if not filas:
                messagebox.showinfo("Usuarios", "No hay usuarios todavía.")
                return

            texto = "\n".join([f"{u[0]} - {u[1]}" for u in filas])
            messagebox.showinfo("Usuarios", texto)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron leer usuarios:\n{e}")


    def run(self): # esta función lo que hace es runear la app después de que lo demás esté listo, por esto está añl final
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop() # esto es para que cuando acaba de ejecutar el código, no se cierre la app, sino que siga runeandose y viendose en pantalla

    def on_close(self):
        from src.conexion_db import DBConnection
        DBConnection.close_connection()
        self.root.destroy()


#@-------------------------------------new mirar ----------------------------------------------------------------------------------------------
    def login(self):
        try:
            nombre, conf = reconocer_usuario(threshold=85.0) # la confianza como en lo del asistente de voz pero al revés. Cuanto mas alto menos certeza

            if nombre is None:
                messagebox.showwarning("Login", f"No reconocido. (confidence={conf})")
            else:
                messagebox.showinfo("Login", f" Hola, {nombre} (confidence={conf:.2f})")
        except Exception as e:
            messagebox.showerror("Error", f"Fallo en login:\n{e}")


if __name__ == "__main__":
    app = BioPassApp()
    app.run()