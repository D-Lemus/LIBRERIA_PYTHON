from typing import TypeVar, Callable
import time
import random
import matplotlib.pyplot as plt

T = TypeVar("T")

# Shell-sort 
def shell_sort(A: list[T], key: Callable = lambda x: x, reverse: bool = False) -> list[T]:
    n = len(A)
    mitad = len(A) // 2
    
    while mitad > 0:
        for i in range(mitad, n):
            temp = A[i]
            j = i
            while j >= mitad and key(A[j - mitad]) > key(temp):
                A[j] = A[j - mitad]
                j -= mitad
            A[j] = temp        
        mitad //= 2
    
    if reverse:
        A.reverse()

# Shell-sort no óptimo con peor caso cuadrático
def shell_no_optimo(A: list[T], key: Callable = lambda x: x, reverse: bool = False) -> list[T]:
    n = len(A)
    gaps = [n // 2, n // 3, n // 4, 1]  # Secuencia de intervalos no óptima
    
    for gap in gaps:
        for i in range(gap, n):
            temp = A[i]
            j = i
            while j >= gap and key(A[j - gap]) > key(temp):
                A[j] = A[j - gap]
                j -= gap
            A[j] = temp        
    
    if reverse:
        A.reverse()

# Función para medir el tiempo de ejecución
def medir_tiempo(algoritmo, estructura_lista, tamanios, repeticiones=5):
    tiempos = []
    for n in tamanios:
        tiempo_total = 0
        for _ in range(repeticiones):
            lista = estructura_lista(n)  
            inicio = time.time()
            algoritmo(lista)
            fin = time.time()
            tiempo_total += (fin - inicio)
        tiempos.append(tiempo_total / repeticiones)
    return tiempos

# Diferentes estructuras de listas
def lista_aleatoria(n): return [random.randint(0, 10000) for _ in range(n)]
def lista_inversa(n): return list(range(n, 0, -1))
def lista_ordenada(n): return list(range(n))


if __name__ == "__main__":
    
    tamanios = [100, 500, 1000, 5000, 10000]

    # Medir tiempos para shell_sort en el mejor caso y caso promedio
    tiempos_aleatorio_shell = medir_tiempo(shell_sort, lista_aleatoria, tamanios)
    tiempos_ordenado_shell = medir_tiempo(shell_sort, lista_ordenada, tamanios)

    # Medir tiempos para shell_no_optimo en el peor caso
    tiempos_inverso_no_optimo = medir_tiempo(shell_no_optimo, lista_inversa, tamanios)
    
    # Graficar todo en una sola gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(tamanios, tiempos_aleatorio_shell, marker='o', linestyle='-', color='b', label='Shell Sort (Caso Promedio)')
    plt.plot(tamanios, tiempos_ordenado_shell, marker='o', linestyle='-', color='g', label='Shell Sort (Mejor Caso)')
    plt.plot(tamanios, tiempos_inverso_no_optimo, marker='o', linestyle='-', color='r', label='Shell Sort (Peor Caso)')
    plt.xlabel("Tamaño de la entrada (n)")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.title("Comparación de Shell Sort")
    plt.legend()
    plt.grid()
    plt.show()