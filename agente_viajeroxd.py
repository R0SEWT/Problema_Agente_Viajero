import tkinter as tk  # front
import random  # matriz aleatoria
import time
import networkx as nx  # armas el grafo
import matplotlib.pyplot as plt  # muestras
from itertools import permutations  # para el FB
from tkinter import messagebox

import consultasAPI

"""

Parte mastemastica, documentar principalmente esta ps 

"""


def generar_matriz(n):
    matriz = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matriz[i][j] = random.randint(1, 10)
            matriz[j][i] = matriz[i][j]
    return matriz


def arreglar_matriz(n):
    error = False
    # recorremos la matriz hasta la diagonal exclusive
    for i in range(n):
        for j in range(i, n - 1):
            if entry_matrix[i][j].get() != entry_matrix[j][i].get():
                entry_matrix[j][i].delete(0, tk.END)
                entry_matrix[j][i].insert(0, entry_matrix[i][j].get())
                error = True

    if error:
        messagebox.showerror("Advertencia", "Se han modificado los valores de la matriz de adyacencia")


def get_distancias_matriz(n):
    arreglar_matriz(n)

    distancias = []
    for i in range(n):
        fila = []
        for j in range(n):
            valor = entry_matrix[i][j].get()
            fila.append(int(valor))
        distancias.append(fila)
    return distancias


def calcular_distancia_total(ruta, distancias):
    distancia_acumulada = 0
    for i in range(len(ruta) - 1):
        distancia_acumulada += distancias[ruta[i]][ruta[i + 1]]
    distancia_acumulada += distancias[ruta[-1]][ruta[0]]  # Regresa a la ciudad inicial
    return distancia_acumulada


def encontrar_ciudad_mas_cercana(n, ciudad_actual, visitadas, distancias):
    ciudad_mas_cercana = None
    distancia_minima = float("inf")

    for ciudad in range(n):
        if not visitadas[ciudad] and distancias[ciudad_actual][ciudad] < distancia_minima:
            ciudad_mas_cercana = ciudad
            distancia_minima = distancias[ciudad_actual][ciudad]

    return ciudad_mas_cercana, distancia_minima


# recomendacion de explicacion o documentacion usando breakpoints y debugger
def fuerza_bruta(matriz_de_distancias):
    # creamos todas las permutaciones
    ciudades = range(len(matriz_de_distancias))
    permutaciones = permutations(ciudades)
    # encontramos la permutacion con menor distancia (posible duplicidad)
    mejor_ruta = None
    min_distancia = float('inf')

    for ruta in permutaciones:
        if ruta[0] != 0:
            break
        distancia = calcular_distancia_total(ruta, matriz_de_distancias)
        if distancia < min_distancia:
            min_distancia = distancia
            mejor_ruta = ruta

    ruta_ciclica = mejor_ruta + (mejor_ruta[0],)  # artificio para anadir un elemento a la tupla

    return ruta_ciclica, min_distancia


def vecino_mas_cercano(distancias):
    origen = 0
    n = len(distancias)

    visitadas = [False] * n
    camino = [origen]
    visitadas[origen] = True

    for _ in range(n - 1):
        ciudad_actual = camino[-1]
        ciudad_mas_cercana, distancia_minima = encontrar_ciudad_mas_cercana(n, ciudad_actual, visitadas, distancias)
        camino.append(ciudad_mas_cercana)
        visitadas[ciudad_mas_cercana] = True

    distancia_total = calcular_distancia_total(camino, distancias)
    camino.append(camino[0])

    return camino, distancia_total


def resolver_tsp():
    global algoritmo_completo
    global modo_consultas_API

    if modo_consultas_API:

        n = len(ciudades_escogidas)
        print(ciudades_escogidas, n)
        matriz_de_distancias = consultasAPI.get_matriz_from_google_maps(ciudades_escogidas, n)
    else:
        n = int(entry_n.get())
        if (n < 5 or n > 15):
            messagebox.showerror("Error", "El valor de 'n' debe estar entre 5 y 15.")
            return

        lbl_result.config(text="Calculando...")
        root.update_idletasks()
        matriz_de_distancias = get_distancias_matriz(n)

    t_start = time.time()

    if algoritmo_completo:
        camino, distancia_minima = fuerza_bruta(matriz_de_distancias)
    else:
        camino, distancia_minima = vecino_mas_cercano(matriz_de_distancias)
    t_end = time.time()
    round_t_eject = round(t_end - t_start, 2)

    lbl_result.config(text=f"Ciclo hamiltoniano:\n {camino}\nDistancia total: \n{distancia_minima} \nTiempo de "
                           f"ejecucion: \n{round_t_eject}s", bg=paleta[0])
    dibujar_TSP(matriz_de_distancias, n, camino)


