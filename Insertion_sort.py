from typing import TypeVar, Callable
from typing import TypeVar, Callable
from math import ceil, log
import time
import random
import matplotlib.pyplot as plt
import numpy as np

T = TypeVar("T")

# Insertion-sort

def insertion_sort( A: list[T], key: Callable = lambda x: x, reverse: bool = False ) -> None:

    for indice in range( 1 , len(A)):
        
        current = A[indice] # Indice actual empezando desde el indice 1 --> indice es 3
        index = indice - 1  # Se pone el indice en 0  ---> index es 2
        
        while index >= 0 and key(A[index]) > key(current):  # 3 > 1
            A[index+1] = A[index]  # 2 , 5 , 5
            index -= 1  # index = 0
        
        A[index+1] = current # 2 , 3
        
    if reverse:
        A = A.reverse()

# Función para medir el tiempo de ejecución
def measure_time(sort_function, data, repeats=10):
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        sort_function(data)
        times.append(time.perf_counter() - start)
    return np.mean(times)

# Generar datos para los casos
def generate_best_case(size):
    # Mejor caso: lista ya ordenada
    return [i for i in range(size)]

def generate_worst_case(size):
    # Peor caso: lista en orden inverso
    return [i for i in range(size, 0, -1)]

def generate_avg_case(size):
    # Caso promedio: lista aleatoria
    return [random.randint(0, 1000) for _ in range(size)]

# Tamaños de entrada
sizes = [100, 500, 1000, 5000, 10000]

# Medir tiempos
best_times = []
worst_times = []
avg_times = []

for size in sizes:
    # Mejor caso
    data_best = generate_best_case(size)
    best_times.append(measure_time(insertion_sort, data_best))

    # Peor caso
    data_worst = generate_worst_case(size)
    worst_times.append(measure_time(insertion_sort, data_worst))

    # Caso promedio
    data_avg = generate_avg_case(size)
    avg_times.append(measure_time(insertion_sort, data_avg))

# Graficar resultados
plt.figure(figsize=(10, 5))
plt.plot(sizes, best_times, 'o-', label='Mejor caso (lista ordenada)')
plt.plot(sizes, worst_times, 's-', label='Peor caso (lista inversa)')
plt.plot(sizes, avg_times, 'd-', label='Caso promedio (lista aleatoria)')
plt.xlabel('Tamaño del arreglo')
plt.ylabel('Tiempo de ejecución (s)')
plt.title('Complejidad Temporal de Insertion Sort')
plt.legend()
plt.grid()
plt.yscale('log')  # Escala logarítmica en el eje Y
plt.show()