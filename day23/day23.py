import networkx as nx

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
            self.len_y = y + 1
            self.len_x = x + 1

    def _create_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from(self.points.keys())
        for node in graph.nodes:
            current_x, current_y = node
            for add_x, add_y in DIRECTIONS.get(self.points.get(node)):
                new_coords = (current_x + add_x, current_y + add_y)
                if new_coords in self.points:
                    graph.add_edge(node, new_coords)
        return graph
    
    def solve_first_part(self):
        graph = self._create_graph()
        return max(len(path) for path in nx.all_simple_edge_paths(graph, self.start, self.end))
    
    def _create_reduced_graph(self):
        graph = nx.grid_2d_graph(self.len_x, self.len_y)
        for x in range(self.len_x):
            for y in range(self.len_y):
                if (x, y) not in self.points:
                    graph.remove_node((x, y))
        simple_nodes = [node for node in graph.nodes if len(graph.edges(node)) == 2]
        for node in simple_nodes:
            neighbours = tuple(graph.neighbors(node))
            weight = sum(graph.edges[node, neighbour].setdefault("weight", 1) for neighbour in neighbours)
            graph.add_edge(*neighbours, weight=weight)
            graph.remove_node(node)
        return graph

    def solve_second_part(self):
        graph = self._create_reduced_graph()
        return max(nx.path_weight(graph, path, "weight") for path in nx.all_simple_paths(graph, self.start, self.end))

        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')