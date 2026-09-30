import random

# ==========================================================
# CASO DE ESTUDIO
# Sistema de diagnóstico para equipos de cómputo
# ==========================================================

print("=" * 65)
print("      BIENVENIDO AL SISTEMA DE DIAGNÓSTICO DE EQUIPOS")
print("=" * 65)

print("\nAntes de comenzar, ingresa los siguientes datos.")

nombre_usuario = input("Nombre del usuario: ")
direccion_usuario = input("Dirección: ")


# ----------------------------------------------------------
# 1. SELECCIÓN DEL TIPO DE DISPOSITIVO
# ----------------------------------------------------------

print("\n" + "=" * 65)
print("              SELECCIÓN DEL DISPOSITIVO")
print("=" * 65)

print("1. PC de escritorio")
print("2. Laptop")
print("3. Servidor")
print("4. Tablet")
print("5. Otro equipo")

opcion_equipo = input("Selecciona una opción (1-5): ")

if opcion_equipo == "1":
    tipo_equipo = "PC de escritorio"
elif opcion_equipo == "2":
    tipo_equipo = "Laptop"
elif opcion_equipo == "3":
    tipo_equipo = "Servidor"
elif opcion_equipo == "4":
    tipo_equipo = "Tablet"
elif opcion_equipo == "5":
    tipo_equipo = "Otro equipo"
else:
    tipo_equipo = "Equipo no especificado"


# ----------------------------------------------------------
# 2. SELECCIÓN DEL PROBLEMA
# ----------------------------------------------------------

print("\n" + "=" * 65)
print("                PROBLEMA DEL EQUIPO")
print("=" * 65)
print("Equipo seleccionado:", tipo_equipo)

if opcion_equipo == "1":
    print("\n1. No enciende")
    print("2. Enciende, pero no da imagen")
    print("3. No inicia el sistema o se congela")
    print("4. No tiene conexión de red")
    print("5. Se apaga, reinicia o funciona lento")

elif opcion_equipo == "2":
    print("\n1. No enciende o no carga")
    print("2. Enciende, pero no da imagen")
    print("3. No inicia el sistema o se congela")
    print("4. No tiene conexión Wi-Fi o de red")
    print("5. Se apaga, reinicia o funciona lento")

elif opcion_equipo == "3":
    print("\n1. No enciende")
    print("2. Enciende, pero no muestra imagen o consola")
    print("3. No inicia el sistema o no detecta almacenamiento")
    print("4. Presenta problemas de red")
    print("5. Se reinicia, se apaga o presenta bajo rendimiento")

elif opcion_equipo == "4":
    print("\n1. No enciende o no carga")
    print("2. Enciende, pero la pantalla no muestra imagen")
    print("3. No inicia correctamente o se congela")
    print("4. No tiene conexión Wi-Fi")
    print("5. Se apaga, reinicia o funciona lento")

else:
    print("\n1. No enciende o no recibe energía")
    print("2. Enciende, pero no da imagen")
    print("3. No inicia correctamente")
    print("4. Presenta problemas de red")
    print("5. Se apaga, reinicia o funciona lento")

opcion_problema = input("Selecciona el problema principal (1-5): ")


# ----------------------------------------------------------
# 3. DIAGNÓSTICO SEGÚN EL PROBLEMA SELECCIONADO
# ----------------------------------------------------------

print("\n" + "=" * 65)
print("                 INICIO DEL DIAGNÓSTICO")
print("=" * 65)

diagnostico = ""
recomendacion = ""

# ----------------------------------------------------------
# PROBLEMA 1: NO ENCIENDE / NO CARGA
# ----------------------------------------------------------

