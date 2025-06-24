
import tkinter as tk
from tkinter import messagebox

import gramatica_module as gramatica
import tramas_module as tramas

def ejecutar_gramatica(root):
    root.destroy()
    gramatica.main()

def ejecutar_tramas(root):
    root.destroy()
    tramas.main()

def main():
    root = tk.Tk()
    root.title("Proyecto Final DII - Menú Principal")
    root.geometry("400x220")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="Sistema de Gramática y Tramas", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)

    tk.Button(
        root,
        text="Módulo Gramática",
        width=30,
        height=2,
        bg="#cce5ff",
        command=lambda: ejecutar_gramatica(root)
    ).pack(pady=5)

    tk.Button(
        root,
        text="Módulo Tramas (FSM)",
        width=30,
        height=2,
        bg="#d5f5e3",
        command=lambda: ejecutar_tramas(root)
    ).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
