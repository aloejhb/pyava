import numpy as np


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
