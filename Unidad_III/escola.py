# SISTEMA AUTOMÁTICO BASADO EN REGLAS FIJAS
# Clasificación del rendimiento académico

# Datos de los estudiantes
estudiantes = {
    "Ana": 8,
    "Luis": 3,
    "María": 10,
    "Carlos": 5
}

# Función para tomar decisiones
def clasificar_rendimiento(horas):

    if horas <= 3:
        return "Bajo rendimiento"

    elif horas <= 5:
        return "Rendimiento regular"

    elif horas <= 8:
        return "Buen rendimiento"

    else:
        return "Excelente rendimiento"


# Mostrar resultados
print("SISTEMA AUTOMÁTICO DE CLASIFICACIÓN ACADÉMICA")
print("-" * 50)

for nombre, horas in estudiantes.items():

    resultado = clasificar_rendimiento(horas)

    print(f"Estudiante: {nombre}")
    print(f"Horas de estudio: {horas}")
    print(f"Clasificación: {resultado}")
    print("-" * 50)