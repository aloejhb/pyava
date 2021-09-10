import os
import glob
import networkx as nx
import pickle

def save_graph_list(graph_list, outdir):
    for j, graph in enumerate(graph_list):
        gname = '{:03d}.gexf'.format(j)
        nx.write_gexf(graph, os.path.join(outdir, gname))


def read_graph_list(indir):
    flist = glob.glob(os.path.join(indir,'*.gexf'))
    graph_list = [nx.read_gexf(f) for f in flist]
    return graph_list


def read_lattice(lattice_file):
    with open(lattice_file, 'rb') as fin:
        lattice = pickle.load(fin)
    return lattice
