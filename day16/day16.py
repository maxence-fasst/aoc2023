NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

DIRECTIONS = {
    NORTH: {
        '.': { 'from_direction': NORTH, 'next_pos': lambda y, x: (y + 1, x) },
        '|': { 'from_direction': NORTH, 'next_pos': lambda y, x: (y + 1, x) },
        '/': { 'from_direction': EAST, 'next_pos': lambda y, x: (y, x - 1) },
        '\\': { 'from_direction': WEST, 'next_pos': lambda y, x: (y, x+ 1) }
    },
    EAST: {
        '.': { 'from_direction': EAST, 'next_pos': lambda y, x: (y, x - 1) },
        '-': { 'from_direction': EAST, 'next_pos': lambda y, x: (y, x - 1) },
        '/': { 'from_direction': NORTH, 'next_pos': lambda y, x: (y + 1, x) },
        '\\': { 'from_direction': SOUTH, 'next_pos': lambda y, x: (y - 1, x) }
    },
    SOUTH: {
        '.': { 'from_direction': SOUTH, 'next_pos': lambda y, x: (y - 1, x) },
        '|': { 'from_direction': SOUTH, 'next_pos': lambda y, x: (y - 1, x) },
        '/': { 'from_direction': WEST, 'next_pos': lambda y, x: (y, x + 1) },
        '\\': { 'from_direction': EAST, 'next_pos': lambda y, x: (y, x - 1) }
    },
    WEST: {
        '.': { 'from_direction': WEST, 'next_pos': lambda y, x: (y, x + 1) },
        '-': { 'from_direction': WEST, 'next_pos': lambda y, x: (y, x + 1) },
        '/': { 'from_direction': SOUTH, 'next_pos': lambda y, x: (y - 1, x) },
        '\\': { 'from_direction': NORTH, 'next_pos': lambda y, x: (y + 1, x) }
    }
}

class Solver:

    def __init__(self, *args, **kwargs):
        self.grid = []
        with open('input.txt') as f:
            for line in f.readlines():
                self.grid.append(line.strip().replace('\n', ''))

    def _split(self, position, from_direction, path, splits):
        result = []
        start_y, start_x = position
        splits.add(position)
        if from_direction in [NORTH, SOUTH]:
            if start_x > 0:
                result = self._run_path((start_y, start_x - 1), EAST, path=path, splits=splits)
            result = self._run_path((start_y, start_x + 1), WEST, path=path, splits=splits)
        else:
            if start_y > 0:
                result = self._run_path((start_y - 1, start_x), SOUTH, path=path, splits=splits)
            result = self._run_path((start_y + 1, start_x), NORTH, path=path, splits=splits)
        return result

    def _run_path(self, position, from_direction, path=None, splits=None):
        try:
            path = path or set()
            splits = splits or set()
            start_y, start_x = position
            if (start_y, start_x, from_direction) in path:
                return path, splits
            try:
                value = self.grid[start_y][start_x]
            except IndexError:
                return path, splits
            path.add((start_y, start_x, from_direction))
            instructions = DIRECTIONS.get(from_direction).get(value)
            if not instructions:
                if position in splits:
                    return path, splits
                return self._split(position, from_direction, path=path, splits=splits)
            next_y, next_x = instructions.get('next_pos')(start_y, start_x)
            if next_y == -1 or next_x == -1:
                return path, splits
            next_from_direction = instructions.get('from_direction')
            return self._run_path((next_y, next_x), next_from_direction, path=path, splits=splits)
        except RecursionError:
            return path, splits
    
    def get_nb_energized_tiles(self, result):
        path, _ = result
        return len(set((y, x) for y, x, _ in path))

    def solve_first_part(self):
        return self.get_nb_energized_tiles(self._run_path((0, 0), WEST))

    def solve_second_part(self):
        len_grid = len(self.grid)
        energized_tiles = set()
        # Top  & bottom rows
        for start_x in range(len_grid):
            energized_tiles.add(self.get_nb_energized_tiles(self._run_path((0, start_x), NORTH)))
            energized_tiles.add(self.get_nb_energized_tiles(self._run_path((len_grid - 1, start_x), SOUTH)))
        # Leftmost & rigtmost columns
        for start_y in range(len_grid):
            energized_tiles.add(self.get_nb_energized_tiles(self._run_path((start_y, 0), WEST)))
            energized_tiles.add(self.get_nb_energized_tiles(self._run_path((start_y, len_grid - 1), EAST)))
        return max(energized_tiles)

        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')
