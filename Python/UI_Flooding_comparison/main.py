import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from flood_protocol_simulation import plot_flood_protocol_simulation
from Python.UI_Flooding_comparison.path_efficiency_comparison import plot_path_efficiency_comparison

def show_flood_protocol_simulation():
    fig = plot_flood_protocol_simulation()
    display_plot(fig)

def show_path_efficiency_comparison():
    fig = plot_path_efficiency_comparison()
    display_plot(fig)

def display_plot(fig):
    for widget in frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

root = tk.Tk()
root.title("Network Simulation")

frame = tk.Frame(root)
frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

btn1 = tk.Button(root, text="泛洪协议传输过程仿真", command=show_flood_protocol_simulation)
btn1.pack(side=tk.LEFT)

btn2 = tk.Button(root, text="查找路径节点运行效率曲线对比", command=show_path_efficiency_comparison)
btn2.pack(side=tk.RIGHT)

root.mainloop()
