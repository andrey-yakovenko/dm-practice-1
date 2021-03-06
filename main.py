from properties import *  # tasks 2-12
from sorting import topological_sorting  # task 13
from graphs import draw_graph  # graph's visualisation

# read a matrix from .xlsx file
binary_relation = pd.read_excel('data.xlsx', index_col=0)
nodes, edges = binary_relation.index.values.tolist(), []
for node_one in nodes:
    for node_two in nodes:
        if binary_relation[node_two][node_one]: edges.append(node_one+node_two)
# nodes, e.g., ['a', 'b', 'c']
# edges, e.g., ['ab', 'bc', 'ca']
print('\nThe binary relation R:\n')
print(binary_relation, '\n')

# tasks 2-10
print('- Is the binary relation R complete?\n-', complete_check(nodes, edges), '\n')
print('- Is the binary relation R reflexive?\n-', reflexive_check(nodes, edges), '\n')
print('- Is the binary relation R asymmetric?\n-', asymmetric_check(nodes, edges), '\n')
print('- Is the binary relation R symmetric?\n-', symmetric_check(nodes, edges), '\n')
print('- Is the binary relation R antisymmetric?\n-', antisymmetric_check(nodes, edges), '\n')
print('- Is the binary relation R transitive?\n-', transitive_check(nodes, edges), '\n')
print('- Is the binary relation R negatively transitive?\n-', negatively_transitive_check(nodes, edges), '\n')
print('- Is the binary relation R a complete order?\n-', complete_order_check(nodes, edges), '\n')
print('- Is the binary relation R a complete preorder?\n-', complete_preorder_check(nodes, edges), '\n')

# tasks 11, 12
print('The strict relation P:\n')
print(strict_relation(nodes, edges), '\n')
print('The indifference relation I:\n')
print(indifference_relation(nodes, edges), '\n')

# tasks 13
groups, dictionary = topological_sorting(nodes, edges)
if groups is None: print('- Topological sorting can not be done: the binary relation R reduced to one node...\n')
else:
    print('- Topological sorting:\n')
    for group in groups:
        print('  ↓', group)
    print('  ... where', dictionary, 'are grouped cycles.\n')

# binary relation visualization
draw_graph(nodes, edges)
