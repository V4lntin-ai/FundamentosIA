# ============================================================
# PRACTICA: TUTOR INTELIGENTE CON LLM
# MODELO LOCAL: LLAMA 3.2 1B
# ============================================================
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import ollama

# ============================================================
# 1. CONFIGURACION DEL MODELO
# ============================================================
MODELO = "llama3.2:1b"

# Opciones para el tutor: temperatura baja = menos invenciones.
# num_ctx fija el contexto; si el historial lo excede, Ollama
# recorta el inicio de la conversación sin avisar.
OPCIONES_TUTOR = {
    "temperature": 0.2,
    "num_ctx": 4096,
    "num_predict": 500
}

# Para el resumen: aún más baja, porque debe ser fiel al texto.
OPCIONES_RESUMEN = {
    "temperature": 0.1,
    "num_ctx": 4096,
    "num_predict": 500
}

# Máximo de caracteres de cada respuesta del tutor al armar el
# resumen. Evita que las respuestas largas saturen el contexto
# del modelo y desplacen las primeras preguntas.
MAX_CHARS_TUTOR_EN_RESUMEN = 300

# ============================================================
# 2. CONFIGURACION DEL SISTEMA
# ============================================================
mensaje_sistema = """
Eres un tutor universitario de Bases de Datos, relacionales y no
relacionales. Ayudas a estudiantes que están aprendiendo.

CÓMO ENSEÑAS:
- Explicas de forma clara, sencilla y breve, en el idioma del estudiante.
- Usas ejemplos cotidianos (cliente -> pedidos, departamento -> empleados).
- Explicas los procedimientos paso a paso, no solo la respuesta final.
- Cuando ayuda, das ejemplos en SQL.
- Si el estudiante comete un error, explicas cuál fue y cómo corregirlo.
- Si la pregunta se relaciona con una respuesta anterior, mantienes el contexto.

CÓMO TE MANTIENES CORRECTO:
- Responde solo con lo que sabes con certeza. Si no estás seguro, di:
  "No tengo suficiente seguridad para responder eso."
- Nunca inventes conceptos, comandos, funciones ni características.
- Si algo funciona distinto según el gestor (PostgreSQL, MySQL,
  MongoDB, etc.), indícalo en lugar de asumir un solo comportamiento.
- Usa las definiciones estándar de los conceptos; no las reinterpretes.
- Antes de dar código, asegúrate de que la sintaxis sea válida.
- Avisa antes de mostrar comandos que borran o modifican datos de forma
  irreversible.

Si la pregunta no trata de bases de datos, di que solo respondes sobre ese tema.
"""

# ============================================================
# 3. HISTORIAL
# ============================================================
mensajes = [
    {
        "role": "system",
        "content": mensaje_sistema
    }
]

# ============================================================
# 4. FUNCIONES DE LA INTERFAZ
# ============================================================

def agregar_chat(nombre, mensaje):
    chat.config(state="normal")
    chat.insert(
        tk.END,
        f"\n{nombre}:\n",
        "nombre"
    )
    chat.insert(
        tk.END,
        f"{mensaje}\n",
        "mensaje"
    )
    chat.config(state="disabled")
    # Llevar el scroll hasta abajo
    chat.see(tk.END)

def desactivar_botones():
    boton_enviar.config(state="disabled")
    boton_resumen.config(state="disabled")
    estado.config(
        text="El modelo está pensando...",
        fg="orange"
    )

def activar_botones():
    boton_enviar.config(state="normal")
    boton_resumen.config(state="normal")
    estado.config(
        text="Listo",
        fg="green"
    )

# ============================================================
# 5. ENVIAR UNA PREGUNTA
# ============================================================

def enviar_pregunta():
    pregunta = entrada.get(
        "1.0",
        tk.END
    ).strip()
    # Validar que exista texto
    if pregunta == "":
        messagebox.showwarning(
            "Pregunta vacía",
            "Escribe una pregunta antes de enviarla."
        )
        return
    # Mostrar pregunta en el chat
    agregar_chat(
        "ESTUDIANTE",
        pregunta
    )
    # Guardar pregunta en historial
    mensajes.append(
        {
            "role": "user",
            "content": pregunta
        }
    )
    # Limpiar entrada
    entrada.delete(
        "1.0",
        tk.END
    )
    # Desactivar botones mientras trabaja el LLM
    desactivar_botones()
    # Crear hilo para evitar congelar la GUI
    hilo = threading.Thread(
        target=consultar_llm,
        daemon=True
    )
    hilo.start()

# ============================================================
# 6. CONSULTAR OLLAMA
# ============================================================

def consultar_llm():
    try:
        respuesta = ollama.chat(
            model=MODELO,
            messages=mensajes,
            options=OPCIONES_TUTOR
        )
        contenido = respuesta[
            "message"
        ][
            "content"
        ]
        # Guardar respuesta en historial
        mensajes.append(
            {
                "role": "assistant",
                "content": contenido
            }
        )
        # Actualizar interfaz desde el hilo principal
        ventana.after(
            0,
            lambda: mostrar_respuesta(contenido)
        )
    except Exception as error:
        # Si falló, quitar la pregunta que quedó sin respuesta
        # para no dejar dos mensajes "user" seguidos en el historial
        if mensajes and mensajes[-1]["role"] == "user":
            mensajes.pop()
        # Guardar el texto ANTES del lambda: en Python 3 la variable
        # "error" se borra al salir del except y el lambda fallaría
        texto_error = str(error)
        ventana.after(
            0,
            lambda: mostrar_error(texto_error)
        )

