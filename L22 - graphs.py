from enum import Enum
from functools import total_ordering
from typing_extensions import Self


class NodeColor(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2


@total_ordering
class Node:
    def __init__(self, value: int):
        self.value = value
        self.color = NodeColor.WHITE
        self.distance = float("inf")
        self.discovered = float("inf")
        self.finished = float("inf")
        self.parent: Node = None

    def __repr__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class GraphType(Enum):
    UNDIRECTED = 0
    DIRECTED = 1


class Graph:
    def __init__(self, type_: GraphType):
        self.type = type_
        self.V: dict[int, Node] = dict()
        self.E: set[tuple[Node, Node]] = set()
        self.Adj: dict[Node, set[Node]] = dict()

    def __repr__(self):
        return str(self.Adj)

    def get_node(self, s: int) -> Node:
        return self.V.get(s, None)

    def add_node(self, v: int):
        v_node = self.get_node(v)
        if not v_node:
            v_node = Node(v)
            self.V[v] = v_node
            self.Adj[v_node] = set()

    def add_edge(self, u: int, v: int):
        u = self.get_node(u)
        v = self.get_node(v)
        if u and v:
            self.E.add((u, v))
            self.Adj[u].add(v)
            if self.type == GraphType.UNDIRECTED:
                self.Adj[v].add(u)
        else:
            raise ValueError("Node not found in graph")

    def add_nodes(self, v_list: list[int]):
        for v in v_list:
            self.add_node(v)

    def add_edges(self, e_list: list[tuple[int, int]]):
        for e in e_list:
            self.add_edge(*e)

    def __reset_nodes(self):
        for v in self.V.values():
            v.color = NodeColor.WHITE
            v.distance = float("inf")
            v.discovered = float("inf")
            v.finished = float("inf")
            v.parent = None

    def bfs(self, s: int) -> Node:
        # TODO
        # pass
        self.__reset_nodes()
        s_node = self.get_node(s)
        s_node.color = NodeColor.GRAY
        s_node.distance = 0
        s_node.parent = None

        q = [s_node]
        while len(q) != 0:
            u = q.pop(0)
            for v in self.Adj[u]:
                if v.color == NodeColor.WHITE:
                    v.color = NodeColor.GRAY
                    v.distance = u.distance + 1
                    v.parent = u
                    q += [v]
            u.color = NodeColor.BLACK

    def get_bft(self, s: int) -> Self:
        # TODO
        # pass
        G_pi = Graph(self.type)
        V_pi = [v.value for v in self.V.values() if v.parent]
        E_pi = [(v.parent.value, v.value) for v in V_pi]
        V_pi = [s] + [v.value for v in V_pi]
        G_pi.add_nodes(V_pi)
        G_pi.add_edges(E_pi)
        return G_pi

    def print_path(self, s: int, v: int) -> list[int]:
        # TODO
        pass

    def dfs(self):
        # TODO
        # pass
        self.__reset_nodes()
        self.time = 0
        for u in self.V.values():
            if u.color == NodeColor.WHITE:
                self.__dfs_visit(u)

    def __dfs_visit(self, u: Node):
        # TODO
        # pass
        self.time += 1
        u.discovered = self.time
        u.color = NodeColor.GRAY
        for v in self.Adj[u]:
            if v.color == NodeColor.WHITE:
                v.parent = u
                self.__dfs_visit(v)
        u.color = NodeColor.BLACK
        self.time += 1
        u.finished = self.time

    def __classify_edges(self) -> dict[str, list[tuple[Node]]]:
        # TODO
        # pass
        # clasificar aristas de mi grafo en 4 categorias
        # 1) tree - aristas que forman parte del bosque DFF
        # 2) forward - aristas que me llevan a alguno de mis descendientes que no es mi hijo
        if u.d < v.d < v.f < u.f:
            if v.parent == u:
                "tree"
            else:
                "forward"
        # 3) backward - aristas que me llevan a alguno de mis predecesores (incluso yo mismo)
        # 4) cross - aristas que me llevan a otro arbol dentro del DFF

    def topological_sort(self) -> list[int]:
        # TODO
        # pass
        assert (self.type == GraphType.DIRECTED), "T-Sort not supported on undirected graphs"
        categories = self.__classify_edges()
        if len(categories["back"]) != 0:
            raise Exception("El grafo no es aciclico")

    # def scc(self) -> list[list[int]]:
    #     # TODO
    #     # pass
    #     assert (self.type == GraphType.DIRECTED), "SCC not supported on undirected graphs"
    #     self.dfs()
    #     G_T = Graph()
    #     G_T.add_nodes(self.V.keys())
    #     for u in self.V.values():
    #         for v in self.Adj[u]:
    #             G_T.add_edge(v, u)
        
    #     sorted_nodes = sorted(self.V.values(), key= lambda u: u.finished, reverse= True)
    #     G_T.time = 0
    #     for u in self.V.values():
    #         if u.color == NodeColor.WHITE:
    #             G_T.__dfs_visit(u)
        
    #     v_pi = [v for v in G_T.V.values() if v.parent]
    #     E_pi = [(v.parent.value, v.value) for v in v_pi]
    #     source_nodes = [v for v in G_T.values() if not v.parent]
    #     for v in source_nodes:

def scc(self) -> list[list[int]]:
    assert (self.type == GraphType.DIRECTED), "SCC not supported on undirected graphs"
    
    self.dfs()
    
    G_T = Graph()
    G_T.add_nodes(self.V.keys())
    for u in self.V.values():
        for v in self.Adj[u]:
            G_T.add_edge(v, u)
    
    sorted_nodes = sorted(self.V.values(), key=lambda u: u.finished, reverse=True)
    
    G_T.time = 0
    components = []
    
    for u in sorted_nodes:
        if u.color == NodeColor.WHITE:
            component = []
            G_T._dfs_visit(u, component)
            components.append([node.value for node in component])
    
    return components

if __name__ == "__main__":
    G = Graph(GraphType.DIRECTED)
    G.add_nodes(list("abcdefgh"))
    G.add_edges(
        [
            ("a", "b"),
            ("b", "c"),
            ("b", "e"),
            ("b", "f"),
            ("c", "d"),
            ("c", "g"),
            ("d", "c"),
            ("d", "h"),
            ("e", "a"),
            ("e", "f"),
            ("f", "g"),
            ("g", "f"),
            ("g", "h"),
            ("h", "h"),
        ]
    )
    print(G.Adj)
    # {a: {b}, b: {c, f, e}, c: {d, g}, d: {h, c}, e: {f, a}, f: {g}, g: {h, f}, h: {h}}
    G.bfs("a")
    for v in G.V.values():
        print(v, v.distance, v.parent)
    # a 0 None
    # b 1 a
    # c 2 b
    # d 3 c
    # e 2 b
    # f 2 b
    # g 3 c
    # h 4 g
    bft = G.get_bft("a")
    print(bft)
    # {g: {h}, f: {g}, a: {b}, h: set(), e: set(), d: set(), b: {c, f, e}, c: {d}}
    print(G.print_path("a", "h"))
    # ['a', 'b', 'c', 'g', 'h']
    G.dfs()
    for v in G.V.values():
        print(v.value, v.parent, v.discovered, v.finished)
    # a None 1 16
    # b a 2 15
    # c b 11 14
    # d c 12 13
    # e b 3 10
    # f e 4 9
    # g f 5 8
    # h g 6 7
    try:
        print(G.topological_sort())
        # TypeError: Topological sort is not defined for cyclic graphs.
    except:
        pass
    print(G._Graph__classify_edges())
    # {'tree': [(a, b), (b, f), (b, c), (b, e), (c, d), (f, g), (g, h)], 'back': [(d, c), (e, a), (g, f), (h, h)], 'forward': [], 'cross': [(c, g), (d, h), (e, f)]}
    print(G.scc())
    # [['b', 'e', 'a'], ['d', 'c'], ['g', 'f'], ['h']]
