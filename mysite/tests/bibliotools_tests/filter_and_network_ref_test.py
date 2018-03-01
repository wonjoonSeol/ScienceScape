import unittest
import sys
import os

lib_path = os.path.abspath(os.path.join(__file__, '..', '..', '..', 'bibliotools3.0', 'scripts'))
sys.path.append(lib_path)

import itertools
import networkx
from networkx.readwrite import json_graph
import json
import codecs
import matplotlib.pyplot as plt

from filter_and_network_ref import add_edge_weight

class TestFilterNetworkRef(unittest.TestCase):

    """
    This test tests that upon calling add_edge_weight for two unconnected nodes,
    an edge is successfully added between these two nodes.
    """
    def test_add_edge_weight_not_connected(self):

        # Mocking a reference graph
        graph = networkx.Graph()
        node1 = "first_node"
        node2 = "second_node"
        graph.add_node(node1, type = "references", occurence_count = 10)
        graph.add_node(node2, type = "references", occurence_count = 15)
        add_edge_weight(graph, node1, node2)
        self.assertEqual(True, graph.has_edge(node1, node2))

    """
    This test tests that upon calling add_edge_weight for two CONNECTED nodes,
    the weighting for the edge will have increased by the number of edges meant to be added.
    """
    def test_add_edge_weight_connected(self):

        # Mocking a reference graph
        graph = networkx.Graph()
        node1 = "first_node"
        node2 = "second_node"
        graph.add_node(node1, type = "references", occurence_count = 10)
        graph.add_node(node2, type = "references", occurence_count = 15)
        # Manually creating an edge between these two nodes.
        graph.add_edge(node1, node2, weight = 1)

        for i in range (1, 10):
            add_edge_weight(graph, node1, node2)
        # Weighting for this edge should now be 10.
        self.assertEqual(True, graph[node1][node2]["weight"] == 10)


if __name__ == '__main__':
    unittest.main()
