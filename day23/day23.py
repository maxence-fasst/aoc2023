import networkx as nx

PATH = '.'
FOREST = '#'

DIRECTIONS = {
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '<': [(-1, 0)],
    '>': [(1, 0)],
    '^': [(0, -1)],
    'v': [(0, 1)]
}


class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.points = {}
            for y, line in enumerate(f.readlines()):
                for x, value in enumerate(line.replace('\n', '')):
                    if value == FOREST:
                        continue
                    coords = (x, y)
                    if y == 0:
                        self.start = coords
                    self.points[coords] = value
            self.end = coords

    def _create_graph(self, treat_slopes_as_normal_path=False):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.points.keys())
        for node in graph.nodes:
            current_x, current_y = node
            for add_x, add_y in DIRECTIONS.get(PATH if treat_slopes_as_normal_path else self.points.get(node)):
                new_coords = (current_x + add_x, current_y + add_y)
                if new_coords in self.points:
                    graph.add_edge(node, new_coords)
        return graph
    
    def solve_first_part(self):
        graph = self._create_graph()
        return max(len(path) for path in nx.all_simple_edge_paths(graph, self.start, self.end))

    def solve_second_part(self):
        # (Not working) Bruteforce taking way too long ;(
        graph = self._create_graph(treat_slopes_as_normal_path=True)
        return max(len(path) for path in nx.all_simple_edge_paths(graph, self.start, self.end))

        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
# print(f'Solution 2 = {solver.solve_second_part()}')