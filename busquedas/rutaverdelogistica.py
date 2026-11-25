"""
RUTA VERDE LOGÍSTICA | Comparación de sistemas inteligentes
Python 3.10+ | pip install matplotlib

Ejecutar: python ruta_verde_algoritmos.py
Prueba sin interfaz: python ruta_verde_algoritmos.py --verificar

Caso de uso: un robot parte del centro logístico, entrega en ocho
edificios y vuelve al centro. Todos los métodos resuelven el mismo
problema y usan los costos de caminos mínimos sobre una red de vías.
"""
from __future__ import annotations

import csv
import heapq
import math
import random
import sys
from itertools import permutations
import tkinter as tk
from dataclasses import dataclass, field
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

NOMBRES = ["Centro logístico"] + [f"Edificio {chr(65 + i)}" for i in range(8)]
CANTIDAD = len(NOMBRES)                 # 9 nodos (1 centro + 8 edificios)
EDIFICIOS = tuple(range(1, CANTIDAD))
SEMILLA_INICIAL = 42
TOTAL_PERMUTACIONES = math.factorial(len(EDIFICIOS))  # 8! = 40320


def distancia_euclidiana(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


class Campus:
    """Red vial no dirigida, conectada y con costos positivos en metros.

    Las coordenadas se generan de forma pseudoaleatoria y reproducible.
    Los pesos de las calles se calculan como la distancia euclidiana.
    Un árbol de expansión mínima garantiza conectividad y se agregan
    enlaces a vecinos cercanos para representar caminos alternativos.
    """

    def __init__(self, semilla=SEMILLA_INICIAL):
        self.semilla = semilla
        rng = random.Random(semilla)
        self.coordenadas = []
        while len(self.coordenadas) < CANTIDAD:
            punto = (rng.randint(95, 905), rng.randint(95, 905))
            if all(distancia_euclidiana(punto, p) >= 145 for p in self.coordenadas):
                self.coordenadas.append(punto)

        posibles = sorted(
            (distancia_euclidiana(self.coordenadas[i], self.coordenadas[j]), i, j)
            for i in range(CANTIDAD) for j in range(i + 1, CANTIDAD)
        )
        padres = list(range(CANTIDAD))

        def raiz(n):
            while padres[n] != n:
                padres[n] = padres[padres[n]]
                n = padres[n]
            return n

        aristas = set()
        # Árbol de expansión mínima (Kruskal): impide componentes aislados.
        for _, a, b in posibles:
            ra, rb = raiz(a), raiz(b)
            if ra != rb:
                padres[ra] = rb
                aristas.add((a, b))

        # Dos vías hacia vecinos cercanos por edificio.
        for a in range(CANTIDAD):
            candidatos = sorted(
                (distancia_euclidiana(self.coordenadas[a], self.coordenadas[b]), b)
                for b in range(CANTIDAD) if b != a
            )
            for _, b in candidatos[:2]:
                aristas.add((min(a, b), max(a, b)))

        # Algunas calles adicionales proporcionan alternativas reales.
        for d, a, b in posibles:
            if d <= 425 and rng.random() < 0.20:
                aristas.add((a, b))

        self.aristas = sorted(aristas)
        self.adyacencia = {i: [] for i in range(CANTIDAD)}
        self.costos_calle = {}
        for a, b in self.aristas:
            costo = round(distancia_euclidiana(self.coordenadas[a],
                                              self.coordenadas[b]), 1)
            self.costos_calle[(a, b)] = costo
            self.adyacencia[a].append((b, costo))
            self.adyacencia[b].append((a, costo))
        for vecinos in self.adyacencia.values():
            vecinos.sort()

        # Matriz de distancias mínimas reales entre edificios, no línea recta.
        self.matriz = [[math.inf] * CANTIDAD for _ in range(CANTIDAD)]
        self.trayectos = {}
        for origen in range(CANTIDAD):
            d, prev = self._dijkstra(origen)
            for destino in range(CANTIDAD):
                self.matriz[origen][destino] = d[destino]
                if origen == destino:
                    self.trayectos[(origen, destino)] = [origen]
                    continue
                ruta = [destino]
                actual = destino
                while actual != origen:
                    actual = prev[actual]
                    if actual is None:
                        raise RuntimeError("Grafo desconectado")
                    ruta.append(actual)
                self.trayectos[(origen, destino)] = list(reversed(ruta))

    def _dijkstra(self, origen):
        dist = [math.inf] * CANTIDAD
        prev = [None] * CANTIDAD
        dist[origen] = 0.0
        pendientes = [(0.0, origen)]
        while pendientes:
            costo, actual = heapq.heappop(pendientes)
            if costo > dist[actual] + 1e-9:
                continue
            for vecino, peso in self.adyacencia[actual]:
                nuevo = costo + peso
                if nuevo < dist[vecino] - 1e-9:
                    dist[vecino], prev[vecino] = nuevo, actual
                    heapq.heappush(pendientes, (nuevo, vecino))
        return dist, prev

    def costo_recorrido(self, orden):
        secuencia = (0, *orden, 0)
        return sum(self.matriz[a][b] for a, b in zip(secuencia, secuencia[1:]))

    def es_recorrido_valido(self, orden):
        return len(orden) == 8 and set(orden) == set(EDIFICIOS)


def texto_ruta(orden):
    return " → ".join(["Centro"] + [chr(64 + i) for i in orden] + ["Centro"])


def enumerar_40320(campus):
    """Referencia exacta: evaluar las 8! permutaciones de las entregas.

    La lista se ordena por (costo, permutación) para poder exportar
    tanto la mejor como las 40 320 alternativas. No es el algoritmo
    genético: la enumeración exhaustiva se utiliza como validación.
    """
    rutas = [(campus.costo_recorrido(p), p) for p in permutations(EDIFICIOS)]
    rutas.sort(key=lambda x: (x[0], x[1]))
    assert len(rutas) == TOTAL_PERMUTACIONES
    return rutas


@dataclass
class Resultado:
    nombre: str
    orden: tuple
    costo: float
    pasos: int
    retrocesos: int
    profundidad: int
    historia: list = field(default_factory=list)
    info: str = ""
    historia_promedio: list = field(default_factory=list)


def dfs(campus):
    """DFS clásico: primera gira válida (NO garantiza costo mínimo).

    La búsqueda sobre estados de entrega usa caminos mínimos entre
    edificios: las calles de tránsito no se consideran entregas nuevas.
    """
    pasos = 0
    retrocesos = 0
    historia = []
    visitados = set()
    orden = []
    total = (1 << len(EDIFICIOS)) - 1

    def buscar(actual, mascara, costo):
        nonlocal pasos, retrocesos
        pasos += 1
        historia.append(costo)
        if mascara == total:
            return tuple(orden)
        for siguiente in EDIFICIOS:
            bit = 1 << (siguiente - 1)
            if mascara & bit:
                continue
            estado = (siguiente, mascara | bit)
            if estado in visitados:
                continue
            visitados.add(estado)
            orden.append(siguiente)
            respuesta = buscar(siguiente, mascara | bit,
                               costo + campus.matriz[actual][siguiente])
            if respuesta is not None:
                return respuesta
            orden.pop()
            retrocesos += 1
        return None

    solucion = buscar(0, 0, 0.0)
    if solucion is None:
        raise RuntimeError("No existe un recorrido de entregas")
    return Resultado("DFS", solucion, campus.costo_recorrido(solucion),
                     pasos, retrocesos, 9, historia,
                     "Primera solución en orden de edificios, sin optimizar el costo.")


def ucs(campus):
    """UCS/Dijkstra sobre estado (posición, entregas realizadas).

    El objetivo es volver a 0 después de visitar todas las entregas.
    Al extraer la meta de la cola de prioridad, el costo es óptimo,
    porque todas las transiciones son no negativas.
    """
    mascara_final = (1 << len(EDIFICIOS)) - 1
    cola = [(0.0, 0, 0, 0, ())]  # costo, desempate, edificio, máscara, orden
    mejores = {(0, 0): 0.0}
    contador = 0
    pasos = 0
    historia = []
    while cola:
        costo, _, actual, mascara, orden = heapq.heappop(cola)
        if costo > mejores.get((actual, mascara), math.inf) + 1e-9:
            continue
        pasos += 1
        historia.append(costo)
        if actual == 0 and mascara == mascara_final:
            return Resultado("UCS", orden, costo, pasos, 0, 9, historia,
                             "Óptimo global: cola de prioridad y costos acumulados.")

        siguientes = (0,) if mascara == mascara_final else EDIFICIOS
        for sig in siguientes:
            if sig != 0 and mascara & (1 << (sig - 1)):
                continue
            nueva_mascara = mascara if sig == 0 else mascara | (1 << (sig - 1))
            nuevo_costo = costo + campus.matriz[actual][sig]
            estado = (sig, nueva_mascara)
            if nuevo_costo < mejores.get(estado, math.inf) - 1e-9:
                mejores[estado] = nuevo_costo
                contador += 1
                nuevo_orden = orden if sig == 0 else (*orden, sig)
                heapq.heappush(cola, (nuevo_costo, contador, sig,
                                      nueva_mascara, nuevo_orden))
    raise RuntimeError("UCS no encontró una ruta válida")


def hill_climbing(campus, semilla):
    """Mejor mejora por inversión de segmentos (2-opt), sin reinicios."""
    rng = random.Random(semilla + 2000)
    orden = list(rng.sample(EDIFICIOS, len(EDIFICIOS)))
    costo = campus.costo_recorrido(orden)
    historia = [costo]
    evaluaciones = 1
    movimientos = 0
    rechazados = 0
    while True:
        mejor_costo, mejor_orden = costo, None
        for i in range(len(orden) - 1):
            for j in range(i + 1, len(orden)):
                candidato = orden[:i] + list(reversed(orden[i:j + 1])) + orden[j + 1:]
                nuevo_costo = campus.costo_recorrido(candidato)
                evaluaciones += 1
                if nuevo_costo < mejor_costo - 1e-9:
                    mejor_costo, mejor_orden = nuevo_costo, candidato
                else:
                    rechazados += 1
        if mejor_orden is None:
            break
        orden, costo = mejor_orden, mejor_costo
        movimientos += 1
        historia.append(costo)
    return Resultado("Hill Climbing", tuple(orden), costo, evaluaciones,
                     0, 9, historia,
                     f"2-opt, {movimientos} mejoras aceptadas, "
                     f"{rechazados} vecinos no seleccionados; "
                     "puede detenerse en un óptimo local.")


def algoritmo_genetico(campus, semilla, poblacion_tam=90,
                        generaciones=180, prob_mutacion=0.24):
    """Permutaciones, torneo, OX, mutación por inversión y elitismo."""
    rng = random.Random(semilla + 3000)
    poblacion = [rng.sample(EDIFICIOS, len(EDIFICIOS))
                 for _ in range(poblacion_tam)]
    evaluaciones = poblacion_tam
    mejores = []
    promedios = []

    def torneo():
        competidores = rng.sample(poblacion, 3)
        return min(competidores, key=campus.costo_recorrido)

    def cruza_ox(padre1, padre2):
        a, b = sorted(rng.sample(range(len(EDIFICIOS)), 2))
        hijo = [None] * len(EDIFICIOS)
        hijo[a:b + 1] = padre1[a:b + 1]
        # Rellenar desde la posición b+1, preservando el orden circular del padre 2.
        orden2 = padre2[b + 1:] + padre2[:b + 1]
        restantes = iter([v for v in orden2 if v not in hijo])
        for i in list(range(b + 1, len(hijo))) + list(range(0, a)):
            hijo[i] = next(restantes)
        return hijo

    for _ in range(generaciones + 1):
        poblacion.sort(key=campus.costo_recorrido)
        valores = [campus.costo_recorrido(orden) for orden in poblacion]
        mejores.append(valores[0])
        promedios.append(sum(valores) / len(valores))
        if len(mejores) == generaciones + 1:
            break
        nueva = [poblacion[0][:], poblacion[1][:]]  # elitismo
        while len(nueva) < poblacion_tam:
            hijo = cruza_ox(torneo(), torneo())
            if rng.random() < prob_mutacion:
                i, j = sorted(rng.sample(range(len(hijo)), 2))
                hijo[i:j + 1] = reversed(hijo[i:j + 1])
            nueva.append(hijo)
            evaluaciones += 1
        poblacion = nueva

    mejor = tuple(poblacion[0])
    return Resultado("Genético", mejor, campus.costo_recorrido(mejor),
                     evaluaciones, 0, 9, mejores,
                     f"Población={poblacion_tam}, generaciones={generaciones}, "
                     f"mutación={prob_mutacion:.0%}, torneo, cruce OX y elitismo.",
                     promedios)


def ejecutar_comparacion(semilla):
    campus = Campus(semilla)
    resultados = [dfs(campus), ucs(campus),
                  hill_climbing(campus, semilla),
                  algoritmo_genetico(campus, semilla)]
    for resultado in resultados:
        assert campus.es_recorrido_valido(resultado.orden), resultado.nombre
        assert math.isclose(resultado.costo, campus.costo_recorrido(resultado.orden),
                            abs_tol=1e-6), resultado.nombre
    assert all(r.costo >= resultados[1].costo - 1e-6 for r in resultados)
    rutas_exactas = enumerar_40320(campus)
    assert math.isclose(resultados[1].costo, rutas_exactas[0][0], abs_tol=1e-7), (
        "UCS debe coincidir con la enumeración exhaustiva de 8! rutas")
    return campus, resultados


def texto_informe(campus, resultados):
    optimo = resultados[1].costo
    lines = [
        "RUTA VERDE LOGÍSTICA - INFORME TÉCNICO DE RESULTADOS",
        "=" * 76,
        f"Semilla reproducible: {campus.semilla}",
        "Problema: una salida del centro, ocho edificios visitados una vez",
        "como paradas de entrega y regreso al centro.",
        "Las distancias representan metros; el robot puede transitar por otros",
        "edificios entre dos entregas sin que ello cambie el orden de paradas.",
        "",
        "Espacio de búsqueda: 8! = 40,320 órdenes de entrega diferentes.",
        "La enumeración exhaustiva verifica el óptimo obtenido por UCS.",
        "El AG NO evalúa forzosamente las 40,320 rutas; evoluciona muestras.",
        "",
        "COORDENADAS DE EDIFICIOS (m)",
    ]
    for nombre, (x, y) in zip(NOMBRES, campus.coordenadas):
        lines.append(f"  {nombre:20s} x={x:4d}  y={y:4d}")
    lines += ["", "CALLES DEL GRAFO (no dirigidas, distancias en m)"]
    for a, b in campus.aristas:
        lines.append(f"  {NOMBRES[a]:20s} -- {NOMBRES[b]:20s}: "
                     f"{campus.costos_calle[(a,b)]:7.1f}")
    rutas_ref = enumerar_40320(campus)
    lines += ["", "VERIFICACIÓN EXHAUSTIVA DE LAS 40,320 PERMUTACIONES",
              f"  Permutaciones evaluadas: {len(rutas_ref):,}",
              f"  Costo mínimo comprobado: {rutas_ref[0][0]:.1f} m",
              f"  Una ruta mínima: {texto_ruta(rutas_ref[0][1])}",
              "  Cinco mejores órdenes (puede haber empates):"]
    for costo, ruta in rutas_ref[:5]:
        lines.append(f"    {costo:8.1f} m | {texto_ruta(ruta)}")
    lines += ["", "COMPARACIÓN DE ALGORITMOS"]
    for r in resultados:
        lines += [f"\n{r.nombre}", f"  Recorrido:    {texto_ruta(r.orden)}",
                  f"  Costo:        {r.costo:.1f} m",
                  f"  Dif. óptimo:  {r.costo - optimo:.1f} m",
                  f"  Profundidad:  {r.profundidad} transiciones (incluido retorno)",
                  f"  Pasos:        {r.pasos} (según el algoritmo)",
                  f"  Retrocesos:   {r.retrocesos} (backtracking explícito)",
                  f"  Nota:         {r.info}"]
    lines += ["", "DEFINICIONES Y CONCLUSIONES",
              "DFS: primera solución válida; el orden de expansión determina la gira.",
              "UCS: solución de costo mínimo, garantizada con costos no negativos.",
              "Hill Climbing: mejora local por inversiones; puede quedar atascado.",
              "Genético: aproximación estocástica; la calidad depende de los parámetros.",
              "Rutas inversas pueden tener el mismo costo en un grafo no dirigido.",
              "Pasos: DFS/UCS = estados expandidos; HC = vecinos evaluados;",
              "genético = cromosomas iniciales y descendientes evaluados.",
              "Retroceso: pop de una rama fallida en DFS; en UCS/HC/AG no aplica",
              "backtracking clásico. Un retroceso 0 no significa cero trabajo.",
              "Distancia óptima: la obtenida por UCS para ESTE escenario.",
              "Los datos son simulados, no una medición física de un campus real."]
    return "\n".join(lines) + "\n"


class Aplicacion:
    COLORES = ("#bd6b2f", "#15846c", "#8254b4", "#206aa5")

    def __init__(self, raiz):
        self.raiz = raiz
        raiz.title("Ruta Verde Logística | DFS · UCS · Hill Climbing · Genético")
        raiz.geometry("1420x900")
        raiz.minsize(1100, 680)
        self.semilla = SEMILLA_INICIAL
        self.campus, self.resultados = ejecutar_comparacion(self.semilla)
        self.rutas_exactas = enumerar_40320(self.campus)
        self._configurar_estilo()

        cabecera = ttk.Frame(raiz, padding=(12, 10))
        cabecera.pack(fill="x")
        ttk.Label(cabecera, text="RUTA VERDE LOGÍSTICA", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(cabecera, text="9 nodos, 8 entregas, caminos reales en un grafo de calles | "
                                     "Todos los algoritmos regresan al centro logístico").pack(anchor="w")
        barra = ttk.Frame(raiz, padding=(12, 2, 12, 5))
        barra.pack(fill="x")
        self.lbl_semilla = ttk.Label(barra)
        self.lbl_semilla.pack(side="left", padx=(0, 15))
        ttk.Button(barra, text="Nueva distribución aleatoria",
                   command=self.nueva_distribucion).pack(side="left", padx=4)
        ttk.Button(barra, text="Repetir con la misma semilla",
                   command=self.repetir).pack(side="left", padx=4)
        ttk.Button(barra, text="Exportar informe (.txt)",
                   command=self.exportar_informe).pack(side="right", padx=4)
        ttk.Button(barra, text="Exportar 40,320 rutas (.csv)",
                   command=self.exportar_permutaciones).pack(side="right", padx=4)

        columnas = ("metodo", "costo", "exceso", "pasos", "retrocesos", "camino")
        self.comparacion = ttk.Treeview(raiz, columns=columnas, show="headings", height=4)
        for col, titulo, ancho in [
            ("metodo", "Método", 145), ("costo", "Costo (m)", 110),
            ("exceso", "Diferencia con UCS", 150), ("pasos", "Pasos *", 95),
            ("retrocesos", "Retrocesos", 90), ("camino", "Ruta de entregas", 550)
        ]:
            self.comparacion.heading(col, text=titulo)
            self.comparacion.column(col, width=ancho,
                                   anchor="w" if col in ("metodo", "camino") else "center")
        self.comparacion.pack(fill="x", padx=12, pady=(0, 4))
        self.notebook = ttk.Notebook(raiz)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(4, 5))
        self.tabs = []
        for nombre in ("DFS", "UCS", "Hill Climbing", "Genético"):
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=nombre)
            izquierda = ttk.Frame(tab, padding=(9, 12))
            izquierda.pack(side="left", fill="y")
            derecha = ttk.Frame(tab, padding=(3, 3))
            derecha.pack(side="right", fill="both", expand=True)
            ttk.Label(izquierda, text=nombre, style="Subtitulo.TLabel").pack(anchor="w")
            datos = tk.Text(izquierda, height=11, width=46, wrap="word", relief="flat",
                            padx=7, pady=8, background="#f1f5f6", state="disabled")
            datos.pack(fill="x", pady=(7, 10))
            ttk.Label(izquierda, text="Tramos y costos acumulados (m)",
                      style="Subtitulo.TLabel").pack(anchor="w")
            tabla = ttk.Treeview(izquierda, columns=("tramo", "cost", "acum"),
                                 show="headings", height=10)
            for col, titulo, w in (("tramo", "Desplazamiento", 170),
                                   ("cost", "Costo", 80), ("acum", "Acum.", 80)):
                tabla.heading(col, text=titulo)
                tabla.column(col, width=w, anchor="center")
            tabla.pack(fill="y", pady=6)
            fig = Figure(figsize=(8.2, 7.8), dpi=100, facecolor="white")
            gs = fig.add_gridspec(2, 1, height_ratios=(3.4, 1.15), hspace=0.30,
                                  left=0.095, right=0.97, top=0.94, bottom=0.09)
            mapa = fig.add_subplot(gs[0])
            curva = fig.add_subplot(gs[1])
            canvas = FigureCanvasTkAgg(fig, master=derecha)
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.tabs.append((datos, tabla, mapa, curva, canvas))
        self.lbl_ayuda = ttk.Label(raiz, padding=(12, 4),
                                   text="* DFS/UCS: estados explorados; Hill Climbing: "
                                        "vecinos evaluados; Genético: individuos evaluados. "
                                        "Retrocesos clásicos solo aplican a DFS.")
        self.lbl_ayuda.pack(fill="x")
        self.refrescar()

    def _configurar_estilo(self):
        estilo = ttk.Style(self.raiz)
        if "clam" in estilo.theme_names():
            estilo.theme_use("clam")
        estilo.configure("Titulo.TLabel", font=("Arial", 17, "bold"))
        estilo.configure("Subtitulo.TLabel", font=("Arial", 11, "bold"))
        estilo.configure("TNotebook.Tab", padding=(17, 7))

    def nueva_distribucion(self):
        self.semilla += 1
        self.repetir()

    def repetir(self):
        self.campus, self.resultados = ejecutar_comparacion(self.semilla)
        self.rutas_exactas = enumerar_40320(self.campus)
        self.refrescar()

    def refrescar(self):
        self.lbl_semilla.config(text=f"Semilla: {self.semilla} | "
                                     f"Calles: {len(self.campus.aristas)} | "
                                     f"8! = {TOTAL_PERMUTACIONES:,} rutas | "
                                     f"Mínimo verificado: {self.rutas_exactas[0][0]:.1f} m")
        for item in self.comparacion.get_children():
            self.comparacion.delete(item)
        optimo = self.resultados[1].costo
        for i, r in enumerate(self.resultados):
            self.comparacion.insert("", "end", values=(
                r.nombre, f"{r.costo:.1f}", f"+{r.costo-optimo:.1f} m",
                r.pasos, r.retrocesos, texto_ruta(r.orden)))
            self.pintar_pestana(i, r, optimo)

    def pintar_pestana(self, indice, resultado, optimo):
        texto, tabla, ax, ax_curva, canvas = self.tabs[indice]
        lineas = [
            f"Ruta: {texto_ruta(resultado.orden)}", "",
            f"Costo total: {resultado.costo:.1f} m",
            f"Diferencia con UCS: +{resultado.costo-optimo:.1f} m",
            f"Profundidad: {resultado.profundidad} transiciones",
            f"Pasos: {resultado.pasos}",
            f"Retrocesos: {resultado.retrocesos}", "",
            resultado.info,
        ]
        if indice == 3:
            lineas.extend(["", "Verificación exhaustiva: 8! = 40,320 rutas.",
                            f"Óptimo exacto: {self.rutas_exactas[0][0]:.1f} m.",
                            "El algoritmo genético NO enumera las 40,320 rutas."])
        texto.config(state="normal")
        texto.delete("1.0", "end")
        texto.insert("1.0", "\n".join(lineas))
        texto.config(state="disabled")
        for item in tabla.get_children():
            tabla.delete(item)
        orden_completo = (0, *resultado.orden, 0)
        acumulado = 0.0
        for a, b in zip(orden_completo, orden_completo[1:]):
            costo = self.campus.matriz[a][b]
            acumulado += costo
            etiqueta = lambda n: "Centro" if n == 0 else chr(64 + n)
            tabla.insert("", "end", values=(
                f"{etiqueta(a)} → {etiqueta(b)}", f"{costo:.1f}", f"{acumulado:.1f}"))

        ax.clear()
        ax.set_facecolor("#f8fbfa")
        color = self.COLORES[indice]
        coords = self.campus.coordenadas
        # Calles y costos del grafo original.
        for a, b in self.campus.aristas:
            (x1, y1), (x2, y2) = coords[a], coords[b]
            ax.plot([x1, x2], [y1, y2], color="#b8c8c8", lw=1.6,
                    zorder=1, alpha=.8)
            ax.text((x1 + x2) / 2, (y1 + y2) / 2,
                    f"{self.campus.costos_calle[(a, b)]:.0f}", fontsize=7,
                    color="#566b72", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=.10", fc="white", ec="none", alpha=.78),
                    zorder=2)

        # Expandir cada tramo en las calles que de verdad recorre el robot.
        for parada_a, parada_b in zip(orden_completo, orden_completo[1:]):
            camino = self.campus.trayectos[(parada_a, parada_b)]
            for a, b in zip(camino, camino[1:]):
                (x1, y1), (x2, y2) = coords[a], coords[b]
                ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                            arrowprops=dict(arrowstyle="->", lw=2.4,
                                            color=color, alpha=0.80,
                                            mutation_scale=13), zorder=3)

        numeros = {n: idx + 1 for idx, n in enumerate(resultado.orden)}
        for i, (x, y) in enumerate(coords):
            ax.scatter([x], [y], s=330, marker="o",
                       color="#184455" if i == 0 else "#ffffff",
                       edgecolors="#184455", linewidths=1.7, zorder=5)
            ax.text(x, y, "C" if i == 0 else chr(64 + i),
                    fontsize=10, fontweight="bold", ha="center", va="center",
                    color="white" if i == 0 else "#184455", zorder=6)
            ax.annotate("Salida / regreso" if i == 0 else f"Entrega {numeros[i]}",
                        (x, y), xytext=(8, 13), textcoords="offset points",
                        fontsize=8, color="#24343e", zorder=7)

        ax.set_title(f"Mapa vial y ruta de {resultado.nombre} | {resultado.costo:.1f} m",
                     fontsize=12, pad=10, fontweight="bold")
        ax.set_xlim(20, 980)
        ax.set_ylim(20, 980)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("Coordenada X (m)")
        ax.set_ylabel("Coordenada Y (m)")
        ax.grid(alpha=.14, linestyle=":")

        ax_curva.clear()
        hist = resultado.historia
        xs = range(1, len(hist) + 1)
        ax_curva.plot(xs, hist, color=color, linewidth=2,
                      label="Costo acumulado" if indice in (0, 1) else "Mejor costo")
        if resultado.historia_promedio:
            ax_curva.plot(xs, resultado.historia_promedio,
                          color="#828a99", linestyle="--", linewidth=1.6,
                          label="Promedio de población")
        if indice >= 2:
            ax_curva.axhline(optimo, color="#11845d", linestyle=":",
                            linewidth=1.6, label="Óptimo UCS")
        ax_curva.set_title(("Costo en la exploración de estados" if indice in (0, 1)
                            else "Evolución de la optimización"), fontsize=10)
        ax_curva.set_xlabel("Estado explorado" if indice in (0, 1) else
                            ("Mejora aceptada" if indice == 2 else "Generación"), fontsize=9)
        ax_curva.set_ylabel("Metros", fontsize=9)
        ax_curva.grid(alpha=.2)
        ax_curva.legend(loc="best", fontsize=8)
        canvas.draw_idle()

    def exportar_permutaciones(self):
        """Guardar TODAS las 40 320 permutaciones con costo y recorrido."""
        destino = filedialog.asksaveasfilename(
            defaultextension=".csv", filetypes=[("CSV", "*.csv")],
            initialfile=f"rutas_40320_semilla_{self.semilla}.csv")
        if not destino:
            return
        with open(destino, "w", encoding="utf-8-sig", newline="") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Posición", "Orden de entrega", "Costo total (m)"])
            for indice, (costo, ruta) in enumerate(self.rutas_exactas, 1):
                escritor.writerow([indice, texto_ruta(ruta), f"{costo:.1f}"])
        messagebox.showinfo("Rutas exportadas", 
                            f"Se exportaron {TOTAL_PERMUTACIONES:,} rutas:\n{destino}")

    def exportar_informe(self):
        destino = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")],
            initialfile=f"informe_ruta_verde_semilla_{self.semilla}.txt")
        if not destino:
            return
        Path(destino).write_text(texto_informe(self.campus, self.resultados),
                                 encoding="utf-8")
        messagebox.showinfo("Informe guardado", f"Se guardó el informe en:\n{destino}")


def verificar():
    for semilla in (42, 43, 44):
        campus, resultados = ejecutar_comparacion(semilla)
        print(f"\nSEMILLA {semilla} | {len(campus.aristas)} calles")
        for r in resultados:
            print(f"{r.nombre:16s} {r.costo:8.1f} m | "
                  f"pasos={r.pasos:5d} | {texto_ruta(r.orden)}")
        assert math.isclose(resultados[1].costo,
                            min(r.costo for r in resultados), abs_tol=1e-7)
    print("\nVerificación correcta.")


if __name__ == "__main__":
    if "--verificar" in sys.argv:
        verificar()
    else:
        ventana = tk.Tk()
        Aplicacion(ventana)
        ventana.mainloop()
