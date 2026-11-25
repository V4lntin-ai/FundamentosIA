# ============================================================
# ALGORITMO HILL CLIMBING CON VISUALIZACION GRAFICA
# Seleccion de productos con presupuesto limitado
# ============================================================

import matplotlib.pyplot as plt

# Presupuesto disponible
presupuesto = 1000

# Productos: nombre, costo y beneficio
productos = {
    "A": {"costo": 200, "beneficio": 30},
    "B": {"costo": 300, "beneficio": 50},
    "C": {"costo": 400, "beneficio": 70},
    "D": {"costo": 250, "beneficio": 40},
    "E": {"costo": 350, "beneficio": 50}
}

# ============================================================
# FUNCION PARA CALCULAR COSTO Y BENEFICIO
# ============================================================

def evaluar(solucion):
    costo = 0
    beneficio = 0

    for producto in solucion:
        costo += productos[producto]["costo"]
        beneficio += productos[producto]["beneficio"]

    return costo, beneficio

# ============================================================
# ALGORITMO HILL CLIMBING
# ============================================================

def hill_climbing():
    solucion_actual = []
    costo_actual = 0
    beneficio_actual = 0
    paso = 0

    # Para guardar la evolución
    historial_pasos = [0]
    historial_costos = [0]
    historial_beneficios = [0]
    historial_soluciones = [solucion_actual.copy()]

    print("=== HILL CLIMBING ===")
    print("Presupuesto:", presupuesto)
    print("Estado inicial:", solucion_actual)

    while True:
        mejor_solucion = solucion_actual.copy()
        mejor_costo = costo_actual
        mejor_beneficio = beneficio_actual

        # Generar vecinos (agregar o quitar un producto)
        for producto in productos:
            vecino = solucion_actual.copy()

            if producto in vecino:
                vecino.remove(producto)
            else:
                vecino.append(producto)

            costo, beneficio = evaluar(vecino)

            # Solo considerar vecinos validos y que mejoren
            if costo <= presupuesto and beneficio > mejor_beneficio:
                mejor_solucion = vecino
                mejor_costo = costo
                mejor_beneficio = beneficio

        # Si no hay mejora, terminar
        if mejor_beneficio == beneficio_actual:
            print("\nNo existen vecinos con mayor beneficio.")
            break

        # Moverse al mejor vecino
        solucion_actual = mejor_solucion
        costo_actual = mejor_costo
        beneficio_actual = mejor_beneficio
        paso += 1

        historial_pasos.append(paso)
        historial_costos.append(costo_actual)
        historial_beneficios.append(beneficio_actual)
        historial_soluciones.append(solucion_actual.copy())

        print(f"\nPaso {paso}")
        print("Productos:", solucion_actual)
        print("Costo:", costo_actual)
        print("Beneficio:", beneficio_actual)

    print("\n========== RESULTADO FINAL ==========")
    print("Productos seleccionados:", solucion_actual)
    print("Costo total:", costo_actual)
    print("Beneficio total:", beneficio_actual)
    print("Presupuesto restante:", presupuesto - costo_actual)
    print("Pasos realizados:", paso)

    return solucion_actual, historial_pasos, historial_costos, historial_beneficios, historial_soluciones

# ============================================================
# FUNCION PARA GRAFICAR RESULTADOS
# ============================================================

def graficar_resultados(solucion_final, pasos, costos, beneficios):
    nombres = list(productos.keys())
    costos_productos = [productos[p]["costo"] for p in nombres]
    beneficios_productos = [productos[p]["beneficio"] for p in nombres]

    # -------------------------------
    # GRAFICA 1: Evolucion del algoritmo
    # -------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(pasos, costos, marker='o', label='Costo acumulado')
    plt.plot(pasos, beneficios, marker='s', label='Beneficio acumulado')
    plt.axhline(y=presupuesto, linestyle='--', label='Presupuesto')
    plt.title("Evolución del Hill Climbing")
    plt.xlabel("Paso")
    plt.ylabel("Valor")
    plt.xticks(pasos)
    plt.legend()
    plt.grid(True)
    plt.show()

    # -------------------------------
    # GRAFICA 2: Costos de productos
    # -------------------------------
    colores_costo = ["green" if p in solucion_final else "gray" for p in nombres]

    plt.figure(figsize=(10, 6))
    barras = plt.bar(nombres, costos_productos, color=colores_costo)
    plt.title("Costo de los productos")
    plt.xlabel("Productos")
    plt.ylabel("Costo")
    plt.axhline(y=presupuesto, linestyle='--', color='red', label='Presupuesto total')
    plt.legend()

    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, altura + 5, str(altura),
                 ha='center')

    plt.show()

    # -------------------------------
    # GRAFICA 3: Beneficios de productos
    # -------------------------------
    colores_beneficio = ["blue" if p in solucion_final else "gray" for p in nombres]

    plt.figure(figsize=(10, 6))
    barras = plt.bar(nombres, beneficios_productos, color=colores_beneficio)
    plt.title("Beneficio de los productos")
    plt.xlabel("Productos")
    plt.ylabel("Beneficio")

    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width()/2, altura + 1, str(altura),
                 ha='center')

    plt.show()

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

solucion_final, pasos, costos, beneficios, soluciones = hill_climbing()
graficar_resultados(solucion_final, pasos, costos, beneficios)