import networkx as nx
import MRZJ_algorithm as mrzj
import more_algorithms as ma
import degree_based_algorithm as db
import lotr
import london
import matplotlib.pyplot as plt


#LOTR---------------------------------------------------------------------------------------------------------------------------------

id_label, label_type = lotr.read_LOTR_types('LOTR/ontology.csv')
graph_lotr = lotr.read_LOTR_graph('LOTR/networks-id-3books.csv', id_label)



#We start with the MRZJ ALGORITHM
C_lotr_mrzj, P_lotr_mrzj = mrzj.raw_MRZJ(graph_lotr)
phi_lotr_mrzj = ma.Phi(graph_lotr, C_lotr_mrzj)

C_lotr_mrzj_imp, P__lotr_mrzj_imp = ma.improve_partition_by_adding(graph_lotr, C_lotr_mrzj, P_lotr_mrzj)
phi_lotr_mrzj_imp = ma.Phi(graph_lotr, C_lotr_mrzj_imp)

#C = ma.improve_partition_by_removing(graph, C)
#phi = ma.Phi(graph, C)
#print(phi)

lotr.plot_graph_lotr(graph_lotr, label_type, C_lotr_mrzj_imp, 'MRZJ', phi_lotr_mrzj_imp)


#We continue with the DB ALGORITHM

C_lotr_db, P_lotr_db, gamma_lotr, phi_lotr_db = db.DB_algorithm(graph_lotr, 150, 150)

C_lotr_db_imp, P_lotr_db_imp = ma.improve_partition_by_adding(graph_lotr, C_lotr_db, P_lotr_db)
phi_lotr_db_imp = ma.Phi(graph_lotr, C_lotr_db_imp)

lotr.plot_graph_lotr(graph_lotr, label_type, C_lotr_db_imp, 'DB', phi_lotr_db_imp)



#We compare the two algorithms
ma.plot_phis(phi_lotr_mrzj, phi_lotr_mrzj_imp, phi_lotr_db, phi_lotr_db_imp, 'MRZJ', 'MRZJ improved', 'DB', 'DB improved', 'LOTR')


comparison = ma.compare_nodes_diff_partitions(graph_lotr, C_lotr_mrzj_imp, C_lotr_db_imp)

ma.plot_comparison(comparison, 'MRZJ', 'DB', 'LOTR')



#SINTHETIC----------------------------------------------------------------------------------------------------------------------------

STAR_SIZE = 10
COMPLETE_SIZE = 10

#Graphs
star_g1 = nx.star_graph(STAR_SIZE) #star graph
star_g2 = nx.star_graph(STAR_SIZE) #star graph
labels = {i: i + STAR_SIZE + 1 for i in star_g2.nodes}
star_g2 = nx.relabel_nodes(star_g2, labels)
star_g = nx.union(star_g1, star_g2)
star_g.add_edge(0, STAR_SIZE + 1)
complete_g = nx.complete_graph(COMPLETE_SIZE) #complete graph
labels = {i: i + STAR_SIZE + 1 for i in star_g.nodes}
complete_g = nx.relabel_nodes(complete_g, labels)
sint_g = nx.Graph() #sinthetic graph
sint_g = nx.union(star_g1, complete_g)
#sint_g.add_edge(0, str(star_size+1))
sint_g.add_node('center')
sint_g.add_edge('center', 0)
sint_g.add_edge('center', (STAR_SIZE + 2))
sint_g.add_node('outside')
sint_g.add_edge('outside', 1)
sint_g.add_edge('outside', 2)
sint_g.add_edge('outside', 3)


#Star graph
C_star_mrzj, P_star_mrzj = mrzj.raw_MRZJ(star_g)
phi_star_mrzj = ma.Phi(star_g, C_star_mrzj)
ma.plot_graph(star_g, C_star_mrzj, 'Star', 'MRZJ and DB', phi_star_mrzj)

C_star_mrzj_imp, P_star_mrzj_imp = ma.improve_partition_by_adding(star_g, C_star_mrzj, P_star_mrzj)
phi_star_mrzj_imp = ma.Phi(star_g, C_star_mrzj_imp)
ma.plot_graph(star_g, C_star_mrzj_imp, 'Star', 'MRZJ improved', phi_star_mrzj_imp)

