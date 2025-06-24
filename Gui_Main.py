import tkinter as tk
from tkinter import messagebox

import gramatica_module as gramatica
import tramas_module as tramas


def ejecutar_gramatica():
    g = gramatica.ingresar_gramatica()
    while True:
        opcion = messagebox.askquestion(
            "Gramática",
            "¿Deseas verificar una frase?\n(Sí para verificar, No para generar frases)"
        )
        if opcion == 'yes':
            frase = input("Ingrese la frase (separada por espacios): ")
            pertenece = gramatica.pertenece_frase(frase, g)
            print("\nResultado: La frase",
                  "pertenece a la gramática." if pertenece else "no pertenece.")
        else:
            frases = gramatica.generar_frases(g)
            print("\nFrases generadas:")
            for i, f in enumerate(frases, 1):
                print(f"{i}. {f}")
        cont = messagebox.askyesno("Gramática", "¿Deseas hacer otra acción?")
        if not cont:
            break


def ejecutar_tramas():
    lista = tramas.ingresar_lista_validacion()
    tramas_ingresadas = tramas.ingresar_tramas()
    resultados = tramas.validar_tramas(tramas_ingresadas, lista)
    print("\nResultados por trama:")
    for i, (t, estado) in enumerate(resultados, 1):
        print(f"Trama {i}: {estado}")
    tramas.evaluar_transmision(resultados)


def main():
    root = tk.Tk()
    root.title("Proyecto Final DII - Menú Principal")
    root.geometry("400x220")
    root.configure(bg="#f0f0f0")

    titulo = tk.Label(root, text="Sistema de Gramática y Tramas", font=("Arial", 14, "bold"), bg="#f0f0f0")
    titulo.pack(pady=15)

    boton_gramatica = tk.Button(
        root, text="🔤 Módulo Gramática", width=30, height=2,
        command=ejecutar_gramatica, bg="#cce5ff", fg="black", font=("Arial", 10)
    )
    boton_gramatica.pack(pady=5)

    boton_tramas = tk.Button(
        root, text="📡 Módulo Tramas (FSM)", width=30, height=2,
        command=ejecutar_tramas, bg="#d5f5e3", fg="black", font=("Arial", 10)
    )
    boton_tramas.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
