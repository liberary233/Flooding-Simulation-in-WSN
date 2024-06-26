import numpy as np
from config import config

def generate_nodes():
    num_nodes=config['num_nodes']
    area_size=config['area_size']
    nodes = np.random.rand(num_nodes, 2) * area_size
    source_node = np.random.randint(0, num_nodes)
    destination_node = np.random.randint(0, num_nodes)
    while destination_node == source_node:
        destination_node = np.random.randint(0, num_nodes)
    
    np.savez('nodes.npz', nodes=nodes, source_node=source_node, destination_node=destination_node)
    return nodes, source_node, destination_node

def load_nodes():
    data = np.load('nodes.npz')
    return data['nodes'], data['source_node'], data['destination_node']
