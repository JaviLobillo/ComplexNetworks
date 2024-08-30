import networkx as nx
import matplotlib.pyplot as plt

def read_LOTR_graph(file_path, id_label):
    graph = nx.Graph()
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            node1, node2, _, _ = line.strip().split(",")
            if node1 not in graph:
                graph.add_node(node1)
            if node2 not in graph:
                graph.add_node(node2)
            if not graph.has_edge(node1, node2):
                graph.add_edge(node1, node2)
    
    #we rename the nodes to have the long names of the nodes
    graph = nx.relabel_nodes(graph, id_label)

    return graph

def read_LOTR_types(file_path):
    label_type = {}
    id_label = {}
    with open(file_path, 'r') as file:
        next(file)
        for line in file:
            if len(line.strip().split()) == 5:
                node, typ, label, _, _ = line.strip().split()
            else:
                node, typ, label, _, _, _ = line.strip().split()
            if typ == 'pla':
                typ = 'Place'
            elif typ == 'per':
                typ = 'Person'
            elif typ == 'gro':
                typ = 'Group'
            elif typ == 'thin':
                typ = 'Thing'

            label_type[label] = typ
            id_label[node] = label
    return id_label, label_type

def plot_graph_lotr(graph, label_type, C, alg, phi):

    #change the size of the plot
    plt.figure(figsize=(10, 10))
    

    #for each type, we use a different node shape
    types = set([label_type[node] for node in graph.nodes]) #Place, Person, Group, Thing
    shapes = {'Place': 'D', 'Person': 's', 'Group': 'p', 'Thing': 'o'}
    pos = nx.spring_layout(graph)

    #We color the nodes differently in the Core and the Periphery
    #We need to create different lists of colors for each type of node
    colors = {}
    for typ in types:
        colors[typ] = []
    for node in graph:
        if node in C:
            colors[label_type[node]].append('gold')
        else:
            colors[label_type[node]].append('tan')

    for typ in types:
        nodelist = [node for node in graph.nodes if label_type[node] == typ]
        nx.draw_networkx_nodes(graph, pos, nodelist=nodelist, node_color = colors[typ],
                               node_shape = shapes[typ], node_size = 200, linewidths=0.5, edgecolors='black')
    nx.draw_networkx_edges(graph, pos, width = 0.1)
    nx.draw_networkx_labels(graph, pos, font_size = 6, font_weight='bold')

    #we add a legend with the node shape meaning, and the symbols have no color in the legend
    shapes = {'Place': 'D', 'Person': 's', 'Group': 'p', 'Thing': 'o'}
    legend_handles = []
    for typ in types:
        legend_handles.append(plt.Line2D([], [], linestyle='None', marker=shapes[typ], markersize=5, label=typ))

    plt.legend(handles=legend_handles, title="Node type", loc='upper right', fontsize=8, title_fontsize=10, markerscale=1.5)

    #we also add to the legend the meaning of the colors
    legend_handles = [plt.Line2D([], [], linestyle='None', marker='o', markersize=5, color='gold', label='Core'),
                      plt.Line2D([], [], linestyle='None', marker='o', markersize=5, color='burlywood', label='Periphery')]
    
    #we add a title
    plt.title('LOTR entities graph with ' + alg + ' algorithm.')

    #finally we add the phi value as a comment to the plot, far away from the bottom
    plt.figtext(0.5, 0.01, 'Phi = ' + str(phi), wrap=True, horizontalalignment='center', fontsize=12, position=(0.5, 0.08))

    plt.show()
