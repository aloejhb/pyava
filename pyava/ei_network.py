import numpy as np
from networkx.utils.decorators import py_random_state


def get_neighbours(node):
    x, y = node
    neighbours = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return neighbours

def node_activation(parents, type_dict):
    ntypes = [type_dict[p] for p in parents]
    return sum(ntypes) > 0

def sample_node_type(p_exc, seed):
    if seed.random() < p_exc:
        ntype = 1
    else:
        ntype = -1
    return ntype

def edge_activation(node, ntype, p, q, seed):
    if ntype == 1:
        p_act = p
    else:
        p_act = q
    if seed.random() < p_act:
        edge_state = 1
    else:
        edge_state = 0
    return edge_state


def activate_neighbours(node, ntype, p, q, parents, seed):
    neighbours = get_neighbours(node)
    new_nbrs = set(neighbours) - set(parents)
    activated_nbrs = []
    for nbr in new_nbrs:
        if edge_activation(node, ntype, p, q, seed):
            activated_nbrs.append(nbr)
    return activated_nbrs


def update_parent_dict(parent_dict, act_nbrs, parent):
    for nbr in act_nbrs:
        if nbr in parent_dict.keys():
            parent_dict[nbr].append(parent)
        else:
            parent_dict[nbr] = [parent]
    return parent_dict


@py_random_state(5)
def ei_perc_2d(p_exc, p, q, tstep, refract_period=np.inf, seed=None):
    start_node = (0, 0)
    start_ntype = 1
    type_dict = {start_node: start_ntype}
    act_nbrs = activate_neighbours(start_node, start_ntype, p, q, [], seed)
    parent_dict = dict(zip(act_nbrs, [[start_node]] * len(act_nbrs)))
    parent_dict_list = [{start_node: start_node}, parent_dict]
    if refract_period == np.inf:
        visited_nodes = [start_node, *act_nbrs]
    for t in np.arange(1,tstep+1):
        parent_dict =  parent_dict_list[t]
        if len(parent_dict) == 0:
            break
        next_parent_dict = {}
        for node in parent_dict.keys():
            if node not in type_dict.keys():
                ntype = sample_node_type(p_exc, seed)
                type_dict.update({node: ntype})
            else:
                ntpye = type_dict[node]
            parents = parent_dict[node]
            if node_activation(parents, type_dict):
                if refract_period == np.inf:
                    excluded_nbrs = visited_nodes
                else:
                    excluded_nbrs = parent_dict_list[t-1].keys()
                act_nbrs = activate_neighbours(node, ntype, p, q,
                                               excluded_nbrs, seed)
                next_parent_dict = update_parent_dict(next_parent_dict,
                                                      act_nbrs, node)
                if refract_period == np.inf:
                    visited_nodes.extend(act_nbrs)

        parent_dict_list.append(next_parent_dict)
    return parent_dict_list


# @py_random_state(3)
# def ed_perc_2d(p_exc, p, tstep, seed=None):
#     q = 0 # dummy parameter for inhibition
#     start_node = (0, 0)
#     start_ntype = 1
#     type_dict = {start_node: start_ntype}
#     act_nbrs = activate_neighbours(start_node, start_ntype, p, q, [], seed)
#     parent_dict = dict(zip(act_nbrs, [[start_node]] * len(act_nbrs)))
#     parent_dict_list = [parent_dict]
#     for t in range(tstep-1):
#         parent_dict =  parent_dict_list[t]
#         if len(parent_dict) == 0:
#             break
#         next_parent_dict = {}
#         for node in parent_dict.keys():
#             if node not in type_dict.keys():
#                 ntype = sample_node_type(p_exc, seed)
#                 type_dict.update({node: ntype})
#             else:
#                 ntpye = type_dict[node]
#             parents = parent_dict[node]
#             if ntype == 1:
#                 act_nbrs = activate_neighbours(node, ntype, p, q, [], seed)
#                 next_parent_dict = update_parent_dict(next_parent_dict,
#                                                       act_nbrs, node)
#         parent_dict_list.append(next_parent_dict)
#     return parent_dict_list
