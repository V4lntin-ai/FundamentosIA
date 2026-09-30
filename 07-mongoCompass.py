from pymongo import MongoClient
import os

cliente = MongoClient('mongodb://localhost:27017/')

db = cliente['Fundamentos'] 

coleccion = db['mi_coleccion']

coleccion.insert_one({'nombre': 'Juan', 'edad': 30, 'ciudad': 'Madrid'})

print(cliente.list_database_names())
print(db.list_collection_names())