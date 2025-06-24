
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import random

def construir_gramatica(no_terminales_str, terminales_str, S_str, producciones_str):
    V = set(no_terminales_str.split())
    T = set(terminales_str.split())
    S = S_str.strip()
    P = {}
    for line in producciones_str.splitlines():
        line = line.strip()
        if not line or '->' not in line:
            continue
        left, right = line.split('->', 1)
        NT = left.strip()
        cuerpo = right.strip().split()
        P.setdefault(NT, []).append(cuerpo)
    return {'V': V, 'T': T, 'S': S, 'P': P}

def pertenece_frase(frase_str, gramatica, max_profundidad=10):
    target = frase_str.split()

    def backtrack(sentencia, profundidad):
        if profundidad > max_profundidad:
            return False
        if sentencia == target and all(sym in gramatica['T'] for sym in sentencia):
            return True
        if all(sym in gramatica['T'] for sym in sentencia):
            return False
        for idx, sym in enumerate(sentencia):
            if sym in gramatica['V']:
                for prod in gramatica['P'].get(sym, []):
                    nueva = sentencia[:idx] + prod + sentencia[idx+1:]
                    if backtrack(nueva, profundidad + 1):
                        return True
                return False
        return False

    return backtrack([gramatica['S']], 0)

def generar_frases(gramatica, n=10, max_profundidad=10):
    frases = []
    intentos = 0
    while len(frases) < n and intentos < n * 5:
        intentos += 1
        sentencia = [gramatica['S']]
        profundidad = 0
        while any(sym in gramatica['V'] for sym in sentencia) and profundidad < max_profundidad:
            idx = next(i for i, s in enumerate(sentencia) if s in gramatica['V'])
            nt = sentencia[idx]
            prods = gramatica['P'].get(nt, [])
            if not prods:
                break
            prod = random.choice(prods)
            sentencia = sentencia[:idx] + prod + sentencia[idx+1:]
            profundidad += 1
        if all(sym in gramatica['T'] for sym in sentencia):
            frases.append(' '.join(sentencia))
    return frases

def main():
    root = tk.Tk()
    root.title("Módulo Gramática")
    root.geometry("600x700")

    tk.Label(root, text="No terminales (espacio separado):").pack(anchor='w', padx=10, pady=(10,0))
    nt_entry = tk.Entry(root, width=60)
    nt_entry.pack(padx=10)

    tk.Label(root, text="Terminales (espacio separado):").pack(anchor='w', padx=10, pady=(10,0))
    t_entry = tk.Entry(root, width=60)
    t_entry.pack(padx=10)

    tk.Label(root, text="Símbolo inicial:").pack(anchor='w', padx=10, pady=(10,0))
    s_entry = tk.Entry(root, width=20)
    s_entry.pack(padx=10)

    tk.Label(root, text="Producciones (una por línea, formato 'A -> a B'):").pack(anchor='w', padx=10, pady=(10,0))
    prod_text = scrolledtext.ScrolledText(root, width=70, height=12)
    prod_text.pack(padx=10, pady=(0,10))

    output = scrolledtext.ScrolledText(root, width=70, height=10, state='disabled')
    output.pack(padx=10, pady=(10,10))

    def load_and_process(mode):
        g = construir_gramatica(nt_entry.get(), t_entry.get(), s_entry.get(), prod_text.get('1.0', 'end'))
        if mode == 'verify':
            frase = simpledialog.askstring("Verificar frase", "Ingrese la frase (separada por espacios):")
            if frase:
                res = pertenece_frase(frase, g)
                msg = f"Frase '{frase}': {'PERTENECE' if res else 'NO PERTENECE'}"
                output.config(state='normal')
                output.insert('end', msg + "\n")
                output.config(state='disabled')
        else:
            frases = generar_frases(g, n=10)
            output.config(state='normal')
            output.insert('end', "Frases generadas:\n")
            for i, f in enumerate(frases, 1):
                output.insert('end', f"{i}. {f}\n")
            output.config(state='disabled')

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Verificar frase", command=lambda: load_and_process('verify')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Generar frases", command=lambda: load_and_process('generate')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Salir", command=lambda: [root.destroy(), __import__('main').main()]).pack(side='left', padx=5)


    root.mainloop()

if __name__ == "__main__":
    main()
