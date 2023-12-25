import re
import math
import networkx as nx
from itertools import combinations

class Solver:

    def __init__(self, *args, **kwargs):
        regex = re.compile(r'\w{3}')
        with open('input.txt') as f:
            self.graph = nx.Graph()
            for line in f.readlines():
                item, *linked_items = [match.group() for match in regex.finditer(line)]
                for linked_item in linked_items:
                    self.graph.add_edge(item, linked_item, capacity=1)

    def solve_first_part(self):
        for pair_of_nodes in combinations(self.graph.nodes, 2):
            nb_cuts, sub_graphs = nx.minimum_cut(self.graph, *pair_of_nodes)
            if nb_cuts == 3:
                return math.prod(len(sub_graph) for sub_graph in sub_graphs)

    def solve_second_part(self):
        return 'Yeehaa !! Merry Christmas !!'
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')