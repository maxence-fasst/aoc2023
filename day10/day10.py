START = 'S'
NORTH = 'NORTH'
EAST = 'EAST'
SOUTH = 'SOUTH'
WEST = 'WEST'

PIPES = {
    '|':  { NORTH: SOUTH, SOUTH: NORTH },
    '-': { EAST: WEST, WEST: EAST },
    'L': { NORTH: EAST, EAST: NORTH },
    'J': { NORTH: WEST, WEST: NORTH },
    '7': { SOUTH: WEST, WEST: SOUTH },
    'F': { SOUTH: EAST, EAST: SOUTH }
}


class Solver:

    def __init__(self, *args, **kwargs):
        self.grid = []
        self.start = None
        with open('input.txt') as f:
            for index, line in enumerate(f.readlines()):
                self.grid.append(line.strip())
                if START in line:
                    self.start = (index, line.index(START))

    def _get_next(self, point, from_direction = None, path = None):
        path = path or []
        pos_y, pos_x = point
        if point == self.start:
            for try_y, try_x in [(pos_y - 1 , pos_x), (pos_y, pos_x + 1), (pos_y + 1, pos_x), (pos_y, pos_x - 1)]:
                if try_x < 0 or try_y < 0:
                    continue
                try:
                    next_coords = (try_y, try_x)
                    next_value = self.grid[try_y][try_x]
                    if next_value in PIPES:
                        path.append(next_coords)
                        if not from_direction:
                            if pos_y == try_y:
                                from_direction = EAST if pos_x > try_x else WEST
                            else:
                                from_direction = SOUTH if pos_y > try_y else NORTH
                        return next_coords, from_direction, path
                except:
                    continue
        actual_value = self.grid[pos_y][pos_x]
        next_direction = PIPES.get(actual_value).get(from_direction)
        if next_direction == NORTH:
            next_coords = (pos_y - 1, pos_x)
            from_direction = SOUTH
        elif next_direction == SOUTH:
            next_coords = (pos_y + 1, pos_x)
            from_direction = NORTH
        elif next_direction == EAST:
            next_coords = (pos_y, pos_x + 1)
            from_direction = WEST
        else:
            next_coords = (pos_y, pos_x - 1)
            from_direction = EAST
        path.append(next_coords)
        return next_coords, from_direction, path
        
    def _get_path(self):
        next = None
        from_direction = None
        path = []
        while next != self.start:
            next, from_direction, path = self._get_next(next or self.start, from_direction=from_direction, path=path)
        return path   

    def solve_first_part(self):
        path = self._get_path()
        return len(path) // 2

    def solve_second_part(self):
        from shapely import Point, Polygon
        path = self._get_path()
        polygon = Polygon([(x, y) for y, x in path])
        nb_points_in_area = 0
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if polygon.contains(Point(x, y)):
                    nb_points_in_area += 1
        return nb_points_in_area

        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')