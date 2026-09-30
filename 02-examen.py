"""Sistema gráfico de autorización para presentar un examen final."""


def evaluar_autorizacion(
    asistencia,
    promedio,
    proyecto_entregado,
    autorizacion_especial,
    tiene_adeudos,
    aparece_en_lista,
):
    """Evalúa las proposiciones y devuelve todos los resultados lógicos."""
    P = asistencia >= 80
    Q = promedio >= 7
    R = proyecto_entregado
    S = autorizacion_especial
    T = tiene_adeudos
    U = aparece_en_lista

    requisitos_academicos = P and Q and R
    cumple_por_requisitos_o_permiso = requisitos_academicos or S
    resultado_final = cumple_por_requisitos_o_permiso and (not T) and U

    return {
        "P": P,
        "Q": Q,
        "R": R,
        "S": S,
        "T": T,
        "U": U,
        "negacion_P": not P,
        "conjuncion": P and Q,
        "disyuncion": Q or S,
        "condicional": (not P) or Q,
        "bicondicional": P == Q,
        "requisitos_academicos": requisitos_academicos,
        "cumple_por_requisitos_o_permiso": cumple_por_requisitos_o_permiso,
        "resultado_final": resultado_final,
    }


def construir_reporte(resultado):
    """Construye el reporte que se muestra en la interfaz."""
    lineas = [
        "=" * 60,
        "                 VALORES DE LAS PROPOSICIONES",
        "=" * 60,
        f"P - Asistencia suficiente (>= 80%): {resultado['P']}",
        f"Q - Promedio aprobatorio (>= 7):     {resultado['Q']}",
        f"R - Proyecto entregado:              {resultado['R']}",
        f"S - Autorización especial:           {resultado['S']}",
        f"T - Tiene adeudos pendientes:        {resultado['T']}",
        f"U - Aparece en la lista oficial:     {resultado['U']}",
        "",
        "-" * 60,
        "                    OPERACIONES LÓGICAS",
        "-" * 60,
        f"NEGACIÓN         ¬P = {resultado['negacion_P']}",
        f"CONJUNCIÓN     P ∧ Q = {resultado['conjuncion']}",
        f"DISYUNCIÓN     Q ∨ S = {resultado['disyuncion']}",
        f"CONDICIONAL    P → Q = {resultado['condicional']}",
        f"BICONDICIONAL  P ↔ Q = {resultado['bicondicional']}",
        "",
        "-" * 60,
        "                       REGLA FINAL",
        "-" * 60,
        "((P ∧ Q ∧ R) ∨ S) ∧ ¬T ∧ U",
        f"Requisitos académicos (P ∧ Q ∧ R): "
        f"{resultado['requisitos_academicos']}",
        f"Requisitos o autorización especial: "
        f"{resultado['cumple_por_requisitos_o_permiso']}",
        f"Resultado final: {resultado['resultado_final']}",
        "",
        "=" * 60,
        "                         DECISIÓN",
        "=" * 60,
    ]

    if resultado["resultado_final"]:
        lineas.append("El alumno PUEDE presentar el examen.")
        if resultado["S"] and not resultado["requisitos_academicos"]:
            lineas.append("La autorización fue concedida mediante permiso especial.")
    else:
        lineas.append("El alumno NO puede presentar el examen.")
        lineas.append("")
        lineas.append("Motivos:")

        if resultado["T"]:
            lineas.append("  - Tiene adeudos pendientes.")
        if not resultado["U"]:
            lineas.append("  - No aparece en la lista oficial.")
        if not resultado["cumple_por_requisitos_o_permiso"]:
            if not resultado["P"]:
                lineas.append("  - No alcanza el 80% de asistencia.")
            if not resultado["Q"]:
                lineas.append("  - No alcanza el promedio mínimo de 7.")
            if not resultado["R"]:
                lineas.append("  - No entregó el proyecto.")
            if not resultado["S"]:
                lineas.append("  - No tiene autorización especial.")

    return "\n".join(lineas)


