# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# given number of nodes n and probability p, output a random graph
# as specified in homework

graph = {'A': ['B', 'C'],
             'B': ['C', 'D'],
             'C': ['D'],
             'D': ['C'],
             'E': ['F'],
             'F': ['C']}

# add neighbor as value for node key-value pair
def add_edge(graph, u, v):
    graph[u].append(v)

# with probability p, add neighbor to the node
def generate_edges(graph,p):
    edges = []
    for node in graph:
        for neighbor in graph[node]:
            edges.append((node,neighbor))
    return edges

# create a graph of n nodes connected to neighbors with probability p
def create_graph(n,p):
    return -1

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G,i,j):
    return -1

# find shortest path from chosen start node to end node.
def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def print_path(path):
    print(path)

def main():
    print_path(find_shortest_path(graph, 'A','D'))

if __name__ == "__main__":
    main()
