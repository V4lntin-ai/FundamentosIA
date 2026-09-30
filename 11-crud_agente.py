import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")
mongo_cluster = os.getenv("mongo_cluster")
mongo_database = os.getenv("mongo_database")
mongo_collection = os.getenv("mongo_collection")


class AgenteClimatizacion:

    def __init__(self):
        self.temperatura = 0.0
        self.humedad = 0.0
        self.accion = ""

    def percibir(self, temperatura, humedad):
        self.temperatura = temperatura
        self.humedad = humedad

    def tomar_decision(self):

        if self.humedad < 0 or self.humedad > 100:
            self.accion = "Error: Humedad fuera de rango"

        elif self.temperatura < -50 or self.temperatura > 60:
            self.accion = "Error: Temperatura fuera de rango"

        elif self.temperatura >= 32 and self.humedad >= 70:
            self.accion = "Encender aire acondicionado y deshumidificador"

        elif self.temperatura >= 30:
            self.accion = "Encender aire acondicionado"

        elif self.temperatura >= 26 and self.humedad >= 70:
            self.accion = "Encender deshumidificador"

        elif self.temperatura >= 26:
            self.accion = "Encender ventilador"

        elif self.temperatura < 18 and self.humedad < 40:
            self.accion = "Encender calefacción y humidificador"

        elif self.temperatura < 18:
            self.accion = "Encender calefacción"

        elif self.humedad >= 75:
            self.accion = "Encender deshumidificador"

        elif self.humedad < 30:
            self.accion = "Encender humidificador"

        else:
            self.accion = "Temperatura y humedad adecuadas"


agente = AgenteClimatizacion()


def conectar():

    uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/"

    cliente = MongoClient(uri)

    db = cliente[mongo_database]

    coleccion = db[mongo_collection]

    return cliente, coleccion

# GUARDAR
def guardar():

    try:
        temperatura = float(entrada_temperatura.get())
        humedad = float(entrada_humedad.get())

        agente.percibir(temperatura, humedad)
        agente.tomar_decision()

        resultado.config(
            text="Acción: " + agente.accion
        )

        if "Error" in agente.accion:
            mensaje.config(
                text="Los datos no fueron guardados"
            )
            return

        cliente, coleccion = conectar()

        dato = {
            "temperatura": temperatura,
            "humedad": humedad,
            "accion": agente.accion
        }

        coleccion.insert_one(dato)

        cliente.close()

        mensaje.config(
            text="Datos guardados correctamente"
        )

        limpiar()
        consultar()

    except ValueError:
        mensaje.config(
            text="Ingresa valores numéricos"
        )

    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )

# CONSULTAR
def consultar():

    try:
        # Limpiar tabla
        for fila in tabla.get_children():
            tabla.delete(fila)

        cliente, coleccion = conectar()

        documentos = coleccion.find()

        for documento in documentos:

            tabla.insert(
                "",
                tk.END,
                values=(
                    str(documento["_id"]),
                    documento.get("temperatura", ""),
                    documento.get("humedad", ""),
                    documento.get("accion", "")
                )
            )

        cliente.close()

        mensaje.config(
            text="Datos consultados correctamente"
        )

    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )

# SELECCIONAR
def seleccionar_registro(event):

    seleccion = tabla.selection()

    if seleccion:

        fila = tabla.item(seleccion[0])

        datos = fila["values"]

        entrada_temperatura.delete(0, tk.END)
        entrada_temperatura.insert(0, datos[1])

        entrada_humedad.delete(0, tk.END)
        entrada_humedad.insert(0, datos[2])

        resultado.config(
            text="Acción: " + str(datos[3])
        )

