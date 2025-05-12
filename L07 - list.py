class My_List:
    def __init__(self, l: list[any]) -> None:
        self._list = l

    def __repr__(self) -> str:
        return str(self._list)

    def add(self, e) -> None:
        self._list.append(e)

    def get(self, i):
        if 0 <= i < len(self._list):
            return self._list[i]
        else:
            raise IndexError("Index out of range")

    def remove(self, i):
        if 0 <= i < len(self._list):
         return self._list.pop(i)
        else:
         raise IndexError("Index out of range")

    def index_of(self, e) -> int:
        try:
            return self._list.index(e)
        except ValueError:
            return -1

    def size(self) -> int:
        return len(self._list)


if __name__ == "__main__":

    L = My_List([3, 2, 5, 1, 9, 0, 8, 6, 7, 4])
    print(L)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    L.add(-1)
    print(L)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4, -1]
    e = L.get(2)
    print(e)
    # 5
    print(L)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4, -1]
    e = L.remove(2)
    print(e)
    # 5
    print(L)
    # [3, 2, 1, 9, 0, 8, 6, 7, 4, -1]
    i = L.index_of(8)
    print(i)
    # 5
    print(L.size())
    # 10
