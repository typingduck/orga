"""Tests for `examples` package.

Checks that the engines/models create by the example run ok (does not test
the plotting etc).

Both ensures the examples stay working and acts as simple integration tests
for the code.
"""

import pytest
from networkx import dag_longest_path_length
import random

from orga import orga

from examples import basic3x3
from examples import basic_model as model
from examples import deep6x3
from examples import depth_vs_breadth
from examples import shape_changing_graph


def test_basic3x3_converges():
    """Ensure the basic 3x3 converges."""
    random.seed(42)
    engine = basic3x3.create_engine()

    # should converage after 20 iteractions
    for _ in zip(range(20), engine): pass

    head = list(engine.graph.nodes)[0]
    assert head.tribute == pytest.approx(9.0, 0.001)


def test_basic3x3_has_expected_types():
    """Ensure the basic 3x3 types are as expected."""
    random.seed(42)
    engine = basic3x3.create_engine()

    # should converage after 20 iteractions
    for _ in zip(range(20), engine): pass

    head = list(engine.graph.nodes)[0]
    for node in engine.graph.nodes:
        children = engine.graph.adj[node]
        if node.name == 'CEO':
            assert node.__class__ == model.Ceo
        elif children:
            assert node.__class__ == model.Red
        else:
            assert node.__class__ == model.Blu


def test_deep6x3():
    """Ensure the deep 6x3 works."""
    random.seed(42)
    engine = deep6x3.create_engine()

    # should converage after 120 iteractions
    for _ in zip(range(120), engine): pass

    head = list(engine.graph.nodes)[0]
    assert head.tribute == pytest.approx(243.0, 0.1)

    for node in engine.graph.nodes:
        children = engine.graph.adj[node]
        if node.name == 'CEO':
            assert node.__class__ == model.Ceo
        elif children:
            assert node.__class__ == model.Red
        else:
            assert node.__class__ == model.Blu


def test_depth_vs_breath_wide():
    """Ensure the depth vs breadth wide example works."""
    random.seed(42)
    engine = depth_vs_breadth.create_wide_engine()

    for _ in zip(range(100), engine): pass

    head = list(engine.graph.nodes)[0]
    assert head.tribute == pytest.approx(25.0, 0.1)

    for node in engine.graph.nodes:
        children = engine.graph.adj[node]
        if node.name == 'CEO':
            assert node.__class__ == model.Ceo
        elif children:
            assert node.__class__ == model.Red
        else:
            assert node.__class__ == model.Blu


def test_depth_vs_breath_deep():
    """Ensure the depth vs breadth deep example works."""
    random.seed(42)
    engine = depth_vs_breadth.create_deep_engine()

    for _ in zip(range(100), engine): pass

    head = list(engine.graph.nodes)[0]
    assert head.tribute == pytest.approx(25.0, 0.1)

    for node in engine.graph.nodes:
        children = engine.graph.adj[node]
        if node.name == 'CEO':
            assert node.__class__ == model.Ceo
        elif children:
            assert node.__class__ == model.Red
        else:
            assert node.__class__ == model.Blu


def test_changing_shape():
    """Ensure the node adding/removing example works."""
    random.seed(42)
    engine = shape_changing_graph.create_engine()

    # should be 3x3 before
    print (list(engine.graph.degree()))
    max_K = max(v for k,v in engine.graph.degree())
    assert max_K == shape_changing_graph.GRAPH_K + 1
    max_D = dag_longest_path_length(engine.graph) + 1
    assert max_D == shape_changing_graph.GRAPH_D

    for _ in zip(range(100), engine): pass

    # shape should change
    max_K = max(v for k,v in engine.graph.degree())
    assert max_K != shape_changing_graph.GRAPH_K + 1
    max_D = dag_longest_path_length(engine.graph) + 1
    assert max_D != shape_changing_graph.GRAPH_D
