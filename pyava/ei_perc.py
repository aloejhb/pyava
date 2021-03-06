import numpy as np
import networkx as nx
from tqdm import tqdm


def get_start_nodes(nb_start_nodes):
    start_nodes = np.arange(nb_start_nodes)
    return start_nodes

def ei_perc(graph, start_nodes=[0], thresh=1):
    graph_act = nx.create_empty_copy(graph, with_data=True)
    graph_act = graph_act.to_directed()

    nb_nodes = graph_act.number_of_nodes()
    nx.set_node_attributes(graph_act, 0, 'state')
    nx.set_node_attributes(graph_act, 0, 'sum_input')
    nx.set_node_attributes(graph_act, nb_nodes+1, 'active_time')
    nx.set_edge_attributes(graph_act, 0, 'explored')
    nx.set_edge_attributes(graph_act, 0, 'etype')

    nb_start_nodes = len(start_nodes)
    newly_activated_nodes = start_nodes
    for node in newly_activated_nodes:
        graph_act.nodes[node]['state'] = 1
        graph_act.nodes[node]['active_time'] = 0
    for t in range(nb_nodes-nb_start_nodes):
        active_children = []
        for node in newly_activated_nodes:
            node_type = graph_act.nodes[node]['ntype']
            children = graph.neighbors(node)
            for child in children:
                if graph_act.nodes[child]['state'] == 1:
                    next
                else: # child.state == 0
                    graph_act.add_edge(node, child)
                    graph_act[node][child]['etype'] = node_type
                    graph_act.nodes[child]['sum_input'] = graph_act.nodes[child]['sum_input'] + node_type
                    if graph_act.nodes[child]['sum_input'] >= thresh:
                        graph_act.nodes[child]['state'] = 1
                        graph_act.nodes[child]['active_time'] = t+1
                        active_children.append(child)
        newly_activated_nodes = active_children
        if len(newly_activated_nodes) == 0:
            break

    return graph_act


def iterate_start_node_ei_perc(graph, thresh=1):
    graph_act_list = []
    for node in tqdm(graph.nodes):
        graph_act = ei_perc(graph, start_nodes=[node], thresh=thresh)
        graph_act_list.append(graph_act)
    return graph_act_list


def get_active_nodes(graph_act):
    try:
        state_dict= nx.get_node_attributes(graph_act, 'state')
    except:
        import pdb; pdb.set_trace()


    active_nodes = [k for k,v in state_dict.items() if v == 1]
    return active_nodes
# time_dict = nx.get_node_attributes(graph_act, 'active_time')
# plt.plot(time_dict.values())
# print(xx)
# print(len(xx))


def get_explored_edges(graph_act):
    exp_edges = [(u,v) for u,v,d in graph_act.edges(data=True)
                 if d['explored'] == 1]
    return exp_edges


def get_activated_nodes_before_t(graph_act, t):
    nodes = [u for u,d in graph_act.nodes(data=True)
             if d['active_time'] <= t]
    return nodes


def get_cluster_size(graph_act):
    active_nodes = get_active_nodes(graph_act)
    return len(active_nodes)

def get_cluster_size_list(graph_act_list):
    cluster_size_list = [get_cluster_size(g) for g in graph_act_list]
    return np.array(cluster_size_list)


def get_perc_proba(graph_act_list, prop_thresh=0.95):
    cs_list = get_cluster_size_list(graph_act_list)
    nb_nodes = graph_act_list[0].number_of_nodes()
    size_thresh = prop_thresh * nb_nodes
    perc_proba = sum(cs_list>size_thresh)/len(cs_list)
    return perc_proba


def get_perc_proba_from_cs(cluster_size_list, nb_nodes, prop_thresh=0.95):
    size_thresh = prop_thresh * nb_nodes
    perc_proba = sum(cs_list>size_thresh)/len(cs_list)
    return perc_proba
