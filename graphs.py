import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(nodes, edges):
    graph = nx.DiGraph()
    for node in nodes: graph.add_node(node)
    for edge in edges: graph.add_weighted_edges_from([(edge[0], edge[1], .01)])
    options = {'node_color': '#ddd', 'node_size': 500}
    plt.subplot(121)
    nx.draw(graph, with_labels=True, **options)
    plt.show()
