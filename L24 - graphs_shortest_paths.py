import random

from enum import Enum
from itertools import combinations
from functools import total_ordering


class NodeColor(Enum):
    WHITE = 0
    GRAY = 1
    BLACK = 2


@total_ordering
class Node:
    def __init__(self, value: int):
        self.value = value
        self.color = NodeColor.WHITE
        self.discovered = float("inf")
        self.finished = float("inf")
        self.d = float("inf")
        self.parent: Node = None

    def __repr__(self) -> str:
        return str(self.value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        if other is None:
            return False
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
        self.E: dict[tuple[Node, Node], float] = dict()
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

    def __reset_nodes(self):
        for v in self.V.values():
            v.color = NodeColor.WHITE
            v.discovered = float("inf")
            v.finished = float("inf")
            v.d = float("inf")
            v.parent = None

    def w(self, u: Node, v: Node) -> float:
        if not isinstance(u, Node):
            u = self.get_node(u)
        if not isinstance(v, Node):
            v = self.get_node(v)
        # graph must be directed
        return self.E.get((u, v), None)

    def __relax(self, u: Node, v: Node) -> bool:
        # Verifica si podemos mejorar la distancia mas corta a v pasando por u
        # Si el peso de la arista (u,v) existe y la distancia actual a v es mayor que
        # la distancia a u mas el peso de la arista (u,v)
        w = self.w(u, v)
        if w is not None and v.d > u.d + w:
            # Actualizamos la distancia de v
            v.d = u.d + w
            # Establecemos u como el padre de v en el camino mas corto
            v.parent = u
            # Retornamos True para indicar que se realizo una relajacion
            return True
        # Si no se puede mejorar la distancia, retornamos False
        return False


    def bellman_ford(self, s: int) -> bool:
        # Reinicia los valores de todos los nodos (distancias, padres, etc.)
        self.__reset_nodes()
        
        # Obtenemos el nodo de inicio y establecemos su distancia a 0
        s_node = self.get_node(s)
        s_node.d = 0
        
        # Relajamos todas las aristas |V| - 1 veces
        # En el peor caso, un camino mas corto puede tener |V| - 1 aristas
        for _ in range(len(self.V) - 1):
            # Iteramos por todas las aristas del grafo
            for (u, v), w in self.E.items():
                # Intentamos relajar cada arista
                self.__relax(u, v)
        
        # Verificamos si hay ciclos de peso negativo
        # Si despues de |V| - 1 iteraciones aun podemos relajar alguna arista,
        # entonces hay un ciclo de peso negativo
        for (u, v), w in self.E.items():
            if v.d > u.d + w:
                # Retornamos False si encontramos un ciclo de peso negativo
                return False
        
        # Si no hay ciclos de peso negativo, retornamos True
        return True

    def dags(self, s: int):
            # Algoritmo para calcular caminos mas cortos en grafos aciclicos dirigidos (DAGs)
        # Reinicia los valores de todos los nodos
        self.__reset_nodes()
        
        # Establecemos la distancia del nodo inicial a 0
        s_node = self.get_node(s)
        s_node.d = 0
        
        # Funcion auxiliar para la visita DFS (Depth-First Search)
        def dfs_visit(u, time):
            # Marcamos el nodo como visitado (gris)
            u.color = NodeColor.GRAY
            # Incrementamos el tiempo de descubrimiento
            time += 1
            u.discovered = time
            
            # Visitamos recursivamente los nodos adyacentes no visitados
            for v in self.Adj[u]:
                if v.color == NodeColor.WHITE:
                    # Establecemos u como padre de v en el arbol DFS
                    v.parent = u
                    # Continuamos la visita DFS desde v
                    time = dfs_visit(v, time)
            
            # Marcamos el nodo como completamente procesado (negro)
            u.color = NodeColor.BLACK
            # Incrementamos y asignamos el tiempo de finalizacion
            time += 1
            u.finished = time
            return time
        
        # Iniciamos el tiempo en 0
        time = 0
        # Realizamos DFS desde cada nodo no visitado
        # Esto es necesario para manejar grafos no conectados
        for u in self.V.values():
            if u.color == NodeColor.WHITE:
                # Iniciamos la visita DFS desde u
                time = dfs_visit(u, time)
        
        # Ordenamos los vertices por tiempo de finalizacion decreciente
        # Esto nos da un ordenamiento topologico del grafo
        sorted_vertices = sorted(self.V.values(), key=lambda x: x.finished, reverse=True)
        
        # Relajamos las aristas siguiendo el orden topologico
        # Esto garantiza que procesamos los nodos en el orden correcto para DAGs
        for u in sorted_vertices:
            for v in self.Adj[u]:
                # Intentamos relajar la arista (u,v)
                self.__relax(u, v)

    def dijkstra(self, s: int):
        assert all(
            [w >= 0 for w in self.E.values()]
        ), "All weights must be non-negative."
        # Aseguramos que todos los pesos son no negativos
        # Dijkstra no funciona correctamente con pesos negativos
        assert all(
            [w >= 0 for w in self.E.values()]
        ), "All weights must be non-negative."
        
        # Reinicia los valores de todos los nodos
        self.__reset_nodes()
        
        # Establecemos la distancia del nodo inicial a 0
        s_node = self.get_node(s)
        s_node.d = 0
        
        # Creamos una lista con todos los vertices
        # Esta lista representa la cola de prioridad
        Q = list(self.V.values())
        
        # Mientras la cola no este vacia
        while Q:
            # Extraemos el vertice con la distancia minima
            # En una implementacion eficiente, usariamos un heap
            u = min(Q, key=lambda x: x.d)
            Q.remove(u)
            
            # Relajamos todas las aristas que salen de u
            for v in self.Adj[u]:
                # Intentamos mejorar la distancia a v pasando por u
                self.__relax(u, v)


    def print_path(self, s: int, v: int) -> list[tuple[int, float]]:
        # Obtenemos los nodos de origen y destino
        s_node = self.get_node(s)
        v_node = self.get_node(v)
        
        # Si la distancia al nodo destino es infinita, no hay camino
        if v_node.d == float("inf"):
            return []  # No hay camino
        
        # Lista para almacenar el camino
        path = []
        # Empezamos desde el nodo destino
        current = v_node
        
        # Recorremos el camino hacia atras desde v hasta s usando los padres
        while current != s_node:
            # Anadimos el nodo actual y su distancia al camino
            path.append((current.value, current.d))
            # Pasamos al padre del nodo actual
            current = current.parent
            # Si encontramos un None, algo esta mal (no deberia ocurrir si hay camino)
            if current is None:
                return []
        
        # Anadimos el nodo de origen al camino
        path.append((s_node.value, s_node.d))
        # Invertimos el camino para que vaya de origen a destino
        path.reverse()
    
        # Devolvemos el camino completo
        return path

    def bellman_ford_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        if self.bellman_ford(s):
            return self.print_path(s, v)
        raise ValueError("Negative weight cycle found in Graph.")

    def dags_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        self.dags(s)
        return self.print_path(s, v)

    def dijkstra_shortest_paths(self, s: Node, v: Node) -> list[tuple[int, float]]:
        self.dijkstra(s)
        return self.print_path(s, v)


if __name__ == "__main__":
    G = Graph(GraphType.DIRECTED)
    nodes = range(20)
    G.add_nodes(nodes)
    edges = [(i, j, random.random()) for i, j in combinations(nodes, 2)]
    random.shuffle(edges)
    edges = edges[:50]
    G.add_edges(edges)

    assert (
        G.bellman_ford_shortest_paths(0, 18)
        == G.dijkstra_shortest_paths(0, 18)
        == G.dags_shortest_paths(0, 18)
    )
