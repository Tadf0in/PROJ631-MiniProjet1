from Network import Network
import networkx as nx
import matplotlib.pyplot as plt

sibra = Network('data/sibra/')
exemple = Network('data/exemple/')

print(exemple.getAllStops())
print(sibra.getAllStops())


def draw_graph(network):
    G = nx.DiGraph()

    for stop in network.getAllStops():
        G.add_node(stop.name)
        for next_stop, line in stop.next:
            G.add_edge(stop.name, next_stop.name, color=line.color)
        for previous_stop, line in stop.previous:
            G.add_edge(stop.name, previous_stop.name, color=line.color)
            
    colors = nx.get_edge_attributes(G, 'color').values()
            
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, 
            edge_color=colors,
            node_size=500, 
            node_color="skyblue", 
            font_size=10, 
            font_weight="bold",
            arrows=True
        )
    plt.show()
    
# exemple.lines[0].color = 'b'
# exemple.lines[1].color = 'r'
# exemple.lines[2].color = 'g'
# draw_graph(exemple)

sibra.lines[0].color = 'g'
sibra.lines[1].color = 'r'
sibra.lines[2].color = 'b'
draw_graph(sibra)