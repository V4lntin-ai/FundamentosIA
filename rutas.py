# Árbol representado mediante un diccionario
arbol = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": ["F"],
    "F": []
}


def encontrar_caminos(arbol, nodo, camino=[]):
    camino = camino + [nodo]

    # Si no tiene hijos, llegamos a una hoja
    if len(arbol[nodo]) == 0:
        print(" -> ".join(camino))
        return

    # Recorrer cada hijo
    for hijo in arbol[nodo]:
        encontrar_caminos(arbol, hijo, camino)


print("Caminos posibles del árbol:\n")

encontrar_caminos(arbol, "A")