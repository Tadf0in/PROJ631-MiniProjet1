import tkinter as tk
from src.gui.Menu import Menu
import networkx as nx
import matplotlib.pyplot as plt

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("BUS")
        
        self.network = None 
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.menu = Menu(self)
        
        self.show_graph_button = tk.Button(self.root, text="Afficher le graphe", command=self.show_graph)
        self.show_graph_button.pack()

    def show_graph(self):
        if not self.network:
            print("No network loaded")
            return
            
        def margin_name(name, margin=3):
            return " " * margin + name
        
        G = nx.DiGraph()

        for stop in self.network.getAllStops():
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
        
        legend_labels = {line.color: line.name for line in self.network.lines}
        for color, name in legend_labels.items():
            plt.plot([], [], color=color, label=name)
            plt.legend(loc='lower left')

        plt.show()
