import math
import matplotlib.pyplot as plt

TAM = 10  # la cuadrícula va de 0 a TAM en x y y

def manhattan(a, b):
    """h(n) = |x1 - x2| + |y1 - y2|"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidiana(a, b):
    """DE = raíz((x1 - x2)² + (y1 - y2)²)"""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


fig, ax = plt.subplots(figsize=(7, 7))
puntos = []


def dibujar():
    ax.clear()
    ax.set_xlim(-0.5, TAM + 0.5)
    ax.set_ylim(-0.5, TAM + 0.5)
    ax.set_xticks(range(TAM + 1))
    ax.set_yticks(range(TAM + 1))
    ax.set_aspect("equal")
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    if len(puntos) == 0:
        ax.set_title("Haz clic para elegir el punto A")
    elif len(puntos) == 1:
        ax.set_title("Haz clic para elegir el punto B")

    nombres = ["A", "B"]
    for nombre, (x, y) in zip(nombres, puntos):
        ax.plot(x, y, "o", color="red", markersize=10)
        ax.annotate(f"{nombre}=({x},{y})", (x, y),
                    textcoords="offset points", xytext=(8, 8))

    if len(puntos) == 2:
        A, B = puntos
        m = manhattan(A, B)
        de = euclidiana(A, B)

        # Camino Manhattan: solo en horizontal y vertical
        ax.plot([A[0], B[0], B[0]], [A[1], A[1], B[1]],
                color="orange", linewidth=3, label=f"Manhattan = {m}")
        # Línea recta: euclidiana
        ax.plot([A[0], B[0]], [A[1], B[1]],
                "--", color="green", linewidth=2, label=f"Euclidiana = {de:.2f}")

        ax.legend(loc="upper left")
        ax.set_title("Clic en cualquier lugar para reiniciar")
        print(f"A = {A}, B = {B} -> M = {m}, DE = {de:.2f}")

    fig.canvas.draw_idle()


def on_click(event):
    if event.inaxes != ax:
        return

    # Ajusta el clic al punto entero más cercano de la cuadrícula
    x = min(max(round(event.xdata), 0), TAM)
    y = min(max(round(event.ydata), 0), TAM)

    if len(puntos) == 2:
        puntos.clear()  # tercer clic: reinicia
    puntos.append((x, y))
    dibujar()


fig.canvas.mpl_connect("button_press_event", on_click)
dibujar()
plt.show()