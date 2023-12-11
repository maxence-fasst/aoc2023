from itertools import combinations

class Solver:

    def __init__(self, *args, **kwargs):
        grid = []
        self.galaxies = []
        with open('input.txt') as f:
            for y, line in enumerate(f.readlines()):
                grid.append(line.strip())
                for x, value in enumerate(line):
                    if value == '#':
                        self.galaxies.append((y, x))
            self.empty_y = self._get_empty_indexes(grid)
            self.empty_x = self._get_empty_indexes(zip(*grid))


    def _get_empty_indexes(self, grid):
        result = []
        for index, line in enumerate(grid):
            if set(line) == {'.'}:
                result.append(index)
        return result
    
    def _get_expanded_coords(self, point, expansion):
        y, x = point
        y += len([index for index in self.empty_y if index < y]) * (expansion - 1)
        x += len([index for index in self.empty_x if index < x]) * (expansion - 1)
        return (y, x)
    
    def _get_min_distance(self, point1, point2, expansion):
        y1, x1 = self._get_expanded_coords(point1, expansion=expansion)
        y2, x2 = self._get_expanded_coords(point2, expansion=expansion)
        return abs(x1 - x2) + abs(y1 - y2) 

    def solve_first_part(self):
        paths_to_solve = combinations(self.galaxies, 2)
        return sum(self._get_min_distance(point1, point2, expansion=2) for point1, point2 in paths_to_solve)

    def solve_second_part(self):
        paths_to_solve = combinations(self.galaxies, 2)
        return sum(self._get_min_distance(point1, point2, expansion=1_000_000) for point1, point2 in paths_to_solve)
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')