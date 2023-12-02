import re

class Resolver:

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

    def _resolve(self, with_string_numbers=False):
        regex = re.compile(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))") if with_string_numbers else re.compile(r'\d') 
        result = 0
        for line in self.data:
            digits = regex.findall(line)
            start, end = digits[0], digits[-1]
            result += int(f'{self.REPLACEMENTS.get(start, start)}{self.REPLACEMENTS.get(end, end)}')
        return result

    def resolve_first_part(self):
        return self._resolve()
    
    def resolve_second_part(self):
        return self._resolve(with_string_numbers=True)


resolver = Resolver()
print(f'Solution 1 = {resolver.resolve_first_part()}')
print(f'Solution 2 = {resolver.resolve_second_part()}')