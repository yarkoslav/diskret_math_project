"""
main module of project
"""


def get_not_oriented_graph_from_file(file_name: str) -> dict:
    edges_dict = {}
    for line in open(file_name, 'r'):
        edge = list(map(int, line.strip().split(',')))
        for i in range(2):
            j = 1 - i
            try:
                edges_dict[edge[i]].add(edge[j])
            except KeyError:
                edges_dict[edge[i]] = {edge[j]}
    return edges_dict


def get_oriented_graph_from_file(file_name: str) -> dict:
    edges_dict = {}
    for line in open(file_name, 'r'):
        edge = list(map(int, line.strip().split(',')))
        try:
            edges_dict[edge[0]].add(edge[1])
        except KeyError:
            edges_dict[edge[0]] = {edge[1]}
    return edges_dict


def write_graph(edges_dict: dict):
    to_write = set()
    for edge1 in edges_dict.keys():
        for edge2 in edges_dict[edge1]:
            to_write.add((edge1, edge2))
    with open('graph.csv', 'w') as file:
        file.write('edge1,edge2\n')
        for edges in to_write:
            file.write(str(edges[0]) + ',' + str(edges[1]) + '\n')


def main():
    pass


if __name__ == '__main__':
    write_graph(get_oriented_graph_from_file('data1.txt'))
    main()
