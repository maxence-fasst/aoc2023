import re
from shapely import Polygon

UP = 'U'
RIGHT = 'R'
DOWN = 'D'
LEFT = 'L'

DIRECTIONS = {
    UP: lambda y, x, nb_moves: (y - nb_moves, x),
    RIGHT: lambda y, x, nb_moves: (y, x + nb_moves),
    DOWN: lambda y, x, nb_moves: (y + nb_moves, x),
    LEFT: lambda y, x, nb_moves: (y, x - nb_moves)
}

DIRECTIONS_CODES = {
    '0': RIGHT,
    '1': DOWN,
    '2': LEFT,
    '3': UP 
}

class Solver:

    def __init__(self, *args, **kwargs):
        self.data = []
        regex = re.compile(rf"([{''.join(DIRECTIONS)}]) (\d+) \(#(\w+)\)")
        with open('input.txt') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                direction, nb_moves, hexa = regex.match(line).groups()
                self.data.append((direction, int(nb_moves), hexa))

    def solve_first_part(self):
        actual_y = actual_x = 0    
        points = [(actual_y, actual_x)]
        for direction, nb_moves, _ in self.data:
            actual_y, actual_x = DIRECTIONS.get(direction)(actual_y, actual_x, nb_moves=nb_moves)
            points.append((actual_y, actual_x))
        polygon = Polygon(points)
        return int(polygon.area + polygon.length // 2 + 1)


    def solve_second_part(self):
        actual_y = actual_x = 0    
        points = [(actual_y, actual_x)]
        for *_, hexa in self.data:
            nb_moves = int(hexa[:5], base=16)
            direction = DIRECTIONS_CODES.get(hexa[-1])
            actual_y, actual_x = DIRECTIONS.get(direction)(actual_y, actual_x, nb_moves=nb_moves)
            points.append((actual_y, actual_x))
        polygon = Polygon(points)
        return int(polygon.area + polygon.length // 2 + 1)
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')