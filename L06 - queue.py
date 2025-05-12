class Queue:
    def __init__(self, q=[]) -> None:
        self._queue = q

    def __repr__(self) -> str:
        return str(self._queue)

    def peek(self):
        return self._queue[0] if not self.is_empty() else None

    def poll(self):
       return self._queue.pop(0) if not self.is_empty() else None
    
    def offer(self, e) -> None:
        self._queue.append(e)

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def clear(self) -> None:
        self._queue.clear()


if __name__ == "__main__":

    Q = Queue([3, 2, 5, 1, 9, 0, 8, 6, 7, 4])
    print(Q)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    print(Q.peek())
    # 3
    print(Q)
    # [3, 2, 5, 1, 9, 0, 8, 6, 7, 4]
    e = Q.poll()
    print(e)
    # 3
    print(Q)
    # [2, 5, 1, 9, 0, 8, 6, 7, 4]
    Q.offer(-1)
    print(Q)
    # [-1, 2, 5, 1, 9, 0, 8, 6, 7]
    print(Q.is_empty())
    # False
    Q.clear()
    print(Q.is_empty())
    # True
