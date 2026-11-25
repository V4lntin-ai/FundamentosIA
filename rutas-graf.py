import networkx as nx
import matplotlib.pyplot as plt

# ==========================================
# DEFINICIÓN DEL ÁRBOL
# ==========================================
arbol = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["E"],
    "D": [],
    "E": ["F"],
    "F": []
}

# ==========================================
# FUNCIÓN PARA ENCONTRAR TODAS LAS RUTAS
# ==========================================
def encontrar_rutas(arbol, nodo_actual, camino=None):
    if camino is None:
        camino = []
    # Agregar el nodo actual al camino
    camino = camino + [nodo_actual]
    # Si el nodo no tiene hijos, entonces es una hoja
    if len(arbol[nodo_actual]) == 0:
        return [camino]
    rutas = []
    # Recorrer cada hijo del nodo
    for hijo in arbol[nodo_actual]:
        nuevas_rutas = encontrar_rutas(
            arbol,
            hijo,
            camino
        )
        rutas.extend(nuevas_rutas)
    return rutas

# ==========================================
# OBTENER LAS RUTAS
# ==========================================
rutas = encontrar_rutas(arbol, "A")

# ==========================================
# MOSTRAR LAS RUTAS EN CONSOLA
# ==========================================
print("\n==============================")
print("     RUTAS DEL ÁRBOL")
print("==============================\n")
for numero, ruta in enumerate(rutas, start=1):
    print(
        f"Ruta {numero}: "
        + " -> ".join(ruta)
    )
print("\nTotal de rutas:", len(rutas))

# ==========================================
# CREAR EL GRAFO
# ==========================================
grafo = nx.DiGraph()
# Agregar los nodos y conexiones
for padre, hijos in arbol.items():
    grafo.add_node(padre)
    for hijo in hijos:
        grafo.add_edge(
            padre,
            hijo
        )

# ==========================================
# POSICIONES DE LOS NODOS
# ==========================================
# Coordenadas para que el árbol se vea
# parecido al dibujo original
posiciones = {
    "A": (0, 3),
    "B": (-1, 2),
    "C": (1, 2),
    "D": (-1, 1),
    "E": (1, 1),
    "F": (1, 0)
}

# ==========================================
# GRAFICAR EL ÁRBOL
# ==========================================
plt.figure(
    figsize=(8, 7)
)
nx.draw_networkx_nodes(
    grafo,
    posiciones,
    node_size=2500
)
nx.draw_networkx_edges(
    grafo,
    posiciones,
    arrows=True,
    arrowsize=25,
    width=2
)
nx.draw_networkx_labels(
    grafo,
    posiciones,
    font_size=16,
    font_weight="bold"
)

# ==========================================
# TÍTULO
# ==========================================
plt.title(
    "Árbol de rutas",
    fontsize=18
)
# Quitar ejes
plt.axis("off")
# Ajustar la gráfica
plt.tight_layout()
# Mostrar ventana
plt.show()
