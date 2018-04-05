import logging
import random
import string

from orga import nxe
from orga import tree

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
    graph = tree.Tree(name='Örg Ås Board')

    last_layer = []
    layer_prefixes = string.ascii_lowercase[:graph_d]
    for d, layer_prefix in enumerate(layer_prefixes):
        layer_count = pow(graph_k, d)
        layer_names = [layer_prefix + str(c) for c in range(layer_count)]
        layer = [validate_new_node(node_gen_fn(name)) for name in layer_names]
        graph.add_nodes_from(layer)

        for i, parent in enumerate(last_layer):
            for j in range(graph_k):
                child = layer[i * graph_k + j]
                graph.add_edge(parent, child)

        last_layer = layer

    return graph


def work_cycle(graph, node):
    """Recursive function to apply 'do_work' to each node.

    Calls the 'do_work' function starting at the leaves first and going
    towards the head.
    """
    children = graph.adj[node]
    for n in children:
        work_cycle(graph, n)
    node.do_work(children)


def feedback_cycle(graph, node):
    """Recursive function to apply 'do_work' to each node.

    Calls the 'feedback' function starting at the head first and going
    towards the leaves.
    """
    children = graph.adj[node]
    node.feedback(children, graph)
    children = graph.adj[node]
    for n in children:
        feedback_cycle(graph, n)
