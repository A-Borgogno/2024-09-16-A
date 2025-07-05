
from database.DAO import DAO
import networkx as nx




class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMap = {}

    def getShapes(self):
        return DAO.getShapes()

    def getMinLat(self):
        return min(DAO.getAllLat())

    def getMaxLat(self):
        return max(DAO.getAllLat())

    def getMinLon(self):
        return min(DAO.getAllLon())

    def getMaxLon(self):
        return max(DAO.getAllLon())

    def buildGraph(self, lat, lon, shape):
        self._graph.clear()
        self._idMap = {}
        nodes = DAO.getNodes(lat, lon, shape)
        for node in nodes:
            self._idMap[node.id] = node
        self._graph.add_nodes_from(nodes)

        nodiPesati = DAO.getNodiPesati(lat, lon, shape)
        for u in nodiPesati.keys():
            for v in nodiPesati.keys():
                if u != v:
                    if DAO.sonoVicini(u, v):
                        self._graph.add_edge(self._idMap[u.upper()], self._idMap[v.upper()], weight=(nodiPesati[u]+nodiPesati[v]))

        return self._graph.number_of_nodes(), self._graph.number_of_edges()


    def getNodiGrado(self):
        return list(sorted(list(self._graph.nodes), key=lambda x: nx.degree(self._graph, x), reverse=True))

    def getGradoNodo(self, n):
        return self._graph.degree(n)

    def getArchiPeso(self):
        return list(sorted(list(self._graph.edges(data=True)), key=lambda a:a[2]["weight"], reverse=True))
