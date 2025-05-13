from typing import TypeVar, Callable
from math import ceil, log

T = TypeVar("T")


def shell_sort(
    A: list[T], key: Callable = lambda x: x, reverse: bool = False
) -> list[T]:
    """
    Sorts (in place) list A using the shell sort algorithm.

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
    # Compute the gap sequence using Knuth's formula: h = 3*h + 1
    # Calculate the maximum gap
    h = 1
    while h < n // 3:
        h = 3 * h + 1
        
    # Shell sort using h-sorting
    while h >= 1:
        # h-sort the array
        for i in range(h, n):
            # Insert A[i] among A[i-h], A[i-2*h], A[i-3*h]...
            j = i
            current = A[i]
            # The XOR operation (!= reverse) flips the comparison based on the reverse flag
            while j >= h and ((key(A[j - h]) > key(current)) != reverse):
                A[j] = A[j - h]
                j -= h
            A[j] = current
        # Move to the next gap
        h = h // 3
    
    return A


if __name__ == "__main__":

    A = [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    shell_sort(A)
    print(A)
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    shell_sort(A, reverse=True)
    print(A)
    # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    B = [(3, 8), (2, 0), (5, 5), (1, 6), (9, 3), (0, 2), (8, 1), (6, 4), (7, 9), (4, 7)]
    shell_sort(B)
    print(B)
    # [(0, 2), (1, 6), (2, 0), (3, 8), (4, 7), (5, 5), (6, 4), (7, 9), (8, 1), (9, 3)]
    shell_sort(B, key=lambda x: x[1])
    print(B)
    # [(2, 0), (8, 1), (0, 2), (9, 3), (6, 4), (5, 5), (1, 6), (4, 7), (3, 8), (7, 9)]