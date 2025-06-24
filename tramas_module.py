
import tkinter as tk
from tkinter import messagebox, scrolledtext

def ingresar_lista_validacion_gui(entry_box, output):
    lista = []
    bits_text = entry_box.get('1.0', 'end').strip().splitlines()
    for line in bits_text:
        bits = line.strip().replace(' ', '')
        if len(bits) != 4 or any(b not in '01' for b in bits):
            output.insert('end', f"Error: '{line}' no es un grupo válido de 4 bits\n")
            continue
        valor = int(bits, 2)
        lista.append(valor)
    return lista

def ingresar_tramas_gui(entry_box, output):
    tramas = []
    trama_lines = entry_box.get('1.0', 'end').strip().splitlines()
    for line in trama_lines:
        trama = line.strip().replace(' ', '')
        if len(trama) != 32 or any(b not in '01' for b in trama):
            output.insert('end', f"Error: Trama inválida '{line}'\n")
            continue
        tramas.append(trama)
    return tramas

def validar_tramas(tramas, lista_validacion):
    resultados = []
    for i, trama in enumerate(tramas):
        if len(trama) != 32:
            resultados.append((trama, 'Invalida'))
            continue
        sub_bits = trama[9:14]
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

def evaluar_transmision_gui(resultados, output):
    total = len(resultados)
    invalidas = sum(1 for _, estado in resultados if estado == 'Invalida')
    error = (invalidas / total) * 100 if total else 0
    output.insert('end', f"\nTotal tramas: {total}\n")
    output.insert('end', f"Tramas inválidas: {invalidas} ({error:.2f}%)\n")
    if error < 20:
        output.insert('end', "Transmisión correcta.\n")
    else:
        output.insert('end', "Transmisión con errores (>20%).\n")

def main():
    root = tk.Tk()
    root.title("Módulo Tramas (FSM)")
    root.geometry("700x700")

    tk.Label(root, text="Lista de validación (una línea por valor, 4 bits):").pack(anchor='w', padx=10, pady=(10, 0))
    valid_box = scrolledtext.ScrolledText(root, width=60, height=6)
    valid_box.pack(padx=10)

    tk.Label(root, text="Tramas (una por línea, 32 bits):").pack(anchor='w', padx=10, pady=(10, 0))
    tramas_box = scrolledtext.ScrolledText(root, width=60, height=10)
    tramas_box.pack(padx=10)

    output = scrolledtext.ScrolledText(root, width=80, height=15, state='normal')
    output.pack(padx=10, pady=10)

    def procesar():
        output.delete('1.0', 'end')
        lista = ingresar_lista_validacion_gui(valid_box, output)
        tramas = ingresar_tramas_gui(tramas_box, output)
        if not lista or not tramas:
            output.insert('end', "Datos insuficientes para evaluar.\n")
            return
        resultados = validar_tramas(tramas, lista)
        for i, (trama, estado) in enumerate(resultados, 1):
            output.insert('end', f"Trama {i}: {estado}\n")
        evaluar_transmision_gui(resultados, output)

    btn = tk.Button(root, text="Evaluar Transmisión", command=procesar)
    btn.pack(pady=10)
    tk.Button(root, text="Salir", command=lambda: [root.destroy(), __import__('main').main()]).pack(pady=5)



    root.mainloop()
