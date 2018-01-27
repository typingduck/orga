"""
Compares the time take to converge between a wide model and a deep model.
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


ITERATIONS = 75
SAMPLES = 50


def create_deep_engine():
    engine = Engine(model.generate_employee, graph_k=3, graph_d=4)
    engine.graph.name = 'deep'
    return engine


def create_wide_engine():
    engine = Engine(model.generate_employee, graph_k=5, graph_d=3)
    engine.graph.name = 'wide'
    return engine


def ticks_off(ax):
    ax.tick_params(
        axis='both', left='off', top='off', right='off', bottom='off',
        labelleft='off', labeltop='off', labelright='off', labelbottom='off')


def plot(deep, wide):
    plt.figure(figsize=(16, 8))
    ax = plt.subplot(121)
    ticks_off(ax)
    plot_hierarchy(ax, deep)

    ax = plt.subplot(122)
    ticks_off(ax)
    plot_hierarchy(ax, wide)

    plt.show()
    plt.close()


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    random.seed(42)  # for debugging repeatability

    deep = create_deep_engine()
    wide = create_wide_engine()
    plot(deep, wide)

    log.info('averaging %d wide runs...' % SAMPLES)
    wide_vals = np.zeros(ITERATIONS)
    for _ in range(SAMPLES):
        wide = create_wide_engine()
        wide_vals += np.asarray([
            wide.graphHead.tribute
            for _ in zip(range(ITERATIONS), wide)
        ])

    log.info('averaging %d deep runs...' % SAMPLES)
    deep_vals = np.zeros(ITERATIONS)
    for _ in range(SAMPLES):
        deep = create_deep_engine()
        deep_vals += np.asarray([
            deep.graphHead.tribute
            for _ in zip(range(ITERATIONS), deep)
        ])

    plot(deep, wide)

    plt.figure(figsize=(16, 8))
    ax = plt.subplot(111)
    ticks_off(ax)
    ax.plot(wide_vals/SAMPLES, label='wide hierarchy performance')
    ax.plot(deep_vals/SAMPLES, label='deep hierarchy performance')
    plt.legend()
    plt.show()

