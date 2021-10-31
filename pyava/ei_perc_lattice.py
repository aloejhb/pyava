import numpy as np
from tqdm import tqdm
from networkx.utils.decorators import random_state

class EiLattice2d:
    def __init__(self, radius):
        self.radius = radius
        width = 2*radius + 1
        self.width = width
        self.node_state_mat = np.zeros((width, width))
        self.node_latent_state_mat = np.zeros((width, width))
        self.node_type_mat = np.zeros((width, width))
        self.hedge_state_mat = np.zeros((width, width))
        self.vedge_state_mat = np.zeros((width, width))
        self.act_time_mat = np.ones((width, width)) * np.inf


    def get_node_idx(self, node):
        idx = np.array(node) + self.radius
        return idx


    def get_node_state(self, idx):
        return self.node_state_mat[idx[0], idx[1]]


    def get_node_latent_state(self, idx):
        return self.node_latent_state_mat[idx[0], idx[1]]

    def set_node_state(self, idx, state, tstep):
        self.node_state_mat[idx[0], idx[1]] = state
        self.act_time_mat[idx[0], idx[1]] = tstep


    def get_node_type(self, idx):
        return self.node_type_mat[idx[0], idx[1]]

    def set_node_type(self, idx, ntype):
        self.node_type_mat[idx[0], idx[1]] = ntype

    def get_edge_state(self, edge):
        idx = edge[0]
        if edge[1] == 0:
            state = self.hedge_state_mat[idx[0], idx[1]]
        else:
            state = self.vedge_state_mat[idx[0], idx[1]]
        return state

    def set_edge_state(self, edge, state):
        idx = edge[0]
        if edge[1] == 0:
            self.hedge_state_mat[idx[0], idx[1]] = state
        else:
            self.vedge_state_mat[idx[0], idx[1]] = state


    def get_neighbours(self, idx):
        nbr_list = np.array([(idx[0], idx[1]+1),
                             (idx[0], idx[1]-1),
                             (idx[0]+1, idx[1]),
                             (idx[0]-1, idx[1])])
        # Implement the periodic boundary condition
        # If the index of any neighbour is smaller than 0,
        # or exceeds the width, go to the other side of the lattice
        nbr_list = (nbr_list + self.width) % self.width
        nbr_list = list(map(tuple, nbr_list))

        # The second element of an edge indicates whether it is
        # an horizontal edge (0) or vertical edge (1)
        edge_list = [(idx, 0),
                     (nbr_list[1], 0),
                     (idx, 1),
                     (nbr_list[3], 1)]

        return zip(nbr_list, edge_list)


    def send_signal(self, target_idx, signal):
        self.node_latent_state_mat[target_idx[0], target_idx[1]] += signal


@random_state(7)
def ei_perc_2d(p, p_exc, tstep, radius=None, inhib=True,
               start_node_list=[(0,0)], thresh=1, seed=None):
    if radius is None:
        radius = tstep
    lattice = EiLattice2d(radius)
    nbr_set = set()

    for start_node in start_node_list:
        start_idx = lattice.get_node_idx(start_node)
        lattice.set_node_state(start_idx, 1, 0)
        lattice.set_node_type(start_idx,sample_node_type(p_exc, seed))
        nbrs = connect_neighbours(lattice, start_idx, p, inhib, seed)
        nbr_set.update(nbrs)

    for t in np.arange(1,tstep+1):
        next_nbr_set = set()
        for node in nbr_set:
            state = update_state(lattice, node, t, thresh)
            if state and t < tstep:
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
    if p == 1:
        edge_state = 1
    else:
        if seed.random() < p:
            edge_state = 1
        else:
            edge_state = 0
    return edge_state


@random_state(4)
def connect_neighbours(lattice, node, p, inhib=True, seed=None):
    nbr_list = []
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


def update_state(lattice, node, tstep, thresh=1):
    state = lattice.get_node_latent_state(node) >= thresh
    if state:
        lattice.set_node_state(node, state, tstep)
    return state
