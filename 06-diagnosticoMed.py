# ============================================
# SISTEMA EXPERTO DE DIAGNÓSTICO
# ============================================

print("=" * 50)
print("       SISTEMA EXPERTO DE DIAGNÓSTICO")
print("=" * 50)

print("\nResponda las siguientes preguntas con s/n.\n")

nombre = input("Nombre del paciente: ")

fiebre = input("¿Tiene fiebre? (s/n): ").lower()
tos = input("¿Tiene tos? (s/n): ").lower()
dolor = input("¿Tiene dolor de garganta? (s/n): ").lower()
congestion = input("¿Tiene congestión nasal? (s/n): ").lower()
estornudos = input("¿Tiene estornudos frecuentes? (s/n): ").lower()
dolor_cabeza = input("¿Tiene dolor de cabeza? (s/n): ").lower()
dolor_muscular = input("¿Tiene dolor muscular? (s/n): ").lower()
cansancio = input("¿Tiene cansancio o debilidad? (s/n): ").lower()
nauseas = input("¿Tiene náuseas o malestar estomacal? (s/n): ").lower()
dificultad_respirar = input("¿Tiene dificultad para respirar? (s/n): ").lower()
dolor_pecho = input("¿Tiene dolor intenso en el pecho? (s/n): ").lower()

    
# ============================================
# PROPOSICIONES
# ============================================

P = fiebre == "s"
Q = tos == "s"
R = dolor == "s"
S = congestion == "s"
T = dolor_muscular == "s"
U = dificultad_respirar == "s"


# ============================================
# VALORES DE LAS PROPOSICIONES
# ============================================

print("\n" + "=" * 50)
print("       VALORES DE LAS PROPOSICIONES")
print("=" * 50)

print("P - Tiene fiebre                :", P)
print("Q - Tiene tos                   :", Q)
print("R - Tiene dolor de garganta     :", R)
print("S - Tiene congestión nasal      :", S)
print("T - Tiene dolor muscular        :", T)
print("U - Tiene dificultad respiratoria:", U)


# ============================================
# IMPLEMENTACIÓN DE MEJORES DECISIONES
# ============================================

# Primero se revisan síntomas que pueden requerir
# una valoración médica prioritaria.

if dificultad_respirar == "s" or dolor_pecho == "s":

    diagnostico = (
        "Se detectaron síntomas de alarma."
    )

    recomendacion = (
        "Se recomienda buscar valoración médica inmediata."
    )


# --------------------------------------------
# POSIBLE CUADRO TIPO INFLUENZA
# --------------------------------------------

elif (
    fiebre == "s"
    and tos == "s"
    and dolor_muscular == "s"
    and cansancio == "s"
):

    diagnostico = (
        "Patrón compatible con una posible infección "
        "respiratoria de tipo gripal."
    )

    recomendacion = (
        "Se recomienda valoración profesional para "
        "determinar la causa."
    )


# --------------------------------------------
# POSIBLE RESFRIADO
# --------------------------------------------

elif (
    congestion == "s"
    and estornudos == "s"
    and dolor == "s"
    and fiebre == "n"
):

    diagnostico = (
        "Patrón compatible con un cuadro respiratorio leve."
    )

    recomendacion = (
        "Vigilar la evolución de los síntomas y solicitar "
        "valoración si empeoran."
    )


# --------------------------------------------
# POSIBLE INFECCIÓN RESPIRATORIA
# --------------------------------------------

elif fiebre == "s" and tos == "s" and dolor == "s":

    diagnostico = (
        "Patrón compatible con una posible "
        "infección respiratoria."
    )

    recomendacion = (
        "Se recomienda una valoración profesional."
    )


# --------------------------------------------
# IRRITACIÓN DE GARGANTA
# --------------------------------------------

elif tos == "s" and dolor == "s" and fiebre == "n":

    diagnostico = (
        "Patrón compatible con irritación de las "
        "vías respiratorias."
    )

    recomendacion = (
        "Vigilar los síntomas y consultar si persisten "
        "o empeoran."
    )


# --------------------------------------------
# POSIBLE CUADRO ALÉRGICO
# --------------------------------------------

elif (
    estornudos == "s"
    and congestion == "s"
    and fiebre == "n"
    and dolor_muscular == "n"
):

    diagnostico = (
        "Patrón que podría relacionarse con una "
        "reacción alérgica."
    )

    recomendacion = (
        "Se recomienda valoración profesional si los "
        "síntomas son frecuentes o intensos."
    )


# --------------------------------------------
# FIEBRE SIN OTROS SÍNTOMAS CLAROS
# --------------------------------------------

elif fiebre == "s":

    diagnostico = (
        "Se presenta fiebre sin un patrón suficientemente "
        "claro para determinar su posible causa."
    )

    recomendacion = (
        "Se recomienda valoración profesional."
    )


# --------------------------------------------
# DOLOR DE CABEZA Y CANSANCIO
# --------------------------------------------

elif dolor_cabeza == "s" and cansancio == "s":

    diagnostico = (
        "Se presenta dolor de cabeza acompañado "
        "de cansancio."
    )

    recomendacion = (
        "No existe información suficiente para establecer "
        "un patrón específico. Se recomienda vigilar "
        "la evolución."
    )


# --------------------------------------------
# MALESTAR ESTOMACAL
# --------------------------------------------

elif nauseas == "s":

    diagnostico = (
        "Se identificó malestar estomacal, pero no hay "
        "información suficiente para establecer una causa."
    )

    recomendacion = (
        "Se recomienda valoración profesional si el "
        "malestar persiste o aumenta."
    )


# --------------------------------------------
# SIN PATRÓN IDENTIFICADO
# --------------------------------------------

else:

    diagnostico = "No se identificó un patrón específico."

    recomendacion = (
        "Si existen síntomas persistentes o preocupantes, "
        "se recomienda una valoración profesional."
    )


# ============================================
# LÓGICA PROPOSICIONAL
# ============================================

negacion = not P

conjuncion = P and Q

disyuncion = Q or R

condicional = (not P) or Q

bicondicional = P == Q

expresion = (P and Q and R) or (S and not P)


print("\n" + "=" * 50)
print("           OPERACIONES LÓGICAS")
print("=" * 50)

print("¬P =", negacion)
print("P ∧ Q =", conjuncion)
print("Q ∨ R =", disyuncion)
print("P → Q =", condicional)
print("P ↔ Q =", bicondicional)
print("(P ∧ Q ∧ R) ∨ (S ∧ ¬P) =", expresion)


# ============================================
# RESULTADO FINAL
# ============================================

print("\n" + "=" * 50)
print("             RESULTADO FINAL")
print("=" * 50)

print("Paciente:", nombre)

print("\nResultado del sistema:")
print(diagnostico)

print("\nRecomendación:")
print(recomendacion)

print("\n" + "=" * 50)
print(
    "Este sistema es únicamente una simulación académica"
)
print(
    "y no sustituye el diagnóstico de un profesional."
)
print("=" * 50)