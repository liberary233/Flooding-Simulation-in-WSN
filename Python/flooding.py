import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random

# 生成随机节点
num_nodes = 200
area_size = 100
radius = 15
speed = 15

# 随机生成节点位置
nodes = np.random.rand(num_nodes, 2) * area_size

# 随机选择源节点和目的节点
source_node = random.randint(0, num_nodes - 1)
destination_node = random.randint(0, num_nodes - 1)
while destination_node == source_node:
    destination_node = random.randint(0, num_nodes - 1)

# 计算节点之间的距离
distances = np.linalg.norm(nodes[:, np.newaxis, :] - nodes[np.newaxis, :, :], axis=-1)

# 创建图
G = nx.Graph()
for i in range(num_nodes):
    G.add_node(i, pos=(nodes[i, 0], nodes[i, 1]))

for i in range(num_nodes):
    for j in range(i + 1, num_nodes):
        if distances[i, j] <= radius:
            G.add_edge(i, j)

# 仿真数据传输过程
time_to_receive = np.full(num_nodes, np.inf)
time_to_receive[source_node] = 0
hops_to_receive = np.full(num_nodes, np.inf)
hops_to_receive[source_node] = 0

queue = [(source_node, 0, 0)]
while queue:
    current_node, current_time, current_hops = queue.pop(0)
    neighbors = list(G.neighbors(current_node))
    for neighbor in neighbors:
        if time_to_receive[neighbor] == np.inf:
            time_to_receive[neighbor] = current_time + 1
            hops_to_receive[neighbor] = current_hops + 1
            queue.append((neighbor, current_time + 1, current_hops + 1))

# 绘制节点
pos = nx.get_node_attributes(G, 'pos')
colors = plt.cm.jet((time_to_receive - time_to_receive.min()) / (time_to_receive.max() - time_to_receive.min()))
plt.figure(figsize=(8, 8))

# 连接节点
for (i, j) in G.edges():
    line_points = np.linspace(nodes[i], nodes[j], int(distances[i, j] / 0.1))
    for k in range(len(line_points) - 1):
        t = (time_to_receive[i] + k * 0.1 / distances[i, j] * (time_to_receive[j] - time_to_receive[i])) / time_to_receive.max()
        plt.plot(line_points[k:k+2, 0], line_points[k:k+2, 1], color=plt.cm.jet(t), marker='o', markersize=1, linestyle='-', linewidth=0.5)

# 绘制节点
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=30, node_shape='o')
nx.draw_networkx_edges(G, pos, alpha=0.3)

# 绘制源节点和目的节点
plt.scatter(nodes[source_node, 0], nodes[source_node, 1], c='palegreen', s=200, edgecolors='black', label='Source Node', marker='^', zorder=5)
plt.scatter(nodes[destination_node, 0], nodes[destination_node, 1], c='pink', s=200, edgecolors='black', label='Destination Node', marker='^', zorder=5)

plt.legend()
plt.title('Data Transmission Simulation')
plt.show()

# 输出结果
destination_time = time_to_receive[destination_node]
destination_hops = hops_to_receive[destination_node]
all_nodes_time = time_to_receive.max()
all_nodes_hops = hops_to_receive.max()

print(f'目的节点接收到数据的时间: {destination_time}')
print(f'目的节点接收到数据的跳数: {destination_hops}')
print(f'所有节点均收到数据的时间: {all_nodes_time}')
print(f'所有节点均收到数据的跳数: {all_nodes_hops}')