if opcion_problema == "1":

    problema = "El equipo no enciende o no recibe carga"

    electricidad = input(
        "¿La toma eléctrica o fuente de energía funciona? (si/no): "
    ).lower()

    cable = input(
        "¿El cable, cargador o fuente está correctamente conectado? (si/no): "
    ).lower()

    indicador = input(
        "¿Se enciende algún LED o indicador de energía? (si/no): "
    ).lower()

    respuesta = input(
        "¿El equipo responde al presionar el botón de encendido? (si/no): "
    ).lower()

    bateria = input(
        "¿La batería o fuente de alimentación parece funcionar correctamente? (si/no): "
    ).lower()

    dano = input(
        "¿El equipo está libre de olor a quemado, calor excesivo o daño visible? (si/no): "
    ).lower()

    # Proposiciones
    P = electricidad == "si"
    Q = cable == "si"
    R = indicador == "si"
    S = respuesta == "si"
    T = bateria == "si"
    U = dano == "si"

    texto_P = "La fuente de energía funciona"
    texto_Q = "El cable/cargador está conectado correctamente"
    texto_R = "Existe indicador de energía"
    texto_S = "El equipo responde al botón de encendido"
    texto_T = "La batería o fuente parece funcionar"
    texto_U = "No hay daño físico evidente"

    resultado = P and Q and R and S and T and U

    if not P:
        diagnostico = "Posible falla en la toma eléctrica o fuente de energía."
        recomendacion = "Probar otra toma eléctrica o verificar la alimentación."
    elif not Q:
        diagnostico = "Posible problema con el cable, cargador o conexión de energía."
        recomendacion = "Revisar conexiones y probar un cable o cargador compatible."
    elif not R:
        diagnostico = "El equipo recibe alimentación, pero no muestra señales de energía."
        recomendacion = "Revisar batería, fuente de poder o circuito de alimentación."
    elif not S:
        diagnostico = "Posible falla en el sistema de encendido."
        recomendacion = "Revisar botón de encendido, batería, fuente o tarjeta principal."
    elif not T:
        diagnostico = "Posible falla de batería o fuente de alimentación."
        recomendacion = "Comprobar la batería o fuente con una alternativa compatible."
    elif not U:
        diagnostico = "Se detectan indicios de daño físico o eléctrico."
        recomendacion = "No continuar encendiendo el equipo y solicitar revisión técnica."
    else:
        diagnostico = "No se detectó una falla evidente en la alimentación."
        recomendacion = "Continuar con una revisión interna del equipo."


# ----------------------------------------------------------
# PROBLEMA 2: ENCIENDE, PERO NO DA IMAGEN
# ----------------------------------------------------------

elif opcion_problema == "2":

    problema = "El equipo enciende, pero no da imagen"

    energia = input(
        "¿El equipo muestra luces, sonido o señales de encendido? (si/no): "
    ).lower()

    pantalla = input(
        "¿La pantalla o monitor está encendido correctamente? (si/no): "
    ).lower()

    brillo = input(
        "¿El brillo o nivel de iluminación es suficiente? (si/no): "
    ).lower()

    conexion_video = input(
        "¿La conexión de video o pantalla está correctamente conectada? (si/no): "
    ).lower()

    pantalla_externa = input(
        "¿Al probar otra pantalla o salida de video se obtiene imagen? (si/no): "
    ).lower()

    arranque = input(
        "¿El equipo parece completar el proceso de arranque? (si/no): "
    ).lower()

    # Proposiciones
    P = energia == "si"
    Q = pantalla == "si"
    R = brillo == "si"
    S = conexion_video == "si"
    T = pantalla_externa == "si"
    U = arranque == "si"

    texto_P = "El equipo presenta señales de encendido"
    texto_Q = "La pantalla/monitor está encendido"
    texto_R = "El brillo es adecuado"
    texto_S = "La conexión de video es correcta"
    texto_T = "Otra pantalla o salida muestra imagen"
    texto_U = "El equipo completa el arranque"

    resultado = P and Q and R and S and T and U

    if not P:
        diagnostico = "El problema podría estar relacionado con el encendido y no con la imagen."
        recomendacion = "Realizar primero el diagnóstico de alimentación."
    elif not Q:
        diagnostico = "Posible falla o falta de alimentación en la pantalla o monitor."
        recomendacion = "Verificar que la pantalla esté encendida y reciba energía."
    elif not R:
        diagnostico = "La imagen podría no ser visible por configuración de brillo."
        recomendacion = "Aumentar el brillo y verificar la iluminación de la pantalla."
    elif not S:
        diagnostico = "Posible problema en la conexión de video."
        recomendacion = "Revisar cable, puerto o conexión interna de pantalla."
    elif T:
        diagnostico = "El equipo genera imagen, pero la pantalla principal podría estar fallando."
        recomendacion = "Revisar pantalla, cable flex, monitor o conexión principal."
    elif not U:
        diagnostico = "El equipo enciende, pero podría no completar el arranque."
        recomendacion = "Revisar memoria, almacenamiento o proceso de inicio."
    else:
        diagnostico = "Posible falla en el sistema gráfico o de video."
        recomendacion = "Revisar salida gráfica, pantalla y componentes de video."


