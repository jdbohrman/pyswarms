#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import modules
import pytest
import numpy as np

# Import from package
from pyswarms.backend.topology import Random


@pytest.mark.parametrize("k", [1, 2])
def test_update_gbest_neighborhood(swarm, k):
    """Test if update_gbest_neighborhood gives the expected return values"""
    topology = Random()
    pos, cost = topology.compute_gbest(swarm, k=k)
    expected_pos = np.array([1, 2, 3])
    expected_cost = 1
    assert (pos == expected_pos).all()
    assert cost == expected_cost


@pytest.mark.parametrize("clamp", [None, (0, 1), (-1, 1)])
def test_compute_velocity_return_values(swarm, clamp):
    """Test if compute_velocity() gives the expected shape and range"""
    topology = Random()
    v = topology.compute_velocity(swarm, clamp)
    assert v.shape == swarm.position.shape
    if clamp is not None:
        assert (clamp[0] <= v).all() and (clamp[1] >= v).all()


@pytest.mark.parametrize(
    "bounds",
    [None, ([-5, -5, -5], [5, 5, 5]), ([-10, -10, -10], [10, 10, 10])],
)
def test_compute_position_return_values(swarm, bounds):
    """Test if compute_position() gives the expected shape and range"""
    topology = Random()
    p = topology.compute_position(swarm, bounds)
    assert p.shape == swarm.velocity.shape
    if bounds is not None:
        assert (bounds[0] <= p).all() and (bounds[1] >= p).all()


@pytest.mark.parametrize("k", [1, 2])
def test_compute_neighbors_return_values(swarm, k):
    """Test if __compute_neighbors() gives the expected shape and symmetry"""
    topology = Random()
    adj_matrix = topology._Random__compute_neighbors(swarm, k)
    assert adj_matrix.shape == (swarm.n_particles, swarm.n_particles)
    assert np.allclose(adj_matrix, adj_matrix.T, atol=1e-8)  # Symmetry test


def test_compute_neighbors_adjacency_matrix(swarm, k):
    """Test if __compute_neighbors() gives the expected matrix"""
    np.random.seed(1)
    topology = Random()
    adj_matrix = topology._Random__compute_neighbors(swarm, k)
    comparison_matrix = np.array([[1, 1, 0], [1, 1, 1], [0, 1, 1]])
    assert np.allclose(adj_matrix, comparison_matrix, atol=1e-8)