"""
==============================================================
Primer Gráfico con Matplotlib (versión mejorada)
==============================================================
Materia: Extracción de Conocimiento en Bases de Datos
Objetivo: Aprender a construir una gráfica profesional
          utilizando Matplotlib.
==============================================================
"""

# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ==========================================================
# DATOS
# ==========================================================
meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# Ventas simuladas (miles de pesos)
ventas = np.array([85, 90, 96, 105, 120, 135,
                   150, 148, 160, 172, 181, 195])

x = np.arange(len(meses))            # posiciones numéricas 0..11
promedio = ventas.mean()
i_max = int(np.argmax(ventas))
i_min = int(np.argmin(ventas))
crecimiento = (ventas[-1] / ventas[0] - 1) * 100

# ==========================================================
# PALETA DE COLORES (una sola fuente de verdad)
# ==========================================================
AZUL = "#1f5fa8"
AZUL_CLARO = "#cfe0f3"
ROJO = "#c0392b"
VERDE = "#1e8449"
NARANJA = "#d68910"
GRIS = "#5f6b76"
GRIS_CLARO = "#d9dee3"

# ==========================================================
# CONFIGURACIÓN GENERAL
# ==========================================================
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": GRIS,
    "axes.labelcolor": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#333333",
})

fig, ax = plt.subplots(figsize=(14, 8))
fig.subplots_adjust(top=0.84, bottom=0.19, left=0.08, right=0.96)

# ==========================================================
# ÁREA BAJO LA CURVA (da volumen visual a la tendencia)
# ==========================================================
ax.fill_between(x, ventas, 60, color=AZUL_CLARO, alpha=0.55, zorder=1)

# ==========================================================
# LÍNEA DE PROMEDIO
# ==========================================================
ax.axhline(promedio, color=ROJO, linestyle="--", linewidth=1.8,
           zorder=2, label=f"Promedio anual ({promedio:.1f})")

# ==========================================================
# GRÁFICA PRINCIPAL
# ==========================================================
ax.plot(x, ventas,
        color=AZUL, linewidth=3, marker="o", markersize=9,
        markerfacecolor="white", markeredgewidth=2.5,
        zorder=3, label="Ventas mensuales")

# ==========================================================
# DESTACAR MÁXIMO Y MÍNIMO
# ==========================================================
ax.scatter(x[i_max], ventas[i_max], s=220, color=VERDE,
           edgecolor="white", linewidth=2, zorder=5,
           label=f"Máximo ({meses[i_max]}: {ventas[i_max]})")
ax.scatter(x[i_min], ventas[i_min], s=220, color=NARANJA,
           edgecolor="white", linewidth=2, zorder=5,
           label=f"Mínimo ({meses[i_min]}: {ventas[i_min]})")

# ==========================================================
# ETIQUETAS DE VALOR (sobre cada punto, con fondo blanco)
# ==========================================================
for xi, yi in zip(x, ventas):
    ax.annotate(
        f"{yi}",
        xy=(xi, yi), xytext=(0, 14), textcoords="offset points",
        ha="center", va="bottom", fontsize=11, fontweight="bold",
        color="#222222",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85),
        zorder=6,
    )

# ==========================================================
# ANOTACIONES CON FLECHA
# ==========================================================
ax.annotate(
    f"Mayor venta del año\n{meses[i_max]}: \\${ventas[i_max]} mil",
    xy=(x[i_max], ventas[i_max]), xytext=(x[i_max] - 2.3, 208),
    ha="center", fontsize=12, fontweight="bold", color=VERDE,
    arrowprops=dict(arrowstyle="->", color=VERDE, lw=2,
                    connectionstyle="arc3,rad=-0.2"),
    zorder=6,
)
ax.annotate(
    f"Menor venta del año\n{meses[i_min]}: \\${ventas[i_min]} mil",
    xy=(x[i_min], ventas[i_min]), xytext=(x[i_min] + 1.2, 68),
    ha="center", fontsize=12, fontweight="bold", color=NARANJA,
    arrowprops=dict(arrowstyle="->", color=NARANJA, lw=2,
                    connectionstyle="arc3,rad=0.2"),
    zorder=6,
)

# ==========================================================
# TÍTULO Y SUBTÍTULO (alineados a la izquierda)
# ==========================================================
fig.text(0.08, 0.94, "Ventas Mensuales de la Empresa EcoMart",
         fontsize=23, fontweight="bold", color="#111111", ha="left")
fig.text(0.08, 0.895,
         f"Periodo enero – diciembre 2026  |  Crecimiento anual: "
         f"+{crecimiento:.0f} % (de \\${ventas[0]} mil a \\${ventas[-1]} mil)",
         fontsize=13, color=GRIS, ha="left")

# ==========================================================
# EJES: ETIQUETAS, ESCALA Y FORMATO
# ==========================================================
ax.set_xlabel("Mes (2026)", fontsize=14, fontweight="bold", labelpad=10)
ax.set_ylabel("Ventas (miles de pesos)", fontsize=14, fontweight="bold",
              labelpad=10)

ax.set_xticks(x)
ax.set_xticklabels(meses, fontsize=12)
ax.set_xlim(-0.6, len(meses) - 0.4)

ax.set_ylim(60, 220)
ax.yaxis.set_major_locator(mticker.MultipleLocator(20))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"\\${v:.0f}"))
ax.tick_params(axis="y", labelsize=12)
ax.tick_params(axis="both", length=5)

# ==========================================================
# CUADRÍCULA (solo horizontal, discreta)
# ==========================================================
ax.set_axisbelow(True)
ax.grid(axis="y", linestyle="--", linewidth=0.7, color=GRIS_CLARO)
ax.grid(axis="x", visible=False)

# ==========================================================
# LEYENDA (fuera del área de datos, parte inferior)
# ==========================================================
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.10), ncol=4,
          fontsize=12, frameon=False)

# ==========================================================
# QUITAR MARCO SUPERIOR Y DERECHO
# ==========================================================
for lado in ("top", "right"):
    ax.spines[lado].set_visible(False)

# ==========================================================
# PIE DE FIGURA
# ==========================================================
fig.text(0.08, 0.015,
         "Fuente: datos simulados  |  Elaboración propia  |  UTVT",
         fontsize=10, color=GRIS, ha="left")

# ==========================================================
# GUARDAR IMAGEN
# ==========================================================
plt.savefig("Grafica_Profesional_01.png", dpi=300,
            bbox_inches="tight", facecolor="white")

# ==========================================================
# MOSTRAR
# ==========================================================
plt.show()

print("=" * 60)
print("Gráfica generada correctamente.")
print("Archivo guardado como:")
print("Grafica_Profesional_01.png")
print("=" * 60)