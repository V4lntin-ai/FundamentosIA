from pymongo import MongoClient
from dotenv import load_dotenv
import tkinter as tk
from tkinter import messagebox
import os

load_dotenv()

mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")
mongo_cluster = os.getenv("mongo_cluster")
mongo_database = os.getenv("mongo_database")
mongo_collection = os.getenv("mongo_collection")


def guardar_dato():
    mensaje = entrada.get()

    if mensaje == "":
        messagebox.showwarning("Aviso", "Escribe un mensaje")
        return

    cliente = None

    try:
        uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/"

        cliente = MongoClient(uri)

        db = cliente[mongo_database]
        coleccion = db[mongo_collection]

        dato = {
            "mensaje": mensaje
        }

        resultado = coleccion.insert_one(dato)

        messagebox.showinfo(
            "Correcto",
            f"Dato insertado correctamente\nID: {resultado.inserted_id}"
        )

        entrada.delete(0, tk.END)

    except Exception as error:
        messagebox.showerror("Error", str(error))

    finally:
        if cliente is not None:
            cliente.close()


# Ventana
ventana = tk.Tk()
ventana.title("MongoDB")
ventana.geometry("400x200")


# Título
titulo = tk.Label(
    ventana,
    text="Guardar dato en MongoDB",
    font=("Arial", 14)
)
titulo.pack(pady=20)


# Etiqueta
etiqueta = tk.Label(
    ventana,
    text="Mensaje:"
)
etiqueta.pack()


# Entrada
entrada = tk.Entry(
    ventana,
    width=40
)
entrada.pack(pady=10)


# Botón
boton = tk.Button(
    ventana,
    text="Guardar",
    command=guardar_dato
)
boton.pack(pady=10)


# Ejecutar ventana
ventana.mainloop()