# ============================================================
# 7. MOSTRAR RESPUESTA
# ============================================================

def mostrar_respuesta(contenido):
    agregar_chat(
        "TUTOR",
        contenido
    )
    activar_botones()

# ============================================================
# 8. MANEJO DE ERROR
# ============================================================

def mostrar_error(error):
    activar_botones()
    messagebox.showerror(
        "Error con Ollama",
        "No fue posible conectarse con el modelo.\n\n"
        f"Error:\n{error}\n\n"
        "Comprueba que Ollama esté funcionando y que "
        "el modelo llama3.2:1b esté instalado."
    )

# ============================================================
# 9. GENERAR RESUMEN DEL HISTORIAL
# ============================================================

def generar_resumen():
    # Solo está el system
    if len(mensajes) <= 1:
        messagebox.showinfo(
            "Resumen",
            "Todavía no existe una conversación para resumir."
        )
        return
    desactivar_botones()
    estado.config(
        text="Generando resumen...",
        fg="blue"
    )
    hilo = threading.Thread(
        target=consultar_resumen,
        daemon=True
    )
    hilo.start()

# ============================================================
# 10. CONSULTAR RESUMEN AL LLM
# ============================================================

def formatear_historial(lista_mensajes):
    """
    Numera cada pregunta del estudiante y devuelve
    (texto_historial, total_preguntas).
    El conteo lo hace el código porque un modelo de 1B cuenta mal.
    Las respuestas del tutor se recortan para no saturar el contexto.
    """
    lineas = []
    n = 0
    for mensaje in lista_mensajes:
        rol = mensaje["role"]
        contenido = mensaje["content"]
        if rol == "user":
            n += 1
            lineas.append(f"Pregunta {n} del estudiante: {contenido}")
        elif rol == "assistant":
            if len(contenido) > MAX_CHARS_TUTOR_EN_RESUMEN:
                contenido = contenido[:MAX_CHARS_TUTOR_EN_RESUMEN] + "..."
            lineas.append(f"Respuesta {n} del tutor: {contenido}")
    return "\n".join(lineas), n

def consultar_resumen():
    try:
        # Ignorar mensaje system
        historial, total_preguntas = formatear_historial(mensajes[1:])

        prompt_resumen = f"""
Esta es una conversación entre un estudiante y su tutor de Bases de Datos.
El estudiante hizo {total_preguntas} preguntas.

=== CONVERSACIÓN ===
{historial}
=== FIN DE LA CONVERSACIÓN ===

Resume la conversación usando solo lo que aparece en ella, cubriendo
las {total_preguntas} preguntas.

Responde exactamente con estas secciones:

TEMAS CONSULTADOS:
(un tema por cada pregunta, de la 1 a la {total_preguntas})

CONCEPTOS APRENDIDOS:
(resumen breve de los conceptos principales explicados)

DIFICULTADES DETECTADAS:
(solo errores o confusiones evidentes del estudiante; si no hubo,
escribe: "No se detectaron dificultades claras.")

RECOMENDACIÓN:
(una sola recomendación sobre los temas estudiados)
"""
        respuesta = ollama.chat(
            model=MODELO,
            messages=[
                {
                    "role": "system",
                    "content":
                    "Eres un asistente que resume "
                    "conversaciones educativas de manera breve."
                },
                {
                    "role": "user",
                    "content": prompt_resumen
                }
            ],
            options=OPCIONES_RESUMEN
        )
        resumen = respuesta[
            "message"
        ][
            "content"
        ]
        ventana.after(
            0,
            lambda: mostrar_resumen(resumen)
        )
    except Exception as error:
        texto_error = str(error)
        ventana.after(
            0,
            lambda: mostrar_error(texto_error)
        )

# ============================================================
# 11. VENTANA DEL RESUMEN
# ============================================================

def mostrar_resumen(resumen):
    activar_botones()
    ventana_resumen = tk.Toplevel(
        ventana
    )
    ventana_resumen.title(
        "Resumen de la sesión"
    )
    ventana_resumen.geometry(
        "650x450"
    )
    titulo_resumen = tk.Label(
        ventana_resumen,
        text="RESUMEN DE LA SESIÓN",
        font=(
            "Arial",
            16,
            "bold"
        )
    )
    titulo_resumen.pack(
        pady=15
    )
    texto = scrolledtext.ScrolledText(
        ventana_resumen,
        wrap=tk.WORD,
        font=(
            "Arial",
            11
        )
    )
    texto.pack(
        padx=20,
        pady=10,
        fill=tk.BOTH,
        expand=True
    )
    texto.insert(
        tk.END,
        resumen
    )
    texto.config(
        state="disabled"
    )

