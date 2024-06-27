import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

def plot_dfs(nodes, radius=4):
    num_nodes = nodes.shape[0]
    distances = np.linalg.norm(nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :], axis=-1)
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and distances[i, j] <= radius:
                G.add_edge(i, j, weight=distances[i, j])

    pos = nx.get_node_attributes(G, 'pos')
    dfs_edges = list(nx.dfs_edges(G, source=0))
    dfs_G = nx.DiGraph(dfs_edges)
    for node in dfs_G.nodes():
        dfs_G.nodes[node]['pos'] = G.nodes[node]['pos']
    
    fig, ax = plt.subplots()
    nx.draw(dfs_G, pos, ax=ax, with_labels=True, node_size=300, node_color="orange", font_size=10, font_color="black")
    ax.set_title('DFS Algorithm')
    return fig
