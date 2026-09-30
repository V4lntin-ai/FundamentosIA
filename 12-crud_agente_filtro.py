import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# VARIABLES DE ENTORNO
load_dotenv()
mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")
mongo_cluster = os.getenv("mongo_cluster")
mongo_database = os.getenv("mongo_database")
mongo_collection = os.getenv("mongo_collection")

# CLASE AGENTE
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

# CONEXIÓN A MONGODB
def conectar():
    uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/"
    cliente = MongoClient(uri)
    db = cliente[mongo_database]
    coleccion = db[mongo_collection]
    return cliente, coleccion

# ACTUALIZAR GRÁFICA
def actualizar_grafica(temperaturas, humedades, accion="Todas las acciones"):
    grafica.clear()
    if len(temperaturas) > 0:
        grafica.scatter(
            temperaturas,
            humedades
        )
        grafica.set_title(
            accion
        )
    else:
        grafica.set_title(
            "No hay datos para mostrar"
        )
    grafica.set_xlabel(
        "Temperatura (°C)"
    )
    grafica.set_ylabel(
        "Humedad (%)"
    )
    grafica.grid(True)
    figura.tight_layout()
    canvas.draw()

# MOSTRAR DOCUMENTOS EN TABLA Y GRÁFICA
def mostrar_documentos(documentos, accion):
    for fila in tabla.get_children():
        tabla.delete(fila)
    temperaturas = []
    humedades = []
    contador = 0
    for documento in documentos:
        temperatura = documento.get(
            "temperatura",
            0
        )
        humedad = documento.get(
            "humedad",
            0
        )
        accion_documento = documento.get(
            "accion",
            ""
        )
        tabla.insert(
            "",
            tk.END,
            values=(
                str(documento["_id"]),
                temperatura,
                humedad,
                accion_documento
            )
        )
        temperaturas.append(
            temperatura
        )
        humedades.append(
            humedad
        )
        contador += 1
    actualizar_grafica(
        temperaturas,
        humedades,
        accion
    )
    return contador

# GUARDAR
def guardar():
    cliente = None
    try:
        temperatura = float(
            entrada_temperatura.get()
        )
        humedad = float(
            entrada_humedad.get()
        )
        agente.percibir(
            temperatura,
            humedad
        )
        agente.tomar_decision()
        resultado.config(
            text="Acción: " + agente.accion
        )
        if "Error" in agente.accion:
            mensaje.config(
                text=agente.accion
            )
            return
        cliente, coleccion = conectar()
        dato = {
            "temperatura": temperatura,
            "humedad": humedad,
            "accion": agente.accion
        }
        coleccion.insert_one(
            dato
        )
        limpiar_campos()
        filtrar_accion()
        mensaje.config(
            text="Datos guardados correctamente en la BD"
        )
    except ValueError:
        mensaje.config(
            text="Ingresa valores numéricos"
        )
    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )
    finally:
        if cliente is not None:
            cliente.close()

# CONSULTAR TODOS
def consultar():
    cliente = None
    try:
        combo_acciones.current(0)
        cliente, coleccion = conectar()
        documentos = list(
            coleccion.find()
        )
        contador = mostrar_documentos(
            documentos,
            "Todas las acciones"
        )
        mensaje.config(
            text=f"Registros encontrados: {contador}"
        )
    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )
    finally:
        if cliente is not None:
            cliente.close()

# FILTRAR POR ACCIÓN
def filtrar_accion(event=None):
    cliente = None
    accion_seleccionada = combo_acciones.get()
    try:
        cliente, coleccion = conectar()
        if accion_seleccionada == "Todas las acciones":
            documentos = list(
                coleccion.find()
            )
        else:
            documentos = list(
                coleccion.find(
                    {
                        "accion": accion_seleccionada
                    }
                )
            )
        contador = mostrar_documentos(
            documentos,
            accion_seleccionada
        )
        mensaje.config(
            text=f"Registros encontrados: {contador}"
        )
    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )
    finally:
        if cliente is not None:
            cliente.close()

# SELECCIONAR REGISTRO
def seleccionar_registro(event):
    seleccion = tabla.selection()
    if seleccion:
        fila = tabla.item(
            seleccion[0]
        )
        datos = fila["values"]
        entrada_temperatura.delete(
            0,
            tk.END
        )
        entrada_temperatura.insert(
            0,
            datos[1]
        )
        entrada_humedad.delete(
            0,
            tk.END
        )
        entrada_humedad.insert(
            0,
            datos[2]
        )
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
    cliente = None
    try:
        fila = tabla.item(
            seleccion[0]
        )
        datos = fila["values"]
        id_documento = datos[0]
        temperatura = float(
            entrada_temperatura.get()
        )
        humedad = float(
            entrada_humedad.get()
        )
        agente.percibir(
            temperatura,
            humedad
        )
        agente.tomar_decision()
        if "Error" in agente.accion:
            mensaje.config(
                text=agente.accion
            )
            return
        cliente, coleccion = conectar()
        coleccion.update_one(
            {
                "_id": ObjectId(id_documento)
            },
            {
                "$set": {
                    "temperatura": temperatura,
                    "humedad": humedad,
                    "accion": agente.accion
                }
            }
        )
        limpiar_campos()
        filtrar_accion()
        mensaje.config(
            text="Registro actualizado correctamente"
        )
    except ValueError:
        mensaje.config(
            text="Ingresa valores numéricos"
        )
    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )
    finally:
        if cliente is not None:
            cliente.close()

