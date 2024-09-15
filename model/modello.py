import copy

from database.DAO import DAO
import networkx as nx

from model.state import State


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0.0

    def get_lat_lng_limits(self):
        return DAO.get_lat_lng_limits()

    def get_shapes(self):
        return DAO.get_shapes()

    def create_graph(self, lat, lng, shape):
        self._grafo.clear()
        nodes = DAO.get_nodes(lat, lng, shape)
        self._grafo.add_nodes_from(nodes)

        # calcolo degli edges in modo programmatico
        for i in range(0, len(nodes) - 1):
            for j in range(i + 1, len(nodes)):
                if nodes[i].id in nodes[j].Neighbors or nodes[j].id in nodes[i].Neighbors:
                    self._grafo.add_edge(nodes[i], nodes[j], weight=nodes[i].duration + nodes[j].duration)

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()

    def get_top5_nodi(self):
        nodes_deg = [(n, self._grafo.degree(n)) for n in self._grafo.nodes()]
        nodes_deg.sort(key=lambda x: x[1], reverse=True)
        return nodes_deg[0:5]

    def get_top5_archi(self):
        edges = [e for e in self._grafo.edges(data=True)]
        edges.sort(key=lambda x: x[2]["weight"], reverse=True)
        return edges[0:5]


    def cammino_ottimo(self):
        self._cammino_ottimo = []
        self._punteggio_ottimo = 0.0

        for nodo in self._grafo.nodes():
            self._calcola_cammino_ricorsivo([nodo], self._calcola_successivi(nodo))
        return self._cammino_ottimo, self._punteggio_ottimo

    def _calcola_cammino_ricorsivo(self, parziale: list[State], successivi: list[State]):
        if len(successivi) == 0:
            score = self._calcola_score(parziale)
            if score > self._punteggio_ottimo:
                self._punteggio_ottimo = score
                self._cammino_ottimo = copy.deepcopy(parziale)
        else:
            for nodo in successivi:
                # aggiungo il nodo in parziale ed aggiorno le occorrenze del mese corrispondente
                parziale.append(nodo)
                # nuovi successivi
                nuovi_successivi = self._calcola_successivi(nodo)
                # ricorsione
                self._calcola_cammino_ricorsivo(parziale, nuovi_successivi)
                parziale.pop()

    def _calcola_successivi(self, nodo: State) -> list[State]:
        """
        Calcola il sottoinsieme dei successivi ad un nodo
        """
        successivi = self._grafo.neighbors(nodo)
        successivi_ammissibili = []
        for s in successivi:
            if (s.Population/s.Area) > (nodo.Population/nodo.Area):
                successivi_ammissibili.append(s)
        return successivi_ammissibili

    def _calcola_score(self, cammino: list[State]) -> float:
        """
        Funzione che calcola il punteggio di un cammino.
        """
        score = 0
        for i in range(0, len(cammino)-1):
            peso = self._grafo.get_edge_data(cammino[i], cammino[i+1])["weight"]
            distanza = cammino[i].distance_HV(cammino[i+1])
            score += peso/distanza
        return score