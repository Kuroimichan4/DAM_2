import tkinter as tk
import threading
from datetime import datetime

from src.auth_dao import AuthDAO
from src.voice_service import VoiceService


class VoiceAuditApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("VoiceAudit Login")
        self.root.geometry("520x420")
        self.root.minsize(520, 420)

        # Servicios
        self.dao = AuthDAO()
        self.voice = VoiceService()

        # --- Layout principal
        container = tk.Frame(root, padx=14, pady=14)
        container.pack(fill="both", expand=True)

        header = tk.Label(container, text="VoiceAudit - Acceso por voz", font=("Segoe UI", 16, "bold"))
        header.pack(anchor="w")

        subtitle = tk.Label(
            container,
            text="Escribe tu usuario y pulsa \"Hablar\" para verificar la frase.",
            fg="#555",
            font=("Segoe UI", 10),
        )
        subtitle.pack(anchor="w", pady=(2, 12))

        # --- Formulario
        form = tk.Frame(container)
        form.pack(fill="x")

        tk.Label(form, text="Username:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.username_entry = tk.Entry(form, width=32, font=("Segoe UI", 11))
        self.username_entry.grid(row=1, column=0, sticky="we", pady=(4, 0))

        form.columnconfigure(0, weight=1)

        # --- Botones
        buttons = tk.Frame(container)
        buttons.pack(fill="x", pady=(12, 8))

        self.btn_hablar = tk.Button(
            buttons,
            text="Hablar",
            font=("Segoe UI", 11, "bold"),
            command=self.login_por_voz,
            padx=10,
            pady=6
        )
        self.btn_hablar.pack(side="left")

        self.btn_limpiar = tk.Button(
            buttons,
            text="Limpiar mensajes",
            font=("Segoe UI", 10),
            command=self.limpiar_log,
            padx=10,
            pady=6
        )
        self.btn_limpiar.pack(side="right")

        # --- notifaciones de stado
        self.status_label = tk.Label(container, text="Estado: esperando…", fg="#666", font=("Segoe UI", 10))
        self.status_label.pack(anchor="w", pady=(4, 8))

        # --- log de oo que se dice
        log_frame = tk.Frame(container, bd=1, relief="solid")
        log_frame.pack(fill="both", expand=True)

        self.log_text = tk.Text(
            log_frame,
            wrap="word",
            height=10,
            font=("Consolas", 10),
            bg="#0f172a",      # fondo oscuro
            fg="#e2e8f0",      # texto claro
            insertbackground="#e2e8f0",
            bd=0,
            padx=10,
            pady=10
        )
        self.log_text.pack(side="left", fill="both", expand=True)

        scroll = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scroll.pack(side="right", fill="y")
        self.log_text.configure(yscrollcommand=scroll.set)

        # Tags de colores por tipo
        self.log_text.tag_configure("INFO", foreground="#e2e8f0")
        self.log_text.tag_configure("OK", foreground="#22c55e")
        self.log_text.tag_configure("WARN", foreground="#f59e0b")
        self.log_text.tag_configure("ERR", foreground="#ef4444")

        # Bloquear el log para que no lo toquen
        self._set_log_readonly(True)

        # Log inicial
        self.log("Aplicación iniciada.", "INFO")
        self.log("Listo para autenticar.", "INFO")

    # helpers
    def _set_log_readonly(self, readonly: bool):
        self.log_text.configure(state=("disabled" if readonly else "normal"))

    def log(self, msg: str, level: str = "INFO"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        self._set_log_readonly(False)
        self.log_text.insert("end", line, level)
        self.log_text.see("end")
        self._set_log_readonly(True)

    def limpiar_log(self):
        self._set_log_readonly(False)
        self.log_text.delete("1.0", "end")
        self._set_log_readonly(True)
        self.log("Mensajes limpiados.", "INFO")

    def set_status(self, text: str, kind: str = "INFO"):
        colors = {"INFO": "#2563eb", "OK": "#16a34a", "WARN": "#d97706", "ERR": "#dc2626"}
        self.status_label.config(text=f"Estado: {text}", fg=colors.get(kind, "#666"))

    # --- Lógica ---
    def login_por_voz(self):
        username = self.username_entry.get().strip()

        if not username:
            self.set_status("falta username", "WARN")
            self.log("Debes escribir el username antes de hablar.", "WARN")
            return

        self.btn_hablar.config(state="disabled")
        self.set_status("escuchando…", "INFO")
        self.log(f"Iniciando escucha para usuario '{username}'…", "INFO")

        threading.Thread(target=self._escuchar_en_hilo, args=(username,), daemon=True).start()

    def _escuchar_en_hilo(self, username: str):
        try:
            passphrase = self.voice.escuchar_frase()
        except Exception as e:
            passphrase = None
            # Log de error técnico
            self.root.after(0, lambda: self.log(f"Error técnico escuchando: {e}", "ERR"))

        self.root.after(0, lambda: self._procesar_resultado_voz(username, passphrase))

    def _procesar_resultado_voz(self, username: str, passphrase: str | None):
        if passphrase is None:
            self.set_status("no se detectó/entendió voz", "WARN")
            self.log("No se detectó voz o no se entendió. Intenta de nuevo.", "WARN")
            self.btn_hablar.config(state="normal")
            return

        self.set_status("verificando…", "INFO")
        self.log(f"Frase detectada: '{passphrase}'", "INFO")

        ok = self.dao.validar_login(username, passphrase)

        if ok:
            self.set_status("✅ acceso concedido", "OK")
            self.log("Acceso concedido.", "OK")
        else:
            self.set_status("❌ acceso denegado", "ERR")
            self.log("Acceso denegado.", "ERR")

        self.btn_hablar.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()