C_star_db, P_star_db, gamma_star, phi_star = db.DB_algorithm(star_g, 10, 10)
phi_star_db = ma.Phi(star_g, C_star_db)
ma.plot_graph(star_g, C_star_db, 'Star', 'DB', phi_star_db)

C_star_db_imp, P_star_db_imp = ma.improve_partition_by_adding(star_g, C_star_db, P_star_db)
phi_star_db_imp = ma.Phi(star_g, C_star_db_imp)
ma.plot_graph(star_g, C_star_db_imp, 'Star', 'DB improved', phi_star_db_imp)


ma.plot_phis(phi_star_mrzj, phi_star_mrzj_imp, phi_star_db, phi_star_db_imp, 'MRZJ', 'MRZJ improved', 'DB', 'DB improved', 'Star')

comparison = ma.compare_nodes_diff_partitions(star_g, C_star_mrzj, C_star_db)
ma.plot_comparison(comparison, 'MRZJ', 'DB', 'Star')




#Complete graph
C_comp_mrzj, P_comp_mrzj = mrzj.raw_MRZJ(complete_g)
ma.plot_graph(complete_g, C_comp_mrzj, 'Complete', 'MRZJ', 0)

# C_comp_mrzj_imp, P_comp_mrzj_imp = ma.improve_partition_by_adding(complete_g, C_comp_mrzj, P_comp_mrzj)
# ma.plot_graph(complete_g, C_comp_mrzj_imp, 'Complete', 'MRZJ improved', phi_comp_mrzj_imp)

# C_comp_db, P_comp_db, gamma_comp, phi_comp = db.DB_algorithm(complete_g, 10, 10)
# phi_comp_db = ma.Phi(complete_g, C_comp_db)
# ma.plot_graph(complete_g, C_comp_db, 'Complete', 'DB', phi_comp_db)

# C_comp_db_imp, P_comp_db_imp = ma.improve_partition_by_adding(complete_g, C_comp_db, P_comp_db)
# phi_comp_db_imp = ma.Phi(complete_g, C_comp_db_imp)
# ma.plot_graph(complete_g, C_comp_db_imp, 'Complete', 'DB improved', phi_comp_db_imp)




#Sinthetic graph
C_sint_mrzj, P_sint_mrzj = mrzj.raw_MRZJ(sint_g)
phi_sint_mrzj = ma.Phi(sint_g, C_sint_mrzj)
ma.plot_graph(sint_g, C_sint_mrzj, 'Sinthetic', 'MRZJ', phi_sint_mrzj)

C_sint_mrzj_imp, P_sint_mrzj_imp = ma.improve_partition_by_adding(sint_g, C_sint_mrzj, P_sint_mrzj)
phi_sint_mrzj_imp = ma.Phi(sint_g, C_sint_mrzj_imp)
ma.plot_graph(sint_g, C_sint_mrzj_imp, 'Sinthetic', 'MRZJ improved', phi_sint_mrzj_imp)

C_sint_db, P_sint_db, gamma_sint, phi_sint = db.DB_algorithm(sint_g, 10, 10)
phi_sint_db = ma.Phi(sint_g, C_sint_db)
ma.plot_graph(sint_g, C_sint_db, 'Sinthetic', 'DB', phi_sint_db)

C_sint_db_imp, P_sint_db_imp = ma.improve_partition_by_adding(sint_g, C_sint_db, P_sint_db)
phi_sint_db_imp = ma.Phi(sint_g, C_sint_db_imp)
ma.plot_graph(sint_g, C_sint_db_imp, 'Sinthetic', 'DB improved', phi_sint_db_imp)


ma.plot_phis(phi_sint_mrzj, phi_sint_mrzj_imp, phi_sint_db, phi_sint_db_imp, 'MRZJ', 'MRZJ improved', 'DB', 'DB improved', 'Sinthetic')

comparison = ma.compare_nodes_diff_partitions(sint_g, C_sint_mrzj, C_sint_db)
ma.plot_comparison(comparison, 'MRZJ', 'DB', 'Sinthetic')

comparison2 = ma.compare_nodes_diff_partitions(sint_g, C_sint_mrzj, C_sint_mrzj_imp)
ma.plot_comparison(comparison2, 'MRZJ', 'MRZJ improved', 'Sinthetic')









