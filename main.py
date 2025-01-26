from src.classes.Network import Network
import os
import networkx as nx
import matplotlib.pyplot as plt


sibra = Network(os.path.join(os.path.dirname(__file__), 'src/data/sibra'))
exemple = Network(os.path.join(os.path.dirname(__file__), 'src/data/exemple'))


def draw_graph(network):        
    def margin_name(name, margin=3):
        return " " * margin + name
    
    G = nx.DiGraph()

    for stop in network.getAllStops():
        G.add_node(margin_name(stop.name))
        G.nodes[margin_name(stop.name)]['size'] = 100 * len(stop.line)
        
        for next_stop, line in stop.next:
            G.add_edge(margin_name(stop.name), margin_name(next_stop.name), color=line.color)
        for previous_stop, line in stop.previous:
            G.add_edge(margin_name(stop.name), margin_name(previous_stop.name), color=line.color)
        
    node_sizes = [G.nodes[node]['size'] for node in G.nodes]
    edge_colors = nx.get_edge_attributes(G, 'color').values()
        
    pos = nx.spring_layout(G)
            
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="white")
    nodes.set_edgecolor('black')
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=5, arrows=False)
    nx.draw_networkx_labels(G, pos, font_size=8, verticalalignment='bottom', horizontalalignment='left')
    
    legend_labels = {line.color: line.name for line in network.lines}
    for color, name in legend_labels.items():
        plt.plot([], [], color=color, label=name)
        plt.legend(loc='lower left')

    plt.show()


# exemple.lines[0].color = 'b'
# exemple.lines[1].color = 'r'
# exemple.lines[2].color = 'g'
# draw_graph(exemple)

sibra.lines[0].color = 'g'
sibra.lines[1].color = 'r'
sibra.lines[2].color = 'b'
draw_graph(sibra)

###############################################################


import tkinter as tk
from src.gui.MainWindow import MainWindow

root = tk.Tk()
app = MainWindow(root)
root.mainloop()