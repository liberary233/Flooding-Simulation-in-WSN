import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# 生成随机节点
num_nodes = 10
area_size = 10
radius = 4
speed = 10

# num_nodes = 50
# area_size = 25
# radius = 10
# speed = 10

# 画图设置
interval = 0.05  # 间隔值变量
pointsize_path = 0.5
linewidth_path = 0.5
k_shortestPath = 5

# 随机生成节点位置
nodes = np.random.rand(num_nodes, 2) * area_size

# 随机选择源节点和目的节点
source_node = random.randint(0, num_nodes - 1)
destination_node = random.randint(0, num_nodes - 1)
while destination_node == source_node:
    destination_node = random.randint(0, num_nodes - 1)

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
lengths = nx.single_source_dijkstra_path_length(G, source_node)

# 找到最长路径的节点（最远节点）
max_distance_node = max(lengths, key=lengths.get)

# 找到从源节点到目的节点和最远节点的最短路径
shortest_path_to_destination = nx.shortest_path(G, source=source_node, target=destination_node, weight='weight')
shortest_path_to_furthest = nx.shortest_path(G, source=source_node, target=max_distance_node, weight='weight')

# 计算从源节点到最远节点的最短路径长度
longest_path_length = lengths[max_distance_node]

# 绘制节点
pos = nx.get_node_attributes(G, 'pos')

# 计算每个节点的时刻
times = {node: lengths[node] / longest_path_length for node in G.nodes()}

# 计算路径上的点数量
num_points = longest_path_length / interval

# 定义一个函数来计算颜色亮度
def get_brightness(color):
    return np.sqrt(0.299 * color[0]**2 + 0.587 * color[1]**2 + 0.114 * color[2]**2)

plt.figure(figsize=(8, 8))

# 连接节点并绘制
for (i, j) in G.edges():
    if times[i] < times[j]:  # 只有 times 值小的节点向 times 值大的节点传送信息
        line_points = np.linspace(nodes[i], nodes[j], int(distances[i, j] / interval))
        for k in range(len(line_points) - 1):
            t = times[i] + (k / num_points)
            color = plt.cm.jet(1 - t)  # 使用1-t以便从红色到蓝色渐变
            plt.plot(line_points[k:k+2, 0], line_points[k:k+2, 1], color=color, marker='o', markersize=pointsize_path, linestyle='-', linewidth=linewidth_path)

        # 在边的中点标注 (i, j)
        mid_point = (nodes[i] + nodes[j]) / 2

# 加粗绘制最短路径到目的节点
for i in range(len(shortest_path_to_destination) - 1):
    start = shortest_path_to_destination[i]
    end = shortest_path_to_destination[i + 1]
    line_points = np.linspace(nodes[start], nodes[end], int(distances[start, end] / interval))
    for k in range(len(line_points) - 1):
        t = times[start] + (k / num_points)
        color = plt.cm.jet(1 - t)  # 使用1-t以便从红色到蓝色渐变
        plt.plot(line_points[k:k+2, 0], line_points[k:k+2, 1], color=color, marker='o', markersize=pointsize_path * k_shortestPath, linestyle='-', linewidth=linewidth_path * k_shortestPath)

# 绘制节点
for i in range(num_nodes):
    color = plt.cm.jet(1 - times[i])
    brightness = get_brightness(color)
    edge_color = 'black' if brightness > 0.5 else 'white'
    nx.draw_networkx_nodes(G, pos, nodelist=[i], node_color=[color], node_size=30, edgecolors=edge_color, linewidths=0.8, node_shape='o')
    plt.text(nodes[i, 0], nodes[i, 1], f'{times[i]:.2f}', fontsize=12, ha='right', va='bottom')

# 绘制源节点和目的节点
plt.scatter(nodes[source_node, 0], nodes[source_node, 1], c='palegreen', s=200, edgecolors='black', label='Source Node', marker='^', zorder=5)
plt.scatter(nodes[destination_node, 0], nodes[destination_node, 1], c='pink', s=200, edgecolors='black', label='Destination Node', marker='^', zorder=5)

plt.legend()
plt.title('Data Transmission Simulation')
plt.show()

# 输出结果
destination_time = lengths[destination_node]
destination_hops = len(shortest_path_to_destination) - 1
all_nodes_time = lengths[max_distance_node]
all_nodes_hops = len(shortest_path_to_furthest) - 1

print(f'目的节点接收到数据的最短时间: {destination_time}')
print(f'目的节点接收到数据的最小跳数: {destination_hops}')
print(f'所有节点均收到数据的最短时间: {all_nodes_time}')
print(f'所有节点均收到数据的最小跳数: {all_nodes_hops}')
