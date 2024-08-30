import numpy as np
import networkx as nx

def raw_MRZJ(graph):
    C = {}
    P = {}
    for i in graph.nodes:
        sum = 0
        for j in graph.neighbors(i):
            sum += (graph.degree(i) - graph.degree(j)) / (graph.degree(i) + graph.degree(j) - 2)
        cent = sum / graph.degree(i) #centrality of the node
        if cent >= 0:
            C[i] = cent
        else:
            P[i] = cent
    
    return C, P
