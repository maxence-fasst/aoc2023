import re

class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.data = [line.replace('\n', '') for line in f.readlines()]

    REPLACEMENTS = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    def _solve(self, with_string_numbers=False):
        regex = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))") if with_string_numbers else re.compile(r'\d') 
        result = 0
        for line in self.data:
            digits = regex.findall(line)
            start, end = digits[0], digits[-1]
            result += int(f'{self.REPLACEMENTS.get(start, start)}{self.REPLACEMENTS.get(end, end)}')
        return result

    def solve_first_part(self):
        return self._solve()
    
    def solve_second_part(self):
        return self._solve(with_string_numbers=True)


solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')