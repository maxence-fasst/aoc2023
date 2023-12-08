import math
import re
from itertools import cycle

class Solver:

    def __init__(self, *args, **kwargs):
        self.instructions = None
        self.network = {}
        with open('input.txt') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                if not self.instructions:
                    self.instructions = line
                else:
                    network_id, left, right = [match.group() for match in re.finditer(r'\w+', line)]
                    self.network[network_id] = { 'L': left, 'R': right }

    def _solve(self, starting_id, end_function):
        network_id = starting_id
        for step, direction in enumerate(cycle(self.instructions), start=1):
            network_id = self.network.get(network_id).get(direction)
            if end_function(network_id):
                return step

    def solve_first_part(self):
        return self._solve('AAA', end_function=lambda nid: nid == 'ZZZ')

    def solve_second_part(self):
        end_func = lambda nid: nid.endswith('Z')
        starting_nodes = { node_id: self._solve(node_id, end_func) for node_id in self.network if node_id.endswith('A') }
        return math.lcm(*starting_nodes.values())
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')