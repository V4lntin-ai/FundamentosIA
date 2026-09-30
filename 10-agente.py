import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
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

    def guardar_mongodb(self):

        cliente = None

        try:
            uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/"

            cliente = MongoClient(uri)

            db = cliente[mongo_database]
            coleccion = db[mongo_collection]

            dato = {
                "temperatura": self.temperatura,
                "humedad": self.humedad,
                "accion": self.accion
            }

            coleccion.insert_one(dato)

            return True

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar en MongoDB:\n{error}"
            )

            return False

        finally:
            if cliente is not None:
                cliente.close()


agente = AgenteClimatizacion()


def evaluar():

    try:
        temperatura = float(entrada_temperatura.get())
        humedad = float(entrada_humedad.get())

        agente.percibir(temperatura, humedad)
        agente.tomar_decision()

        resultado.config(
            text="Acción: " + agente.accion
        )

        if "Error" not in agente.accion:

            guardado = agente.guardar_mongodb()

            if guardado:
                mensaje_bd.config(
                    text="Datos guardados correctamente en la BD"
                )

        else:
            mensaje_bd.config(
                text="Los datos no fueron guardados"
            )

    except ValueError:
        mensaje_bd.config(text="")
        messagebox.showerror(
            "Error",
            "Ingresa valores numéricos."
        )

# Ventana
ventana = tk.Tk()
ventana.title("Agente de Climatización")
ventana.geometry("500x350")

# Título
titulo = tk.Label(
    ventana,
    text="Agente de Climatización",
    font=("Arial", 16)
)
titulo.pack(pady=20)

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

# Botón
boton = tk.Button(
    ventana,
    text="Evaluar y guardar",
    command=evaluar
)
boton.pack(pady=20)

# Resultado
resultado = tk.Label(
    ventana,
    text="Acción: ",
    font=("Arial", 11)
)
resultado.pack(pady=5)


# Mensaje de guardado
mensaje_bd = tk.Label(
    ventana,
    text=""
)
mensaje_bd.pack(pady=5)

ventana.mainloop()  