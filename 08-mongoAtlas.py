from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

cliente = None

mongo_user = os.getenv("mongo_user")
mongo_password = os.getenv("mongo_password")
mongo_cluster = os.getenv("mongo_cluster")
mongo_database = os.getenv("mongo_database")
mongo_collection = os.getenv("mongo_collection")

try:
    uri = f"mongodb+srv://{mongo_user}:{mongo_password}@{mongo_cluster}/"

    cliente = MongoClient(uri)

    db = cliente[mongo_database]
    coleccion = db[mongo_collection]

    dato = {
        "mensaje": "Me gusta Mac Miller"
    }

    resultado = coleccion.insert_one(dato)

    print("Dato insertado correctamente")
    print("ID:", resultado.inserted_id)

except Exception as error:
    print("Error:", error)

finally:
    if cliente is not None:
        cliente.close()