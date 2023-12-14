from itertools import pairwise

NORTH = 'NORTH'
WEST = 'WEST'
SOUTH = 'SOUTH'
EAST = 'EAST'

class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.grid = []
            for line in f.readlines():
                self.grid.append(line.strip())

    def _reverse_grid(self, grid):
        return [''.join(element) for element in zip(*grid)]
    
    def _move(self, grid, direction):
        result = []
        len_line = len(grid)
        if direction == NORTH:
            grid = self._reverse_grid(grid)
            transform_line = lambda line: line
            transform_result = lambda result: self._reverse_grid(result)
        elif direction == WEST:
            transform_line = lambda line: line
            transform_result = lambda result: result
        elif direction == SOUTH:
            grid = self._reverse_grid(grid)
            transform_line = lambda line: ''.join(list(reversed(line)))
            transform_result = lambda result: self._reverse_grid(result)
        elif direction == EAST:
            transform_line = lambda line: ''.join(list(reversed(line)))
            transform_result = lambda result: result
        for line in grid:
            new_line = ''
            line = transform_line(line)
            cube_rock_indexes = [i for i, value in enumerate(line) if value == '#']
            for start_index, end_index in pairwise(sorted(set([-1, *cube_rock_indexes, len_line]))):
                nb_rocks = line[start_index + 1:end_index].count('O')
                new_line += 'O' * nb_rocks + line[nb_rocks + start_index + 1:end_index + 1].replace('O', '.') 
            result.append(transform_line(new_line[:len_line]))
        return transform_result(result)
    
    def solve_first_part(self):
        return self._get_total_north_load(self._move(self.grid, NORTH))
        
    def _run_cycle(self, grid):
        result = grid
        for direction in [NORTH, WEST, SOUTH, EAST]:
            result = self._move(result, direction)
        return result
    
    def _get_total_north_load(self, grid):
        result = 0
        for index, line in enumerate(reversed(grid), start=1):
            result += line.count('O') * index
        return result

    def solve_second_part(self):
        result = self.grid
        cycle_results = []
        while True:
            result = self._run_cycle(result)
            if result in cycle_results:
                break
            cycle_results.append(result)
        find_index = cycle_results.index(result)
        cycle_results = cycle_results[find_index:]
        result_to_get = cycle_results[(1_000_000_000 - find_index) % len(cycle_results) - 1]
        return self._get_total_north_load(result_to_get)

        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')