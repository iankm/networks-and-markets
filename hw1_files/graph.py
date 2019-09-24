# include any code you need for your assignment in this file or in auxiliary
# files that can be imported here.

# given number of nodes n and probability p, output a random graph
# as specified in homework

"""
DELETE THIS COMMENT AFTER LEARNING HOW TO RUN THIS PROGRAM.

PLEASE READ:
To run this program, you need python installed natively on your computer,
as well as the Python Package Installer, pip. Pip will allow you to install
two libraries installed for this program: numpy and matplotlib.

If you do not know how to install Python, pip, or use Terminal on Mac,
please refer to the following:

    1) How to use Terminal on Mac:
        https://macpaw.com/how-to/use-terminal-on-mac
    2) How to install Python on Mac:
        https://wsvincent.com/install-python3-mac/
    3) How to install pip on Mac:
        https://pip.pypa.io/en/stable/

Also, if you do not have an IDE on your laptop, I suggest downloading Atom.
It's very intuitive. You can get it here: https://atom.io/

HOW TO RUN:
    1) Using Terminal, navigate to your hw1_files folder
    2) Use the following command: python graph.py [n] [p] [i] [j] [f]
        - n is the number of nodes in your graph
        - p is the probability that two nodes are connected
        - i is your starting node for the breadth-first search algorithm
        - j is your ending node for the breadth-first search algorithm
        - f is the fb_flag to determine whether you are completing the general
        question (8) or the facebook question (9)
        For example, if I wanted to create a graph with 1000 nodes with
        probability 0.1 and find the path between node 0 and node 8 without
        running the code for Facebook Data, I would
        run the command:
        python graph.py 1000 0.1 0 8 0
    3) Running this will produce answers for questions a, b, c and d for Part 3
"""

import sys
import random
import numpy as np
import matplotlib.pyplot as plt


p_list = []
avg_path_list = []

# create a graph of n nodes connected to neighbors with probability p
def create_graph(n,p):
    g = {}
    x = 0
    # initiate graph with empty values
    for x in range(0,n):
        g[x] = set([])
    # add neigbors for each graph with probability p
    for x in range(0,n):
        for y in range(0,n):
            if (y in g[x]) or (x in g[y]) or (y == x):
                continue
            if random.random() < p:
                g[x].add(y)
                g[y].add(x)
    return g

def create_fb_graph():
    g = {}
    # split into nodes and neigbors
    # data is a dictionary with key-value pairs (node,[neighbors])
    file = open('facebook_combined.txt','r')
    for l in file:
        line = l.rstrip('\n')
        data = line.split(' ')
        current = int(data[0])
        neighbor = int(data[1])
        if current not in g:
            g[current] = set([])
        if neighbor not in g:
            g[neighbor] = set([])
        if (neighbor in g[current]) or (current in g[neighbor]) or (current == neighbor):
            continue
        g[current].add(neighbor)
        g[neighbor].add(current)
    return g
        # ultimately we want tuples of node and neighbor

# given a graph G and nodes i,j, output the length of the shortest
# path between i and j in G.
def shortest_path(G,i,j):
    explored = []
    # keep track of all the paths to be checked
    queue = [[i]]
    # return path if start is goal
    if i == j:
        return
    # keeps looping until all possible paths have been checked
    while queue:
        # pop the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        if node not in explored:
            neighbours = G[node]
            # go through all neighbour nodes, construct a new path and
            # push it into the queue
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                # return path if neighbour is goal
                if neighbour == j:
                    return new_path
            # mark node as explored
            explored.append(node)
    # in case there's no path between the 2 nodes
    return None
"""
print a trace of the shortest paths between n random pairs of nodes in graph G
calculate and print the average shortest path for graph G
@output : boolean, True prints to file.
                   False prints to terminal.
"""
def avg_shortest_path(G, n, output, file):
    sum_path_lengths = 0
    avg_path_length = 0
    total_paths = len(G)
    # change sys to print to file
    if output:
        orig_stdout = sys.stdout
        f = open(file, 'w')
        sys.stdout = f
    #iterate through all n nodes in graph G
    for x in range(0,n):
        # generate a random start and end
        i = int(random.random() * len(G))
        j = int(random.random() * len(G))
        pair = (i,j)
        # keep generating end if start is equal to end
        while i == j:
            j = int(random.random() * len(G))
        print(pair)
        # get shortest path for the random pair of nodes
        short = shortest_path(G,i,j)
        # keep track of total shortest paths if they exist
        if short != None:
            sum_path_lengths += len(short)
            # create a printable (start, end, path length) tuple
            sp_tuple = (i,j,len(short))
            if output:
                print(sp_tuple)
        else:
            total_paths -= 1
    # calculate average path length
    avg_path_length = float(sum_path_lengths) / (total_paths)
    if output:
        sys.stdout = orig_stdout
        f.close()
    print("Average Shortest Path Length: " + str(avg_path_length))

    return avg_path_length

# calculate average shortest path for varying probabilities p for a Graph of
# size n.
def varying_p_shortest_paths(n):
    # change sys to print to file
    orig_stdout = sys.stdout
    f = open('varying_p.txt', 'w')
    sys.stdout = f
    for p in range(1,21):
        p = float(p) * 0.05
        graph = create_graph(n,p)
        aspl = avg_shortest_path(graph,n,False,'')
        p_list.append(p)
        avg_path_list.append(aspl)
        print(str(p) + "," + str(aspl))
    sys.stdout = orig_stdout
    f.close()

# create a plot for average shortest path length as a probability of p.
def plot_length_vs_p(n):
    colors = (0,0,0)
    area = np.pi*3
    # change to dot plot later
    plt.plot(p_list,avg_path_list,c=colors,alpha=1)
    plt.title("Average Shortest Path Length for Probability p Given Graph G of size " + str(n))
    plt.xlabel('p, probability of edge between two nodes')
    plt.ylabel('average shortest path length')
    plt.show()

def print_shortest_path(path):
    if path == None:
        print("infinity")
    else:
        print(path)
        print("Length of shortest path: " + str(len(path)))

def main():
    num_nodes = 0
    if len(sys.argv) > 1:
        num_nodes = int(sys.argv[1])
        prob = float(sys.argv[2])
        first = int(sys.argv[3])
        last = int(sys.argv[4])
        fb_flag = int(sys.argv[5])
    if fb_flag:
        fb = create_fb_graph()
        avg_shortest_path(fb,1000,True,'fb_shortest_path.txt')
    else:
        if num_nodes:
            if (num_nodes < first) or (num_nodes < last):
                print("Invalid Arguments")
                exit()
            graph = create_graph(num_nodes,prob)
            print_shortest_path(shortest_path(graph,first,last))
            avg_shortest_path(graph,num_nodes,True,'avg_shortest_path.txt')
            varying_p_shortest_paths(num_nodes)
            plot_length_vs_p(num_nodes)

if __name__ == "__main__":
    main()
