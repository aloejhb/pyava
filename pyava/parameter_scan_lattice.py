import os
import glob
import json
import numpy as np
import pickle
import multiprocessing as mp
import itertools
from functools import partial
from tqdm import tqdm
from networkx.utils.decorators import random_state
from .ei_perc_lattice import ei_perc_2d, EiLattice2d


@random_state(4)
def parameter_scan(par_list, mesh_list, fixed_par, run_func,
                   seed=None, outdir='', parallel=False):
    if parallel:
        pool = mp.Pool()
    if not os.path.exists(outdir):
        raise OSError('Output dir does not exists! {}'.format(outdir))
    mesh1 = mesh_list[0]
    mesh2 = mesh_list[1]


    scan_par = dict(par_list=par_list,
                    mesh_list=np.array(mesh_list).tolist(),
                    fixed_par=fixed_par,
                    run_func_name=run_func.__name__)
    scan_par_path = os.path.join(outdir, 'scan_par.json')
    with open(scan_par_path, 'w') as outfile:
        json.dump(scan_par, outfile)

    param_iter = itertools.product(enumerate(mesh1),
                                   enumerate(mesh2))
    if parallel:
        pool.map(partial(use_par, outdir, seed, fixed_par, par_list, run_func),
                 param_iter)
        pool.close()
    else:
        res_list = list(map(partial(use_par, outdir, seed, fixed_par, par_list, run_func),
                            param_iter))
        # TODO
        # [[use_par((j, p1), (k, p2)) for j, p1 in enumerate(mesh1)]
        #  for k, p2 in enumerate(mesh2)]


def use_par(outdir, seed, fixed_par, par_list, run_func, pp):
    j, p1 = pp[0]
    k, p2 = pp[1]
    print('{:d} {:d}'.format(j, k))
    res_name = 'j_{:03d}_k_{:03d}'.format(j, k)
    subdir = os.path.join(outdir, res_name)
    if not os.path.exists(subdir):
        os.mkdir(subdir)
    par_dict = {par_list[0]: p1, par_list[1]: p2,
                'seed': seed,
                'outdir': subdir}
    par_dict = {**fixed_par, **par_dict}
    res = run_func(**par_dict)
    return res




@random_state(5)
def run_ei_perc_2d(nb_repeats, p, p_exc, tstep, inhib=True,
                   seed=None, outdir=None):
    for r in tqdm(range(nb_repeats)):
        lattice = ei_perc_2d(p, p_exc, tstep, inhib, seed)
        fname = '{:03d}.pkl'.format(r)
        fpath = os.path.join(outdir, fname)
        with open(fpath, 'wb') as fout:
            pickle.dump(lattice, fout)

def load_scan_par(indir):
    with open(os.path.join(indir, 'scan_par.json')) as f:
        scan_par = json.load(f)
    return scan_par


def get_cluster_size_mat(indir):
    with open(os.path.join(indir, 'scan_par.json')) as f:
        scan_par = json.load(f)
    mesh_list = scan_par['mesh_list']
    m1 = len(mesh_list[0])
    m2 = len(mesh_list[1])


    def get_cs(j, k):
        res_name = 'j_{:03d}_k_{:03d}'.format(j, k)
        subdir = os.path.join(indir, res_name)
        files = glob.glob(os.path.join(subdir, '*.pkl'))
        cluster_list = [get_cluster_size(f) for f in files]
        return cluster_list

    cluster_size_mat = [[get_cs(j, k) for j in range(m1)] for
                        k in range(m2)]

    return np.array(cluster_size_mat), scan_par


def get_cluster_size(lattice_file):
    with open(lattice_file, 'rb') as fin:
        lattice = pickle.load(fin)
    return np.sum(lattice.node_state_mat)


def get_scan_prop_mat(indir, prop_func):
    with open(os.path.join(indir, 'scan_par.json')) as f:
        scan_par = json.load(f)
    mesh_list = scan_par['mesh_list']
    m1 = len(mesh_list[0])
    m2 = len(mesh_list[1])


    def get_prop_list(j, k):
        res_name = 'j_{:03d}_k_{:03d}'.format(j, k)
        subdir = os.path.join(indir, res_name)
        files = glob.glob(os.path.join(subdir, '*.pkl'))
        prop_list = [get_prop_from_file(f, prop_func) for f in files]
        return prop_list

    prop_mat = [[get_prop_list(j, k) for j in range(m1)] for
                        k in range(m2)]

    return np.array(prop_mat), scan_par


def get_prop_from_file(lattice_file, prop_func):
    with open(lattice_file, 'rb') as fin:
        lattice = pickle.load(fin)
    return prop_func(lattice)


def get_perc_proba(lattice):
    pass


def get_bounding_box(lat):
    active_node = np.array(np.where(lat.node_state_mat))- lat.radius
    bb = np.vstack((np.min(active_node, axis=1), np.max(active_node, axis=1)))
    return bb


def get_reach(lat):
    bb = get_bounding_box(lat)
    return np.max(np.abs(bb))
