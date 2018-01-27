"""
Useful shared matplotlib plotting libraries.
"""

import networkx as nx


def plot_hierarchy(ax, orga_engine):
    """Plot a directed graph.
    
    args:
        ax: matplotlib axes
        graph: networkx graph
        pos: dictionary of graph nodes to (x,y) coordinates.
    """
    graph = orga_engine.graph
    pos = orga_engine.nodeToPos

    ax.set_title(graph.name)

    clrs = [node.color() for node in graph.nodes()]
    alfs = [node.alpha() for node in graph.nodes()]

    # draw nodes (with a white edge first)
    nx.draw_networkx_nodes(graph, pos, node_color='w', node_size=500, alpha=1)
    nx.draw_networkx_nodes(graph, pos, node_color=clrs, node_size=400, alpha=alfs)

    # draw edges (with a white edge first)
    nx.draw_networkx_edges(graph, pos, width=4, edge_color='w', alpha=1)
    nx.draw_networkx_edges(graph, pos, width=2, edge_color='r', alpha=0.5)

