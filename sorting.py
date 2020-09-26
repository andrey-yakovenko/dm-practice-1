def build_node_paths(old_paths, edges):
    new_paths = []
    for path in old_paths:
        for edge in edges:
            if edge[0] == path[-1]: new_paths.append(path+edge[1])
    if not new_paths: return None
    else:
        for path in new_paths:
            return path if path[-1] in path[:-1] else build_node_paths(new_paths, edges)


def detect_cycled_path(nodes, edges):
    filtered_edges = edges.copy()
    for edge in filtered_edges:
        if edge[0] == edge[1]: filtered_edges.remove(edge)
    for node in nodes:
        paths = []
        for edge in filtered_edges:
            if edge[0] == node: paths.append(edge)
        cycled_path = build_node_paths(paths, filtered_edges)
        if cycled_path is not None: return cycled_path
    return None


def reduce_relation(nodes, edges):
    new_nodes, new_edges, dictionary = nodes.copy(), edges.copy(), {}
    cycled_path = detect_cycled_path(nodes, edges)
    while cycled_path is not None:
        index = cycled_path.index(cycled_path[-1])
        cycled_path = cycled_path[index:-1]

        flag = True
        for node in cycled_path:
            if node.isupper():
                dictionary[node] += cycled_path.replace(node, '')
                flag = False
                break
        if flag: dictionary[cycled_path[0].upper()] = cycled_path

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
            temp_nodes.append(cycled_path[0].upper())
        new_nodes = temp_nodes

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
        cycled_path = detect_cycled_path(new_nodes, new_edges)
    return new_nodes, new_edges, dictionary


def topological_sorting(initial_nodes, initial_edges):
    new_nodes, new_edges, dictionary = reduce_relation(initial_nodes, initial_edges)
    nodes, edges = new_nodes.copy(), new_edges.copy()
    if len(new_nodes) == 1: return None, None
    else:
        groups, grouped = [[]], []
        for node in nodes:
            flag = True
            for edge in edges:
                if edge[1] == node:
                    flag = False
                    break
            if flag:
                groups[0].append(node)
                grouped.append(node)
                nodes.remove(node)
        while nodes:
            new_group = []
            for node in nodes:
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
        return groups, dictionary
