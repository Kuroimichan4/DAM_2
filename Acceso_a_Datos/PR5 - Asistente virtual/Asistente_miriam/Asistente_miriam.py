# app.py
import os # lee variables del sistema (es para la api key)
import tkinter as tk # basicamnete para construit la ventanadonde se podrá preguntar
from tkinter import scrolledtext, messagebox
from pathlib import Path # esto es el path de las variables de entorno
from dotenv import load_dotenv # esto lee en env donde esta lo de la api key
import google.generativeai as genai # librería para hablar con gemini

# Carga la API key  -------------------------------------------
load_dotenv() # le el env
API_KEY = os.getenv("API_KEY", "").strip() # guarda lo del archivo env en la variable
MODEL_NAME = "models/gemini-2.5-flash" # versión de gemini. hay que revisar en el pc de casa si tengo la misma versió. Para revisar el terminal: python list_models.py


def leer_servicios() -> str: # lee  el txt para tener la info del negocio
    p = Path("servicios.txt")
    if not p.exists():
        return "# (No se encontró servicios.txt)"
    return p.read_text(encoding="utf-8")

CONTEXTO = leer_servicios()
# esto es una instruccion para la IA
SYSTEM_INSTRUCTIONS = (
    "Eres un asistente de un negocio de Consultoría de Soluciones Permanentes. Responde usando EXCLUSIVAMENTE la información del contexto "
    "si está disponible; si falta algún dato, dilo claramente y sugiere llamar o escribir para confirmar. "
    "Sé breve, claro y amable. Formato en texto plano."
)

# esto es para construir el prompt que se le pasará a la IA
def construir_prompt(pregunta: str) -> str:
    return f"""{SYSTEM_INSTRUCTIONS}

=== CONTEXTO ===
{CONTEXTO}
=== FIN CONTEXTO ===

Usuario: {pregunta}
"""

# Configurar Gemini de mierda con la key para configurar la libreria y usar mi cuenta
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("Falta API_KEY en .env")

# --- GUI ---
root = tk.Tk()
root.title("Asistente de Consultoría de Soluciones Permanentes (IA)")

frm = tk.Frame(root, padx=10, pady=10)
frm.pack(fill="both", expand=True)

tk.Label(frm, text="En qué te puedo ayudar? (servicios, horarios, precios...):").pack(anchor="w")

entrada = scrolledtext.ScrolledText(frm, height=5, wrap="word")
entrada.pack(fill="both", expand=False, pady=(0,8))

btn = tk.Button(frm, text="Enviar")
btn.pack(anchor="w")

salida = scrolledtext.ScrolledText(frm, height=12, wrap="word", state="disabled")
salida.pack(fill="both", expand=True, pady=(8,0))

def mostrar(texto: str):
    salida.configure(state="normal")
    salida.delete("1.0", tk.END)
    salida.insert(tk.END, texto)
    salida.configure(state="disabled")

def on_enviar():
    pregunta = entrada.get("1.0", tk.END).strip()
    if not pregunta:
        messagebox.showinfo("Escribe una pregunta")
        return

    if not API_KEY:
        mostrar("Falta API_KEY en .env")
        return

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        prompt = construir_prompt(pregunta)
        resp = model.generate_content(prompt)
        texto = getattr(resp, "text", None)
        if not texto and getattr(resp, "candidates", None):
            texto = resp.candidates[0].content.parts[0].text
        mostrar(texto or "(Sin texto de respuesta)")
    except Exception as e:
        mostrar(f"Ocurrió un error: {e}")

btn.configure(command=on_enviar)
root.minsize(700, 500)
root.mainloop()
