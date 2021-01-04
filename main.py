"""
module with functions for working with graphs
"""
import copy


###############################################################################
# TASK 1
###############################################################################
def read_graph(file_name: str, directed=False) -> dict:
    def get_not_oriented_graph_from_file(file_name: str) -> dict:
        with open(file_name, 'r') as f:
            nodes = list(map(int, (f.readline()).strip().split()))[0]
            edges_dict = {i:set() for i in range(1, nodes + 1)}
            line = f.readline()
            while line != '':
                edge = list(map(int, line.strip().split()))
                for i in range(2):
                    j = 1 - i
                    edges_dict[edge[i]].add(edge[j])
                line = f.readline()
        return edges_dict

    def get_oriented_graph_from_file(file_name: str) -> dict:
        with open(file_name, 'r') as f:
            nodes = list(map(int, (f.readline()).strip().split()))[0]
            edges_dict = {i:set() for i in range(1, nodes + 1)}
            line = f.readline()
            while line != '':
                edge = list(map(int, line.strip().split()))
                edges_dict[edge[0]].add(edge[1])
                line = f.readline()
        return edges_dict

    if directed:
        graph = get_oriented_graph_from_file(file_name)
    else:
        graph = get_not_oriented_graph_from_file(file_name)
    return graph


###############################################################################
# TASK 2
###############################################################################
def write_graph(edges_dict: dict, file_name='graph.csv', directed=False):
    to_write = set()
    nodes = set()
    for edge1 in edges_dict.keys():
        for edge2 in edges_dict[edge1]:
            if directed:
                to_write.add((edge1, edge2))
            else:
                to_write.add(frozenset((edge1, edge2)))
            nodes.add(edge1)
            nodes.add(edge2)
    with open(file_name, 'w') as file:
        file.write(f'{len(nodes)},{len(to_write)}\n')
        for edge in to_write:
            edge = tuple(edge)
            file.write(str(edge[0]) + ',' + str(edge[1]) + '\n')


###############################################################################
# TASK 3
###############################################################################
def find_components_min_nodes(graph: dict) -> list:
    lst_tops = list()
    counter = 0
    while graph != {}:
        set_tops = set()
        for element in graph:
            set_tops.add(element)
            while True:
                for top in graph[element]:
                    set_tops.add(top)
                help_set = copy.deepcopy(set_tops)
                for top in help_set:
                    if top in graph:
                        for each_top in graph[top]:
                            set_tops.add(each_top)
                if help_set == set_tops:
                    break
            lst_tops.append(set_tops)
            break
        for top in lst_tops[counter]:
            graph.pop(top)
        counter += 1
    return [min(top) for top in lst_tops]


###############################################################################
# TASK 4
###############################################################################
def strong_connection(graph: dict) -> list:
    def make_transponed_graph(graph: dict) -> dict:
        graph_t = {}
        for node in graph:
            for edge_end in graph[node]:
                try:
                    graph_t[edge_end].add(node)
                except KeyError:
                    graph_t[edge_end] = {node}
        for node in range(1, len(graph) + 1):
            if node not in graph_t:
                graph_t[node] = set()
        return graph_t

    def dfs1(node: int, graph: dict, used: list, order: list):
        used[node - 1] = True
        stack = [node]
        while stack:
            new_node = stack[-1]
            is_dead_end = True
            for next_node in graph[new_node]:
                if not used[next_node - 1]:
                    stack.append(next_node)
                    used[next_node - 1] = True
                    is_dead_end = False
                    break
            if is_dead_end:
                stack.pop()
                order.append(new_node)

    def dfs2(node: int, graph_t: dict, used: list, component: list):
        used[node - 1] = True
        stack = [node]
        while stack:
            new_node = stack[-1]
            is_dead_end = True
            for next_node in graph_t[new_node]:
                if not used[next_node - 1]:
                    stack.append(next_node)
                    used[next_node - 1] = True
                    is_dead_end = False
                    break
            if is_dead_end:
                stack.pop()
                component.append(new_node)

    order = []
    used = [False] * len(graph)
    for node in graph:
        if not used[node - 1]:
            dfs1(node, graph, used, order)
    graph_t = make_transponed_graph(graph)
    used = [False] * len(graph)
    components = []
    for i in range(len(graph)):
        component = []
        node = order[len(graph) - 1 - i]
        if not used[node - 1]:
            dfs2(node, graph_t, used, component)
            if min(component) not in components:
                components.append(min(component))
    components.sort()
    return components


