import sys

graph = {}
edges = []
for line in open(sys.argv[1], 'r'):
    node, connections = line.strip().split(": ")
    connections = connections.split(" ")
    if node not in graph:
        graph[node] = []
    for connection in connections:
        if connection not in graph:
            graph[connection] = []
    for connection in connections:
        edges.append((node, connection))
        if connection not in graph[node]:
            graph[node].append(connection)
        if node not in graph[connection]:
            graph[connection].append(node)

def flood(graph, node, cut):
    nodes = set()
    frontier = [node]
    while len(frontier) > 0:
        node = frontier.pop()
        if node not in nodes:
            nodes.add(node)
            for connection in graph[node]:
                is_cut = (connection, node) in cut or (node, connection) in cut
                if not is_cut:
                    frontier.append(connection)
    return len(nodes)

for (i, edge) in enumerate(edges):
    print(i, edge)
# 2, 10, 17

start = edges[0][0]
for i in range(len(edges)):
    print("i", i, "/", len(edges))
    for j in range(i + 1, len(edges)):
        print("  j", j, "/", len(edges))
        for k in range(j + 1, len(edges)):
            cut = [edges[i], edges[j], edges[k]]
            size = flood(graph, start, cut)
            if size < len(graph):
                print("Cut", cut)
                print("-> flood", flood(graph, start, cut))
                print("solution:", size * (len(graph) - size))
                sys.exit(1)
