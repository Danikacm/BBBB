import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from bingo_database import BingoDatabase

class BingoUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bingo Database")

        self.db = BingoDatabase("bingo.db")
        self.db.create_tables()

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label = tk.Label(self.frame, text="Bingo Database", font=("Arial", 18))
        self.label.grid(row=0, columnspan=2, pady=10)

        self.add_user_button = tk.Button(self.frame, text="Agregar Usuario", command=self.add_user)
        self.add_user_button.grid(row=1, column=0, padx=5, pady=5)

        self.update_credits_button = tk.Button(self.frame, text="Actualizar Créditos", command=self.update_credits)
        self.update_credits_button.grid(row=1, column=1, padx=5, pady=5)

    def add_user(self):
        nombre = simpledialog.askstring("Agregar Usuario", "Ingrese el nombre del usuario:")
        creditos = simpledialog.askinteger("Agregar Usuario", "Ingrese los créditos del usuario:")
        if nombre and creditos is not None:
            self.db.insert_usuario(nombre, creditos)
            messagebox.showinfo("Éxito", "Usuario agregado correctamente.")

    def update_credits(self):
        nombre = simpledialog.askstring("Actualizar Créditos", "Ingrese el nombre del usuario:")
        if nombre:
            nuevos_creditos = simpledialog.askinteger("Actualizar Créditos", "Ingrese los nuevos créditos:")
            if nuevos_creditos is not None:
                self.db.update_creditos(nombre, nuevos_creditos)
                messagebox.showinfo("Éxito", "Créditos actualizados correctamente.")

def main():
    root = tk.Tk()
    app = BingoUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()