
# ============================================================
# BÚSQUEDA CIEGA - DEPTH FIRST SEARCH (DFS)
# ============================================================
#
# DFS = Depth First Search
#       Búsqueda en Profundidad
#
# OBJETIVO:
# Buscar el nodo H desde el nodo A y mostrar:
# - Ruta encontrada
# - Profundidad del objetivo
# - Pasos de exploración
# - Retrocesos realizados
# ============================================================


# ------------------------------------------------------------
# 1. DEFINIMOS EL ESPACIO DE BÚSQUEDA
# ------------------------------------------------------------
#
# Estructura del árbol:
#
#               A
#              / \
#             B   C
#            / \   \
#           D   E   F
#              / \
#             G   H
#
# ------------------------------------------------------------

grafo = {

    "A": ["B", "C"],

    "B": ["D", "E"],

    "C": ["F"],

    "D": [],

    "E": ["G", "H"],

    "F": [],

    "G": [],

    "H": []
}


# ------------------------------------------------------------
# 2. FUNCIÓN DFS
# ------------------------------------------------------------

def dfs(actual, objetivo, visitados=None,
        camino=None, estadisticas=None):

    # Crear estructuras en la primera llamada
    if visitados is None:
        visitados = set()

    if camino is None:
        camino = []

    if estadisticas is None:
        estadisticas = {
            "pasos": 0,
            "retrocesos": 0,
            "profundidad_maxima": 0
        }

    # --------------------------------------------------------
    # 3. MARCAR EL ESTADO COMO VISITADO
    # --------------------------------------------------------

    visitados.add(actual)
    camino.append(actual)

    # Contar cada nodo explorado como un paso
    estadisticas["pasos"] += 1

    # La raíz A tiene profundidad 0
    profundidad_actual = len(camino) - 1

    estadisticas["profundidad_maxima"] = max(
        estadisticas["profundidad_maxima"],
        profundidad_actual
    )

    print(
        f"Paso {estadisticas['pasos']}: "
        f"Visitando {actual} | "
        f"Profundidad: {profundidad_actual}"
    )

    # --------------------------------------------------------
    # 4. COMPROBAR SI ENCONTRAMOS EL OBJETIVO
    # --------------------------------------------------------

    if actual == objetivo:
        return camino.copy()

    # --------------------------------------------------------
    # 5. EXPLORAR LOS VECINOS
    # --------------------------------------------------------

    for vecino in grafo[actual]:

        if vecino not in visitados:

            resultado = dfs(
                vecino,
                objetivo,
                visitados,
                camino,
                estadisticas
            )

            if resultado is not None:
                return resultado

    # --------------------------------------------------------
    # 6. RETROCESO (BACKTRACKING)
    # --------------------------------------------------------
    #
    # Si no encontramos el objetivo, regresamos
    # al nodo anterior.
    # --------------------------------------------------------

    camino.pop()

    estadisticas["retrocesos"] += 1

    print(
        f"Retroceso {estadisticas['retrocesos']}: "
        f"Regresando desde {actual}"
    )

    return None


# ============================================================
# 7. EJECUTAR LA BÚSQUEDA
# ============================================================

inicio = "A"
objetivo = "H"

estadisticas = {
    "pasos": 0,
    "retrocesos": 0,
    "profundidad_maxima": 0
}

print("=" * 55)
print("       BÚSQUEDA EN PROFUNDIDAD (DFS)")
print("=" * 55)

ruta = dfs(
    inicio,
    objetivo,
    estadisticas=estadisticas
)


# ============================================================
# 8. MOSTRAR RESULTADOS
# ============================================================

print("\n" + "=" * 55)
print("             RESULTADOS DFS")
print("=" * 55)

if ruta:

    print("\nObjetivo encontrado:", objetivo)

    print("Ruta encontrada:", " -> ".join(ruta))

    print("Profundidad del objetivo:", len(ruta) - 1)

    print("Nodos en la ruta:", len(ruta))

    print("Pasos de exploración:",
          estadisticas["pasos"])

    print("Retrocesos realizados:",
          estadisticas["retrocesos"])

    print("Profundidad máxima explorada:",
          estadisticas["profundidad_maxima"])

else:

    print("\nNo se encontró una ruta.")

    print("Pasos de exploración:",
          estadisticas["pasos"])

    print("Retrocesos realizados:",
          estadisticas["retrocesos"])

print("=" * 55)
