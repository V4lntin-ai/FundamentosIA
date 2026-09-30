# ==========================================================
# CASO DE ESTUDIO
# Sistema de autorización para examen
# ==========================================================

print("=" * 55)
print("       SISTEMA DE AUTORIZACIÓN PARA EXAMEN")
print("=" * 55)

# ----------------------------------------------------------
# 1. ENTRADA DE DATOS
# ----------------------------------------------------------

asistencia = float(input("Ingresa el porcentaje de asistencia: "))
promedio = float(input("Ingresa el promedio: "))

proyecto = input(
    "¿Entregó el proyecto? (si/no): "
).lower()

adeudos = input(
    "¿Tiene adeudos? (si/no): "
).lower()

autorizacion = input(
    "¿Tiene autorización especial? (si/no): "
).lower()

lista_oficial = input(
    "¿Aparece en la lista oficial? (si/no): "
).lower()


# ----------------------------------------------------------
# 2. CREACIÓN DE LAS PROPOSICIONES
# ----------------------------------------------------------

# P: El alumno tiene asistencia suficiente
P = asistencia >= 80

# Q: El alumno tiene promedio aprobatorio
Q = promedio >= 8

# R: El alumno entregó el proyecto
R = proyecto == "si"

# S: El alumno NO tiene adeudos
S = adeudos == "no"

# T: El alumno tiene autorización especial
T = autorizacion == "si"

# U: El alumno aparece en la lista oficial
U = lista_oficial == "si"


# ----------------------------------------------------------
# 3. MOSTRAR LAS PROPOSICIONES
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("             VALORES DE LAS PROPOSICIONES")
print("=" * 55)

print("P - Asistencia suficiente :", P)
print("Q - Promedio aprobatorio  :", Q)
print("R - Proyecto entregado    :", R)
print("S - Sin adeudos           :", S)
print("T - Autorización especial :", T)
print("U - Aparece en lista      :", U)


# ==========================================================
# 4. NEGACIÓN
# ==========================================================

# La negación invierte el valor de una proposición.
#
# Si P = True  → NOT P = False
# Si P = False → NOT P = True
#
# Lo mismo aplica para U.

no_P = not P
no_U = not U

print("\nNEGACIÓN")
print("¬P =", no_P)
print("¬U =", no_U)


# ==========================================================
# 5. CONJUNCIÓN
# ==========================================================

# AND significa "Y".
# Ambas proposiciones deben ser verdaderas.
#
# P ∧ Q:
# El alumno tiene asistencia suficiente
# Y tiene promedio aprobatorio.

conjuncion = P and Q

print("\nCONJUNCIÓN")
print("P ∧ Q =", conjuncion)


# ==========================================================
# 6. DISYUNCIÓN
# ==========================================================

# OR significa "O".
# Basta con que una condición sea verdadera.
#
# Q ∨ T:
# Tiene promedio aprobatorio
# O tiene autorización especial.

disyuncion = Q or T

print("\nDISYUNCIÓN")
print("Q ∨ T =", disyuncion)


# ==========================================================
# 7. CONDICIONAL
# ==========================================================

# P → Q  se lee  "Si P, entonces Q"
#
# En lógica proposicional:
# P → Q = (NOT P) OR Q

condicional = (not P) or Q

print("\nCONDICIONAL")
print("P → Q =", condicional)


# ==========================================================
# 8. BICONDICIONAL
# ==========================================================

# P ↔ Q  se lee  "P si y solo si Q"
#
# Es verdadero cuando ambas proposiciones
# tienen el mismo valor de verdad.

bicondicional = P == Q

print("\nBICONDICIONAL")
print("P ↔ Q =", bicondicional)


# ==========================================================
# 9. EXPRESIÓN CON PARÉNTESIS
# ==========================================================

# Regla de la universidad:
#
# El alumno puede presentar el examen si:
#
# ( (P ∧ Q ∧ R ∧ S) ∨ T ) ∧ U
#
# Es decir:
# (Asistencia Y promedio Y proyecto Y sin adeudos)
# O autorización especial
# Y obligatoriamente aparece en la lista oficial.
#
# U es requisito absoluto: sin importar el camino
# que tome el alumno, debe estar en la lista.

resultado = ((P and Q and R and S) or T) and U

print("\nEXPRESIÓN CON PARÉNTESIS")
print("((P ∧ Q ∧ R ∧ S) ∨ T) ∧ U =", resultado)


# ==========================================================
# 10. BICONDICIONAL PARA AUTORIZACIÓN
# ==========================================================

# Verificación adicional:
# La autorización especial es correcta
# SI Y SOLO SI el alumno aparece en la lista.
#
# T ↔ U

autorizacion_correcta = T == U

print("\nBICONDICIONAL DE AUTORIZACIÓN")
print("T ↔ U =", autorizacion_correcta)


# ==========================================================
# 11. RESULTADO FINAL
# ==========================================================

print("\n" + "=" * 55)
print("                  RESULTADO FINAL")
print("=" * 55)

if resultado:
    print("El alumno PUEDE presentar el examen.")
else:
    print("El alumno NO puede presentar el examen.")
    if no_U:
        print("MOTIVO: No aparece en la lista oficial (¬U = True).")

if autorizacion_correcta:
    print("La autorización COINCIDE con la lista oficial.")
else:
    print("ADVERTENCIA: La autorización NO coincide con la lista oficial.")