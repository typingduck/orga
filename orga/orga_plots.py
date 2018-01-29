"""
Useful shared matplotlib plotting libraries.
"""

from matplotlib import animation
import networkx as nx


def plot_hierarchy(ax, orga_engine):
    """Plot a directed graph.

    args:
        ax: matplotlib axes
        orga_engine: orga.Engine
    """
    graph = orga_engine.graph
    pos = orga_engine.nodeToPos

    ax.set_title(graph.name)

    clrs = [node.color() for node in graph.nodes()]
    alfs = [node.alpha() for node in graph.nodes()]

    # draw nodes (with a white edge first)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color='w', node_size=500, alpha=1)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_color=clrs, node_size=400, alpha=alfs)

    # draw edges (with a white edge first)
    nx.draw_networkx_edges(graph, pos, ax=ax, width=4, edge_color='w', alpha=1)
    nx.draw_networkx_edges(graph, pos, ax=ax, width=2, edge_color='r', alpha=0.5)


def plot_animation(fig, ax, orga_engine, iterations):
    """Call plot_hierarchy many times in an animation."""
    eng_iter = iter(orga_engine)

    ax.tick_params(
            axis='both', left='off', top='off', right='off', bottom='off',
            labelleft='off', labeltop='off', labelright='off', labelbottom='off')

    def init():
        pass

    def animate(i):
        next(eng_iter)
        plot_hierarchy(ax, orga_engine)
        ax.set_title(i+1)

    return animation.FuncAnimation(
        fig, animate, init_func=init, frames=12, interval=1000)