# ----------------------------------------------------------
# PROBLEMA 3: NO INICIA / SE CONGELA
# ----------------------------------------------------------

elif opcion_problema == "3":

    problema = "El sistema no inicia correctamente o se congela"

    enciende = input(
        "¿El equipo enciende normalmente? (si/no): "
    ).lower()

    imagen = input(
        "¿El equipo muestra imagen durante el arranque? (si/no): "
    ).lower()

    almacenamiento = input(
        "¿El equipo detecta la unidad de almacenamiento? (si/no): "
    ).lower()

    logo = input(
        "¿El equipo llega a mostrar el logotipo o pantalla de inicio del sistema? (si/no): "
    ).lower()

    sistema = input(
        "¿El sistema operativo logra iniciar? (si/no): "
    ).lower()

    estable = input(
        "¿El sistema funciona sin congelarse o reiniciarse? (si/no): "
    ).lower()

    # Proposiciones
    P = enciende == "si"
    Q = imagen == "si"
    R = almacenamiento == "si"
    S = logo == "si"
    T = sistema == "si"
    U = estable == "si"

    texto_P = "El equipo enciende"
    texto_Q = "El equipo muestra imagen"
    texto_R = "El almacenamiento es detectado"
    texto_S = "Aparece la pantalla de inicio"
    texto_T = "El sistema operativo inicia"
    texto_U = "El sistema permanece estable"

    resultado = P and Q and R and S and T and U

    if not P:
        diagnostico = "El problema está relacionado con el encendido."
        recomendacion = "Realizar primero el diagnóstico de alimentación."
    elif not Q:
        diagnostico = "El equipo enciende, pero existe un problema de imagen."
        recomendacion = "Realizar el diagnóstico de pantalla o video."
    elif not R:
        diagnostico = "Posible falla o desconexión de la unidad de almacenamiento."
        recomendacion = "Revisar SSD, HDD, memoria interna o sus conexiones."
    elif not S:
        diagnostico = "El equipo no llega correctamente a la etapa de inicio del sistema."
        recomendacion = "Revisar configuración de arranque y almacenamiento."
    elif not T:
        diagnostico = "Posible falla en el arranque del sistema operativo."
        recomendacion = "Revisar archivos de inicio, sistema operativo o almacenamiento."
    elif not U:
        diagnostico = "El sistema inicia, pero presenta inestabilidad."
        recomendacion = "Revisar temperatura, memoria, almacenamiento y uso de recursos."
    else:
        diagnostico = "El proceso de arranque funciona correctamente."
        recomendacion = "La falla puede ser intermitente; continuar con pruebas específicas."


# ----------------------------------------------------------
# PROBLEMA 4: RED / INTERNET
# ----------------------------------------------------------

