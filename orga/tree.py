import networkx as nx


class Tree(nx.DiGraph):
    """
    Extends networkx DiGraph to implement a tree.

    Would prefer to implement own b-tree (\o/) but keeping with networkx
    leaves opening using different graphs for different cases in future.
    """

    def remove_node(self, node):
        children = self.adj[node]
        for n in list(children):
            self.remove_node(n)
        super().remove_node(node)
