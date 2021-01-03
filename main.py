"""
main module of project
"""


def get_not_oriented_graph_from_file(file_name: str) -> dict:
    edges_dict = {}
    with open(file_name, 'r') as f:
        f.readline()
        line = f.readline()
        while line != '':
            edge = list(map(int, line.strip().split()))
            for i in range(2):
                j = 1 - i
                try:
                    edges_dict[edge[i]].add(edge[j])
                except KeyError:
                    edges_dict[edge[i]] = {edge[j]}
            line = f.readline()
    return edges_dict


def get_oriented_graph_from_file(file_name: str) -> dict:
    edges_dict = {}
    with open(file_name, 'r') as f:
        f.readline()
        line = f.readline()
        while line != '':
            edge = list(map(int, line.strip().split()))
            try:
                edges_dict[edge[0]].add(edge[1])
            except KeyError:
                edges_dict[edge[0]] = {edge[1]}
            line = f.readline()
    return edges_dict


def read_graph(file_name: str) -> (dict, int):
    graph = {}
    dir_not_dir = -1 # not directed (0) or directed (1)
    if file_name[-4:] == '.csv':
        dir_not_dir = int(file_name[-5])
        if dir_not_dir == 0:
            graph = get_not_oriented_graph_from_file(file_name)
        elif dir_not_dir == 1:
            graph = get_oriented_graph_from_file(file_name)
    return graph, dir_not_dir


def write_graph(edges_dict: dict):
    to_write = set()
    for edge1 in edges_dict.keys():
        for edge2 in edges_dict[edge1]:
            to_write.add((edge1, edge2))
    with open('graph.csv', 'w') as file:
        file.write('edge1,edge2\n')
        for edges in to_write:
            file.write(str(edges[0]) + ',' + str(edges[1]) + '\n')


def del_node(graph: dict, node: int) -> dict:
    if graph.get(node) is not None:
        del graph[node]
    for edge in graph.keys():
        if node in graph[edge]:
            graph[edge].remove(node)
    return graph


def find_component(graph: dict, source):
    if source is None or source not in graph:
        return "Invalid input"
    graph_c = graph.copy()
    stack = {source}
    used_nodes = set()

    while len(stack) != 0:
        stack_c = stack.copy()
        for node in stack_c:
            used_nodes.add(node)
            to_add = graph[node]
            stack.remove(node)
            stack |= to_add
            graph_c = del_node(graph_c, node)
    return used_nodes


def find_components(graph: dict):
    graph_c = graph.copy()
    min_points = set()
    keys = set(graph_c.keys())
    while graph_c:
        component = find_component(graph_c, keys.pop())
        print(component)
        min_points.add(min(component))
        keys -= component
        for key0 in component:
            del graph_c[key0]
    return min_points


def zvyaznist(graph: dict) -> list:
    lst_tops = list()
    counter = 0
    while graph != {}:
        for element in graph:
            if len(lst_tops) == counter:
                lst_tops.append(graph[element])
            else:
                if element in lst_tops[counter]:
                    for top in graph[element]:
                        lst_tops[counter].add(top)
        for top in lst_tops[counter]:
            graph.pop(top)
        counter += 1
    return [min(top) for top in lst_tops]
def main():
    pass


if __name__ == '__main__':
    # print(get_not_oriented_graph_from_file('data1.txt'))
    # gr = get_not_oriented_graph_from_file('data1.txt')
    # print(list(gr.keys())[0])

    graph = {"A": {"B", "C", "D"},
             "B": {"E"},
             "C": {"F", "G"},
             "D": {"H"},
             "E": {"I"},
             "F": {"J"}}
    # print(find_components(gr))
    # main()
