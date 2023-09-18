import tkinter as tk
from tkinter import messagebox
import random
import networkx as nx
import matplotlib.pyplot as plt

"""
Registro de cambios

    Front
        Widgets ahora usan coords relativs
        Implementacion de paleta
        Cambio de cursor en widgets

    Estilo:
        Cambio de nombre de variables
    Funcional:
        La matriz se limpia antes de generarse

Por realizar
    Funcionales
        resize a tabla

    Estilo
        refactorizar code

Utilidades
- Colores tk    https://www.plus2net.com/python/tkinter-colors.php
- Paletas       https://mybrandnewlogo.com/es/generador-de-paleta-de-colores
- Cursores tk   https://www.tutorialspoint.com/python/tk_cursors.htm
- Fonts         https://docs.python.org/es/3.9/library/tkinter.font.html

"""


def generar_matriz(n):
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = random.randint(1, 100)
            matriz[j][i] = matriz[i][j]
    return matriz


def calcular_distancia_total(camino, distancias):
    distancia_total = 0
    for i in range(len(camino) - 1):
        distancia_total += distancias[camino[i]][camino[i + 1]]
    return distancia_total


def resolver_tsp():
    n = int(entry_n.get())
    if n < 5 or n > 15:
        messagebox.showerror("Error", "El valor de 'n' debe estar entre 5 y 15.")
        return

    distancias = []
    for i in range(n):
        fila = []
        for j in range(n):
            valor = entry_matrix[i][j].get()
            fila.append(int(valor))
        distancias.append(fila)

    lbl_result.config(text="Calculando...")
    root.update_idletasks()

    ciudad_inicial = 0  # Puedes cambiar la ciudad de inicio si lo deseas
    visitadas = [False] * n
    camino = [ciudad_inicial]
    visitadas[ciudad_inicial] = True

    for _ in range(n - 1):
        ciudad_actual = camino[-1]
        ciudad_mas_cercana = None
        distancia_minima = float("inf")

        for ciudad in range(n):
            if not visitadas[ciudad] and distancias[ciudad_actual][ciudad] < distancia_minima:
                ciudad_mas_cercana = ciudad
                distancia_minima = distancias[ciudad_actual][ciudad]

        camino.append(ciudad_mas_cercana)
        visitadas[ciudad_mas_cercana] = True

    camino.append(ciudad_inicial)
    distancia_total = calcular_distancia_total(camino, distancias)

    lbl_result.config(text=f"Ciclo hamiltoniano:\n {camino}\nDistancia total: \n{distancia_total}", bg=palet[0])

    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distancias[i][j])
    pos = nx.spring_layout(G)  # Configura la posición de los nodos
    nx.draw(G, pos, with_labels=True, node_size=500, font_size=10, font_color="black")
    etiquetas_aristas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_aristas)
    plt.show()


def generar_matriz_y_mostrar():
    limpiar_matriz()
    n = int(entry_n.get())
    distancias = generar_matriz(n)

    for i in range(n):
        for j in range(n):
            entry_matrix[i][j].delete(0, tk.END)
            entry_matrix[i][j].insert(0, str(distancias[i][j]))


def limpiar_matriz():
    for i in range(len(entry_matrix)):
        for j in range(len(entry_matrix[i])):
            entry_matrix[i][j].delete(0, tk.END)


def resizeMatriz(*entry_matrix):
    a = []
    for i in range(10):  # Limitado a 15 filas para simplificar la interfaz
        fila_entradas = []
        for j in range(10):  # Limitado a 15 columnas para simplificar la interfaz
            entrada = tk.Entry(matrix_frame, width=3)
            entrada.grid(row=i, column=j)
            fila_entradas.append(entrada)
        a.append(fila_entradas)
    entry_matrix = a


def cerrar_programa():
    root.destroy()


root = tk.Tk()

# paleta : https://paletadecolores.com.mx/paleta/352640/92394b/a9767a/d1b4a2/f1f2ce/
palet = ["#352640", "#92394b", "#a9767a", "#d1b4a2", "#f1f2ce"]
fonts = ["NORMAL", "ITALIC", "ROMAN", "BOLD"]  # lbl ,matriz , none, button
aims = ["heart", "tcross", "tcross", "target"]  # lbl, matriz, txt, button

root.frame()
root.configure(bg=palet[0], cursor=aims[0])
root.title("Solucionador del PAV")
root.geometry("640x450")

lbl_n = tk.Label(root, bg=palet[0], fg=palet[-1], font=fonts[0], text="Ingrese la cantidad de ciudades (entre 5 y 15):")
lbl_n.pack()
lbl_n.place(relx=0.01, rely=0.05)

entry_n = tk.Entry(root, bg=palet[1], fg=palet[-1], width=3, cursor=aims[2])
entry_n.pack()
entry_n.place(relx=0.55, rely=0.05)

matrix_frame = tk.Frame(root)
matrix_frame.pack()
matrix_frame.place(relx=0.02, rely=0.15)

entry_matrix = []
for i in range(15):  # Limitado a 15 filas para simplificar la interfaz
    fila_entradas = []
    for j in range(15):  # Limitado a 15 columnas para simplificar la interfaz
        entrada = tk.Entry(matrix_frame, width=3, bg=palet[1], fg=palet[4], cursor=aims[1], font=fonts[1])
        entrada.grid(row=i, column=j)
        fila_entradas.append(entrada)
    entry_matrix.append(fila_entradas)

dy_button = 0.10
x_button = 0.78
y_button = 0.05

bnt_generate = tk.Button(root, fg=palet[-1], bg=palet[2], font=fonts[3], cursor=aims[3], text="Generar Matriz",
                         command=generar_matriz_y_mostrar)
bnt_generate.pack()
bnt_generate.place(relx=x_button, rely=y_button)

bnt_clean = tk.Button(root, fg=palet[-1], bg=palet[2], font=fonts[3], cursor=aims[3], text="Limpiar Matriz",
                      command=limpiar_matriz)
bnt_clean.pack()
bnt_clean.place(relx=x_button, rely=y_button + dy_button * 1)

bnt_solve = tk.Button(root, fg=palet[-1], bg=palet[2], font=fonts[3], cursor=aims[3], text="Resolver PAV",
                      command=resolver_tsp)
bnt_solve.pack()
bnt_solve.place(relx=x_button, rely=y_button + dy_button * 2)

lbl_result = tk.Label(root, fg=palet[-1], bg=palet[0], font=fonts[0], cursor=aims[0], text="", wraplength=300)
lbl_result.pack()
lbl_result.place(relx=x_button, rely=y_button + dy_button * 5)

btn_close = tk.Button(root, fg=palet[-1], bg=palet[1], font=fonts[3], cursor=aims[3], text="Cerrar Programa",
                      command=cerrar_programa)
btn_close.pack()
btn_close.place(relx=x_button, rely=y_button + dy_button * 3)

root.mainloop()
