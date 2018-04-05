"""
Investigate simple rules to allow adding or removing of nodes.
"""

import logging
import math
import random
import string
import sys

import matplotlib.pyplot as plt
import numpy as np

from orga.orga import Engine
from orga.orga_plots import plot_hierarchy


GRAPH_D = 3
GRAPH_K = 3
ITERATIONS = 20


log = logging.getLogger(__name__)


class RandomChildrenModel(object):
    """A model that randomly adds/removes children."""

    def __init__(self, name=None):
        pass

    def do_work(self, reportees):
        pass

    def feedback(self, reportees, graph):
        r = random.random()
        if r < 0.1:
          to_add = RandomChildrenModel()
          graph.add_node(to_add)
          graph.add_edge(self, to_add)
        elif r < 0.15 and reportees:
          to_remove = random.choice(list(reportees))
          graph.remove_node(to_remove)

    def color(self):
        return 'k'

    def alpha(self):
        return 1


def create_engine():
    return Engine(RandomChildrenModel, graph_k=GRAPH_K, graph_d=GRAPH_D)


def plot(eng):
    plt.figure(figsize=(16, 8))
    plt.tick_params(
        axis='both', left='off', top='off', right='off', bottom='off',
        labelleft='off', labeltop='off', labelright='off', labelbottom='off')
    ax = plt.subplot(111)
    plot_hierarchy(ax, eng)
    plt.show()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    random.seed(10)  # for debugging repeatability

    engine = create_engine()
    for it, _ in zip(range(ITERATIONS), engine):
        plot(engine)
        log.info('%d' % (it+1))
