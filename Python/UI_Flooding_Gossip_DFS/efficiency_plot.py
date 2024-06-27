import numpy as np
import matplotlib.pyplot as plt
import random
from flooding import plot_flooding
from gossip import plot_gossip

# 初始化数据结构
data = {
    'flooding': {
        'destination_time': [],
        'destination_hops': [],
        'all_time': [],
        'all_hops': [],
        'redundant_transmissions': []
    },
    'gossip': {
        'destination_time': [],
        'destination_hops': [],
        'all_time': [],
        'all_hops': [],
        'redundant_transmissions': []
    }
}

def collect_data(nodes, source_node, destination_node):
    # Flooding数据收集
    _, flooding_results = plot_flooding(nodes, source_node, destination_node)
    data['flooding']['destination_time'].append(flooding_results['destination_time'])
    data['flooding']['destination_hops'].append(flooding_results['destination_hops'])
    data['flooding']['all_time'].append(flooding_results['all_time'])
    data['flooding']['all_hops'].append(flooding_results['all_hops'])
    data['flooding']['redundant_transmissions'].append(flooding_results['redundant_transmissions'])

    # Gossip数据收集
    _, gossip_results = plot_gossip(nodes, source_node, destination_node)
    data['gossip']['destination_time'].append(gossip_results['destination_time'])
    data['gossip']['destination_hops'].append(gossip_results['destination_hops'])
    data['gossip']['all_time'].append(gossip_results['all_time'])
    data['gossip']['all_hops'].append(gossip_results['all_hops'])
    data['gossip']['redundant_transmissions'].append(gossip_results['redundant_transmissions'])

def plot_efficiency_comparison(nodes):
    source_node = random.randint(0, len(nodes) - 1)
    destination_node = random.randint(0, len(nodes) - 1)
    while destination_node == source_node:
        destination_node = random.randint(0, len(nodes) - 1)

    # 收集数据
    collect_data(nodes, source_node, destination_node)

    # 绘制对比图
    fig, axs = plt.subplots(3, 2, figsize=(15, 15))
    
    # 数据传输到目的节点的最短时间
    axs[0, 0].boxplot([data['flooding']['destination_time'], data['gossip']['destination_time']], labels=['Flooding', 'Gossip'])
    axs[0, 0].set_title('Time to Destination Node')
    
    # 数据传输到目的节点的最短跳数
    axs[0, 1].boxplot([data['flooding']['destination_hops'], data['gossip']['destination_hops']], labels=['Flooding', 'Gossip'])
    axs[0, 1].set_title('Hops to Destination Node')
    
    # 数据传输到全图的最短时间
    axs[1, 0].boxplot([data['flooding']['all_time'], data['gossip']['all_time']], labels=['Flooding', 'Gossip'])
    axs[1, 0].set_title('Time to All Nodes')
    
    # 数据传输到全图的最短跳数
    axs[1, 1].boxplot([data['flooding']['all_hops'], data['gossip']['all_hops']], labels=['Flooding', 'Gossip'])
    axs[1, 1].set_title('Hops to All Nodes')
    
    # 冗余传输数量
    axs[2, 0].boxplot([data['flooding']['redundant_transmissions'], data['gossip']['redundant_transmissions']], labels=['Flooding', 'Gossip'])
    axs[2, 0].set_title('Redundant Transmissions')
    
    plt.tight_layout()
    return fig
