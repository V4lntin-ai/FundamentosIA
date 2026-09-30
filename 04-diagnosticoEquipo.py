import random

# ==========================================================
# CASO DE ESTUDIO
# Sistema de Diagnóstico de Equipos
# ==========================================================

print("=" * 55)
print("       SISTEMA DE DIAGNÓSTICO DE EQUIPOS")
print("=" * 55)

# ----------------------------------------------------------
# 1. DATOS DEL CLIENTE Y MENÚS DE SELECCIÓN
# ----------------------------------------------------------

nombre_usuario = input("Ingrese su nombre: ")
direccion_usuario = input("Ingrese su dirección: ")

print("\n--- TIPO DE DISPOSITIVO ---")
print("1. PC")
print("2. Laptop")
print("3. Servidor")
print("4. Tablet")
print("5. Otro")
tipo_dispositivo = input("Seleccione el número correspondiente a su equipo: ")

print("\n--- PROBLEMA PRINCIPAL ---")
print("1. No enciende")
print("2. Enciende pero no da imagen")
print("3. Lentitud o fallos del sistema operativo")
print("4. Se apaga repentinamente")
print("5. Otro")
problema_reportado = input("Seleccione el número del problema reportado: ")


# ----------------------------------------------------------
# 2. ENTRADA DE DATOS (DIAGNÓSTICO)
# ----------------------------------------------------------

print("\nPor favor responda (si/no) a las siguientes preguntas de diagnóstico:")

electricidad = input("¿El equipo está conectado a la corriente o tiene batería? (si/no): ").lower()
enciende = input("¿El equipo enciende (luces, ventiladores, sonidos)? (si/no): ").lower()
imagen = input("¿El equipo muestra imagen en la pantalla? (si/no): ").lower()
pitidos = input("¿El equipo emite pitidos o luces de error? (si/no): ").lower()
garantia = input("¿El equipo cuenta con garantía vigente? (si/no): ").lower()
dano_fisico = input("¿El equipo presenta daño físico evidente (golpes, derrames)? (si/no): ").lower()


# ----------------------------------------------------------
# 3. CREACIÓN DE LAS PROPOSICIONES
# ----------------------------------------------------------

# P: El equipo tiene suministro eléctrico
P = electricidad == "si"

# Q: El equipo enciende
Q = enciende == "si"

# R: El equipo da imagen
R = imagen == "si"

# S: El equipo NO emite pitidos de error
S = pitidos == "no"

# T: El equipo tiene garantía vigente
T = garantia == "si"

# U: El equipo NO tiene daño físico evidente
U = dano_fisico == "no"


# ----------------------------------------------------------
# 4. MOSTRAR LAS PROPOSICIONES
# ----------------------------------------------------------

print("\n" + "=" * 55)
print("             VALORES DE LAS PROPOSICIONES")
print("=" * 55)

print("P - Tiene electricidad    :", P)
print("Q - El equipo enciende    :", Q)
print("R - Da imagen en pantalla :", R)
print("S - Sin pitidos de error  :", S)
print("T - Garantía vigente      :", T)
print("U - Sin daño físico       :", U)


# ==========================================================
# 5. NEGACIÓN
# ==========================================================

no_P = not P
no_U = not U

print("\nNEGACIÓN")
print("¬P (No tiene electricidad) =", no_P)
print("¬U (Tiene daño físico)     =", no_U)


# ==========================================================
# 6. CONJUNCIÓN
# ==========================================================

conjuncion = P and Q

print("\nCONJUNCIÓN")
print("P ∧ Q (Tiene electricidad Y enciende) =", conjuncion)


# ==========================================================
# 7. DISYUNCIÓN
# ==========================================================

disyuncion = Q or T

print("\nDISYUNCIÓN")
print("Q ∨ T (Enciende O tiene garantía) =", disyuncion)


# ==========================================================
# 8. CONDICIONAL
# ==========================================================

condicional = (not P) or Q

print("\nCONDICIONAL")
print("P → Q (Si tiene electricidad, entonces enciende) =", condicional)


# ==========================================================
# 9. BICONDICIONAL
# ==========================================================

bicondicional = P == Q

print("\nBICONDICIONAL")
print("P ↔ Q (Tiene electricidad si y solo si enciende) =", bicondicional)


# ==========================================================
# 10. EXPRESIÓN CON PARÉNTESIS
# ==========================================================

# Regla del taller:
# El equipo es apto para reparación estándar o uso normal si:
# ( (P ∧ Q ∧ R ∧ S) ∨ T ) ∧ U
# Es decir, (Funciona correctamente O tiene garantía) Y no presenta daño físico.

resultado = ((P and Q and R and S) or T) and U

print("\nEXPRESIÓN CON PARÉNTESIS")
print("((P ∧ Q ∧ R ∧ S) ∨ T) ∧ U =", resultado)


# ==========================================================
# 11. BICONDICIONAL DE GARANTÍA
# ==========================================================

# La garantía aplica de forma correcta SI Y SOLO SI no hay daño físico
garantia_correcta = T == U

print("\nBICONDICIONAL DE GARANTÍA")
print("T ↔ U (Garantía coincide con estado físico) =", garantia_correcta)


# ==========================================================
# 12. RESULTADO FINAL Y REPORTE
# ==========================================================

numero_reporte = random.randint(1000, 9999)

print("\n" + "=" * 55)
print(f"            REPORTE DE DIAGNÓSTICO #{numero_reporte}")
print("=" * 55)
print(f"Cliente   : {nombre_usuario}")
print(f"Dirección : {direccion_usuario}")
print(f"Equipo    : Opción {tipo_dispositivo}")
print(f"Problema  : Opción {problema_reportado}")
print("-" * 55)

if resultado:
    print("DIAGNÓSTICO: El equipo está operativo o cubierto para reparación estándar.")
else:
    print("DIAGNÓSTICO: El equipo requiere revisión profunda o cotización de refacciones.")
    if no_U:
        print("MOTIVO: Presenta daño físico evidente (¬U = True), lo cual anula procesos estándar.")

if garantia_correcta:
    print("ESTADO: El registro de garantía es congruente con el estado del equipo.")
else:
    print("ADVERTENCIA: Conflicto de cobertura (Posible daño físico anula la garantía vigente).")