import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

def plot_path_efficiency_comparison():
    num_nodes = 10
    area_size = 10
    radius = 4

    # 随机生成节点位置
    nodes = np.random.rand(num_nodes, 2) * area_size

    # 随机选择源节点和目的节点
    source_node = random.randint(0, num_nodes - 1)

    # 计算节点之间的距离
    distances = np.linalg.norm(nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :], axis=-1)

    # 创建有向图
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and distances[i, j] <= radius:
                G.add_edge(i, j, weight=distances[i, j])  # 使用距离作为权重

    # 使用Dijkstra算法计算从源节点到所有其他节点的最短路径
    lengths, paths = nx.single_source_dijkstra(G, source_node)

    fig, ax = plt.subplots(figsize=(10, 6))

    # 绘制时间-跳数关系曲线
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
