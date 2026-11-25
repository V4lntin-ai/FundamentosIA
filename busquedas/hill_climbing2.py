import random
import matplotlib.pyplot as plt

EMPLEADOS = ["Ana", "Luis", "Carlos", "Maria"]
TURNOS = ["Mañana", "Tarde", "Noche", "Mixto"]
PREFERENCIAS = {"Ana": "Mañana", "Luis": "Tarde", "Carlos": "Noche", "Maria": "Mañana"}


def satisfaccion(estado):
    """Función objetivo: cuántos empleados quedaron en su turno preferido."""
    return sum(1 for emp, turno in zip(EMPLEADOS, estado) if PREFERENCIAS[emp] == turno)


def vecinos(estado):
    """Cada vecino intercambia los turnos de DOS empleados (así siempre hay 1 empleado por turno)."""
    resultado = []
    for i in range(len(estado)):
        for j in range(i + 1, len(estado)):
            vecino = list(estado)
            vecino[i], vecino[j] = vecino[j], vecino[i]
            resultado.append(vecino)
    return resultado


def mostrar(paso, estado):
    asignacion = ", ".join(f"{e}->{t}" for e, t in zip(EMPLEADOS, estado))
    print(f"Paso {paso}: {asignacion} | satisfacción = {satisfaccion(estado)}")


def hill_climbing(estado_inicial):
    actual = list(estado_inicial)
    historial = [satisfaccion(actual)]
    paso = 0
    mostrar(paso, actual)

    while True:
        mejor_vecino = max(vecinos(actual), key=satisfaccion)

        # Si ningún vecino mejora el estado actual, nos detenemos
        if satisfaccion(mejor_vecino) <= satisfaccion(actual):
            return actual, historial

        actual = mejor_vecino
        paso += 1
        historial.append(satisfaccion(actual))
        mostrar(paso, actual)


def graficar(historial, estado_final):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Izquierda: cómo mejora la satisfacción en cada paso
    ax1.step(range(len(historial)), historial, where="post", marker="o", linewidth=2)
    ax1.set_xticks(range(len(historial)))
    ax1.set_yticks(range(len(EMPLEADOS) + 1))
    ax1.set_xlabel("Paso de Hill Climbing")
    ax1.set_ylabel("Empleados satisfechos")
    ax1.set_title("Evolución de la satisfacción")
    ax1.grid(True)

    # Derecha: asignación final (empleado x turno)
    matriz = [[1 if t == turno else 0 for t in TURNOS] for turno in estado_final]
    ax2.imshow(matriz, cmap="Blues", vmin=0, vmax=1.5)
    ax2.set_xticks(range(len(TURNOS)))
    ax2.set_xticklabels(TURNOS)
    ax2.set_yticks(range(len(EMPLEADOS)))
    ax2.set_yticklabels(EMPLEADOS)
    ax2.set_title("Asignación final (✔ = turno preferido)")

    for i, emp in enumerate(EMPLEADOS):
        for j, turno in enumerate(TURNOS):
            if matriz[i][j]:
                texto = "✔" if PREFERENCIAS[emp] == turno else "✘"
                color = "green" if texto == "✔" else "red"
                ax2.text(j, i, texto, ha="center", va="center",
                         fontsize=22, color=color, fontweight="bold")

    plt.tight_layout()
    plt.show()


# Estado: lista de turnos, uno por empleado (en el orden de EMPLEADOS)
random.seed(1)
inicial = random.sample(TURNOS, len(TURNOS))

print("=== Hill Climbing ===")
final, historial = hill_climbing(inicial)
print(f"\nSatisfacción final: {satisfaccion(final)} de {len(EMPLEADOS)}")

graficar(historial, final)