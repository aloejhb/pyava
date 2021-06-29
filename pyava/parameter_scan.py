import numpy as np
from networkx.utils.decorators import random_state
from .graph_generators import er_graph_dale
from .ei_perc import iterate_start_node_ei_perc


@random_state(4)
def parameter_scan(par_list, mesh_list, fixed_par, run_net_func, seed=None):
    mesh1 = mesh_list[0]
    mesh2 = mesh_list[1]

    def use_par(j, p1, k, p2):
        print('{:d} {:d}'.format(j, k))
        par_dict = {par_list[0]: p1, par_list[1]: p2}
        par_dict = {**fixed_par, **par_dict}
        res = run_net_func(**par_dict)
        return res

    results = [[use_par(j, p1, k, p2) for j, p1 in enumerate(mesh1)]
               for k, p2 in enumerate(mesh2)]

    return results


@random_state(5)
def run_ei_perc(nb_nodes, p, p_exc, thresh, nb_instances=1, seed=None):
    gli_list = []
    for j in nb_instances:
        graph = er_graph_dale(nb_nodes, p, p_exc, seed)
        graph_act_list = iterate_start_node_ei_perc(graph, thresh)
        gli_list.append(graph_act_list)
    return gli_list
