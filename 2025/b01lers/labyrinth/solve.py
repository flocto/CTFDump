import re

data = open('nodes.txt', 'r').readlines()

graph = {}
modifications = {}

class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_edge(self, node):
        self.edges.append(node)

cur_node = None
for line in data:
    # parsing node at 0xH...
    if re.match(r'parsing node at 0x[0-9a-fA-F]+', line):
        cur_node = line.split(' ')[-1].strip()
        graph[cur_node] = []