elif opcion_problema == "4":

    problema = "El equipo presenta problemas de red o Internet"

    adaptador = input(
        "¿El adaptador de red o Wi-Fi está habilitado? (si/no): "
    ).lower()

    red_detectada = input(
        "¿El equipo detecta la red disponible? (si/no): "
    ).lower()

    otros_equipos = input(
        "¿Otros equipos pueden conectarse a la misma red? (si/no): "
    ).lower()

    conectado = input(
        "¿El equipo logra conectarse a la red? (si/no): "
    ).lower()

    direccion_ip = input(
        "¿El equipo obtiene una dirección de red correctamente? (si/no): "
    ).lower()

    internet = input(
        "¿El equipo puede acceder a Internet? (si/no): "
    ).lower()

    # Proposiciones
    P = adaptador == "si"
    Q = red_detectada == "si"
    R = otros_equipos == "si"
    S = conectado == "si"
    T = direccion_ip == "si"
    U = internet == "si"

    texto_P = "El adaptador de red está habilitado"
    texto_Q = "El equipo detecta la red"
    texto_R = "La red funciona en otros equipos"
    texto_S = "El equipo se conecta a la red"
    texto_T = "El equipo obtiene dirección de red"
    texto_U = "Existe acceso a Internet"

    resultado = P and Q and R and S and T and U

    if not P:
        diagnostico = "El adaptador de red está deshabilitado o no funciona correctamente."
        recomendacion = "Habilitar o revisar el adaptador de red."
    elif not Q:
        diagnostico = "El equipo no detecta la red."
        recomendacion = "Revisar Wi-Fi, cable de red, adaptador o alcance de la señal."
    elif not R:
        diagnostico = "La falla podría encontrarse en el módem, router o servicio de red."
        recomendacion = "Revisar el equipo de red y la conexión del proveedor."
    elif not S:
        diagnostico = "El equipo detecta la red, pero no logra conectarse."
        recomendacion = "Revisar contraseña, configuración y autenticación de la red."
    elif not T:
        diagnostico = "Posible problema de configuración de red."
        recomendacion = "Revisar configuración IP, DHCP o parámetros de red."
    elif not U:
        diagnostico = "El equipo está conectado a la red, pero no tiene acceso a Internet."
        recomendacion = "Revisar puerta de enlace, DNS, router o servicio de Internet."
    else:
        diagnostico = "La conexión de red funciona correctamente."
        recomendacion = "La falla puede estar relacionada con una aplicación o servicio específico."


# ----------------------------------------------------------
# PROBLEMA 5: APAGADOS, REINICIOS O BAJO RENDIMIENTO
# ----------------------------------------------------------

elif opcion_problema == "5":

    problema = "El equipo se apaga, reinicia o funciona lento"

    espacio = input(
        "¿El equipo tiene suficiente espacio de almacenamiento disponible? (si/no): "
    ).lower()

    temperatura = input(
        "¿La temperatura del equipo se mantiene en un nivel normal? (si/no): "
    ).lower()

    memoria = input(
        "¿La memoria disponible parece suficiente durante el uso? (si/no): "
    ).lower()

    energia = input(
        "¿La alimentación eléctrica o batería se mantiene estable? (si/no): "
    ).lower()

    sistema = input(
        "¿El sistema operativo inicia y responde correctamente? (si/no): "
    ).lower()

    estable = input(
        "¿El equipo puede trabajar sin apagarse, reiniciarse o congelarse? (si/no): "
    ).lower()

    # Proposiciones
    P = espacio == "si"
    Q = temperatura == "si"
    R = memoria == "si"
    S = energia == "si"
    T = sistema == "si"
    U = estable == "si"

    texto_P = "Existe suficiente espacio de almacenamiento"
    texto_Q = "La temperatura es normal"
    texto_R = "La memoria disponible es suficiente"
    texto_S = "La alimentación es estable"
    texto_T = "El sistema operativo responde correctamente"
    texto_U = "El equipo funciona de manera estable"

    resultado = P and Q and R and S and T and U

    if not P:
        diagnostico = "El bajo rendimiento puede relacionarse con falta de espacio."
        recomendacion = "Liberar espacio y revisar el estado del almacenamiento."
    elif not Q:
        diagnostico = "Posible problema de sobrecalentamiento."
        recomendacion = "Revisar ventilación, disipación, polvo y temperatura."
    elif not R:
        diagnostico = "Posible falta de memoria disponible."
        recomendacion = "Revisar consumo de memoria y procesos en ejecución."
    elif not S:
        diagnostico = "Posible inestabilidad en la alimentación eléctrica o batería."
        recomendacion = "Revisar fuente, cargador, batería y conexiones."
    elif not T:
        diagnostico = "Posible problema del sistema operativo."
        recomendacion = "Revisar procesos, actualizaciones y estado del sistema."
    elif not U:
        diagnostico = "El equipo presenta una falla de estabilidad."
        recomendacion = "Revisar temperatura, memoria, energía y almacenamiento."
    else:
        diagnostico = "No se detectó una causa evidente de bajo rendimiento."
        recomendacion = "Realizar pruebas adicionales de hardware y software."


