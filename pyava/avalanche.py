import numpy as np
from tqdm import tqdm
from networkx.utils.decorators import py_random_state


def activation_movie(parent_dict_list, box_diam, start_node=(0,0)):
    tstep = len(parent_dict_list)
    box_width = box_diam*2 + 1
    box = np.zeros((tstep, box_width, box_width))
    for t, parent_dict in enumerate(parent_dict_list):
        act_nodes = parent_dict.keys()
        if len(act_nodes) == 0:
            break
        coords = np.array(list(act_nodes))
        if np.any(np.abs(coords) > box_diam):
            raise ValueError('Box diameter is too small to contain all active nodes')
        coords = coords + box_diam
        box[np.ones(len(coords)).astype(int) * t,
            coords[:,0].astype(int),
            coords[:,1].astype(int)] = 1
    return box

def activation_cluster(parent_dict_list, box_diam, start_node=(0,0)):
    tstep = len(parent_dict_list)
    box_width = box_diam*2 + 1
    box = np.zeros((box_width, box_width))
    for t, parent_dict in enumerate(parent_dict_list):
        act_nodes = parent_dict.keys()
        if len(act_nodes) == 0:
            break
        coords = np.array(list(act_nodes))
        if np.any(np.abs(coords) > box_diam):
            raise ValueError('Box diameter is too small to contain all active nodes')
        coords = coords + box_diam
        box[coords[:,0].astype(int),
            coords[:,1].astype(int)] = 1
    return box


@py_random_state(3)
def run_network(network_func, param, nb_repeats, seed=None):
    cluster_list = []
    param.update(dict(seed=seed))
    for r in tqdm(range(nb_repeats)):
        parent_dict_list = network_func(**param)
        cluster_list.append(parent_dict_list)
    return cluster_list


flatten = lambda t: [item for sublist in t for item in sublist]
def extract_visited_nodes(cluster):
    """
    Returns a list of visited nodes of a cluster.
    Parameters
    ----------
    cluster: list of parent_dict (the same as parent_dict_list)
    """
    nodes = set(flatten([parent_dict.keys() for parent_dict in cluster]))
    return nodes


def compute_cluster_size(cluster):
    """
    Returns size of a cluster.
    Parameters
    ----------
    cluster: list of parent_dict (the same as parent_dict_list)
    """
    vnodes = extract_visited_nodes(cluster)
    return len(vnodes)


def compute_cluster_dur(cluster):
    """
    Returns duration of a cluster.
    Parameters
    ----------
    cluster: list of parent_dict (the same as parent_dict_list)
    """
    return len(cluster)
