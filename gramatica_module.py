import random


def ingresar_gramatica():
    """
    Solicita al usuario ingresar la gramática:
    - No terminales (separados por espacios)
    - Terminales (separados por espacios)
    - Símbolo inicial
    - Producciones (en formato 'A -> a B'
      o 'A -> a')
    Devuelve un diccionario con:
    {
      'V': set de no terminales,
      'T': set de terminales,
      'S': símbolo inicial,
      'P': dict de producciones
    }
    """
    no_terminales = input("Ingrese los no terminales (separados por espacios): ").split()
    terminales = input("Ingrese los terminales (separados por espacios): ").split()
    S = input("Ingrese el símbolo inicial: ").strip()
    P = {}
    print("Ingrese las producciones (una por línea) en formato 'A -> a B'. Escriba 'fin' para terminar:")
    while True:
        linea = input().strip()
        if linea.lower() == 'fin':
            break
        if '->' not in linea:
            print("Formato incorrecto. Use 'NT -> X Y ...'")
            continue
        left, right = linea.split('->')
        NT = left.strip()
        cuerpo = right.strip().split()
        P.setdefault(NT, []).append(cuerpo)
    return {'V': set(no_terminales), 'T': set(terminales), 'S': S, 'P': P}


def pertenece_frase(frase, gramatica, max_profundidad=10):
    """
    Determina si la cadena de terminales 'frase' (string) pertenece a la gramática
    mediante derivación recursiva (backtracking) limitada por max_profundidad.
    Devuelve True o False.
    """
    # Convertir frase en lista de símbolos
    target = frase.split()

    def backtrack(sentencia, profundidad):
        # Si superamos profundidad máxima, abandonamos
        if profundidad > max_profundidad:
            return False
        # Si la sentencia es igual a target y solo terminales, aceptamos
        if sentencia == target and all(sym in gramatica['T'] for sym in sentencia):
            return True
        # Si la sentencia solo contiene terminales pero no es target, no sigue
        if all(sym in gramatica['T'] for sym in sentencia):
            return False
        # Buscar primer no terminal en la sentencia
        for idx, sym in enumerate(sentencia):
            if sym in gramatica['V']:
                # Expandir con cada producción
                for prod in gramatica['P'].get(sym, []):
                    nueva = sentencia[:idx] + prod + sentencia[idx+1:]
                    if backtrack(nueva, profundidad + 1):
                        return True
                # Si ninguna producción funcionó, terminar
                return False
        return False

    # Iniciar desde el símbolo inicial
    return backtrack([gramatica['S']], 0)


def generar_frases(gramatica, n=10, max_profundidad=10):
    """
    Genera 'n' frases válidas de la gramática usando expansiones aleatorias.
    Limita la profundidad para evitar bucles.
    Devuelve lista de strings (frases).
    """
    frases = []
    intentos = 0
    while len(frases) < n and intentos < n * 5:
        intentos += 1
        sentencia = [gramatica['S']]
        profundidad = 0
        # Expandir hasta solo terminales o agotar profundidad
        while any(sym in gramatica['V'] for sym in sentencia) and profundidad < max_profundidad:
            # Elegir un no terminal al azar
            idx = next(i for i,sym in enumerate(sentencia) if sym in gramatica['V'])
            sym = sentencia[idx]
            producciones = gramatica['P'].get(sym, [])
            if not producciones:
                break
            prod = random.choice(producciones)
            sentencia = sentencia[:idx] + prod + sentencia[idx+1:]
            profundidad += 1
        # Si resultó una frase válida (solo terminales)
        if all(sym in gramatica['T'] for sym in sentencia):
            frases.append(' '.join(sentencia))
    return frases
