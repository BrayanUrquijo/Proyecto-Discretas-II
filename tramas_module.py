def ingresar_lista_validacion():
    """
    Pide al usuario ingresar una lista de validación compuesta por valores enteros
    entre 0 y 15. Cada valor se construye con 4 bits ingresados uno a uno.
    Devuelve una lista de enteros.
    """
    lista = []
    print("Ingrese la cantidad de elementos de la lista de validación (max 20):")
    cantidad = int(input())
    for i in range(cantidad):
        bits = []
        print(f"Elemento {i+1} (4 bits):")
        while len(bits) < 4:
            bit = input(f"  Bit {len(bits)+1}: ")
            if bit not in ('0', '1'):
                print("  Solo se permiten 0 o 1")
                continue
            bits.append(bit)
        valor = int(''.join(bits), 2)
        lista.append(valor)
    return lista


def ingresar_tramas():
    """
    Permite ingresar entre 5 y 20 tramas de 32 bits, bit por bit.
    Devuelve una lista de cadenas de bits.
    """
    tramas = []
    print("Ingrese la cantidad de tramas (entre 5 y 20):")
    n = int(input())
    for i in range(n):
        bits = []
        print(f"Trama {i+1} (32 bits):")
        while len(bits) < 32:
            bit = input(f"  Bit {len(bits)+1}: ")
            if bit not in ('0', '1'):
                print("  Solo se permiten 0 o 1")
                continue
            bits.append(bit)
        tramas.append(''.join(bits))
    return tramas


def validar_tramas(tramas, lista_validacion):
    """
    Valida cada trama según las siguientes condiciones:
    - Se extraen los bits 10 al 14 (inclusive) de cada trama.
    - Se convierten en entero y se verifica:
        a) Si es múltiplo de 3.
        b) Si su suma con el valor correspondiente de la lista es múltiplo de 5.
    Devuelve lista de tuplas: (trama, 'Valida' o 'Invalida')
    """
    resultados = []
    for i, trama in enumerate(tramas):
        if len(trama) != 32:
            resultados.append((trama, 'Invalida'))
            continue
        sub_bits = trama[9:14]  # bits 10 a 14
        valor = int(sub_bits, 2)
        if i >= len(lista_validacion):
            resultados.append((trama, 'Invalida'))
            continue
        suma = valor + lista_validacion[i]
        if valor % 3 == 0 and suma % 5 == 0:
            resultados.append((trama, 'Valida'))
        else:
            resultados.append((trama, 'Invalida'))
    return resultados


def evaluar_transmision(resultados):
    """
    Evalúa si la transmisión es válida según la cantidad de tramas inválidas.
    Si el porcentaje de error es menor al 20%, la transmisión es válida.
    """
    total = len(resultados)
    invalidas = sum(1 for _, estado in resultados if estado == 'Invalida')
    error = (invalidas / total) * 100
    print(f"\nTotal tramas: {total}")
    print(f"Tramas inválidas: {invalidas} ({error:.2f}%)")
    if error < 20:
        print("\nTransmisión correcta.")
    else:
        print("\nTransmisión con errores (>20%).")
