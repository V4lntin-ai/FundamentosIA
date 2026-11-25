import math
import random
import tkinter as tk
from itertools import permutations
from tkinter import ttk

import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ---------------------------------------------------------------------------
# Datos del problema
# ---------------------------------------------------------------------------
NOMBRES = ["Almacén", "A", "B", "C", "D", "E"]
COORDS = [(0, 0), (2, 6), (5, 3), (6, 9), (8, 2), (1, 1)]
CLIENTES = [1, 2, 3, 4, 5]  # índices de A..E (como el [1,2,3,4,5] del pizarrón)


def euclidiana(p, q):
    """DE = raíz((x1 - x2)² + (y1 - y2)²)"""
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


MATRIZ = [[euclidiana(p, q) for q in COORDS] for p in COORDS]


def distancia_ruta(ruta):
    """Almacén -> clientes en el orden de la ruta -> Almacén."""
    camino = (0, *ruta, 0)
    return sum(MATRIZ[a][b] for a, b in zip(camino, camino[1:]))


def nombre_ruta(ruta, con_almacen=False):
    letras = [NOMBRES[i] for i in ruta]
    if con_almacen:
        letras = ["Almacén", *letras, "Almacén"]
    return " → ".join(letras)


# 5! = 120 rutas posibles, ordenadas de la más corta a la más larga
RUTAS = sorted(permutations(CLIENTES), key=distancia_ruta)

# ---------------------------------------------------------------------------
# Algoritmo genético
# ---------------------------------------------------------------------------
TAM_POBLACION = 10
GENERACIONES = 30
PROB_MUTACION = 0.5
ELITE = 2  # los 2 mejores pasan directo a la siguiente generación


def aptitud(individuo):
    """Función fitness: entre más corta la ruta, mayor la aptitud."""
    return 1 / distancia_ruta(individuo)


def seleccion(poblacion):
    """Torneo: de 3 individuos al azar gana el más apto."""
    return max(random.sample(poblacion, 3), key=aptitud)


def cruza(padre1, padre2):
    """Order Crossover (OX): copia un tramo del padre 1 y completa con el orden del padre 2.
    Así el hijo nunca repite ni omite clientes."""
    a, b = sorted(random.sample(range(len(padre1)), 2))
    tramo = padre1[a:b + 1]
    restantes = [g for g in padre2 if g not in tramo]
    hijo = [None] * len(padre1)
    hijo[a:b + 1] = tramo
    for i in range(len(hijo)):
        if hijo[i] is None:
            hijo[i] = restantes.pop(0)
    return hijo


def mutacion(individuo):
    """Con cierta probabilidad invierte un tramo de la ruta (mutación por inversión)."""
    if random.random() < PROB_MUTACION:
        i, j = sorted(random.sample(range(len(individuo)), 2))
        individuo[i:j + 1] = reversed(individuo[i:j + 1])
    return individuo


def algoritmo_genetico():
    poblacion = [random.sample(CLIENTES, len(CLIENTES)) for _ in range(TAM_POBLACION)]
    mejores, promedios = [], []

    for _ in range(GENERACIONES):
        poblacion.sort(key=distancia_ruta)
        mejores.append(distancia_ruta(poblacion[0]))
        promedios.append(sum(map(distancia_ruta, poblacion)) / len(poblacion))

        nueva = [list(ind) for ind in poblacion[:ELITE]]
        while len(nueva) < TAM_POBLACION:
            hijo = cruza(seleccion(poblacion), seleccion(poblacion))
            nueva.append(mutacion(hijo))
        poblacion = nueva

    poblacion.sort(key=distancia_ruta)
    mejores.append(distancia_ruta(poblacion[0]))
    promedios.append(sum(map(distancia_ruta, poblacion)) / len(poblacion))
    return tuple(poblacion[0]), mejores, promedios


# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Robot repartidor: 120 rutas y algoritmo genético")
        root.geometry("1300x760")

        izq = ttk.Frame(root)
        izq.pack(side="left", fill="y", padx=8, pady=8)
        der = ttk.Frame(root)
        der.pack(side="right", fill="both", expand=True, padx=8, pady=8)

        self.crear_tabla_distancias(izq)
        self.crear_tabla_rutas(izq)
        self.crear_boton_genetico(izq)
        self.crear_graficas(der)

        self.seleccionar_ruta(RUTAS[0])

    # --- Tabla de distancias (como la del pizarrón) ---
    def crear_tabla_distancias(self, padre):
        ttk.Label(padre, text="Distancias euclidianas", font=("", 11, "bold")).pack(anchor="w")
        cols = [""] + NOMBRES
        tabla = ttk.Treeview(padre, columns=cols, show="headings", height=6)
        for c in cols:
            tabla.heading(c, text=c)
            tabla.column(c, width=62, anchor="center")
        for i, nombre in enumerate(NOMBRES):
            tabla.insert("", "end", values=[nombre] + [f"{d:.2f}" for d in MATRIZ[i]])
        tabla.pack(anchor="w", pady=(2, 10))

    # --- Tabla con las 120 rutas ---
    def crear_tabla_rutas(self, padre):
        ttk.Label(padre, text="Las 120 rutas (clic para ver)", font=("", 11, "bold")).pack(anchor="w")
        marco = ttk.Frame(padre)
        marco.pack(fill="both", expand=True)

        self.tabla = ttk.Treeview(marco, columns=("n", "ruta", "dist"), show="headings", height=14)
        self.tabla.heading("n", text="#")
        self.tabla.heading("ruta", text="Ruta")
        self.tabla.heading("dist", text="Distancia")
        self.tabla.column("n", width=40, anchor="center")
        self.tabla.column("ruta", width=170, anchor="center")
        self.tabla.column("dist", width=80, anchor="center")
        self.tabla.tag_configure("mejor", background="#c8f7c5")
        self.tabla.tag_configure("peor", background="#f7c5c5")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.iid_de = {}  # ruta -> id de la fila
        min_d, max_d = distancia_ruta(RUTAS[0]), distancia_ruta(RUTAS[-1])
        for n, ruta in enumerate(RUTAS, start=1):
            d = distancia_ruta(ruta)
            tag = "mejor" if math.isclose(d, min_d) else "peor" if math.isclose(d, max_d) else ""
            iid = self.tabla.insert("", "end", values=(n, "".join(NOMBRES[i] for i in ruta), f"{d:.2f}"),
                                    tags=(tag,))
            self.iid_de[ruta] = iid
        self.ruta_de = {iid: ruta for ruta, iid in self.iid_de.items()}
        self.tabla.bind("<<TreeviewSelect>>", self.al_seleccionar)

    def crear_boton_genetico(self, padre):
        ttk.Button(padre, text="Ejecutar algoritmo genético", command=self.correr_genetico).pack(
            fill="x", pady=(10, 2))
        self.lbl_genetico = ttk.Label(padre, text="", wraplength=300, justify="left")
        self.lbl_genetico.pack(anchor="w")

    # --- Gráficas en pestañas ---
    def crear_graficas(self, padre):
        pestañas = ttk.Notebook(padre)
        pestañas.pack(fill="both", expand=True)
        self.pestañas = pestañas

        # Pestaña 1: mapa de la ruta
        f1 = ttk.Frame(pestañas)
        pestañas.add(f1, text="Mapa de la ruta")
        self.fig_mapa = Figure(figsize=(6, 6))
        self.ax_mapa = self.fig_mapa.add_subplot(111)
        self.canvas_mapa = FigureCanvasTkAgg(self.fig_mapa, master=f1)
        self.canvas_mapa.get_tk_widget().pack(fill="both", expand=True)
        self.lbl_suma = ttk.Label(f1, text="", wraplength=800, justify="left")
        self.lbl_suma.pack(anchor="w", pady=4)

        # Pestaña 2: las 120 rutas en barras
        f2 = ttk.Frame(pestañas)
        pestañas.add(f2, text="120 rutas")
        self.fig_barras = Figure(figsize=(6, 6))
        self.ax_barras = self.fig_barras.add_subplot(111)
        self.canvas_barras = FigureCanvasTkAgg(self.fig_barras, master=f2)
        self.canvas_barras.get_tk_widget().pack(fill="both", expand=True)

        # Pestaña 3: evolución del algoritmo genético
        f3 = ttk.Frame(pestañas)
        pestañas.add(f3, text="Algoritmo genético")
        self.fig_ag = Figure(figsize=(6, 6))
        self.ax_ag = self.fig_ag.add_subplot(111)
        self.canvas_ag = FigureCanvasTkAgg(self.fig_ag, master=f3)
        self.canvas_ag.get_tk_widget().pack(fill="both", expand=True)
        self.ax_ag.set_title("Corre el algoritmo genético para ver la evolución")
        self.canvas_ag.draw()

    # --- Eventos ---
    def al_seleccionar(self, _evento):
        seleccion_actual = self.tabla.selection()
        if seleccion_actual:
            self.mostrar_ruta(self.ruta_de[seleccion_actual[0]])

    def seleccionar_ruta(self, ruta):
        iid = self.iid_de[tuple(ruta)]
        self.tabla.selection_set(iid)
        self.tabla.see(iid)

    def correr_genetico(self):
        mejor, mejores, promedios = algoritmo_genetico()
        optimo = distancia_ruta(RUTAS[0])
        d = distancia_ruta(mejor)
        estado = "es el óptimo" if math.isclose(d, optimo) else f"el óptimo es {optimo:.2f}"
        self.lbl_genetico.config(text=f"AG: {nombre_ruta(mejor)} = {d:.2f} ({estado})")

        ax = self.ax_ag
        ax.clear()
        ax.plot(mejores, marker="o", label="Mejor individuo")
        ax.plot(promedios, linestyle="--", label="Promedio de la población")
        ax.axhline(optimo, color="green", linestyle=":", label=f"Óptimo (fuerza bruta) = {optimo:.2f}")
        ax.set_xlabel("Generación")
        ax.set_ylabel("Distancia total")
        ax.set_title("Evolución del algoritmo genético")
        ax.grid(True)
        ax.legend()
        self.canvas_ag.draw()

        self.seleccionar_ruta(mejor)
        self.pestañas.select(2)

    # --- Dibujo ---
    def mostrar_ruta(self, ruta):
        ax = self.ax_mapa
        ax.clear()
        camino = [0, *ruta, 0]

        for a, b in zip(camino, camino[1:]):
            (x1, y1), (x2, y2) = COORDS[a], COORDS[b]
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="orange", lw=2))
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, f"{MATRIZ[a][b]:.2f}", fontsize=8, ha="center",
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

        for i, (x, y) in enumerate(COORDS):
            ax.plot(x, y, "o", color="red" if i == 0 else "tab:blue", markersize=11, zorder=3)
            ax.annotate(f"{NOMBRES[i]} ({x},{y})", (x, y), textcoords="offset points", xytext=(8, 8))

        total = distancia_ruta(ruta)
        ax.set_title(f"{nombre_ruta(ruta, True)}\nDistancia total = {total:.2f}")
        ax.set_xlim(-1, 10)
        ax.set_ylim(-1, 10.5)
        ax.set_aspect("equal")
        ax.grid(True)
        self.canvas_mapa.draw()

        tramos = [f"{MATRIZ[a][b]:.2f}" for a, b in zip(camino, camino[1:])]
        self.lbl_suma.config(text=" + ".join(tramos) + f" = {total:.2f}")

        self.dibujar_barras(ruta)

    def dibujar_barras(self, ruta_actual):
        ax = self.ax_barras
        ax.clear()
        distancias = [distancia_ruta(r) for r in RUTAS]
        colores = ["green" if math.isclose(d, distancias[0]) else
                   "red" if math.isclose(d, distancias[-1]) else "steelblue" for d in distancias]
        ax.bar(range(1, len(RUTAS) + 1), distancias, color=colores)

        pos = RUTAS.index(tuple(ruta_actual)) + 1
        ax.axvline(pos, color="orange", linewidth=2, label=f"Ruta seleccionada (#{pos})")
        ax.set_xlabel("Ruta (ordenadas de menor a mayor distancia)")
        ax.set_ylabel("Distancia total")
        ax.set_title("Las 120 rutas posibles (verde = más corta, rojo = más larga)")
        ax.legend()
        self.canvas_barras.draw()


if __name__ == "__main__":
    ventana = tk.Tk()
    App(ventana)
    ventana.mainloop()