# ELIMINAR
def eliminar():
    seleccion = tabla.selection()
    if not seleccion:
        mensaje.config(
            text="Selecciona un registro para eliminar"
        )
        return
    cliente = None
    try:
        fila = tabla.item(
            seleccion[0]
        )
        datos = fila["values"]
        id_documento = datos[0]
        cliente, coleccion = conectar()
        coleccion.delete_one(
            {
                "_id": ObjectId(id_documento)
            }
        )
        limpiar_campos()
        filtrar_accion()
        mensaje.config(
            text="Registro eliminado correctamente"
        )
    except Exception as error:
        mensaje.config(
            text="Error: " + str(error)
        )
    finally:
        if cliente is not None:
            cliente.close()

# LIMPIAR CAMPOS
def limpiar_campos():
    entrada_temperatura.delete(
        0,
        tk.END
    )
    entrada_humedad.delete(
        0,
        tk.END
    )
    resultado.config(
        text="Acción:"
    )

# INTERFAZ GRÁFICA
ventana = tk.Tk()
ventana.title(
    "Agente de Climatización"
)
ventana.geometry(
    "1000x750"
)

# TÍTULO
titulo = tk.Label(
    ventana,
    text="Agente de Climatización",
    font=("Arial", 16)
)
titulo.pack(
    pady=10
)

# CAMPOS
frame_campos = tk.Frame(
    ventana
)
frame_campos.pack(
    pady=5
)
tk.Label(
    frame_campos,
    text="Temperatura actual (°C):"
).grid(
    row=0,
    column=0,
    padx=5
)
entrada_temperatura = tk.Entry(
    frame_campos,
    width=15
)
entrada_temperatura.grid(
    row=0,
    column=1,
    padx=5
)
tk.Label(
    frame_campos,
    text="Humedad actual (%):"
).grid(
    row=0,
    column=2,
    padx=5
)
entrada_humedad = tk.Entry(
    frame_campos,
    width=15
)
entrada_humedad.grid(
    row=0,
    column=3,
    padx=5
)

# BOTONES CRUD
frame_botones = tk.Frame(
    ventana
)
frame_botones.pack(
    pady=10
)
tk.Button(
    frame_botones,
    text="Guardar",
    command=guardar
).grid(
    row=0,
    column=0,
    padx=5
)
tk.Button(
    frame_botones,
    text="Consultar",
    command=consultar
).grid(
    row=0,
    column=1,
    padx=5
)
tk.Button(
    frame_botones,
    text="Actualizar",
    command=actualizar
).grid(
    row=0,
    column=2,
    padx=5
)
tk.Button(
    frame_botones,
    text="Eliminar",
    command=eliminar
).grid(
    row=0,
    column=3,
    padx=5
)
tk.Button(
    frame_botones,
    text="Limpiar",
    command=limpiar_campos
).grid(
    row=0,
    column=4,
    padx=5
)

# RESULTADO
resultado = tk.Label(
    ventana,
    text="Acción:",
    font=("Arial", 11)
)
resultado.pack(
    pady=5
)
mensaje = tk.Label(
    ventana,
    text=""
)
mensaje.pack(
    pady=5
)

# FILTRO POR ACCIÓN
frame_filtro = tk.Frame(
    ventana
)
frame_filtro.pack(
    pady=10
)
tk.Label(
    frame_filtro,
    text="Filtrar por acción:"
).grid(
    row=0,
    column=0,
    padx=5
)
acciones = [
    "Todas las acciones",
    "Encender aire acondicionado y deshumidificador",
    "Encender aire acondicionado",
    "Encender deshumidificador",
    "Encender ventilador",
    "Encender calefacción y humidificador",
    "Encender calefacción",
    "Encender humidificador",
    "Temperatura y humedad adecuadas"
]
combo_acciones = ttk.Combobox(
    frame_filtro,
    values=acciones,
    width=45,
    state="readonly"
)
combo_acciones.grid(
    row=0,
    column=1,
    padx=5
)
combo_acciones.current(0)
tk.Button(
    frame_filtro,
    text="Filtrar",
    command=filtrar_accion
).grid(
    row=0,
    column=2,
    padx=5
)
combo_acciones.bind(
    "<<ComboboxSelected>>",
    filtrar_accion
)

# TABLA
frame_tabla = tk.Frame(
    ventana
)
frame_tabla.pack(
    padx=20,
    pady=5,
    fill="both",
    expand=True
)
tabla = ttk.Treeview(
    frame_tabla,
    columns=(
        "id",
        "temperatura",
        "humedad",
        "accion"
    ),
    show="headings",
    height=8
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
    width=190
)
tabla.column(
    "temperatura",
    width=100
)
tabla.column(
    "humedad",
    width=100
)
tabla.column(
    "accion",
    width=400
)
tabla.pack(
    fill="both",
    expand=True
)
tabla.bind(
    "<<TreeviewSelect>>",
    seleccionar_registro
)

# GRÁFICA DE DISPERSIÓN
figura = Figure(
    figsize=(8, 3),
    dpi=100
)
grafica = figura.add_subplot(
    111
)
grafica.set_title(
    "Temperatura y Humedad"
)
grafica.set_xlabel(
    "Temperatura (°C)"
)
grafica.set_ylabel(
    "Humedad (%)"
)
grafica.grid(True)
canvas = FigureCanvasTkAgg(
    figura,
    master=ventana
)
canvas.get_tk_widget().pack(
    padx=20,
    pady=10,
    fill="both",
    expand=True
)

# CONSULTAR DATOS AL INICIAR
consultar()

# EJECUTAR PROGRAMA
ventana.mainloop()
