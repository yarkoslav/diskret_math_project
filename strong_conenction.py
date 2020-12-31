def get_oriented_graph_from_file(file_name: str) -> dict:
    edges_dict = {}
    with open(file_name, "r") as file:
        nodes = list(map(int, file.readline().strip().split()))[0]
        for line in file:
            edge = list(map(int, line.strip().split()))
            try:
                edges_dict[edge[0]].add(edge[1])
            except KeyError:
                edges_dict[edge[0]] = {edge[1]}
        for node in range(1, nodes+1):
            if node not in edges_dict:
                edges_dict[node] = set()
    return edges_dict


def make_transponed_graph(graph: dict) -> dict:
    graph_t = {}
    for node in graph:
        for edge_end in graph[node]:
            try:
                graph_t[edge_end].add(node)
            except KeyError:
                graph_t[edge_end] = {node}
    for node in range(1, len(graph)+1):
        if node not in graph_t:
            graph_t[node] = set()
    return graph_t


def dfs1(node: int, graph: dict, used: list, order: list):
    used[node-1] = True
    stack = [node]
    while stack:
        new_node = stack[-1]
        is_dead_end = True
        for next_node in graph[new_node]:
            if not used[next_node-1]:
                stack.append(next_node)
                used[next_node-1] = True
                is_dead_end = False
                break
        if is_dead_end:
            stack.pop()
            order.append(new_node)


def dfs2(node: int, graph_t: dict, used: list, component: list):
    used[node-1] = True
    stack = [node]
    while stack:
        new_node = stack[-1]
        is_dead_end = True
        for next_node in graph_t[new_node]:
            if not used[next_node-1]:
                stack.append(next_node)
                used[next_node-1] = True
                is_dead_end = False
                break
        if is_dead_end:
            stack.pop()
            component.append(new_node)


if __name__ == "__main__":
    # graph = get_oriented_graph_from_file('test2.csv')
    graph = {1: {2, 3, 4}, 2: {1}, 3: {4}, 4: {3}}
    order = []
    used = [False] * len(graph)
    for node in graph:
        if not used[node-1]:
            dfs1(node, graph, used, order)
    graph_t = make_transponed_graph(graph)
    used = [False] * len(graph)
    components = []
    for i in range(len(graph)):
        component = []
        node = order[len(graph)-1-i]
        if not used[node-1]:
            dfs2(node, graph_t, used, component)
            if min(component) not in components:
                components.append(min(component))
    components.sort()
    print(components)