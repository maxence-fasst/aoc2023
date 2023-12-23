START = 'S'
ROCK = '#'


class Solver:

    def __init__(self, *args, **kwargs):
        self.garden = []
        self.start = None
        with open('input.txt') as f:
            for y, line in enumerate(f.readlines()):
                self.garden.append(line.replace('\n', ''))
                if not self.start and START in line:
                    self.start = (y, line.index(START))
    
    def _is_in_range(self, y, x):
        if y < 0 or x < 0:
            return False
        if y == len(self.garden) or x == len(self.garden[0]):
            return False
        return True
        
    def _run_step(self, targets):
        result = set()
        for y, x in targets:
            for add_y, add_x in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                new_y = y + add_y
                new_x = x + add_x
                if not self._is_in_range(new_y, new_x) or self.garden[new_y][new_x] == ROCK:
                    continue
                result.add((new_y, new_x))
        return result

    def solve_first_part(self):
        targets = set()
        targets.add(self.start)
        for _ in range(64):
            targets = self._run_step(targets=targets)
        return len(targets)

    def solve_second_part(self):
        pass
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')