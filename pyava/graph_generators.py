import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.utils.decorators import random_state


@random_state(2)
def assign_cell_type(G, p_exc, seed=None):
    """
    Returns a graph with inhibitory and excitatory cells.
    Parameters
    ----------
    G : nx.DiGraph
        The directed graph
    p : float
        Probability for each cell to be excitatory.
    """
    nt_list = seed.choice([-1, 1], size=G.number_of_nodes(), p=[1-p_exc, p_exc])
    keys = list(G.nodes)
    node_types = dict(zip(keys, nt_list))
    nx.set_node_attributes(G, node_types, 'ntype')
    return G


@random_state(3)
def er_graph_dale(n, p, p_exc, seed=None):
    G = nx.gnp_random_graph(n, p, seed=seed)
    G = assign_cell_type(G, p_exc, seed=seed)
    return G
