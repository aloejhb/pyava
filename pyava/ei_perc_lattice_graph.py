from networkx.utils.decorators import py_random_state
@random_state(3)
def ei_perc_2d(p_exc, p, tstep, seed=None):


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


def connect_neighbours(graph, node, p, seed):
    nbr_list = []
    for node, nbr, d in graph.get_edges(node, data=True):
        if graph.nodes[nbr]['state'] == 0:
            edge_state = activate_edge(p)
            d['state'] = edge_state
            if edge_state:
                nbr_list.append(nbr)
    return nbr_list


def update_state(graph, node):
    latent_state = 0
    for node, nbr, d  in graph.get_edges(node, data=True):
        latent_state += d['state'] * graph.nodes[nbr]['ntype']
        graph.nodes[nbr]['state'] = 1
    return latent_state



@random_state(4)
def ei_perc(graph, p_exc, p, tstep, seed=None):
    graph.set_edge_attributes('state', 0)
    start_node = (0, 0)
    graph.nodes[start_node]['state'] = 1
    graph.nodes[start_node]['ntype'] = 1
    nbr_list = connect_neighbours(graph, start_node, p, seed)
    for t in range(tstep):
        next_nbr_list = []
        for node in nbr_list:
            state = update_state(graph, node)
            if state:
                graph.nodes[node]['ntype'] = sample_node_type(p_exc, seed)
                nbrs = connect_neighbours(graph, node, p, seed)
                next_nbr_list.extend(nbrs)
        nbr_list = next_nbr_list
