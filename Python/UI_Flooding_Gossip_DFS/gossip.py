import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
from config import config

def plot_gossip(nodes, source_node, destination_node):
    radius = config['radius']
    interval = config['interval']
    pointsize_path = config['pointsize_path']
    linewidth_path = config['linewidth_path']
    k_shortestPath = config['k_shortestPath']
    TTL = config['TTL']
    gossip_probability = config['gossip_probability']

    num_nodes = nodes.shape[0]

    # 计算节点之间的距离
    distances = np.linalg.norm(nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :], axis=-1)

    # 创建有向图
    G = nx.DiGraph()
    for i in range(num_nodes):
        G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))

    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and distances[i, j] <= radius and random.random() < gossip_probability:
                G.add_edge(i, j, weight=distances[i, j])  # 使用距离作为权重

    # 使用Dijkstra算法计算从源节点到所有其他节点的最短路径
    lengths, paths = nx.single_source_dijkstra(G, source_node)

    # 找到最长路径的节点（最远节点）
    max_distance_node = max(lengths, key=lengths.get)

    # 找到从源节点到目的节点和最远节点的最短路径
    shortest_path_to_destination = paths[destination_node] if destination_node in paths else None
    shortest_path_to_furthest = paths[max_distance_node] if max_distance_node in paths else None

    # 计算从源节点到最远节点的最短路径长度
    longest_path_length = lengths[max_distance_node] if max_distance_node in lengths else None

    # 绘制节点
    pos = nx.get_node_attributes(G, 'pos')

    # 计算每个节点的时刻
    times = {node: lengths[node] / longest_path_length for node in G.nodes()} if longest_path_length else {}

    # 计算路径上的点数量
    num_points = longest_path_length / interval if longest_path_length else None

    # 定义一个函数来计算颜色亮度
    def get_brightness(color):
        return np.sqrt(0.299 * color[0]**2 + 0.587 * color[1]**2 + 0.114 * color[2]**2)

    fig, ax = plt.subplots(figsize=(8, 8))

    # 创建一个字典来存储每个节点的TTL
    ttl_dict = {}
    for path in paths.values():
        for idx, node in enumerate(path):
            ttl_dict[node] = max(TTL - idx, 0)

    # 连接节点并绘制
    for (i, j) in G.edges():
        if times.get(i, 1) < times.get(j, 0) and ttl_dict.get(i, 0) > 0:  # 只有 times 值小的节点向 times 值大的节点传送信息且TTL未超限
            if ttl_dict.get(j, 0) > 0:  # 确保目标节点的TTL值大于0
                line_points = np.linspace(nodes[i], nodes[j], int(distances[i, j] / interval))
                for k in range(len(line_points) - 1):
                    t = times[i] + (k / num_points)
                    color = plt.cm.jet(1 - t)  # 使用1-t以便从红色到蓝色渐变
                    ax.plot(line_points[k:k+2, 0], line_points[k:k+2, 1], color=color, marker='o', markersize=pointsize_path, linestyle='-', linewidth=linewidth_path)

    # 检查目的节点是否可达
    if destination_node not in paths:
        print("目的节点不可达")
    else:
        # 加粗绘制最短路径到目的节点
        for i in range(len(shortest_path_to_destination) - 1):
            start = shortest_path_to_destination[i]
            end = shortest_path_to_destination[i + 1]
            line_points = np.linspace(nodes[start], nodes[end], int(distances[start, end] / interval))
            for k in range(len(line_points) - 1):
                t = times[start] + (k / num_points)
                color = plt.cm.jet(1 - t)  # 使用1-t以便从红色到蓝色渐变
                ax.plot(line_points[k:k+2, 0], line_points[k:k+2, 1], color=color, marker='o', markersize=pointsize_path * k_shortestPath, linestyle='-', linewidth=linewidth_path * k_shortestPath)

    # 绘制节点
    for i in range(num_nodes):
        color = plt.cm.jet(1 - times.get(i, 1))
        brightness = get_brightness(color)
        edge_color = 'black' if brightness > 0.5 else 'white'
        nx.draw_networkx_nodes(G, pos, nodelist=[i], node_color=[color], node_size=30, edgecolors=edge_color, linewidths=0.8, node_shape='o', ax=ax)
        ax.text(nodes[i, 0], nodes[i, 1], f'TTL:{ttl_dict.get(i, 0)}', fontsize=12, ha='right', va='bottom')  # 显示TTL值

    # 绘制源节点和目的节点
    ax.scatter(nodes[source_node, 0], nodes[source_node, 1], c='palegreen', s=200, edgecolors='black', label='Source Node', marker='^', zorder=5)
    ax.scatter(nodes[destination_node, 0], nodes[destination_node, 1], c='pink', s=200, edgecolors='black', label='Destination Node', marker='^', zorder=5)

    ax.legend()
    ax.set_title('Data Transmission Simulation (Gossip)')

    # 输出结果
    if destination_node in paths:
        destination_time = lengths[destination_node]
        destination_hops = len(shortest_path_to_destination) - 1
        all_nodes_time = lengths[max_distance_node]
        all_nodes_hops = len(shortest_path_to_furthest) - 1

        print(f'目的节点接收到数据的最短时间: {destination_time}')
        print(f'目的节点接收到数据的最小跳数: {destination_hops}')


        # 检查是否能全图广播
        can_broadcast = all(ttl_dict[node] > 0 for node in G.nodes())

        if not can_broadcast:
            print("不能全图广播")
        else:
            print(f'所有节点均收到数据的最短时间: {all_nodes_time}')
            print(f'所有节点均收到数据的最小跳数: {all_nodes_hops}')

    # 返回数据字典
    gossip_data = {}
    if destination_node in paths:
        destination_time = lengths[destination_node]
        destination_hops = len(shortest_path_to_destination) - 1
        all_nodes_time = lengths[max_distance_node]
        all_nodes_hops = len(shortest_path_to_furthest) - 1

        can_broadcast = all(ttl_dict[node] > 0 for node in G.nodes())

        gossip_data = {
            'destination_time': destination_time,
            'destination_hops': destination_hops,
            'all_time': all_nodes_time if can_broadcast else float('inf'),
            'all_hops': all_nodes_hops if can_broadcast else float('inf'),
            'redundant_transmissions': len(G.edges)
        }
    else:
        gossip_data = {
            'destination_time': float('inf'),
            'destination_hops': float('inf'),
            'all_time': float('inf'),
            'all_hops': float('inf'),
            'redundant_transmissions': len(G.edges)
        }

    return fig, gossip_data
