from functools import cache

class Solver:

    def __init__(self, *args, **kwargs):
        self.rows = []
        with open('input.txt') as f:
            for line in f.readlines():
                pattern, groups = line.strip().split(' ')
                groups = [int(group) for group in groups.split(',')]
                self.rows.append((pattern, tuple(groups)))
    
    @cache
    def _get_nb_options(self, pattern, groups, done=0):
        if not pattern:
            return not groups and not done
        result = 0
        pattern = pattern if pattern.endswith(".") else pattern + "."
        if pattern.startswith("?"):
            cells = ".#"
        else:
            cells = pattern[:1]
        for cell in cells:
            if cell == "#":
                result += self._get_nb_options(pattern[1:], groups, done + 1)
            elif done and groups and groups[0] == done:
                result += self._get_nb_options(pattern[1:], groups[1:])
            elif not done:
                result += self._get_nb_options(pattern[1:], groups)
        return result
    
    def solve_first_part(self):
        return sum(self._get_nb_options(pattern, groups) for pattern, groups in self.rows)

    def solve_second_part(self):
        return sum(self._get_nb_options('?'.join([pattern] * 5), groups * 5) for pattern, groups in self.rows)
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')
