import copy
import matplotlib.pyplot as plt
import networkx as nx

def Phi(graph, C):
    E11 = 0
    E12 = 0
    E22 = 0
    for e in graph.edges:
        if e[0] in C and e[1] in C:
            E11 += 1
        elif e[0] not in C and e[1] not in C:
            E22 += 1
        else:
            E12 += 1
    
    n1 = len(C)
    n2 = len(graph.nodes) - n1
    Phi = 2 * E11/(n1*(n1-1)) + E12/(n1*n2) + 2 * E22/(n2*(n2-1))
    return Phi

def improve_partition_by_adding(graph, C, P):
    next_C = copy.deepcopy(C)
    next_P = copy.deepcopy(P)
    change = False
    for j in P: #we tray for all nodes not in C
        C_prime = copy.deepcopy(C)
        C_prime[j] = P[j] #we add the node to C
        P_prime = copy.deepcopy(P)
        P_prime.pop(j)
        if Phi(graph, C_prime) > Phi(graph, C):
            next_C = C_prime
            change = True
    if change:
        return improve_partition_by_adding(graph, next_C, next_P)
    else:
        return next_C, next_P
    
def improve_partition_by_removing(graph, C):
    P = [i for i in graph.nodes if i not in C]
    next_C = copy.deepcopy(C)
    next_P = copy.deepcopy(P)
    change = False
    for i in C:
        C_prime = copy.deepcopy(C)
        P_prime = copy.deepcopy(P)
        P_prime[i] = C[i]
        C_prime.pop(i)
        if Phi(graph, C_prime, P_prime) > Phi(graph, C, P):
            next_C = C_prime
            next_P = P_prime
            change = True
    if change:
        return improve_partition_by_removing(graph, next_C, next_P)
    else:
        return next_C, next_P

    
def compare_nodes_diff_partitions(graph, C, C_prime): #returns a dictionary with the comparison of the nodes
    #0: in C and C'
    #1: in C and P'
    #2: P and C'
    #3: P and P'
    comparison = {0: [], 1: [], 2: [], 3: []}
    for i in graph.nodes:
        if i in C and i in C_prime:
            comparison[0].append(i)
        elif i in C and i not in C_prime:
            comparison[1].append(i)
        elif i not in C and i in C_prime:
            comparison[2].append(i)
        else:
            comparison[3].append(i)

    return comparison
            

#Now we plot the dictionary comparison where the columns are C & C', C & P', P & C', P & P' and show
# the number of nodes in each category

def plot_comparison(comparison, alg1, alg2, name):
    categories = ['C & C\'', 'C & P\'', 'P & C\'', 'P & P\'']
    counts = [len(comparison[i]) for i in range(4)]

    plt.bar(categories, counts)
    plt.xlabel('Categories')
    plt.ylabel('Number of Nodes')
    plt.title(name + ' - C-P and C\'-P\' Comparison. C-P from ' + alg1 + ' and C\'-P\' from ' + alg2 + '.')
    plt.show()

def plot_phis(phi1, phi2, phi3, phi4, alg1, alg2, alg3, alg4, name):
    plt.bar([alg1, alg2, alg3, alg4], [phi1, phi2, phi3, phi4])
    plt.xlabel('Algorithm')
    plt.ylabel('Phi')
    plt.title(name + ' - Phi values for ' + alg1 + ', ' + alg2 + ', ' + alg3 + ' and ' + alg4 + '.')
    plt.show()

def plot_graph(graph, C, name, alg, phi = 0):
    pos = nx.spring_layout(graph)
    colors = []
    if C is None:
        C = set()
    for node in graph:
        if node in C:
            colors.append('tomato')
        else:
            colors.append('cornflowerblue')
    plt.figure(figsize=(10, 10))
    #We add a title
    plt.title(name + ' graph with ' + alg + ' partition.')
    #and we draw the graph
    nx.draw(graph, pos, node_color=colors, with_labels=True, font_size=10, font_weight='bold', node_size=300, width=0.3)

    #finally we add the phi value as a comment to the plot, far away from the bottom
    plt.figtext(0.5, 0.01, 'Phi = ' + str(phi), wrap=True, horizontalalignment='center', fontsize=12, position=(0.5, 0.05))
    
    plt.show()