from typing import TypeVar, Callable

T = TypeVar("T")


def partition(A: list[T], p: int, r: int, key: Callable) -> int:
    # TODO
    # pass
    x = A[r]
    i = p - 1
    for j in range(p, r):
        if key(A[j]) <= key(x):
            i += 1
            t = A[i]
            A[i] = A[j]
            A[j] = t
    t = A[i + 1]
    A[i + 1] = A[r]
    A[r] = t

    return i + 1




def quick_sort(A: list[T], key: Callable = lambda x: x, reverse: bool = False) -> None:
    def quicksort_rec(A, p, r):
        # TODO
        # pass
        if p < r:
            q = partition(A, p, r, key)
            quicksort_rec(A, p, q - 1)
            quicksort_rec(A, q + 1, r)

    quicksort_rec(A, 0, len(A) - 1)
    if reverse:
        A.reverse()  # opcion 1
        # A[::] = A[::-1]  # opcion 2


def select(A: list[T], i: int, key: Callable = lambda x: x) -> T:
    def select_rec(A, p, r, i):
        # TODO
        # pass
        if p == r:
            return A[p]
        q = partition(A, p, r, key)
        k = q - p
        if i == k:
            return A[q]
        elif i < k:
            return select_rec(A, p, q - 1, i)
        else:
            return select_rec(A, q + 1, r, i - k - 1)

    return select_rec(A, 0, len(A) - 1, i)


if __name__ == "__main__":

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    quick_sort(A)
    print(A)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    quick_sort(A, reverse=True)
    print(A)
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    quick_sort(B)
    print(B)
    # [(0, 2), (1, 6), (2, 0), (3, 8), (4, 7), (5, 5), (6, 4), (7, 9), (8, 1), (9, 3)]
    quick_sort(B, key=lambda x: x[1])
    print(B)
    # [(2, 0), (8, 1), (0, 2), (9, 3), (6, 4), (5, 5), (1, 6), (4, 7), (3, 8), (7, 9)]
    print(select(B, 4))
    # (4, 7)
    print(select(B, 4, key=lambda x: x[1]))
    # (6, 4)
