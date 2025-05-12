from enum import Enum
from typing import TypeVar, Callable

T = TypeVar("T")


def parent(i):
    return i >> 1


def left(i):
    return i << 1


def right(i):
    return (i << 1) + 1


class HeapType(Enum):
    MAX = 0
    MIN = 1


class Heap:
    def __init__(
        self,
        A: list[T],
        heapType: HeapType = HeapType.MAX,
        key: Callable = lambda x: x,
    ) -> None:
        self._heap = [None] + list(A)  # Make the array 1-indexed
        self._key = key
        self.heap_size = len(A)
        self.type = heapType
        self.build_heap()

    def __repr__(self):
        return str(self._heap[1 : self.heap_size + 1])

    def _compare_eq(self, a, b) -> bool:
        return (
            self._key(a) >= self._key(b)
            if self.type == HeapType.MAX
            else self._key(a) <= self._key(b)
        )

    def assert_heap_property(self) -> None:
        for i in range(2, self.heap_size + 1):
            assert self._compare_eq(
                self._heap[parent(i)], self._heap[i]
            ), f"{self._heap[parent(i)]}, {self._heap[i]}, {self.type}"

    def heapify(self, i) -> None:

        largest = i
        l = left(i)
        r = right(i)

        if l <= self.heap_size and self._heap[l] > self._heap[i]:
                largest = l

        if r <= self.heap_size and self._heap[r] > self._heap[largest]:
            largest = r

        if not largest == i:
            temp = self._heap[i]
            self._heap[i] = self._heap[largest]
            self._heap[largest] = temp
            self.heapify(largest)



    def build_heap(self) -> None:
        #self.heap_size = len(self._heap)
        for i in range (self.heap_size//2,0,-1):
            self.heapify(i)

    def get_heap(self) -> list[T]:
        return self._heap[1:self.heap_size + 1]


def heapsort(A: list[T], key: Callable = lambda x: x, reverse: bool = False) -> None:
    
    
    heap_type = HeapType.MIN if reverse else HeapType.MAX

    H = Heap(A,heap_type,key)
    original_size = H.heap_size

    sorted_array = []

    for i in range (original_size):
        #swapping the root with the last element of the heap
        H._heap[1],H._heap[H.heap_size] = H._heap[H.heap_size],H._heap[1]
        #we add to the new sorted array the element we swapped
        sorted_array.append(H._heap[H.heap_size])
        #we reduce the heap size
        H.heap_size -= 1
        #Fixing the heap startnig the root
        H.heapify(1)


        
    
    


if __name__ == "__main__":
    H = Heap([3, 2, 5, 1, 9, 0, 8, 6, 7, 4], HeapType.MIN)
    print(H)
    # [0, 1, 3, 2, 4, 5, 8, 6, 7, 9]
    H = Heap([3, 2, 5, 1, 9, 0, 8, 6, 7, 4], HeapType.MAX)
    print(H)
    # [9, 7, 8, 6, 4, 0, 5, 3, 1, 2]

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    C = heapsort(A)
    print(C)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    C = heapsort(A, reverse=True)
    print(C)
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    C = heapsort(B)
    print(C)
    # [(0, 2), (1, 6), (2, 0), (3, 8), (4, 7), (5, 5), (6, 4), (7, 9), (8, 1), (9, 3)]
    C = heapsort(B, key=lambda x: x[1])
    print(C)
    # [(2, 0), (8, 1), (0, 2), (9, 3), (6, 4), (5, 5), (1, 6), (4, 7), (3, 8), (7, 9)]
