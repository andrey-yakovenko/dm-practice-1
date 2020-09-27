# Main function - topological_sorting (task 13)


# additional function to detect_cycled_path that recursively builds tree's paths until it detects a cycled one
def build_node_paths(old_paths, edges):
    new_paths = []
    for path in old_paths:
        for edge in edges:
            if edge[0] == path[-1]: new_paths.append(path+edge[1])
    if not new_paths: return None  # no more paths are possible to build
    else:
        for path in new_paths:
            # return cycled path if detected, else build next deeper level of paths
            return path if path[-1] in path[:-1] else build_node_paths(new_paths, edges)


# function to detect the first possible cycle in the relation if it exists
def detect_cycled_path(nodes, edges):
    filtered_edges = edges.copy()  # a list for all edges except 'aa', 'bb' and so on
    for edge in filtered_edges:
        if edge[0] == edge[1]: filtered_edges.remove(edge)
    for node in nodes:  # for each node we build all possible paths
        paths = []
        for edge in filtered_edges:
            if edge[0] == node: paths.append(edge)
        cycled_path = build_node_paths(paths, filtered_edges)  # returns cycled path if detected or None
        if cycled_path is not None: return cycled_path
    return None


# function that goes through relation while there are any cycles and replace them with group nodes
def reduce_relation(nodes, edges):
    # dictionary is a dict of substitutions,
    #       e.g., {'A': 'abc'} means that 'abc' is a cycle within the relation that was replaced by the node 'A'
    new_nodes, new_edges, dictionary = nodes.copy(), edges.copy(), {}
    cycled_path = detect_cycled_path(nodes, edges)  # initial cycled path if exists
    while cycled_path is not None:
        index = cycled_path.index(cycled_path[-1])  # technical part to extract a cycle from a path
        cycled_path = cycled_path[index:-1]  # e.g., path 'abcdb' -> cycle 'bcd'
        # substitution of a cycle by new node
        flag = True
        for node in cycled_path:
            if node.isupper():  # if a cycle includes another cycle we merge them in the older one
                dictionary[node] += cycled_path.replace(node, '')
                flag = False
                break
        if flag: dictionary[cycled_path[0].upper()] = cycled_path  # cycles are always uppercase letters
        # substitution of all nodes, that are connected with a cycle, using new nodes
        temp_nodes = []
        flag = True
        for node in cycled_path:
            if node.isupper():
                for temp_node in new_nodes:
                    if temp_node.isupper() or temp_node not in cycled_path: temp_nodes.append(temp_node)
                flag = False
                break
        if flag:
            for node in new_nodes:
                if node not in cycled_path: temp_nodes.append(node)
            temp_nodes.append(cycled_path[0].upper())  # appending of a new node
        new_nodes = temp_nodes
        # substitution of all edges, that are connected with a cycle, using new nodes, excluding all inner cycle edges
        temp_edges = []
        flag = True
        for node in cycled_path:
            if node.isupper():
                for edge in new_edges:
                    if edge[0] not in cycled_path and edge[1] not in cycled_path:
                        temp_edges.append(edge)
                    elif edge[0] in cycled_path and edge[1] not in cycled_path:
                        temp_edge = node + edge[1]
                        if temp_edge not in temp_edges: temp_edges.append(temp_edge)
                    elif edge[0] not in cycled_path and edge[1] in cycled_path:
                        temp_edge = edge[0] + node
                        if temp_edge not in temp_edges: temp_edges.append(temp_edge)
                flag = False
                break
        if flag:
            for edge in new_edges:
                if edge[0] != edge[1]:
                    if edge[0] not in cycled_path and edge[1] not in cycled_path:
                        temp_edges.append(edge)
                    elif edge[0] in cycled_path and edge[1] not in cycled_path:
                        temp_edge = cycled_path[0].upper()+edge[1]
                        if temp_edge not in temp_edges: temp_edges.append(temp_edge)
                    elif edge[0] not in cycled_path and edge[1] in cycled_path:
                        temp_edge = edge[0]+cycled_path[0].upper()
                        if temp_edge not in temp_edges: temp_edges.append(temp_edge)
        new_edges = temp_edges
        # looking for another cycled path
        cycled_path = detect_cycled_path(new_nodes, new_edges)
    return new_nodes, new_edges, dictionary  # new relation with a dictionary of substitutions


# function that goes through relation while there are any cycles and replace them with group nodes
def topological_sorting(initial_nodes, initial_edges):
    new_nodes, new_edges, dictionary = reduce_relation(initial_nodes, initial_edges)
    nodes, edges = new_nodes.copy(), new_edges.copy()
    if len(new_nodes) == 1: return None, None  # if the initial relation is reduced to one node
    else:
        groups, grouped = [[]], []  # (i) levels of sorting and (ii) already sorted nodes
        for node in nodes:  # first level nodes detecting
            flag = True
            for edge in edges:
                if edge[1] == node:
                    flag = False
                    break
            if flag:  # if node have no input edges
                groups[0].append(node)
                grouped.append(node)
                nodes.remove(node)
        while nodes:  # while there are still ungrouped nodes
            new_group = []
            for node in nodes:  # checking if nodes are on the highest level within those that left
                flag = True
                for edge in edges:
                    if edge[1] == node and edge[0] not in grouped:
                        flag = False
                        break
                if flag:
                    new_group.append(node)
            groups.append(new_group)
            for node in groups[-1]:
                grouped.append(node)
                nodes.remove(node)
        return groups, dictionary  # returns groups (levels) of sorting and the dictionary of cycle substitutions
