import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from node_generator import generate_nodes, load_nodes
from flooding import plot_flooding
from gossip import plot_gossip
from efficiency_plot import plot_efficiency_comparison
from plot_nodes import plot_nodes

# 用于存储加载的节点图及其源节点和目的节点
nodes = None
source_node = None
destination_node = None

def load_and_display_nodes():
    global nodes, source_node, destination_node
    nodes, source_node, destination_node = load_nodes()
    print("Loaded nodes:", nodes)  # 调试信息
    print("Source node:", source_node, "Destination node:", destination_node)  # 调试信息

def display_plot(fig):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def show_flooding_simulation():
    if nodes is None:
        load_and_display_nodes()
    fig, _ = plot_flooding(nodes, source_node, destination_node)
    display_plot(fig)

def show_gossip_simulation():
    if nodes is None:
        load_and_display_nodes()
    fig, _ = plot_gossip(nodes, source_node, destination_node)
    display_plot(fig)

def show_efficiency_comparison():
    if nodes is None:
        load_and_display_nodes()
    fig = plot_efficiency_comparison(nodes)
    display_plot(fig)

def generate_new_nodes():
    global nodes, source_node, destination_node
    nodes, source_node, destination_node = generate_nodes()
    print("Generated nodes:", nodes)  # 调试信息
    print("Source node:", source_node, "Destination node:", destination_node)  # 调试信息
    fig = plot_nodes(nodes, source_node, destination_node)
    display_plot(fig)
    print("新节点图生成完成！")

def close_program():
    root.quit()
    root.destroy()

root = tk.Tk()
root.title("Network Simulation")

# 按钮框架
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, fill=tk.X)

btn_flooding = tk.Button(button_frame, text="Flooding 仿真图显示", command=show_flooding_simulation)
btn_flooding.pack(side=tk.LEFT)

btn_gossip = tk.Button(button_frame, text="Gossip 仿真图显示", command=show_gossip_simulation)
btn_gossip.pack(side=tk.LEFT)

btn_efficiency = tk.Button(button_frame, text="运行效率曲线", command=show_efficiency_comparison)
btn_efficiency.pack(side=tk.LEFT)

btn_generate_nodes = tk.Button(button_frame, text="生成新节点图", command=generate_new_nodes)
btn_generate_nodes.pack(side=tk.LEFT)

btn_close_program = tk.Button(button_frame, text="关闭程序", command=close_program)
btn_close_program.pack(side=tk.RIGHT)

# 图像显示框架
plot_frame = tk.Frame(root)
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
