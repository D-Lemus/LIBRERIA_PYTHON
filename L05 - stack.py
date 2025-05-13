class Stack:
    def __init__(self, s=[]) -> None:
        self._stack = s

    def __repr__(self) -> str:
        return str(self._stack)

    def top(self):
        # TODO
        pass

    def pop(self):
        # TODO
        pass

    def push(self, e) -> None:
        # TODO
        pass

    def is_empty(self) -> bool:
        # TODO
        pass

    def clear(self) -> None:
        # TODO
        pass


if __name__ == "__main__":

    S = Stack([3, 2, 5, 1, 9, 0, 8, 6, 7, 4])
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    print(S.top())
    # 4
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    e = S.pop()
    print(e)
    # 4
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7]
    S.push(-1)
    print(S)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, -1]
    print(S.is_empty())
    # False
    S.clear()
    print(S.is_empty())
    # True
