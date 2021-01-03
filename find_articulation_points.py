def find_articulation_points(graph_dict):

    visited = set()
    result = set()
    parents = {}
    low = {}
    def dfs(idx, node, parent):
        visited.add(node)
        parents[node] = parent 
        edges_count = 0
        low[node] = idx

        for element in graph_dict[node]:
            if element == parent:
                continue
            if element not in visited:
                parents[element] = node 
                edges_count += 1    
                dfs(idx+1, element, node) 
            
            low[node] = min(low[node], low[element])

            if idx <= low[element]: 
                if parents[node] != -1: 
                    result.add(node)

        
        if (parents[node] == -1 and edges_count >= 2):
            result.add(node)

    dfs(0, 0, -1)
    return list(result)