# ----------------------------------------------------------
# OPCIÓN DE PROBLEMA NO VÁLIDA
# ----------------------------------------------------------

else:

    problema = "Problema no especificado"

    P = False
    Q = False
    R = False
    S = False
    T = False
    U = False

    texto_P = "Opción de diagnóstico válida"
    texto_Q = "Datos de alimentación disponibles"
    texto_R = "Datos de imagen disponibles"
    texto_S = "Datos de almacenamiento disponibles"
    texto_T = "Datos del sistema disponibles"
    texto_U = "Datos de red disponibles"

    resultado = False
    diagnostico = "No se seleccionó una opción de problema válida."
    recomendacion = "Ejecutar nuevamente el programa y seleccionar una opción del 1 al 5."


# ==========================================================
# 4. MOSTRAR LAS PROPOSICIONES
# ==========================================================

print("\n" + "=" * 65)
print("               VALORES DE LAS PROPOSICIONES")
print("=" * 65)

print("P -", texto_P, ":", P)
print("Q -", texto_Q, ":", Q)
print("R -", texto_R, ":", R)
print("S -", texto_S, ":", S)
print("T -", texto_T, ":", T)
print("U -", texto_U, ":", U)


# ==========================================================
# 5. NEGACIÓN
# ==========================================================

no_P = not P
no_U = not U

print("\nNEGACIÓN")
print("¬P =", no_P)
print("¬U =", no_U)


# ==========================================================
# 6. CONJUNCIÓN
# ==========================================================

conjuncion = P and Q

print("\nCONJUNCIÓN")
print("P ∧ Q =", conjuncion)


# ==========================================================
# 7. DISYUNCIÓN
# ==========================================================

disyuncion = Q or T

print("\nDISYUNCIÓN")
print("Q ∨ T =", disyuncion)


# ==========================================================
# 8. CONDICIONAL
# ==========================================================

# P → Q equivale a (NOT P) OR Q

condicional = (not P) or Q

print("\nCONDICIONAL")
print("P → Q =", condicional)


# ==========================================================
# 9. BICONDICIONAL
# ==========================================================

bicondicional = P == Q

print("\nBICONDICIONAL")
print("P ↔ Q =", bicondicional)


# ==========================================================
# 10. EXPRESIÓN CON PARÉNTESIS
# ==========================================================

# El diagnóstico general considera:
#
# ((P ∧ Q ∧ R) ∧ (S ∧ T ∧ U))
#
# Todas las condiciones revisadas deben ser verdaderas
# para considerar que el área diagnosticada funciona
# correctamente.

resultado_logico = ((P and Q and R) and (S and T and U))

print("\nEXPRESIÓN CON PARÉNTESIS")
print("((P ∧ Q ∧ R) ∧ (S ∧ T ∧ U)) =", resultado_logico)


# ==========================================================
# 11. BICONDICIONAL DEL DIAGNÓSTICO
# ==========================================================

diagnostico_coherente = resultado == resultado_logico

print("\nBICONDICIONAL DEL DIAGNÓSTICO")
print("Resultado ↔ Expresión lógica =", diagnostico_coherente)


# ==========================================================
# 12. GENERACIÓN DEL REPORTE
# ==========================================================

numero_reporte = random.randint(100000, 999999)

print("\n" + "=" * 65)
print("                 REPORTE DE DIAGNÓSTICO")
print("=" * 65)

print("Número de reporte :", numero_reporte)
print("Usuario           :", nombre_usuario)
print("Dirección         :", direccion_usuario)
print("Tipo de equipo    :", tipo_equipo)
print("Problema reportado:", problema)

print("\nDIAGNÓSTICO:")
print(diagnostico)

print("\nRECOMENDACIÓN:")
print(recomendacion)

print("\nRESULTADO LÓGICO:")
if resultado_logico:
    print("El área evaluada NO presenta fallas según las respuestas.")
else:
    print("El área evaluada PRESENTA una posible falla.")

if diagnostico_coherente:
    print("El diagnóstico coincide con la expresión proposicional.")
else:
    print("ADVERTENCIA: Revisar los valores del diagnóstico.")

print("\n" + "=" * 65)
print("                 FIN DEL REPORTE")
print("=" * 65)