def crear_interfaz():
    """Crea y ejecuta la interfaz gráfica del sistema."""
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError as error:
        raise SystemExit(
            "Tkinter no está instalado. Instala el paquete python3-tk "
            "para ejecutar la interfaz."
        ) from error

    ventana = tk.Tk()
    ventana.title("Sistema de autorización para examen final")
    ventana.geometry("820x700")
    ventana.minsize(720, 620)

    tk.Label(
        ventana,
        text="SISTEMA DE AUTORIZACIÓN PARA EXAMEN FINAL",
        font=("Arial", 14, "bold"),
    ).pack(pady=(14, 8))

    tk.Label(
        ventana,
        text="Captura los datos del alumno y presiona Evaluar",
        font=("Arial", 10),
    ).pack(pady=(0, 8))

    marco_datos = tk.LabelFrame(ventana, text="Datos del alumno", padx=14, pady=10)
    marco_datos.pack(fill="x", padx=18, pady=5)

    tk.Label(marco_datos, text="Porcentaje de asistencia:").grid(
        row=0, column=0, sticky="e", padx=5, pady=4
    )
    caja_asistencia = tk.Entry(marco_datos, width=12)
    caja_asistencia.grid(row=0, column=1, sticky="w", padx=5)

    tk.Label(marco_datos, text="Promedio:").grid(
        row=1, column=0, sticky="e", padx=5, pady=4
    )
    caja_promedio = tk.Entry(marco_datos, width=12)
    caja_promedio.grid(row=1, column=1, sticky="w", padx=5)

    proyecto = tk.BooleanVar()
    autorizacion = tk.BooleanVar()
    adeudos = tk.BooleanVar()
    lista_oficial = tk.BooleanVar()

    opciones = [
        ("Entregó el proyecto", proyecto),
        ("Tiene autorización especial", autorizacion),
        ("Tiene adeudos pendientes", adeudos),
        ("Aparece en la lista oficial", lista_oficial),
    ]

    for fila, (texto, variable) in enumerate(opciones, start=2):
        tk.Checkbutton(marco_datos, text=texto, variable=variable).grid(
            row=fila, column=0, columnspan=2, sticky="w", padx=5, pady=2
        )

    marco_reporte = tk.Frame(ventana)
    marco_reporte.pack(fill="both", expand=True, padx=18, pady=8)

    barra = tk.Scrollbar(marco_reporte)
    barra.pack(side="right", fill="y")

    salida = tk.Text(
        marco_reporte,
        font=("Courier New", 10),
        wrap="none",
        state="disabled",
        yscrollcommand=barra.set,
    )
    salida.pack(fill="both", expand=True)
    barra.config(command=salida.yview)

    def mostrar_reporte(texto):
        salida.config(state="normal")
        salida.delete("1.0", tk.END)
        salida.insert("1.0", texto)
        salida.config(state="disabled")

    def evaluar_desde_interfaz():
        try:
            asistencia = float(caja_asistencia.get().strip())
            promedio = float(caja_promedio.get().strip())
        except ValueError:
            messagebox.showwarning(
                "Datos inválidos",
                "La asistencia y el promedio deben ser valores numéricos.",
            )
            return

        if not 0 <= asistencia <= 100:
            messagebox.showwarning(
                "Asistencia inválida",
                "La asistencia debe encontrarse entre 0 y 100.",
            )
            return

        if not 0 <= promedio <= 10:
            messagebox.showwarning(
                "Promedio inválido",
                "El promedio debe encontrarse entre 0 y 10.",
            )
            return

        resultado = evaluar_autorizacion(
            asistencia,
            promedio,
            proyecto.get(),
            autorizacion.get(),
            adeudos.get(),
            lista_oficial.get(),
        )
        mostrar_reporte(construir_reporte(resultado))

    def limpiar():
        caja_asistencia.delete(0, tk.END)
        caja_promedio.delete(0, tk.END)
        proyecto.set(False)
        autorizacion.set(False)
        adeudos.set(False)
        lista_oficial.set(False)
        mostrar_reporte("")
        caja_asistencia.focus_set()

    marco_botones = tk.Frame(ventana)
    marco_botones.pack(pady=(0, 14))

    tk.Button(
        marco_botones,
        text="Evaluar",
        width=16,
        command=evaluar_desde_interfaz,
    ).pack(side="left", padx=6)

    tk.Button(
        marco_botones,
        text="Limpiar",
        width=16,
        command=limpiar,
    ).pack(side="left", padx=6)

    caja_asistencia.focus_set()
    ventana.mainloop()


if __name__ == "__main__":
    crear_interfaz()
