import numpy as np


def perc_motif_2step(edge_vector):
    results_list = []
    start_node = 0
    nbr_list = get_neighbours(start_node, edge_vector)
    nb_nbr = len(nbr_list)
    if nb_nbr == 0:
        state_bvector = 1 # only the starting node is activated
        results = dict(state_bvector=state_bvector)
        results_list.append(results)
        return results_list
    else:
        # Loop over assignments of node types to each neighbour
        for type_vector in range(2**nb_nbr):
            if type_vector == 0: # all neighbours inhibitory:
                state_bvector = 1 # only the starting node is activated
                results = dict(state_bvector=state_bvector,
                               nbr_list = nbr_list,
                               type_vector = type_vector)
                results_list.append(results)
            else:
                state_vector = np.zeros(13, dtype=np.bool_)
                latent_vector = np.zeros(13, dtype=np.int)
                # Activate all neighbours
                next_nbr_set = set()
                for idx, nbr in enumerate(nbr_list):
                    nbr_type = get_node_type(idx, type_vector)# type of this nbr
                    state_vector[nbr] = 1
                    # each neighbour sends signal to its connected nodes
                    next_nbr_list = get_neighbours(nbr, edge_vector)
                    next_nbr_set.update(next_nbr_list)
                    for nnbr in next_nbr_list:
                        latent_vector[nnbr] += (nbr_type - 0.5) * 2
                # Update states of all connected nodes
                active_nnbr = []
                for nnbr in next_nbr_set:
                    state_vector[nnbr] = latent_vector[nnbr] > 0
                    if state_vector[nnbr]:
                        active_nnbr.append(nnbr)
                if len(active_nnbr):
                    # Loop over assignments of node types to
                    # each active next neighbour
                    for next_type_vector in range(2**len(active_nnbr)):
                        state_bvector = convert_vector_to_bnum(state_vector)
                        results = dict(state_bvector=state_bvector,
                                       nbr_list = nbr_list,
                                       active_nnbr = active_nnbr,
                                       type_vector = type_vector,
                                       next_type_vector = next_type_vector)
                        results_list.append(results)
        return results_list


def convert_vector_to_bnum(vector):
    return vector.dot(1 << np.arange(vector.size)[::-1])

def convert_bnum_to_vector(bnum):
    pass

def get_nth_digit(n, bnum):
    return (bnum & (1 << n)) >> n

def get_node_type(node, type_vector):
    return get_nth_digit(node, type_vector)

def get_edge_state(edge, edge_vector):
    return get_nth_digit(edge, edge_vector)

def get_edge_list_from_node(node):
    if node == 0:
        edge_list = np.arange(4)
        to_node_list = [1, 2, 3, 4]
    elif node in [1, 2, 3, 4]:
        edge_list = np.arange(3) + 4 + 3*(node-1)
        if node == 1:
            to_node_list = np.array([9, 5, 8])
        else:
            to_node_list = np.array([10, 6, 5]) + (node-2)
    else:
        raise ValueError('Node must be in 0 to 4')
    return edge_list, to_node_list

def get_neighbours(node, edge_vector):
    edge_list, to_node_list = get_edge_list_from_node(node)
    estate_list = [get_edge_state(e, edge_vector) for e in edge_list]
    estate_list = np.array(estate_list)
    tnlist = to_node_list * estate_list
    nbr_list = tnlist[np.nonzero(tnlist)]
    return nbr_list
