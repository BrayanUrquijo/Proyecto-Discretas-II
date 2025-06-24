import tkinter as tk
from tkinter import messagebox

def ingresar_lista_validacion_entry(entries, output):
    lista = []
    for i, entry in enumerate(entries):
        bits = entry.get().strip().replace(' ', '')
        if len(bits) != 4 or any(b not in '01' for b in bits):
            output.insert('end', f"⚠️ Línea {i+1} inválida: '{bits}' no es un grupo de 4 bits.\n")
            continue
        lista.append(int(bits, 2))
    return lista

def ingresar_tramas_entry(entries, output):
    tramas = []
    for i, entry in enumerate(entries):
        bits = entry.get().strip().replace(' ', '')
        if len(bits) != 32 or any(b not in '01' for b in bits):
            output.insert('end', f"⚠️ Trama {i+1} inválida: debe tener 32 bits.\n")
            continue
        tramas.append(bits)
    return tramas

def validar_tramas(tramas, lista_validacion):
    resultados = []
    for i, trama in enumerate(tramas):
        sub_bits = trama[9:14]  # bits 10 a 14 según la rúbrica
        valor = int(sub_bits, 2)
        if i >= len(lista_validacion):
            resultados.append((trama, 'Invalida'))
            continue
        suma = valor + lista_validacion[i]
        mult3 = valor % 3 == 0
        mult5 = suma % 5 == 0
        estado = 'Valida' if mult3 and mult5 else 'Invalida'
        resultados.append((trama, estado))
    return resultados

def evaluar_transmision_gui(resultados, output):
    total = len(resultados)
    invalidas = sum(1 for _, estado in resultados if estado == 'Invalida')
    error = (invalidas / total) * 100 if total else 0
    output.insert('end', f"\n📊 Total de tramas: {total}\n")
    output.insert('end', f"❌ Tramas inválidas: {invalidas} ({error:.2f}%)\n")
    if error < 20:
        output.insert('end', "✅ Transmisión correcta.\n")
    else:
        output.insert('end', "⚠️ Transmisión con errores (>20%).\n")

def main():
    root = tk.Tk()
    root.title("🧪 Evaluador de Tramas (FSM)")
    root.geometry("720x820")
    root.configure(bg="#f4f4f4")

    tk.Label(root, text="🔢 Lista de validación (5 valores de 4 bits)", font=('Arial', 12, 'bold'), bg="#f4f4f4").pack(pady=5)
    valid_entries = []
    for _ in range(5):
        e = tk.Entry(root, width=10, justify='center', font=('Consolas', 12))
        e.pack(pady=2)
        valid_entries.append(e)

    tk.Label(root, text="💾 Tramas (5 tramas de 32 bits)", font=('Arial', 12, 'bold'), bg="#f4f4f4").pack(pady=(15, 0))
    trama_entries = []
    for _ in range(5):
        e = tk.Entry(root, width=45, justify='center', font=('Consolas', 12))
        e.pack(pady=2)
        trama_entries.append(e)

    output = tk.Text(root, height=20, width=85, borderwidth=2, relief='solid', bg='#ffffff')
    output.pack(padx=10, pady=10)

    def procesar():
        output.delete('1.0', 'end')
        lista = ingresar_lista_validacion_entry(valid_entries, output)
        tramas = ingresar_tramas_entry(trama_entries, output)
        if not lista or not tramas:
            output.insert('end', "⚠️ Datos insuficientes para evaluar.\n")
            return
        resultados = validar_tramas(tramas, lista)
        output.insert('end', "🔍 Resultados por trama:\n------------------------------\n")
        for i, (_, estado) in enumerate(resultados, 1):
            output.insert('end', f"Trama {i}: {'✅' if estado == 'Valida' else '❌'} {estado}\n")
        output.insert('end', "------------------------------\n")
        evaluar_transmision_gui(resultados, output)

    tk.Button(root, text="🧾 Evaluar Transmisión", command=procesar, font=('Arial', 11, 'bold'), bg="#d0f0c0").pack(pady=10)
    tk.Button(root, text="⏹️ Salir", command=lambda: [root.destroy(), __import__('main').main()], font=('Arial', 11), bg="#ffcccc").pack(pady=5)

    root.mainloop()
