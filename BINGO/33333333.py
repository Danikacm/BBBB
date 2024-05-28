import tkinter as tk
from tkinter import messagebox, PhotoImage, simpledialog
import pygame
import time
import pyttsx3
from bingo_database import BingoDatabase
from bingo_ui import BingoUI
from bingo_board_generator import BingoBoardGenerator

class SegundaVentana:
    def __init__(self, ventana_principal):
        pygame.mixer.music.stop()
        ventana_principal.destroy()

        self.segunda_ventana = tk.Tk()
        self.segunda_ventana.title("Segunda Pantalla")
        self.segunda_ventana.geometry("800x600")

        self.fondo_imagen = PhotoImage(file="imagenes/fondo1.2.png")
        self.fondo_label = tk.Label(self.segunda_ventana, image=self.fondo_imagen)
        self.fondo_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.menu_frame = tk.Frame(self.segunda_ventana, bg="red", bd=2)
        self.menu_frame.place(relx=0, rely=1, anchor="sw")

        self.pausar_button = tk.Button(self.menu_frame, text="Pausar", command=self.pausar)
        self.pausar_button.pack(side="left", padx=5, pady=5)

        self.continuar_button = tk.Button(self.menu_frame, text="Iniciar", command=self.continuar)
        self.continuar_button.pack(side="left", padx=5, pady=5)

        self.contar_button = tk.Button(self.menu_frame, text="Contar", command=self.mostrar_conteo)
        self.contar_button.pack(side="left", padx=5, pady=5)

        self.iniciar_voz_button = tk.Button(self.menu_frame, text="Iniciar Voz", command=self.iniciar_voz)
        self.iniciar_voz_button.pack(side="left", padx=5, pady=5)

        self.detener_voz_button = tk.Button(self.menu_frame, text="Detener Voz", command=self.detener_voz)
        self.detener_voz_button.pack(side="left", padx=5, pady=5)

        self.generar_tablero_button = tk.Button(self.menu_frame, text="Generar Tablero", command=self.generar_tablero)
        self.generar_tablero_button.pack(side="left", padx=5, pady=5)

        self.ajustar_velocidad_button = tk.Button(self.menu_frame, text="Ajustar Velocidad", command=self.ajustar_velocidad)
        self.ajustar_velocidad_button.pack(side="left", padx=5, pady=5)

        self.numero_actual = 0
        self.velocidad_lanzamiento = 3000  # Velocidad predeterminada

        self.balotas = self.generar_balotas()
        self.numeros_mostrados = []

        self.engine = pyttsx3.init()
        self.voz_activa = False

        self.segunda_ventana.mainloop()

    def generar_balotas(self):
        balotas = set()
        letras = ['B', 'I', 'N', 'G', 'O']
        for letra in letras:
            for _ in range(15 if letra != 'G' else 5):
                numero = self.generar_numero(letra)
                while (letra, numero) in balotas:
                    numero = self.generar_numero(letra)
                balotas.add((letra, numero))
        return list(balotas)

    def mostrar_siguiente_numero(self):
        if self.numero_actual >= len(self.balotas):
            messagebox.showinfo("Fin del juego", "Se han mostrado todos los números.")
            return

        letra, numero = self.balotas[self.numero_actual]

        self.numero_etiqueta = tk.Label(self.segunda_ventana, text=f"{letra}{numero}", font=("Arial", 65), bg="white")
        self.numero_etiqueta.place(relx=0.21, rely=0.55, anchor="center")

        self.numeros_mostrados.append(f"{letra}{numero}")

        self.numero_actual += 1

        self.siguiente_id = self.segunda_ventana.after(self.velocidad_lanzamiento, self.mostrar_siguiente_numero)

        if self.voz_activa:
            self.decir_numero_en_voz(letra, numero)

    def pausar(self):
        self.segunda_ventana.after_cancel(self.siguiente_id)

    def continuar(self):
        self.mostrar_siguiente_numero()

    def mostrar_conteo(self):
        numeros_mostrados_texto = "\n".join(self.numeros_mostrados)
        messagebox.showinfo("Números mostrados", f"Números mostrados hasta ahora:\n{numeros_mostrados_texto}")

    def generar_numero(self, letra):
        milliseconds = int(round(time.time() * 1000))
        seed = ((milliseconds * 9301) + 49297) % 233280
        if letra == 'B':
            return seed % 15 + 1
        elif letra == 'I':
            return seed % 15 + 16
        elif letra == 'N':
            return seed % 15 + 31
        elif letra == 'G':
            return seed % 15 + 46
        elif letra == 'O':
            return seed % 15 + 61

    def iniciar_voz(self):
        self.voz_activa = True

    def detener_voz(self):
        self.voz_activa = False

    def decir_numero_en_voz(self, letra, numero):
        self.engine.say(f"{letra} {numero}")
        self.engine.runAndWait()

    def generar_tablero(self):
        generator = BingoBoardGenerator()
        board = generator.generate_board()
        print("Tablero generado:")
        for row in board:
            print(row)

    def ajustar_velocidad(self):
        velocidad = simpledialog.askinteger("Ajustar Velocidad", "Ingrese la velocidad deseada (en milisegundos):", parent=self.segunda_ventana)
        if velocidad is not None:
            self.velocidad_lanzamiento = velocidad
            self.pausar()
            self.continuar()

def mostrar_segunda_pantalla(ventana_principal):
    SegundaVentana(ventana_principal)

def Boton_base():
    db = BingoDatabase("bingo.db")
    db.create_tables()
    db.close_connection()

    root = tk.Tk()
    app = BingoUI(root)
    root.mainloop()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.music.load("Musiquita/PEDRO.PEDRO.mp3") 
    pygame.mixer.music.play(-1)

    ventana_principal = tk.Tk()
    ventana_principal.title("Pantalla Principal")
    ventana_principal.geometry("1000x500")

    imagen_fondo_principal = PhotoImage(file="imagenes/fondo1.png")
    canvas = tk.Canvas(ventana_principal, width=300, height=400)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=imagen_fondo_principal)

    boton_empezar = tk.Button(ventana_principal, text="Empezar", command=lambda: mostrar_segunda_pantalla(ventana_principal),bg="red")
    boton_empezar.place(relx=0.5, rely=0.9, anchor="center")

    boton_ejecutar = tk.Button(ventana_principal, text="Añadir usuario", command=Boton_base, bg="red")
    boton_ejecutar.place(relx=0.3, rely=0.9, anchor="center")

    ventana_principal.mainloop()
