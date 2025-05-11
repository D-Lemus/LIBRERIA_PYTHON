import random

from enum import Enum
from itertools import combinations
from functools import total_ordering


@total_ordering
class Node:
    def __init__(self, value: int):
        self.value = value
        self.key = float("inf")  # prim (WEIGHT EN LAS DIAPOSITIVAS)
        self.parent: Node = None  # prim

    def __repr__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)


class DisjointSets:
    def __init__(self):
        self.sets = []

    def make_set(self, x):
        self.sets.append({x})

    def find_set(self, x):
        for s in self.sets:
            if x in s:
                return s
        return None

    def union(self, x, y):
        s_x = self.find_set(x)
        s_y = self.find_set(y)
        if s_x and s_y and s_x != s_y:
            s_union = s_x.union(s_y)
            self.sets.remove(s_x)
            self.sets.remove(s_y)
            self.sets.append(s_union)


class GraphType(Enum):
    UNDIRECTED = 0
    DIRECTED = 1


class Graph:
    def __init__(self, type_: GraphType):
        self.type = type_
        self.V: dict[int, Node] = dict()
        self.E: dict[tuple[Node, Node], float] = dict()
        self.Adj: dict[Node, set[Node]] = dict()

    def w(self, u: Node, v: Node) -> float:
        if not isinstance(u, Node):
            u = self.get_node(u)
        if not isinstance(v, Node):
            v = self.get_node(v)
        return self.E.get((u, v), self.E.get((v, u), None))

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

    def add_edge(self, u: int, v: int, w: float):
        u = self.get_node(u)
        v = self.get_node(v)
        if u and v:
            self.E[(u, v)] = w
            self.Adj[u].add(v)
            if self.type == GraphType.UNDIRECTED:
                self.Adj[v].add(u)
        else:
            raise ValueError("Node not found in graph")

    def add_nodes(self, v_list: list[int]):
        for v in v_list:
            self.add_node(v)

    def add_edges(self, e_list: list[tuple[int, int, float]]):
        for e in e_list:
            self.add_edge(*e)

    def kruskal(self) -> set[tuple[int, int, float]]:

#       creamos un conjunto vacio 
        A = set()
#       inicializamos la estructura de DisjointSets
        disjoint_sets = DisjointSets()

#       Recorremos los nodos almacenados en el grafo y creamos un conjunto con un nodo individual
        for v in self.V.values():
            disjoint_sets.make_set(v)

#       Hacemos un sorted de la tupla de E donde estamos ordenando la union de vertices con el peso de
#       la arista que se encuentra en el segundo elemento del par x[1]
        sorted_edges = sorted(self.E.items(), key = lambda x:x[1])

#       Nested Tuple Unpacking: desempaquetamos cada par en la tupla de nodos (u,v) y su peso "w"
#       -EN CADA ITERAION:
#           u  contiene un objeto Node
#           v contiene otro
#           w contiene un float
        for(u,v),w in sorted_edges:
#           Si el valor u o v no son parte del set se agregan la arista al MST y se hace una union
#           dentro de disjoit sets para mostrar que los nodos u y v estan conectados 
            if disjoint_sets.find_set(u) != disjoint_sets.find_set(v):
                A.add((u.value, v.value, w))
                disjoint_sets.union(u,v)

        return A

    def prim(self, r: int) -> set[tuple[int, int, float]]:
#       Creamos un conjunto vacio para almacenar las aristas del MST
        A = set()
        
#       Inicializamos todos los vertices
#       Para cada vertice, establecemos una clave infinita (distancia) y un padre nulo
        for v in self.V.values():
            v.key = float("inf")  # La clave representa el peso minimo de cualquier arista que conecte v con un vertice en el MST
            v.parent = None       # El padre sera el nodo desde el cual anadimos v al MST
        
#       Establecemos la clave del vertice inicial 'r' a 0
#       Este sera el punto de partida del algoritmo
        r_node = self.get_node(r)
        r_node.key = 0
        
#       Creamos una cola Q con todos los vertices
#       Esta cola contiene los vertices que aun no han sido anadidos al MST
        Q = list(self.V.values())
        
#       Inicializamos el conjunto de aristas del MST
        A = set()
        
#       Mientras la cola no este vacia
        while Q:
#           Extraemos el vertice con el valor de clave minimo
#           Esto es una operacion de extraccion de minimo (extract-min)
#           En una implementacion eficiente, usariamos un monticulo (heap)
            u = min(Q, key=lambda x: x.key)
            Q.remove(u)
            
#           Si el vertice u tiene un padre, anadimos la arista correspondiente al MST
#           No anadimos nada para el vertice inicial, ya que su padre es None
            if u.parent is not None:
                A.add((u.parent.value, u.value, self.w(u.parent, u)))
            
#           Para cada vertice adyacente a u que aun esta en Q
            for v in self.Adj[u]:
#                  Si v esta en Q y el peso de la arista (u,v) es menor que la clave actual de v
                if v in Q and self.w(u, v) < v.key:
#                   Actualizamos el padre de v a u
                    v.parent = u
#                   Actualizamos la clave de v al peso de la arista (u,v)
                    v.key = self.w(u, v)
        
#       Devolvemos el conjunto de aristas que forman el MST
        return A


if __name__ == "__main__":
    G = Graph(GraphType.UNDIRECTED)
    nodes = range(20)
    G.add_nodes(nodes)
    edges = [(i, j, random.random()) for i, j in combinations(nodes, 2)]
    random.shuffle(edges)
    edges = edges[:50]
    G.add_edges(edges)

    A_k = G.kruskal()
    A_p = G.prim(0)
    assert abs(sum([w for u, v, w in A_k]) - sum([w for u, v, w in A_p])) <= 0.001