###############################################################################
# help for tasks 5 and 6
def find_components(graph: dict) -> list:
    lst_tops = list()
    counter = 0
    graph_c = copy.deepcopy(graph)
    while graph_c != {}:
        set_tops = set()
        for element in graph_c:
            set_tops.add(element)
            while True:
                for top in graph_c[element]:
                    set_tops.add(top)
                help_set = copy.deepcopy(set_tops)
                for top in help_set:
                    if top in graph_c:
                        for each_top in graph_c[top]:
                            set_tops.add(each_top)
                if help_set == set_tops:
                    break
            lst_tops.append(set_tops)
            break
        for top in lst_tops[counter]:
            graph_c.pop(top)
        counter += 1
    components = [{node: graph[node] for node in component}
                  for component in lst_tops]
    return components


###############################################################################
# TASK 5
###############################################################################
def cutpoints_searching(graph: dict) -> list:
    def find_articulation_points(graph_dict: dict, input_node: int):
        stack = [input_node]
        used = {input_node}
        result = set()
        parents = {input_node: -1}
        sons = {key: set() for key in graph_dict}
        tin = {input_node: 0}
        low = {input_node: 0}
        idx = 0
        order = [input_node]
        while stack:
            node = stack[-1]
            is_dead_end = True
            for element in graph_dict[node]:
                if element not in used:
                    is_dead_end = False
                    parents[element] = node
                    sons[node].add(element)
                    idx += 1
                    tin[element] = idx
                    stack.append(element)
                    used.add(element)
                    order.append(element)
                    break
            if is_dead_end:
                stack.pop()
        swap = order[1:]
        swap = swap[::-1]
        for idx in range(len(swap)):
            possible_values = [tin[swap[idx]]]
            for node in graph_dict[swap[idx]]:
                if (node not in sons[swap[idx]]) and (node != parents[swap[idx]]):
                    possible_values.append(tin[node])
            for node in sons[swap[idx]]:
                possible_values.append(low[node])
            low[swap[idx]] = min(possible_values)
        for idx in graph_dict:
            if idx != input_node:
                is_articulation = True
                if len(sons[idx]) == 0:
                    is_articulation = False
                for node in sons[idx]:
                    if low[node] < tin[idx]:
                        is_articulation = False
                        break
                if is_articulation:
                    result.add(idx)
        if len(sons[input_node]) > 1:
            result.add(input_node)
        return result


    res = set()
    components = find_components(graph)
    for component in components:
        node = list(component.keys())[0]
        result = find_articulation_points(component, node)
        res = res | result
    return list(res)


    used = set()
    res = set()
    for node in graph:
        if node not in used:
            result, order = find_articulation_points(graph, node)
            res = res | set(result)
            used = used | set(order)
    return list(res)


###############################################################################
# TASK 6
###############################################################################
def bridge_searching(graph: dict) -> list:
    def find_bridges(graph_dict: dict, input_node: int):
        stack = [input_node]
        used = {input_node}
        result = set()
        parents = {input_node: -1}
        sons = {key: set() for key in graph_dict}
        tin = {input_node: 0}
        low = {input_node: 0}
        idx = 0
        order = [input_node]
        while stack:
            node = stack[-1]
            is_dead_end = True
            for element in graph_dict[node]:
                if element not in used:
                    is_dead_end = False
                    parents[element] = node
                    sons[node].add(element)
                    idx += 1
                    tin[element] = idx
                    stack.append(element)
                    used.add(element)
                    order.append(element)
                    break
            if is_dead_end:
                stack.pop()
        swap = order[1:]
        swap = swap[::-1]
        for idx in range(len(swap)):
            possible_values = [tin[swap[idx]]]
            for node in graph_dict[swap[idx]]:
                if (node not in sons[swap[idx]]) and (node != parents[swap[idx]]):
                    possible_values.append(tin[node])
            for node in sons[swap[idx]]:
                possible_values.append(low[node])
            low[swap[idx]] = min(possible_values)
        for idx in graph_dict:
            for node in sons[idx]:
                if low[node] > tin[idx]:
                    result.add((idx, node))
        return result

    res = set()
    components = find_components(graph)
    for component in components:
        node = list(component.keys())[0]
        result = find_bridges(component, node)
        res = res | result
    return list(res)


if __name__ == '__main__':
    print('This module has functions that you can use while working with graphs')
