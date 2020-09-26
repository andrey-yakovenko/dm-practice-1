import pandas as pd


def complete_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        node_one_index = nodes.index(node_one)
        for node_two in nodes[node_one_index:]:
            if node_one+node_two not in edges and node_two+node_one not in edges:
                flag = False
                if node_one == node_two: msg = ': not(' + node_one + 'R' + node_two + ')...'
                else: msg = ': not(' + node_one + 'R' + node_two + ') and not(' + node_two + 'R' + node_one + ')'
                break
        if not flag: break
    return str(flag)+msg


def reflexive_check(nodes, edges):
    flag, msg = True, ''
    for node in nodes:
        if node*2 not in edges:
            flag = False
            msg = ': not(' + node + 'R' + node + ')'
            break
    return str(flag)+msg


def asymmetric_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        for node_two in nodes:
            if node_one+node_two in edges and node_two+node_one in edges:
                flag = False
                if node_one == node_two: msg = ': ' + node_one + 'R' + node_two
                else: msg = ': ' + node_one + 'R' + node_two + ' and ' + node_two + 'R' + node_one
                break
        if not flag: break
    return str(flag)+msg


def symmetric_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        for node_two in nodes:
            if node_one+node_two in edges and node_two+node_one not in edges:
                flag = False
                msg = ': ' + node_one + 'R' + node_two + ', but not(' + node_two + 'R' + node_one + ')'
                break
        if not flag: break
    return str(flag)+msg


def antisymmetric_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        for node_two in nodes:
            if node_one+node_two in edges and node_two+node_one in edges and node_one != node_two:
                flag = False
                msg = ': ' + node_one + 'R' + node_two + ' and ' + node_two + 'R' + node_one
                msg += ', but "' + node_one + '" not equal "' + node_two + '"'
                break
        if not flag: break
    return str(flag)+msg


def transitive_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        for node_two in nodes:
            for node_three in nodes:
                if node_one+node_two in edges and node_two+node_three in edges and node_one+node_three not in edges:
                    flag = False
                    msg = ': ' + node_one + 'R' + node_two + ' and ' + node_two + 'R' + node_three
                    msg += ', but not(' + node_one + 'R' + node_three + ')'
                    break
            if not flag: break
        if not flag: break
    return str(flag)+msg


def negatively_transitive_check(nodes, edges):
    flag, msg = True, ''
    for node_one in nodes:
        for node_two in nodes:
            for node_three in nodes:
                if node_one+node_two not in edges and node_two+node_three not in edges and node_one+node_three in edges:
                    flag = False
                    msg = ': not(' + node_one + 'R' + node_two + ') and not(' + node_two + 'R' + node_three + ')'
                    msg += ', but ' + node_one + 'R' + node_three
                    break
            if not flag: break
        if not flag: break
    return str(flag)+msg


def complete_order_check(nodes, edges):
    flag, msg = True, ': the binary relation R is complete, antisymmetric, and transitive'
    complete_result = complete_check(nodes, edges)[0]
    antisymmetric_result = antisymmetric_check(nodes, edges)[0]
    transitive_result = transitive_check(nodes, edges)[0]
    if complete_result+antisymmetric_result+transitive_result != 'TTT':
        flag = False
        msg = ': the binary relation R is '
        if complete_result == 'T': msg += 'complete, '
        else: msg += 'not complete, '
        if antisymmetric_result == 'T': msg += 'antisymmetric, '
        else: msg += 'not antisymmetric, '
        if transitive_result == 'T': msg += 'and transitive'
        else: msg += 'and not transitive'
    return str(flag) + msg


def complete_preorder_check(nodes, edges):
    flag, msg = True, ': the binary relation R is complete and transitive'
    complete_result = complete_check(nodes, edges)[0]
    transitive_result = transitive_check(nodes, edges)[0]
    if complete_result+transitive_result != 'TT':
        flag = False
        msg = ': the binary relation R is '
        if complete_result == 'T': msg += 'complete and '
        else: msg += 'not complete and '
        if transitive_result == 'T': msg += 'transitive'
        else: msg += 'not transitive'
    return str(flag) + msg


def strict_relation(nodes, edges):
    strict_matrix = pd.DataFrame(index=nodes, columns=nodes)
    for node_one in nodes:
        node_one_index = nodes.index(node_one)
        for node_two in nodes[node_one_index:]:
            if node_one+node_two in edges and node_two+node_one not in edges:
                strict_matrix[node_two][node_one] = 1
            else:
                strict_matrix[node_two][node_one] = 0
            if node_two+node_one in edges and node_one+node_two not in edges:
                strict_matrix[node_one][node_two] = 1
            else:
                strict_matrix[node_one][node_two] = 0
    return strict_matrix


def indifference_relation(nodes, edges):
    indifference_matrix = pd.DataFrame(index=nodes, columns=nodes)
    for node_one in nodes:
        node_one_index = nodes.index(node_one)
        for node_two in nodes[node_one_index:]:
            if node_one+node_two in edges and node_two+node_one in edges:
                indifference_matrix[node_two][node_one] = indifference_matrix[node_one][node_two] = 1
            else:
                indifference_matrix[node_two][node_one] = indifference_matrix[node_one][node_two] = 0
    return indifference_matrix
