
# ============================================================
# BÚSQUEDA CIEGA - UNIFORM COST SEARCH (UCS)
# ============================================================
#
# UCS = Uniform Cost Search
#       Búsqueda de Costo Uniforme
#
# OBJETIVO:
# Encontrar el camino de menor costo desde A hasta J.
#
# El programa muestra:
# - Camino encontrado
# - Profundidad
# - Pasos de exploración
# - Retrocesos
# - Costo total
# ============================================================

import heapq


# ------------------------------------------------------------
# 1. DEFINIMOS EL GRAFO CON COSTOS
# ------------------------------------------------------------
#
#                 A
#              2 / \ 8
#               B   C
#            4 / \1 2/ \8
#             D   E  F   G
#            3\   \2 \3
#              H   I   J
#
# Cada conexión tiene un costo.
# ------------------------------------------------------------

grafo = {

    "A": [("B", 2), ("C", 5)],

    "B": [("D", 4), ("E", 1)],

    "C": [("F", 2), ("G", 8)],

    "D": [("H", 3)],

    "E": [("I", 2)],

    "F": [("J", 3)],

    "G": [],

    "H": [],

    "I": [],

    "J": []
}


# ------------------------------------------------------------
# 2. FUNCIÓN UCS
# ------------------------------------------------------------

def ucs(inicio, objetivo):

    # Cola de prioridad:
    # (costo acumulado, nodo actual, camino)
    cola = [(0, inicio, [inicio])]

    heapq.heapify(cola)

    # Nodos que ya fueron explorados
    visitados = set()

    # Contadores
    pasos = 0
    retrocesos = 0
    profundidad_maxima = 0

    # --------------------------------------------------------
    # 3. INICIAR LA BÚSQUEDA
    # --------------------------------------------------------

    while cola:

        # Extraemos el nodo de menor costo acumulado
        costo_actual, actual, camino = heapq.heappop(cola)

        # Evitar explorar nuevamente un nodo
        if actual in visitados:
            continue

        visitados.add(actual)

        pasos += 1

        profundidad_actual = len(camino) - 1

        profundidad_maxima = max(
            profundidad_maxima,
            profundidad_actual
        )

        print(
            f"Paso {pasos}: "
            f"Visitando {actual} | "
            f"Costo acumulado: {costo_actual} | "
            f"Profundidad: {profundidad_actual}"
        )

        # ----------------------------------------------------
        # 4. COMPROBAR SI ENCONTRAMOS EL OBJETIVO
        # ----------------------------------------------------

        if actual == objetivo:

            return {
                "camino": camino,
                "costo": costo_actual,
                "profundidad": profundidad_actual,
                "pasos": pasos,
                "retrocesos": retrocesos,
                "profundidad_maxima": profundidad_maxima,
                "visitados": visitados
            }

        # ----------------------------------------------------
        # 5. EXPLORAR LOS VECINOS
        # ----------------------------------------------------

        for vecino, costo in grafo[actual]:

            if vecino not in visitados:

                nuevo_costo = costo_actual + costo

                nuevo_camino = camino + [vecino]

                # Agregar a la cola de prioridad
                heapq.heappush(
                    cola,
                    (
                        nuevo_costo,
                        vecino,
                        nuevo_camino
                    )
                )

    # --------------------------------------------------------
    # 6. OBJETIVO NO ENCONTRADO
    # --------------------------------------------------------

    return {
        "camino": None,
        "costo": None,
        "profundidad": None,
        "pasos": pasos,
        "retrocesos": retrocesos,
        "profundidad_maxima": profundidad_maxima,
        "visitados": visitados
    }


# ============================================================
# 7. EJECUTAR LA BÚSQUEDA
# ============================================================

inicio = "A"
objetivo = "J"

print("=" * 60)
print("       BÚSQUEDA DE COSTO UNIFORME (UCS)")
print("=" * 60)

resultado = ucs(inicio, objetivo)


# ============================================================
# 8. MOSTRAR RESULTADOS
# ============================================================

print("\n" + "=" * 60)
print("                 RESULTADOS UCS")
print("=" * 60)

if resultado["camino"]:

    print("\nObjetivo encontrado:", objetivo)

    print(
        "Camino encontrado:",
        " -> ".join(resultado["camino"])
    )

    print(
        "Profundidad:",
        resultado["profundidad"]
    )

    print(
        "Pasos de exploración:",
        resultado["pasos"]
    )

    print(
        "Retrocesos:",
        resultado["retrocesos"]
    )

    print(
        "Costo total:",
        resultado["costo"]
    )

    print(
        "Profundidad máxima explorada:",
        resultado["profundidad_maxima"]
    )

    print(
        "Nodos explorados:",
        len(resultado["visitados"])
    )

else:

    print("\nNo se encontró el objetivo.")

    print(
        "Pasos de exploración:",
        resultado["pasos"]
    )

print("=" * 60)
