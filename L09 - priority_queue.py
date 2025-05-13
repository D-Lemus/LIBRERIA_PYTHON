from heapsort import *


class PriorityQueue(Heap):

    def __init__(self, A, queueType, key):
        super().__init__(A=A, heapType=queueType, key=key)

    def extremum(self):
        # TODO
        pass

    def extract_extremum(self):
        # TODO
        pass

    def upsert(self, e):
        # TODO
        pass


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
    # [('@', 16), ('BB', 14), ('A', 10), ('X', 8), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('a', 4), ('b', 1)]
    print(pq.extremum())
    # ('@', 16)
    e = pq.extract_extremum()
    print(e)
    # ('@', 16)
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('b', 1)]
    pq.upsert(("@", 5))
    print(pq)
    # [('BB', 14), ('X', 8), ('A', 10), ('a', 4), ('-', 7), ('d', 9), ('1', 3), ('Z', 2), ('b', 1), ('@', 5)]
    pq.upsert(("@", 12))
    print(pq)
    # [('BB', 14), ('@', 12), ('A', 10), ('a', 4), ('X', 8), ('d', 9), ('1', 3), ('Z', 2), ('b', 1), ('-', 7)]
