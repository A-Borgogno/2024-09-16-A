from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._grafo = nx.Graph()

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

        # # calcolo degli edges tramite query
        # for n in self._nodes:
        #     self._idMap[n.id] = n
        # edges = DAO.getEdges(year, shape, self._idMap)
        # self._grafo.add_edges_from(edges)

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()