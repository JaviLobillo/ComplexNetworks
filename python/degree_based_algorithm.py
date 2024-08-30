import numpy as np
import networkx as nx
import math
import random as rd
import more_algorithms as ma

def DB_algorithm(graph, n_gamma, n_P):  # n_gamma, n_p are the numbers of gamma and P values to try out.
    #We want to find the best combination of gamma and P values
    n = len(graph.nodes)
    best_gamma_1 = 0 #here we will store the best gamma_1 value out of all combinations for gammas and Ps
    best_Phi = 0 #here we will store the best Phi value """"
    it_phi = 0 #where we will store the Phi value for the current combination of gamma and P
    best_C = {} #where we will store the best C partition
    suitable = False #to check whether the gamma_1 value is suitable (not exploding towards 0 or 1)
    unsuitable_gammas = [0,0] #to check whether we didn't find a suitable gamma_1 value
    for g in range(n_gamma):
        gamma_1 = rd.uniform(0,1)
        gamma_2 = 1 - gamma_1
        for ps in range(n_P):
            p = [0, 0, 0]
            p[0] = rd.uniform(0, 1) #We generate random values for p11 = p[0], p12 = p[1], p22 = p[2]
            p[1] = rd.uniform(0, 1)
            p[2] = rd.uniform(0, 1)
            p.sort(reverse=True)

            c = [i * n for i in p] #We compute the c values

            d1 = gamma_1 * c[0] + gamma_2 * c[1]
            d2 = gamma_1 * c[1] + gamma_2 * c[2]

            R = c[1] / c[2]

            gamma_1_old = 0 #to store the value of gamma_1 from the previous iteration, so we can check whether it converges
            while not (abs(gamma_1 - gamma_1_old) < 0.0001):
                gamma_1_old = gamma_1 #we store old value
                q = DB_from_gamma_1_R_to_q(graph, gamma_1, R, d1, d2) #we compute q values
                gamma_1, R = DB_from_q_to_gamma_1_R(graph, q) #we compute gamma_1 and R values again
            
            if gamma_1 > 0.1 and gamma_1 < 0.9: #we only consider gamma_1 values that don't explode towards 0 or 1
                suitable = True
                n_1 = gamma_1 * n #the size of the core

                #We take the n_1 nodes with the highes degree and put them in the core
                C = {}
                for i in sorted(graph.nodes, key=lambda x: graph.degree(x), reverse=True)[:int(n_1)]: 
                    C[i] = 1 #we write this 1 as to have the same format as in the MRZJ algorithm
                
                if len(C) <= 1 or len(C) >= n - 1: #we don't consider partitions with only one node in the core
                    it_phi = 0.0001 #we set a low value for Phi so it is not considered as the best
                else:
                    it_phi = ma.Phi(graph, C) #we compute the Phi value for the current combination of gamma and P values

                if it_phi > best_Phi:
                    best_Phi = it_phi
                    best_gamma_1 = gamma_1
                    best_C = C
            elif gamma_1 <= 0.1:
                unsuitable_gammas[0] += 1
            else:
                unsuitable_gammas[1] += 1
    
    if not suitable: #if we didn't find a suitable gamma_1 value, we return an empty partition
        if unsuitable_gammas[0] >= unsuitable_gammas[1]:
            best_C = {}
        else:
            best_C = {i: 1 for i in graph.nodes}
    
    
    #We compute P
    best_P = {}
    for i in graph.nodes:
        if i not in best_C:
            best_P[i] = 1

    return best_C, best_P, best_gamma_1, best_Phi

def DB_from_gamma_1_R_to_q(graph, gamma_1, R, d1, d2):
    n = len(graph.nodes)
    #It is enough to provide gamma_1 and R because gamma_2 = 1 - gamma_1
    gamma_2 = 1 - gamma_1

    q = {}
    for i in graph.nodes:
        q1 = (gamma_1 * math.exp(-d1) * R**(graph.degree(i))) / (gamma_2 * math.exp(-d2) + gamma_1 * math.exp(-d1) * R**(graph.degree(i)))
        q2 = 1 - q1
        q[i] = (q1, q2)
    return q

def DB_from_q_to_gamma_1_R(graph, q):
    n = len(graph.nodes)
    #we apply the formula for kappa_1 and kappa_2. Then we compute R
    numerator = sum([ graph.degree(i) * q[i][0] for i in q])
    denominator = sum([ q[i][0] for i in q])
    kappa_1 = numerator / denominator
    numerator2 = sum([ graph.degree(i) * q[i][1] for i in q])
    denominator2 = sum([ q[i][1] for i in q])
    kappa_2 = numerator2 / denominator2
    R = kappa_1 / kappa_2
    #We apply the formula for gamma_1. It follows from the theory that gamma_2 = 1 - gamma_1
    gamma_1 = (1/n) * sum([ q[i][0] for i in q])

    return (gamma_1, R)