import os
import glob
import json
import numpy as np
from tqdm import tqdm
from networkx.utils.decorators import random_state
from .graph_generators import er_graph_dale
from .ei_perc import iterate_start_node_ei_perc, get_cluster_size_list
from .graphio import save_graph_list, read_graph_list


@random_state(4)
def parameter_scan(par_list, mesh_list, fixed_par, run_func,
                   seed=None, outdir=''):
    if not os.path.exists(outdir):
        raise OSError('Output dir does not exists! {}'.format(outdir))
    mesh1 = mesh_list[0]
    mesh2 = mesh_list[1]

    def use_par(j, p1, k, p2):
        print('{:d} {:d}'.format(j, k))
        res_name = 'j_{:03d}_k_{:03d}'.format(j, k)
        par_dict = {par_list[0]: p1, par_list[1]: p2,
                    'seed': seed,
                    'outdir': outdir, 'res_name': res_name}
        par_dict = {**fixed_par, **par_dict}
        res = run_func(**par_dict)
        return res

    for j, p1 in enumerate(mesh1):
        for k, p2 in enumerate(mesh2):
            res = use_par(j, p1, k, p2)

    scan_par = dict(par_list=par_list,
                    mesh_list=mesh_list,
                    fixed_par=fixed_par,
                    run_func_name=run_func.__name__)
    scan_par_path = os.path.join(outdir, 'scan_par.json')
    with open(scan_par_path, 'w') as outfile:
        json.dump(scan_par, outfile)



@random_state(4)
def run_ei_perc(nb_nodes, p, p_exc, thresh, seed=None, outdir=None,
                res_name=''):
    graph = er_graph_dale(nb_nodes, p, p_exc, seed)
    graph_act_list = iterate_start_node_ei_perc(graph, thresh)
    if outdir is not None:
        subdir = os.path.join(outdir, res_name)
        if not os.path.exists(subdir):
            os.mkdir(subdir)
        save_graph_list(graph_act_list, subdir)
    return graph_act_list



def get_cluster_size_mat(indir):
    with open(os.path.join(indir, 'scan_par.json')) as f:
        scan_par = json.load(f)
    mesh_list = scan_par['mesh_list']
    m1 = len(mesh_list[0])
    m2 = len(mesh_list[1])


    def get_cs(j, k):
        res_name = 'j_{:03d}_k_{:03d}'.format(j, k)
        subdir = os.path.join(indir, res_name)
        graph_list = read_graph_list(subdir)
        cluster_list = get_cluster_size_list

    cluster_size_mat = [[get_cs(j, k) for j in tqdm(range(m1))] for
                        k in range(m2)]

    return cluster_size_mat, scan_par
