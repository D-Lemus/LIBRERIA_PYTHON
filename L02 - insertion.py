from typing import TypeVar, Callable

T = TypeVar("T")


def insertion_sort(
    A: list[T], key: Callable = lambda x: x, reverse: bool = False
) -> None:
    """
    Sorts (in place) list A using the insertion sort algorithm.

    Parameters
    ----------
    A: list[T]
        List of comparable elements.
    key: Callable
        Function used to compare elements in A. Defaults to comparing the elements themselves.
    reverse: bool
        Whether to sort in decreasing order or not. Defaults to False.
    """
    n = len(A)
    for j in range(1, n):
        current = A[j]
        i = j - 1
        # If reverse is False, we sort in ascending order (a <= b)
        # If reverse is True, we sort in descending order (a >= b)
        # XOR operation to flip the comparison based on reverse flag
        while i >= 0 and ((key(A[i]) > key(current)) != reverse):
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = current


if __name__ == "__main__":

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    insertion_sort(A)
    print(A)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    insertion_sort(A, reverse=True)
    print(A)
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    insertion_sort(B)
    print(B)
    # [(0, 2), (1, 6), (2, 0), (3, 8), (4, 7), (5, 5), (6, 4), (7, 9), (8, 1), (9, 3)]
    insertion_sort(B, key=lambda x: x[1])
    print(B)
    # [(2, 0), (8, 1), (0, 2), (9, 3), (6, 4), (5, 5), (1, 6), (4, 7), (3, 8), (7, 9)]