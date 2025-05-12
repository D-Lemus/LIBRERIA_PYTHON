import random
import time

class Nodo:
    def __init__(self, clave):
        self.clave = clave  # Solo guardamos la clave
        self.siguiente = None  # Inicialmente, el siguiente nodo en None

class HashTableChaining:
    
    def __init__(self, tamaño=100):
        self.tamaño = tamaño  # Tamaño de la tabla hash
        self.tabla = [None] * tamaño  # creamos la tabla dependiendo del tamaño que el usuario pida.

    def _hash(self, clave):
        return hash(clave) % self.tamaño # Multiplicamos por el módulo del tamaño del arreglo para hacer más propenso a colisiones.

    def insertar(self, clave):
        # Calculamos el índice de la clave utilizando la función hash
        indice = self._hash(clave)
        
        nodo = self.tabla[indice]  # Obtenemos el nodo en esa posición de la tabla

        # Si la clave ya existe, no la insertamos de nuevo
        while nodo:
            
            if nodo.clave == clave:
                return  # La clave ya existe, no la insertamos de nuevo
            nodo = nodo.siguiente # Si existe un nodo recorremos sus nodos hasta el ultimo

        # Si no existe, insertamos la clave al inicio de la lista enlazada en ese índice
        nuevo_nodo = Nodo(clave)
        nuevo_nodo.siguiente = self.tabla[indice]  # hacemos que el nodo apunte al siguiente nodo o a null si no existe siguiente nodo.
        self.tabla[indice] = nuevo_nodo  # El nuevo nodo se convierte en el primer nodo en esa posición

    def obtener(self, clave):
        
        indice = self._hash(clave)
        nodo = self.tabla[indice]

        while nodo:
            if nodo.clave == clave:
                return True  # La clave existe en la tabla
            nodo = nodo.siguiente
        return False  # La clave no está presente

    def eliminar(self, clave):
       
        indice = self._hash(clave)
        nodo = self.tabla[indice]
        anterior = None

        while nodo:
            if nodo.clave == clave:
                if anterior:
                    anterior.siguiente = nodo.siguiente
                else:
                    self.tabla[indice] = nodo.siguiente
                return True  # La clave fue eliminada
            anterior = nodo
            nodo = nodo.siguiente
        return False  # La clave no existe en la tabla


class HashTableOpenAddressing:
    
    def __init__(self, tamaño=10):
        self.tamaño = tamaño
        self.tabla = [None] * tamaño
        self.marcador_borrado = "<BORRADO>" # necesario por si se borra un elemento pero ya existia desplzamiento de indices.

    def _hash(self, clave):
        return hash(clave) % self.tamaño

    def insertar(self, clave):
        
        indice = self._hash(clave)
        
        for i in range(self.tamaño):
            
            nuevo_indice = (indice + i) % self.tamaño
            
            if self.tabla[nuevo_indice] is None or self.tabla[nuevo_indice] == self.marcador_borrado:
                self.tabla[nuevo_indice] = clave
                return
            if self.tabla[nuevo_indice] == clave:
                return  # Ya existe, no insertamos de nuevo

    def obtener(self, clave):
        indice = self._hash(clave)
        for i in range(self.tamaño):
            nuevo_indice = (indice + i) % self.tamaño
            if self.tabla[nuevo_indice] is None:
                return False 
            if self.tabla[nuevo_indice] == clave:
                return True
        return False

    def eliminar(self, clave):
        indice = self._hash(clave)
        for i in range(self.tamaño):
            nuevo_indice = (indice + i) % self.tamaño
            if self.tabla[nuevo_indice] is None:
                return False
            if self.tabla[nuevo_indice] == clave:
                self.tabla[nuevo_indice] = self.marcador_borrado
                return True
        return False



def generar_clave(longitud=8): # crea las claves alfanumericas que se utilizaran en cada insersion 
    caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# tablas hash con direccionamiento encadenado y direccionamiento abierto
tabla_encadenada = HashTableChaining(tamaño=10000)
tabla_abierta = HashTableOpenAddressing(tamaño=10000)

# Insertar 10,000 claves aleatorias
claves_iniciales = [generar_clave() for _ in range(10000)]

# Medir el tiempo de inserción para la tabla de encadenamiento
start_time = time.time()

for clave in claves_iniciales:
    tabla_encadenada.insertar(clave)
print(f"Tiempo de inserción en tabla de encadenamiento: {time.time() - start_time} segundos")

# Medir el tiempo de inserción para la tabla de direccionamiento abierto
start_time = time.time()
for clave in claves_iniciales:
    tabla_abierta.insertar(clave)
print(f"Tiempo de inserción en tabla de direccionamiento abierto: {time.time() - start_time} segundos")

# Elegir un subconjunto de claves para realizar búsquedas y eliminaciones
subconjunto_claves = random.sample(claves_iniciales, 1000)

# Medir el tiempo de búsqueda en la tabla de encadenamiento
start_time = time.time()
for clave in subconjunto_claves:
    tabla_encadenada.obtener(clave)
print(f"Tiempo de búsqueda en tabla de encadenamiento: {time.time() - start_time} segundos")

# Medir el tiempo de búsqueda en la tabla de direccionamiento abierto
start_time = time.time()
for clave in subconjunto_claves:
    tabla_abierta.obtener(clave)
print(f"Tiempo de búsqueda en tabla de direccionamiento abierto: {time.time() - start_time} segundos")

# Medir el tiempo de eliminación en la tabla de encadenamiento
start_time = time.time()
for clave in subconjunto_claves:
    tabla_encadenada.eliminar(clave)
print(f"Tiempo de eliminación en tabla de encadenamiento: {time.time() - start_time} segundos")

# Medir el tiempo de eliminación en la tabla de direccionamiento abierto
start_time = time.time()
for clave in subconjunto_claves:
    tabla_abierta.eliminar(clave)
print(f"Tiempo de eliminación en tabla de direccionamiento abierto: {time.time() - start_time} segundos")