"""

Networkx y matplotlib
- Representacion del grafo con nodos y aristas
- Almacenamiento e impresion como PNG

"""


def crear_grafo(distancias, n):
    G = nx.Graph()
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=distancias[i][j])
    return G


def dibujar_grafo(G, pos):
    # Configura la posición de los nodos
    nx.draw(G, pos, with_labels=True, node_size=300, node_color='lightblue', font_size=10, font_color="black",
            edge_color='gray', alpha=0.7)
    etiquetas_aristas = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas_aristas)


def dibujar_recorrido(G, pos, recorrido):
    nx.draw_networkx_edges(G, pos, edgelist=[(recorrido[i], recorrido[i + 1]) for i in range(len(recorrido) - 1)],
                           edge_color='r', width=2)


def dibujar_TSP(matriz_de_distancias, n, camino):
    G = crear_grafo(matriz_de_distancias, n)
    pos = nx.spring_layout(G)
    dibujar_grafo(G, pos)
    dibujar_recorrido(G, pos, camino)
    plt.show()


"""

Tkinter / Front

Utilidades 
- Colores tk    https://www.plus2net.com/python/tkinter-colors.php
- Paletas       https://mybrandnewlogo.com/es/generador-de-paleta-de-colores
- Cursores tk   https://www.tutorialspoint.com/python/tk_cursors.htm
- Fonts         https://docs.python.org/es/3.9/library/tkinter.font.html


"""


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


def interpretar_paleta(paleta: str):
    aux = paleta.split('/')
    l_paleta = []
    cont = 6
    while cont > 1:
        l_paleta.append("#" + aux[-cont])
        cont -= 1
    print(l_paleta)
    return l_paleta


def cerrar_programa():
    root.destroy()


def configurar_ventana(paleta):
    root = tk.Tk()
    root.configure(bg=paleta[0], cursor="heart")
    root.title("Solucionador del TSP")
    root.geometry("640x450")
    return root


def crear_etiqueta(root, text, x, y, font_type):
    label = tk.Label(root, bg=paleta[0], fg=paleta[-1], font=font_type, text=text)
    label.pack()
    label.place(relx=x, rely=y)
    return label


def crear_entrada(root, bg_color, fg_color, width, cursor_type, x, y):
    entry = tk.Entry(root, bg=bg_color, fg=fg_color, width=width, cursor=cursor_type)
    entry.place(relx=x, rely=y)
    return entry


# Función para crear matriz de entradas
def crear_matriz_de_entradas(root):
    matrix_frame = tk.Frame(root)
    matrix_frame.grid(row=1, column=0)  # Utiliza grid() para el frame
    matrix_frame.pack()
    matrix_frame.place(relx=0.01, rely=0.14)

    entry_matrix = []
    for i in range(15):
        fila_entradas = []
        for j in range(15):
            entrada = crear_entrada(matrix_frame, paleta[1], paleta[4], 3, "tcross", i,
                                    j)  # Usar i y j para las filas y columnas
            entrada.grid(row=i, column=j)
            fila_entradas.append(entrada)
        entry_matrix.append(fila_entradas)

    return entry_matrix


def crear_boton(root, text, fg_color, bg_color, font_type, cursor_type, x, y, command):
    button = tk.Button(root, fg=fg_color, bg=bg_color, font=font_type, cursor=cursor_type, text=text, command=command)
    button.pack()
    button.place(relx=x, rely=y)
    return button


def crear_checkbutton(root, text, fg_color, bg_color, font_type, cursor_type, x, y, variable):
    checkbutton = tk.Checkbutton(root, text=text, fg=fg_color, bg=bg_color, font=font_type, cursor=cursor_type,
                                 variable=variable)
    checkbutton.pack()
    checkbutton.place(relx=x, rely=y)
    return checkbutton


def iniciar_ventana(root):
    root.mainloop()


def crear_listbox(root, items, x, y, width, height):
    listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=width, height=height)

    for item in items:
        listbox.insert(tk.END, item)

    listbox.pack()
    listbox.place(relx=x, rely=y)

    return listbox


def obtener_nombres_seleccionados(listbox):
    selected_indices = listbox.curselection()
    selected_names = [listbox.get(index) for index in selected_indices]
    return selected_names


