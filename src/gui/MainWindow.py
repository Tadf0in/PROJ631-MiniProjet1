import tkinter as tk
from src.gui.Menu import Menu
from src.gui.Path import Path
import networkx as nx
import matplotlib.pyplot as plt
from .edit_stop import *

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("BUS")
        
        self.network = None 
        self.selected_line = None
        
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        Menu(self)
        
        self.show_graph_button = tk.Button(self.root, text="Afficher le graphe", command=self.show_graph)
        self.show_graph_button.pack(pady=5)
        
        Path(self)
        
        self.error_message = tk.StringVar()
        self.error_label = tk.Label(self.root, textvariable=self.error_message, fg="red")
        self.error_label.pack()

        self.lines_frame = tk.LabelFrame(self.root, text="Lignes")
        self.lines_frame.pack(fill="both", expand="yes")

        self.lines_listbox = tk.Listbox(self.lines_frame)
        self.lines_listbox.pack(side="left", fill="both", expand=True)

        self.stops_listbox = tk.Listbox(self.lines_frame)
        self.stops_listbox.pack(side="right", fill="both", expand=True)

        self.lines_listbox.bind("<<ListboxSelect>>", lambda event: update_stops_listbox(self))
        
        self.color_frame = tk.Frame(self.root, width=50, height=50, bg="black")
        self.color_frame.pack(pady=10, side="left")
        self.color_frame.bind("<Button-1>", lambda event: change_line_color(self))
        
        self.add_stop_button = tk.Button(self.root, text="+", command=lambda: add_stop(self, self.selected_line))
        self.add_stop_button.pack(pady=5, padx=5, side="right")

        self.remove_stop_button = tk.Button(self.root, text="-", command=lambda: remove_stop(self, self.selected_line))
        self.remove_stop_button.pack(pady=5, padx=5, side="right")

        self.move_up_stop_button = tk.Button(self.root, text="Λ", command=lambda: move_up_stop(self, self.selected_line))
        self.move_up_stop_button.pack(pady=5, padx=5, side="right")

        self.move_down_stop_button = tk.Button(self.root, text="V", command=lambda: move_down_stop(self, self.selected_line))
        self.move_down_stop_button.pack(pady=5, padx=5, side="right")
        
        self.edit_stop_button = tk.Button(self.root, text="Modifier", command=lambda: edit_date_stop(self, self.selected_line))
        self.edit_stop_button.pack(pady=5, padx=5, side="right")
  

    def show_graph(self):
        if not self.network:
            self.error_message.set("Aucun réseau chargé")
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
        
        legend_labels = {line.name: line.color for line in self.network.lines}
        for name, color in legend_labels.items():
            plt.plot([], [], color=color, label=name)
            plt.legend(loc='lower left')

        self.error_message.set("")
        plt.show()
