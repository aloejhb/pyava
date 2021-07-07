import numpy as np
from tqdm import tqdm
from networkx.utils.decorators import random_state

class EiLattice2d:
    def __init__(self, radius):
        self.radius = radius
        width = 2*radius + 1
        self.node_state_mat = np.zeros((width, width))
        self.node_latent_state_mat = np.zeros((width, width))
        self.node_type_mat = np.zeros((width, width))
        self.hedge_state_mat = np.zeros((width, width))
        self.vedge_state_mat = np.zeros((width, width))
        self.act_time_mat = np.zeros((width, width))


    def get_node_idx(self, node):
        idx = np.array(node) + self.radius
        return idx


    def get_node_state(self, node):
        idx = self.get_node_idx(node)
        return self.node_state_mat[idx[0], idx[1]]


    def get_node_latent_state(self, node):
        idx = self.get_node_idx(node)
        return self.node_latent_state_mat[idx[0], idx[1]]

    def set_node_state(self, node, state):
        idx = self.get_node_idx(node)
        self.node_state_mat[idx[0], idx[1]] = state


    def get_node_type(self, node):
        idx = self.get_node_idx(node)
        return self.node_type_mat[idx[0], idx[1]]

    def set_node_type(self, node, ntype):
        idx = self.get_node_idx(node)
        self.node_type_mat[idx[0], idx[1]] = ntype


    def set_edge_state(self, edge, state):
        idx = self.get_node_idx(edge[0])
        if edge[1] == 0:
            self.hedge_state_mat[idx[0], idx[1]] = state
        else:
            self.vedge_state_mat[idx[0], idx[1]] = state


    def get_neighbours(self, node):
        nbr_list = [(node[0], node[1]+1),
                    (node[0], node[1]-1),
                    (node[0]+1, node[1]),
                    (node[0]-1, node[1])]
        edge_list = [(node, 0),
                     ((node[0], node[1]-1), 0),
                     (node, 1),
                     ((node[0]-1, node[1]), 1)]
        return zip(nbr_list, edge_list)


    def send_signal(self, target_node, signal):
        tidx = self.get_node_idx(target_node)
        self.node_latent_state_mat[tidx[0], tidx[1]] += signal


@random_state(4)
def ei_perc_2d(p_exc, p, tstep, inhib=True, seed=None):
    radius = tstep
    lattice = EiLattice2d(radius)
    start_node = (0, 0)
    idx = lattice.get_node_idx(start_node)
    lattice.node_state_mat[idx[0], idx[1]] = 1
    lattice.node_type_mat[idx[0], idx[1]] = 1
    nbr_set = connect_neighbours(lattice, start_node, p, inhib, seed)
    nbr_set = set(nbr_set)
    for t in tqdm(range(tstep)):
        next_nbr_set = set()
        for node in nbr_set:
            state = update_state(lattice, node)
            if state:
                lattice.set_node_type(node,sample_node_type(p_exc, seed))
                nbrs = connect_neighbours(lattice, node, p, inhib, seed)
                next_nbr_set.update(nbrs)
        if len(next_nbr_set) == 0:
            break
        nbr_set = next_nbr_set
    return lattice


def sample_node_type(p_exc, seed):
    if seed.random() < p_exc:
        ntype = 1
    else:
        ntype = -1
    return ntype


def activate_edge(p, seed):
    if seed.random() < p:
        edge_state = 1
    else:
        edge_state = 0
    return edge_state


@random_state(4)
def connect_neighbours(lattice, node, p, inhib=True, seed=None):
    nbr_list = []
    # TODO no signal from inhib neurons
    if inhib:
        signal = lattice.get_node_type(node)
    else:
        signal = lattice.get_node_type(node) > 0
    for nbr, e in lattice.get_neighbours(node):
        if lattice.get_node_state(nbr) == 0:
            edge_state = activate_edge(p, seed)
            lattice.set_edge_state(e, edge_state)
            if edge_state:
                lattice.send_signal(nbr, signal)
                nbr_list.append(nbr)
    return nbr_list


def update_state(lattice, node, thresh=1):
    state = lattice.get_node_latent_state(node) >= thresh
    if state:
        lattice.set_node_state(node, state)
    return state
