#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Práctica 03: reglas fijas frente a aprendizaje supervisado.

Adaptación de p03primermodelo(1).py a las indicaciones de NotasIA.
Requiere Python 3.9 o posterior.
Instalación: python -m pip install numpy pandas matplotlib scikit-learn
Ejecución:   python p03primermodelo_mejorado.py
Sin ventanas: python p03primermodelo_mejorado.py --sin-ventanas

Genera 500 estudiantes, separa 300/100/100, selecciona un árbol con
validación y compara ambos sistemas sobre la misma prueba reservada.
Guarda CSV, un informe de texto y una gráfica en resultados_practica03.
Los archivos de salida con el mismo nombre se reemplazan al ejecutar.

SUPUESTOS DIDÁCTICOS (no especificados en NotasIA):
* Calificación final de 0 a 10; aprobación desde 6.
* Calificación simulada mediante una suma ponderada más ruido.
* Participación mínima de 5 en el sistema de reglas manuales.
Estos datos son sintéticos: los resultados describen esta simulación,
no el desempeño de estudiantes reales ni una política institucional.
"""

import argparse
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text


# 1. CONFIGURACIÓN: rangos de NotasIA y supuestos modificables.
N_ESTUDIANTES = 500
SEMILLA = 42
CALIFICACION_APROBATORIA = 6.0
DESVIACION_RUIDO = 0.65
CARACTERISTICAS = [
    "horas_estudio", "asistencia", "actividades_entregadas", "participacion"
]
RANGOS = {
    "horas_estudio": (0, 15),
    "asistencia": (30, 100),
    "actividades_entregadas": (10, 100),
    "participacion": (0, 10),
}
PROFUNDIDADES = [1, 2, 3, 4, 5, 6, 8, 10, None]
MINIMOS_HOJA = [1, 5, 10, 20]


# 2. DATOS SINTÉTICOS: se genera una sola tabla antes de dividirla.
def generar_datos(semilla=SEMILLA):
    """La misma semilla reproduce exactamente los mismos 500 registros."""
    if not 0 < CALIFICACION_APROBATORIA <= 10:
        raise ValueError("El mínimo aprobatorio debe estar entre 0 y 10.")
    rng = np.random.default_rng(semilla)
    df = pd.DataFrame({
        columna: rng.integers(minimo, maximo + 1, size=N_ESTUDIANTES)
        for columna, (minimo, maximo) in RANGOS.items()
    })

    # Todos los componentes se expresan en escala 0-10.
    # Pesos: estudio 35 %, asistencia 15 %, actividades 35 %, participación 15 %.
    # El ruido simula factores no observados; no se usa como entrada del árbol.
    nota_base = (
        0.35 * (df["horas_estudio"] / 15 * 10)
        + 0.15 * (df["asistencia"] / 10)
        + 0.35 * (df["actividades_entregadas"] / 10)
        + 0.15 * df["participacion"]
    )
    ruido = rng.normal(0, DESVIACION_RUIDO, size=N_ESTUDIANTES)
    df["calificacion_final"] = np.round(np.clip(nota_base + ruido, 0, 10), 1)
    df["aprueba"] = (df["calificacion_final"] >= CALIFICACION_APROBATORIA).astype(int)
    df.index = pd.Index(range(1, N_ESTUDIANTES + 1), name="id_estudiante")
    validar_datos(df)
    return df


def validar_datos(df):
    """Comprueba cantidad, integridad, rangos y coherencia de las etiquetas."""
    if len(df) != N_ESTUDIANTES or df.isna().any().any():
        raise ValueError("Se requieren 500 registros completos.")
    if not df.index.is_unique:
        raise ValueError("Los identificadores deben ser únicos.")
    for columna, (minimo, maximo) in RANGOS.items():
        if not df[columna].between(minimo, maximo).all():
            raise ValueError(f"Valores fuera de rango en {columna}.")
    if not df["calificacion_final"].between(0, 10).all():
        raise ValueError("Calificaciones fuera de la escala 0-10.")
    esperadas = (df["calificacion_final"] >= CALIFICACION_APROBATORIA).astype(int)
    if not df["aprueba"].equals(esperadas):
        raise ValueError("Las etiquetas no corresponden a las calificaciones.")
    if df["aprueba"].nunique() != 2 or df["aprueba"].value_counts().min() < 5:
        raise ValueError("Se necesitan suficientes ejemplos de ambas clases para dividir.")


# 3. DIVISIÓN: primero 60/40; después el 40 % se divide en dos mitades.
def dividir_datos(df, semilla=SEMILLA):
    entrenamiento, reserva = train_test_split(
        df, train_size=300, test_size=200,
        random_state=semilla, stratify=df["aprueba"],
    )
    validacion, prueba = train_test_split(
        reserva, train_size=100, test_size=100,
        random_state=semilla, stratify=reserva["aprueba"],
    )
    # Cada estudiante pertenece a un solo conjunto.
    conjuntos = [set(parte.index) for parte in (entrenamiento, validacion, prueba)]
    if any(conjuntos[i] & conjuntos[j] for i, j in [(0, 1), (0, 2), (1, 2)]):
        raise ValueError("Hay estudiantes repetidos entre conjuntos.")
    return entrenamiento, validacion, prueba


# 4. REGLAS FIJAS: criterios definidos antes de evaluar, sin entrenamiento.
def predecir_con_reglas(X):
    """Conserva los umbrales originales y añade participación >= 5."""
    return (
        (X["horas_estudio"] >= 5)
        & (X["asistencia"] >= 70)
        & (X["actividades_entregadas"] >= 65)
        & (X["participacion"] >= 5)
    ).astype(int)


# 5. ENTRENAMIENTO Y VALIDACIÓN: la prueba no participa en esta función.
def seleccionar_modelo(entrenamiento, validacion, semilla=SEMILLA):
    X_ent, y_ent = entrenamiento[CARACTERISTICAS], entrenamiento["aprueba"]
    X_val, y_val = validacion[CARACTERISTICAS], validacion["aprueba"]
    modelos, filas = [], []
    for profundidad in PROFUNDIDADES:
        for minimo in MINIMOS_HOJA:
            modelo = DecisionTreeClassifier(
                max_depth=profundidad, min_samples_leaf=minimo, random_state=semilla
            )
            modelo.fit(X_ent, y_ent)
            pred_ent, pred_val = modelo.predict(X_ent), modelo.predict(X_val)
            modelos.append(modelo)
            filas.append({
                "profundidad": "Sin límite" if profundidad is None else str(profundidad),
                "orden_profundidad": 999 if profundidad is None else profundidad,
                "min_samples_leaf": minimo,
                "exactitud_entrenamiento": accuracy_score(y_ent, pred_ent),
                "exactitud_validacion": accuracy_score(y_val, pred_val),
                "f1_macro_entrenamiento": f1_score(y_ent, pred_ent, average="macro", zero_division=0),
                "f1_macro_validacion": f1_score(y_val, pred_val, average="macro", zero_division=0),
            })
    resultados = pd.DataFrame(filas)
    # F1 macro da el mismo peso a cada clase, aunque haya más reprobados.
    # En empate se prefiere menor profundidad y después hojas más grandes.
    orden = resultados.sort_values(
        ["f1_macro_validacion", "orden_profundidad", "min_samples_leaf"],
        ascending=[False, True, False], kind="mergesort",
    )
    indice = int(orden.index[0])
    resultados["seleccionado"] = resultados.index == indice
    return modelos[indice], resultados


# 6. EVALUACIÓN FINAL: ambos sistemas usan los mismos 100 casos reservados.
def evaluar(y_real, predicciones):
    return {
        "exactitud": accuracy_score(y_real, predicciones),
        "precision_macro": precision_score(y_real, predicciones, average="macro", zero_division=0),
        "recall_macro": recall_score(y_real, predicciones, average="macro", zero_division=0),
        "f1_macro": f1_score(y_real, predicciones, average="macro", zero_division=0),
    }


# 7. VISUALIZACIÓN: métricas expresadas en %, matrices con conteos.
def crear_grafica(busqueda, modelo, y_real, predicciones, metricas, destino, mostrar):
    import matplotlib.pyplot as plt
    from matplotlib.ticker import PercentFormatter

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                         "axes.spines.right": False})
    fig, ejes = plt.subplots(2, 2, figsize=(15, 10), layout="constrained")
    fig.suptitle("Práctica 03 · 500 estudiantes sintéticos · División 300 / 100 / 100",
                 fontsize=16, fontweight="bold")
    ax = ejes[0, 0]
    # Para aislar el efecto de la profundidad se mantiene fijo el tamaño de hoja.
    curva = busqueda[busqueda["min_samples_leaf"] == modelo.min_samples_leaf]
    posiciones = np.arange(len(curva))
    ax.plot(posiciones, curva["f1_macro_entrenamiento"], "o-", label="Entrenamiento", color="#2563eb")
    ax.plot(posiciones, curva["f1_macro_validacion"], "s-", label="Validación", color="#d97706")
    elegido = int(np.flatnonzero(curva["seleccionado"].to_numpy())[0])
    ax.axvline(elegido, color="#64748b", linestyle="--", label="Profundidad elegida")
    ax.set(xticks=posiciones, xticklabels=curva["profundidad"], ylim=(0, 1.05),
           xlabel="Profundidad máxima", ylabel="F1 macro",
           title=f"Complejidad del árbol · mínimo por hoja: {modelo.min_samples_leaf}")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.grid(axis="y", alpha=0.2)
    ax.legend(fontsize=9)

    ax = ejes[0, 1]
    posiciones = np.arange(4)
    for i, (nombre, fila) in enumerate(metricas.iterrows()):
        barras = ax.bar(posiciones + (i - 0.5) * 0.36, fila.to_numpy(dtype=float),
                        width=0.36, label=nombre, color=["#64748b", "#2563eb"][i])
        ax.bar_label(barras, labels=[f"{v:.0%}" for v in fila], padding=3, fontsize=9)
    ax.set(xticks=posiciones, xticklabels=["Exactitud", "Precisión\nmacro", "Recall\nmacro", "F1\nmacro"],
           ylim=(0, 1.18), title="Resultados finales · 100 registros de prueba")
    ax.yaxis.set_major_formatter(PercentFormatter(1))
    ax.legend(loc="upper center", ncol=2, fontsize=9)
    ax.grid(axis="y", alpha=0.2)
    ax.set_axisbelow(True)

    for ax, (nombre, pred) in zip(ejes[1], predicciones.items()):
        ConfusionMatrixDisplay.from_predictions(
            y_real, pred, labels=[0, 1], display_labels=["No aprueba", "Aprueba"],
            ax=ax, cmap="Blues", colorbar=False, values_format="d",
        )
        ax.set(title=f"Matriz de confusión · {nombre}",
               xlabel="Resultado predicho", ylabel="Resultado simulado de referencia")
    fig.savefig(destino / "comparacion_modelos.png", dpi=160)
    if mostrar:
        plt.show()
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--semilla", type=int, default=SEMILLA, help="Semilla aleatoria (42 por defecto).")
    parser.add_argument("--sin-ventanas", action="store_true", help="Guardar la gráfica sin abrir una ventana.")
    parser.add_argument("--salida", type=Path, default=Path(__file__).resolve().parent / "resultados_practica03",
                        help="Carpeta para CSV, informe y gráfica.")
    args = parser.parse_args()
    if args.semilla < 0:
        parser.error("La semilla debe ser un entero no negativo.")
    if args.sin_ventanas:
        matplotlib.use("Agg")
    args.salida.mkdir(parents=True, exist_ok=True)

    df = generar_datos(args.semilla)
    entrenamiento, validacion, prueba = dividir_datos(df, args.semilla)
    modelo, busqueda = seleccionar_modelo(entrenamiento, validacion, args.semilla)
    # Se conserva el árbol entrenado con 300 casos: no se reentrena con validación.
    X_prueba, y_prueba = prueba[CARACTERISTICAS], prueba["aprueba"]
    predicciones = {
        "Reglas fijas": predecir_con_reglas(X_prueba),
        "Árbol de decisiones": modelo.predict(X_prueba),
    }
    metricas = pd.DataFrame({nombre: evaluar(y_prueba, pred)
                            for nombre, pred in predicciones.items()}).T
    metricas.index.name = "sistema"
    comparacion = prueba.copy()
    comparacion["prediccion_reglas"] = predicciones["Reglas fijas"]
    comparacion["prediccion_ml"] = predicciones["Árbol de decisiones"]
    comparacion["acierto_reglas"] = comparacion["aprueba"] == comparacion["prediccion_reglas"]
    comparacion["acierto_ml"] = comparacion["aprueba"] == comparacion["prediccion_ml"]

    # Los identificadores, la nota y el conjunto NO se incluyen en las entradas.
    exportacion = df.copy()
    for nombre, parte in [("entrenamiento", entrenamiento), ("validacion", validacion), ("prueba", prueba)]:
        exportacion.loc[parte.index, "conjunto"] = nombre
    exportacion.to_csv(args.salida / "estudiantes_500.csv", encoding="utf-8-sig")
    comparacion.sort_index().to_csv(args.salida / "predicciones_prueba.csv", encoding="utf-8-sig")
    busqueda.drop(columns="orden_profundidad").to_csv(args.salida / "validacion_modelos.csv", index=False, encoding="utf-8-sig")
    metricas.to_csv(args.salida / "metricas_prueba.csv", encoding="utf-8-sig")

    elegido = busqueda.loc[busqueda["seleccionado"]].iloc[0]
    distribucion = pd.crosstab(exportacion["conjunto"], exportacion["aprueba"]).rename(
        columns={0: "No aprueba", 1: "Aprueba"}
    ).reindex(["entrenamiento", "validacion", "prueba"])
    distribucion["Total"] = distribucion.sum(axis=1)
    lineas = [
        "PRÁCTICA 03: REGLAS FIJAS VS. APRENDIZAJE AUTOMÁTICO",
        f"Semilla: {args.semilla} | Registros: {len(df)} | Aprueba desde: {CALIFICACION_APROBATORIA}/10",
        "Datos sintéticos. La fórmula de calificación y los umbrales son supuestos didácticos.",
        "Calificación = 35% estudio normalizado + 15% asistencia/10 + 35% actividades/10",
        f"              + 15% participación + ruido normal (desviación {DESVIACION_RUIDO}).",
        "Se limita a 0-10 y se redondea a un decimal antes de asignar aprueba.",
        "\nPRIMEROS 10 REGISTROS (la tabla completa está en estudiantes_500.csv)",
        df.head(10).to_string(),
        "\nCALIDAD DE DATOS",
        f"Valores faltantes: {int(df.isna().sum().sum())}",
        f"Filas completas duplicadas, sin considerar ID: {int(df.duplicated().sum())}",
        "Coincidencias aleatorias pueden representar estudiantes distintos; no se eliminan automáticamente.",
        "\nDIVISIÓN ESTRATIFICADA", distribucion.to_string(),
        "\nMODELO ELEGIDO SOLO CON VALIDACIÓN",
        f"Candidatos: {len(busqueda)} | Profundidad: {elegido['profundidad']} | Mínimo por hoja: {modelo.min_samples_leaf}",
        f"F1 macro entrenamiento: {elegido['f1_macro_entrenamiento']:.2%}",
        f"F1 macro validación: {elegido['f1_macro_validacion']:.2%}",
        "\nMÉTRICAS FINALES DE PRUEBA (precisión, recall y F1 usan promedio macro)",
        metricas.to_string(float_format=lambda valor: f"{valor:.2%}"),
    ]
    for nombre, pred in predicciones.items():
        lineas += [f"\nREPORTE POR CLASE: {nombre}", classification_report(
            y_prueba, pred, labels=[0, 1], target_names=["No aprueba", "Aprueba"],
            digits=3, zero_division=0,
        )]

    nuevo = pd.DataFrame({"horas_estudio": [6], "asistencia": [80],
                          "actividades_entregadas": [75], "participacion": [7]})
    etiquetas = {0: "No aprueba", 1: "Aprueba"}
    lineas += [
        "\nEJEMPLO NUEVO (sin calificación final conocida)", nuevo.to_string(index=False),
        f"Reglas fijas: {etiquetas[int(predecir_con_reglas(nuevo).iloc[0])]}",
        f"Árbol: {etiquetas[int(modelo.predict(nuevo)[0])]}",
        "\nINTERPRETACIÓN",
        "Una brecha amplia entre entrenamiento y validación puede indicar sobreajuste.",
        "Resultados bajos en ambos pueden indicar subajuste; también dependen del ruido y de los datos.",
        "La gráfica compara profundidades manteniendo fijo el mínimo de ejemplos por hoja elegido.",
        "El mejor modelo se elige por F1 macro de validación, sin consultar la prueba.",
        "La prueba se usa para la evaluación final, no para volver a ajustar parámetros.",
        "El árbol aprende la relación simulada; no necesariamente superará las reglas en cada semilla.",
        "Los resultados no demuestran capacidad predictiva sobre estudiantes reales.",
        "\nREGLAS APRENDIDAS POR EL ÁRBOL (class 0: no aprueba; class 1: aprueba)",
        export_text(modelo, feature_names=CARACTERISTICAS, max_depth=modelo.get_depth()),
        f"\nArchivos guardados en: {args.salida.resolve()}",
    ]
    informe = "\n".join(lineas)
    (args.salida / "informe_resultados.txt").write_text(informe, encoding="utf-8")
    print(informe)
    crear_grafica(busqueda, modelo, y_prueba, predicciones, metricas, args.salida,
                  mostrar=not args.sin_ventanas)


if __name__ == "__main__":
    main()
