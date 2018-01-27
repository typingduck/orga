import logging
import random
import string

import networkx as nx

from orga import nxe

log = logging.getLogger(__name__)


class Engine(object):
    """A hierarchial graph and iterates over it.

    node_gen_fn should return generate nodes required to have towo functions
    'do_work' and 'feedback' while will be called in each cycle.
    """

    def __init__(self, node_gen_fn, graph_k=3, graph_d=3):
        """
        args:
            graph_k: number of children per node
            graph_d: how many layers the graph should have
        """
        self.graph = create_hierarchy_graph(graph_k, graph_d, node_gen_fn)
        self.graphHead = next(iter(self.graph.nodes))
        self.nodeToPos = add_noise(nxe.hierarchy_pos(self.graph, self.graphHead))

    def __iter__(self):
        while True:  # Let the caller dictate the duration
            work_cycle(self.graph, self.graphHead)
            yield None
            feedback_cycle(self.graph, self.graphHead)


def validate_new_node(node):
    assert(hasattr(node, 'do_work'))
    assert(hasattr(node, 'feedback'))
    return node


def create_hierarchy_graph(graph_k, graph_d, node_gen_fn):
    g = nx.DiGraph(name='Örg Ås Board')

    last_layer = []
    layer_prefixes = string.ascii_lowercase[:graph_d]
    for d, layer_prefix in enumerate(layer_prefixes):
        layer_count = pow(graph_k, d)
        layer_names = [layer_prefix + str(c) for c in range(layer_count)]
        layer = [validate_new_node(node_gen_fn(name)) for name in layer_names]
        g.add_nodes_from(layer)

        for i, parent in enumerate(last_layer):
            for j in range(graph_k):
                child = layer[i * graph_k + j]
                g.add_edge(parent, child)

        last_layer = layer

    return nx.freeze(g)


def work_cycle(G, node):
    """Recursive function to apply 'do_work' to each node.

    Calls the 'do_work' function starting at the leaves first and going
    towards the head.
    """
    children = G.adj[node]
    for n in children:
        work_cycle(G, n)
    node.do_work(children)


def feedback_cycle(G, node):
    """Recursive function to apply 'do_work' to each node.

    Calls the 'feedback' function starting at the head first and going
    towards the leaves.
    """
    children = G.adj[node]
    node.feedback(children)
    for n in children:
        feedback_cycle(G, n)


def add_noise(pos_dict):
    """Adds a little noise to node location tuples.

    pos_dict should be a dict of node to 2D tuple location.
    """
    def noise(x):
        return x + (-0.5 + random.random())/30
    for n in pos_dict.keys():
        pt = pos_dict[n]
        pos_dict[n] = (noise(pt[0]), noise(pt[1]))
    return pos_dict
