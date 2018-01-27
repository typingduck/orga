"""
Depth of 3 and 3 children per node example.
"""

import logging
import math
import random
import sys

import matplotlib.pyplot as plt
import numpy as np

from orga.orga import Engine
from orga.orga_plots import plot_hierarchy

from examples import basic_model as model


log = logging.getLogger(__name__)


GRAPH_D = 3
GRAPH_K = 3
ITERATIONS = 10


def create_engine():
    return Engine(model.generate_employee, graph_k=GRAPH_K, graph_d=GRAPH_D)


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
    random.seed(42)  # for debugging repeatability

    engine = create_engine()
    for it, _ in zip(range(ITERATIONS), engine):
        plot(engine)
        log.info('{:>5} | total income: {:6.2f}'.format(it+1, engine.graphHead.tribute))
