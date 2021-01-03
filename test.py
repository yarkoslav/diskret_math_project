def zvyaznist(graph):
    lst_tops = list()
    n = 0
    while graph != {}:
        for i in graph:
            if len(lst_tops) == n:
                lst_tops.append(graph[i])
            else:
                if i in lst_tops[n]:
                    for top in graph[i]:
                        lst_tops[n].add(top)
        for top in lst_tops[n]:
            graph.pop(top)
        n += 1
    return {min(i) for i in lst_tops}


print(zvyaznist({1: {2, 5}, 2: {1}, 3: {4}, 4: {3}, 5: {1}}))
