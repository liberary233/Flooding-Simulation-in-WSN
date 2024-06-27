import matplotlib.pyplot as plt
import networkx as nx

def plot_nodes(nodes, source_node, destination_node):
    G = nx.DiGraph()
    num_nodes = nodes.shape[0]
    for i in range(num_nodes):
        G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))
    
    pos = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(8, 8))
    
    nx.draw_networkx_nodes(G, pos, node_size=30, node_color='blue', ax=ax)
    
    # 绘制源节点和目的节点
    ax.scatter(nodes[source_node, 0], nodes[source_node, 1], c='palegreen', s=200, edgecolors='black', label='Source Node', marker='^', zorder=5)
    ax.scatter(nodes[destination_node, 0], nodes[destination_node, 1], c='pink', s=200, edgecolors='black', label='Destination Node', marker='^', zorder=5)
    
    ax.legend()
    ax.set_title('Generated Node Graph')
    
    return fig
