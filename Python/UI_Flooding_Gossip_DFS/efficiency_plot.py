import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_efficiency_comparison(nodes):
    num_nodes = nodes.shape[0]
    radius = 4

    distances = np.linalg.norm(nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :], axis=-1)
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and distances[i, j] <= radius:
                G.add_edge(i, j, weight=distances[i, j])

    lengths, paths = nx.single_source_dijkstra(G, 0)
    
    fig, ax = plt.subplots()

    nodes_list = list(range(num_nodes))
    time_values = [lengths[node] for node in nodes_list]
    hop_values = [len(paths[node]) - 1 for node in nodes_list]

    ax.plot(nodes_list, time_values, marker='o', linestyle='-', color='b', label='Time')
    ax.plot(nodes_list, hop_values, marker='x', linestyle='--', color='r', label='Hops')

    ax.set_xlabel('Node Index')
    ax.set_ylabel('Value')
    ax.set_title('Path Efficiency Comparison')
    ax.legend()
    ax.grid(True)
    
    return fig
