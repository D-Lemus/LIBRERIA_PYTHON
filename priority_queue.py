from heapsort import *

class PriorityQueue(Heap):
    def __init__(self, A, queueType, key):
        super().__init__(A=A, heapType=queueType, key=key)

    def extremum(self):
        return self._heap[1]
    
    def extract_extremum(self):
        #guardamos el root
        extracted = self._heap[1]

        self._heap[1] = self._heap[self.heap_size]

        self.heap_size -= 1

        self.heapify(1)

        return extracted

    def upsert(self, e):
        
        self.heap_size += 1
        
        # Si necesitamos más espacio expandimos el array
        if self.heap_size >= len(self._heap):
            self._heap.append(None)
        
        # Colocamos el nuevo elemento al final
        self._heap[self.heap_size] = e
        
        # Reubicamos el elemento hacia arriba para mantener la propiedad del heap
        i = self.heap_size
        # En un min heap subimos si el padre es mayor y en un max si es menor
        parentIndex = i // 2
        
        if self.heap_type == HeapType.MIN:
            while parentIndex > 0 and self._key(self._heap[parentIndex]) > self._key(self._heap[i]):
                # Intercambiamos con el padre
                self._heap[parentIndex], self._heap[i] = self._heap[i], self._heap[parentIndex]
                i = parentIndex
                parentIndex = i // 2
        else:  # max heap
            while parentIndex > 0 and self._key(self._heap[parentIndex]) < self._key(self._heap[i]):
                # Intercambiamos con el padre
                self._heap[parentIndex], self._heap[i] = self._heap[i], self._heap[parentIndex]
                i = parentIndex
                parentIndex = i // 2

if __name__ == "__main__":
    A = [
        ("a", 4),
        ("b", 1),
        ("1", 3),
        ("Z", 2),
        ("@", 16),
        ("d", 9),
        ("A", 10),
        ("BB", 14),
        ("X", 8),
        ("-", 7),
    ]
    pq = PriorityQueue(A=A, queueType=HeapType.MAX, key=lambda x: x[1])
    print(pq.heap_size)
    # 10
    print(pq)
    # [('@', 16), ('BB', 14), ('A', 10), ('X', 8), ('-', 7), ('d', 9), ('1', 3),
    #  ('Z', 2), ('a', 4), ('b', 1)]
    print(pq.extremum())
    # ('@', 16)
    e = pq.extract_extremum()
    print(e)
    # ('@', 16)
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3),
    #  ('Z', 2), ('b', 1)]
    pq.upsert(("@", 5))
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3),
    #  ('Z', 2), ('b', 1), ('@', 5)]
    pq.upsert(("@", 12))
    print(pq)
    # [('BB', 14), ('@', 12), ('A', 10), ('a', 4), ('X', 8), ('d', 9), ('1', 3),
    #  ('Z', 2), ('b', 1), ('-', 7)]
