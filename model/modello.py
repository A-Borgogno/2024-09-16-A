import copy

from database.DAO import DAO
import networkx as nx

from model.sighting import Sighting
from model.state import State
import geopy.distance as distance


class Model:
    def __init__(self):
        pass

    def get_years(self):
        return DAO.get_years()

    def get_shapes_year(self, year: int):
        return DAO.get_shapes_year(year)

    def create_graph(self, year: int, shape: str):
        self._grafo.clear()
        self._nodes = DAO.get_nodes(year, shape)
        self._grafo.add_nodes_from(self._nodes)
        self._idMapStates = {n.id: n for n in self._nodes}
        self._edges = DAO.get_all_edges(self._idMapStates)
        self._grafo.add_weighted_edges_from(self._edges)

    def get_top5_nodi(self):
        nodesDeg = []
        nodesDeg = [(n, self._grafo.degree(n)) for n in self._nodes]
        nodesDeg.sort(key=lambda x: x[1], reverse=True)
        return nodesDeg[0:5]

    def get_top5_archi(self):
        edgesPeso = []
        edgesPeso = [(n, n[2]) for n in self._edges]
        edgesPeso.sort(key=lambda x: x[1], reverse=True)
        return edgesPeso[0:5]

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()

    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._score_ottimo = 0

        for nodo in self._nodes:
            self._calcola_cammino_ricorsivo([nodo]),
        return self._cammino_ottimo, self._score_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[State], distanza: float = 0):
        if distanza > self._score_ottimo:
            self._cammino_ottimo = copy.deepcopy(parziale)
            self._score_ottimo = distanza

        edges = self._grafo.out_edges(parziale[-1])
        for e in edges:
            print(e[1].Lat, e[0].Lat)
            if e[1].Area < e[0].Area:
                parziale.append(e[1])
                distanza = distanza + distance.distance((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km
                self._calcola_cammino_ricorsivo(parziale, distanza)
                parziale.pop()
                distanza = distanza - distance.distance((e[0].Lat, e[0].Lng), (e[1].Lat, e[1].Lng)).km

