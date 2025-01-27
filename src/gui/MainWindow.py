import tkinter as tk
from tkinter import colorchooser
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
        
        self.error_message = tk.StringVar()
        self.error_label = tk.Label(self.root, textvariable=self.error_message, fg="red")
        self.error_label.pack()

        self.lines_frame = tk.LabelFrame(self.root, text="Lignes")
        self.lines_frame.pack(fill="both", expand="yes")

        self.lines_listbox = tk.Listbox(self.lines_frame)
        self.lines_listbox.pack(side="left", fill="both", expand=True)

        self.stops_listbox = tk.Listbox(self.lines_frame)
        self.stops_listbox.pack(side="right", fill="both", expand=True)

        self.lines_listbox.bind("<<ListboxSelect>>", self.update_stops_listbox)
        
        self.color_frame = tk.Frame(self.root, width=50, height=50, bg="white")
        self.color_frame.pack(pady=10)
        self.color_frame.bind("<Button-1>", self.change_line_color)


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
        

    def update_lines_listbox(self):
        if not self.network:
            self.error_message.set("Aucun réseau chargé")
            return

        self.lines_listbox.delete(0, tk.END)
        for line in self.network.lines:
            self.lines_listbox.insert(tk.END, line.name)
        
        self.error_message.set("")


    def update_stops_listbox(self, event):
        selected_line_index = self.lines_listbox.curselection()
        if not selected_line_index:
            return

        selected_line = self.network.lines[selected_line_index[0]]
        self.stops_listbox.delete(0, tk.END)
        for stop in selected_line.getAllStopsOnLine():
            self.stops_listbox.insert(tk.END, stop.name)
        
        self.color_frame.config(bg=selected_line.color)


    def change_line_color(self, event):
        selected_line_index = self.lines_listbox.curselection()
        if not selected_line_index:
            self.error_message.set("Aucune ligne sélectionnée")
            return

        selected_line = self.network.lines[selected_line_index[0]]
        new_color = colorchooser.askcolor()[1]
        if new_color:
            selected_line.color = new_color
            self.color_frame.config(bg=new_color)
            self.error_message.set("")