if __name__ == '__main__':
    paleta = interpretar_paleta('https://paletadecolores.com.mx/paleta/352640/92394b/a9767a/d1b4a2/f1f2ce/')
    # Crear la ventana principal
    root = configurar_ventana(paleta)

    # Crear etiqueta para ingresar la cantidad de ciudades
    crear_etiqueta(root, "Ingrese la cantidad de ciudades (entre 5 y 15):", 0.01, 0.05, "NORMAL")

    # Entrada para la cantidad de ciudades
    entry_n = crear_entrada(root, paleta[1], paleta[-1], 3, "tcross", 0.665, 0.065)

    # Crear matriz de entradas
    entry_matrix = crear_matriz_de_entradas(root)

    ciudades_api = []

    # Definir posiciones y estilos de botones
    dy_button = 0.10
    x_button = 0.53
    y_button = 0.14

    # Botones
    bnt_generate = crear_boton(root, "Generar Matriz", paleta[-1], paleta[2], "BOLD", "target", x_button, y_button,
                               generar_matriz_y_mostrar)

    bnt_clean = crear_boton(root, "Limpiar Matriz", paleta[-1], paleta[2], "BOLD", "target", x_button + 0.24,
                            y_button, limpiar_matriz)

    bnt_solve = crear_boton(root, "Resolver TSP", paleta[-1], paleta[1], "BOLD", "target", x_button,
                            y_button + dy_button, resolver_tsp)

    lbl_result = crear_etiqueta(root, "", x_button + 0.05, y_button + dy_button * 4.2, "NORMAL")

    btn_close = crear_boton(root, "Cerrar Programa", paleta[-1], paleta[1], "BOLD", "target", x_button + 0.21,
                            y_button + dy_button, cerrar_programa)

    # Crear una etiqueta para ingresar ciudades
    # crear_etiqueta(root, "Ingrese una ciudad:", x_button - 0.55, y_button + dy_button * 9, "NORMAL")
    # Entrada para ingresar ciudades
    entry_ciudad = crear_entrada(root, paleta[1], paleta[-1], 15, "tcross", x_button + 30,
                                 y_button + dy_button * 6)

    # Lista para mostrar las ciudades
    ciudades_peruanas = [
        "Lima",
        "Arequipa",
        "Trujillo",
        "Chiclayo",
        "Piura",
        "Cusco",
        "Chimbote",
        "Huancayo",
        "Tacna",
        "Ica",
        "Cajamarca",
        "Sullana",
        "Ayacucho",
        "Puno",
    ]

    listbox = crear_listbox(root, ciudades_peruanas, 0.01, 0.78, 20, 6)
    ciudades_escogidas = ciudades_peruanas


    def mostrar_seleccion():
        global ciudades_escogidas
        ciudades_escogidas = obtener_nombres_seleccionados(listbox)
        print("Ciudad seleccionados:", ciudades_escogidas)


    boton_mostrar = tk.Button(root, text="Actualizar", command=mostrar_seleccion)
    boton_mostrar.pack()
    boton_mostrar.place(relx=0.21, rely=0.78)

    # Checkbuttons para alternar entre algoritmo GUI y algoritmo API
    var_toggle_gui = tk.BooleanVar()  # Variable para el Checkbutton "Heuristico"
    var_toggle_api = tk.BooleanVar()  # Variable para el Checkbutton "Usar API"

    '''bnt_toggle_gui = crear_checkbutton(root, "Heuristico", paleta[-1], paleta[2], "BOLD", "target", x_button,
                                       y_button + dy_button * 7, var_toggle_gui)
    bnt_toggle_api = crear_checkbutton(root, "Usar API", paleta[-1], paleta[2], "BOLD", "target", x_button,
                                       y_button + dy_button * 9, var_toggle_api)'''
    # Botones para alternar entre algoritmo GUI y algoritmo API

    algoritmo_completo = True
    modo_consultas_API = False


    def toggle_algoritmo_completo():
        global algoritmo_completo
        algoritmo_completo = not algoritmo_completo
        if algoritmo_completo:
            messagebox.showinfo("Advertencia", "Se buscara el camino mas corto, no usar para mas de 10 nodos")
        else:
            messagebox.showinfo("Advertencia", "Se encontrara un camino corto, ideal para grandes volumenes")


    def toggle_consulta_api():
        global modo_consultas_API
        modo_consultas_API = not modo_consultas_API

        if modo_consultas_API:
            messagebox.showinfo("Advertencia", "Se esta usando como entrada las ciudades de la lista.")
            mostrar_seleccion()
        else:
            messagebox.showinfo("Advertencia", "Se esta usando como entrada la matriz de adyacencia")


    bnt_toggle_completo = crear_boton(root, "Algoritmo FB/ Nearneighbor", paleta[-1], paleta[2], "BOLD", "target",
                                      x_button,
                                      y_button + dy_button * 2, toggle_algoritmo_completo)
    bnt_toggle_api = crear_boton(root, "Consulta GUI/API", paleta[-1], paleta[2], "BOLD", "target", x_button,
                                 y_button + dy_button * 3, toggle_consulta_api)
    bnt_toggle_completo.config(command=lambda: toggle_algoritmo_completo())
    bnt_toggle_api.config(command=lambda: toggle_consulta_api())

    # Algoritmo GUI o API

    # Iniciar la ventana principal
    iniciar_ventana(root)