# ============================================================
# 12. LIMPIAR CONVERSACION
# ============================================================

def limpiar_chat():
    confirmar = messagebox.askyesno(
        "Limpiar conversación",
        "¿Deseas eliminar el historial actual?"
    )
    if not confirmar:
        return
    # Vaciar lista
    mensajes.clear()
    # Volver a colocar el mensaje system
    mensajes.append(
        {
            "role": "system",
            "content": mensaje_sistema
        }
    )
    # Limpiar chat visual
    chat.config(
        state="normal"
    )
    chat.delete(
        "1.0",
        tk.END
    )
    chat.config(
        state="disabled"
    )
    agregar_chat(
        "TUTOR",
        "Hola. Soy tu tutor inteligente de Bases de Datos.\n\n"
        "Puedes preguntarme sobre SQL, PostgreSQL, "
        "MongoDB, modelos relacionales, normalización "
        "y otros temas relacionados."
    )

# ============================================================
# 13. SALIR
# ============================================================

def salir():
    confirmar = messagebox.askyesno(
        "Salir",
        "¿Deseas cerrar el programa?"
    )
    if confirmar:
        ventana.destroy()

# ============================================================
# 14. ENVIAR CON ENTER
# ============================================================

def enviar_con_enter(event):
    # Shift + Enter = salto de línea
    if event.state & 0x0001:
        return
    enviar_pregunta()
    return "break"

# ============================================================
# 15. CREAR VENTANA PRINCIPAL
# ============================================================
ventana = tk.Tk()
ventana.title(
    "Tutor Inteligente de Bases de Datos"
)
ventana.geometry(
    "850x700"
)
ventana.minsize(
    700,
    600
)

# ============================================================
# TITULO
# ============================================================
titulo = tk.Label(
    ventana,
    text="TUTOR INTELIGENTE DE BASES DE DATOS",
    font=(
        "Arial",
        20,
        "bold"
    )
)
titulo.pack(
    pady=(15, 3)
)

# ============================================================
# MODELO UTILIZADO
# ============================================================
modelo_label = tk.Label(
    ventana,
    text=f"Modelo local: {MODELO}",
    font=(
        "Arial",
        10
    )
)
modelo_label.pack(
    pady=(0, 10)
)

# ============================================================
# AREA DEL CHAT
# ============================================================
chat = scrolledtext.ScrolledText(
    ventana,
    wrap=tk.WORD,
    font=(
        "Arial",
        11
    )
)
chat.pack(
    padx=20,
    pady=10,
    fill=tk.BOTH,
    expand=True
)
chat.tag_config(
    "nombre",
    font=(
        "Arial",
        11,
        "bold"
    )
)
chat.tag_config(
    "mensaje",
    spacing3=10
)
chat.config(
    state="disabled"
)

# ============================================================
# ETIQUETA DE PREGUNTA
# ============================================================
label_pregunta = tk.Label(
    ventana,
    text="Escribe tu pregunta:",
    font=(
        "Arial",
        11,
        "bold"
    )
)
label_pregunta.pack(
    anchor="w",
    padx=20
)

# ============================================================
# CUADRO DE TEXTO
# ============================================================
entrada = tk.Text(
    ventana,
    height=4,
    font=(
        "Arial",
        11
    )
)
entrada.pack(
    padx=20,
    pady=5,
    fill=tk.X
)

# ============================================================
# BOTONES
# ============================================================
frame_botones = tk.Frame(
    ventana
)
frame_botones.pack(
    pady=10
)
boton_enviar = tk.Button(
    frame_botones,
    text="Enviar",
    width=15,
    command=enviar_pregunta
)
boton_enviar.grid(
    row=0,
    column=0,
    padx=5
)
boton_resumen = tk.Button(
    frame_botones,
    text="Resumen",
    width=15,
    command=generar_resumen
)
boton_resumen.grid(
    row=0,
    column=1,
    padx=5
)
boton_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    width=15,
    command=limpiar_chat
)
boton_limpiar.grid(
    row=0,
    column=2,
    padx=5
)
boton_salir = tk.Button(
    frame_botones,
    text="Salir",
    width=15,
    command=salir
)
boton_salir.grid(
    row=0,
    column=3,
    padx=5
)

# ============================================================
# ESTADO
# ============================================================
estado = tk.Label(
    ventana,
    text="Listo",
    fg="green",
    font=(
        "Arial",
        10
    )
)
estado.pack(
    pady=(0, 10)
)

# ============================================================
# MENSAJE DE BIENVENIDA
# ============================================================
agregar_chat(
    "TUTOR",
    "Hola. Soy tu tutor inteligente de Bases de Datos.\n\n"
    "Puedes preguntarme sobre SQL, PostgreSQL, MongoDB, "
    "modelos relacionales, normalización, consultas y "
    "otros temas relacionados."
)

# ============================================================
# EVENTOS
# ============================================================
entrada.bind(
    "<Return>",
    enviar_con_enter
)
ventana.protocol(
    "WM_DELETE_WINDOW",
    salir
)

# ============================================================
# EJECUTAR
# ============================================================
ventana.mainloop()