# ACTUALIZAR
def actualizar():

    seleccion = tabla.selection()

    if not seleccion:
        mensaje.config(
            text="Selecciona un registro para actualizar"
        )
        return

    try:
        fila = tabla.item(seleccion[0])

        datos = fila["values"]

        id_documento = datos[0]

        temperatura = float(entrada_temperatura.get())
        humedad = float(entrada_humedad.get())

        agente.percibir(temperatura, humedad)
        agente.tomar_decision()

        if "Error" in agente.accion:
            mensaje.config(
                text=agente.accion
            )
            return

        cliente, coleccion = conectar()

        coleccion.update_one(
            {"_id": ObjectId(id_documento)},
            {
                "$set": {
                    "temperatura": temperatura,
                    "humedad": humedad,
                    "accion": agente.accion
                }
            }
        )

        cliente.close()

        resultado.config(
            text="Acción: " + agente.accion
        )

        mensaje.config(
            text="Registro actualizado correctamente"
        )

        limpiar()
        consultar()

    except ValueError:
        mensaje.config(
            text="Ingresa valores numéricos"
        )

    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )

# ELIMINAR
def eliminar():

    seleccion = tabla.selection()

    if not seleccion:
        mensaje.config(
            text="Selecciona un registro para eliminar"
        )
        return

    try:
        fila = tabla.item(seleccion[0])

        datos = fila["values"]

        id_documento = datos[0]

        cliente, coleccion = conectar()

        coleccion.delete_one(
            {"_id": ObjectId(id_documento)}
        )

        cliente.close()

        mensaje.config(
            text="Registro eliminado correctamente"
        )

        limpiar()
        consultar()

    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )

# LIMPIAR CAMPOS
def limpiar():

    entrada_temperatura.delete(0, tk.END)
    entrada_humedad.delete(0, tk.END)

    resultado.config(
        text="Acción:"
    )

# FILTRAR POR ACCIÓN
    

# INTERFAZ
ventana = tk.Tk()
ventana.title("Agente de Climatización")
ventana.geometry("850x550")

# Título
titulo = tk.Label(
    ventana,
    text="Agente de Climatización",
    font=("Arial", 16)
)

titulo.pack(pady=15)

# Temperatura
tk.Label(
    ventana,
    text="Temperatura actual (°C):"
).pack()

entrada_temperatura = tk.Entry(
    ventana,
    width=20
)

entrada_temperatura.pack(pady=5)

# Humedad
tk.Label(
    ventana,
    text="Humedad actual (%):"
).pack()

entrada_humedad = tk.Entry(
    ventana,
    width=20
)

entrada_humedad.pack(pady=5)

# BOTONES
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=15)

boton_guardar = tk.Button(
    frame_botones,
    text="Guardar",
    command=guardar
)

boton_guardar.grid(
    row=0,
    column=0,
    padx=5
)

boton_consultar = tk.Button(
    frame_botones,
    text="Consultar",
    command=consultar
)

boton_consultar.grid(
    row=0,
    column=1,
    padx=5
)

boton_actualizar = tk.Button(
    frame_botones,
    text="Actualizar",
    command=actualizar
)

boton_actualizar.grid(
    row=0,
    column=2,
    padx=5
)

boton_eliminar = tk.Button(
    frame_botones,
    text="Eliminar",
    command=eliminar
)

boton_eliminar.grid(
    row=0,
    column=3,
    padx=5
)

boton_limpiar = tk.Button(
    frame_botones,
    text="Limpiar",
    command=limpiar
)

boton_limpiar.grid(
    row=0,
    column=4,
    padx=5
)

# RESULTADO DEL AGENTE
resultado = tk.Label(
    ventana,
    text="Acción:",
    font=("Arial", 11)
)

resultado.pack(pady=5)

# Mensajes de la base de datos
mensaje = tk.Label(
    ventana,
    text=""
)

mensaje.pack(pady=5)

# TABLA
tabla = ttk.Treeview(
    ventana,
    columns=(
        "id",
        "temperatura",
        "humedad",
        "accion"
    ),
    show="headings"
)

tabla.heading(
    "id",
    text="ID"
)

tabla.heading(
    "temperatura",
    text="Temperatura"
)

tabla.heading(
    "humedad",
    text="Humedad"
)

tabla.heading(
    "accion",
    text="Acción"
)

tabla.column(
    "id",
    width=180
)

tabla.column(
    "temperatura",
    width=90
)

tabla.column(
    "humedad",
    width=90
)

tabla.column(
    "accion",
    width=350
)

tabla.pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

# Detectar selección de registro
tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar_registro
)

# Mostrar datos al iniciar
consultar()

# Ejecutar ventana
ventana.mainloop()