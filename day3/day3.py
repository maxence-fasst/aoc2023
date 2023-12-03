import math
import re

class Resolver:

    REGEX_NUMBERS = r'\d+'

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.data = [line.replace('\n', '') for line in f.readlines()]
            self.line_length = len(self.data[0])

    def _is_part_number(self, line_index, start_index, end_index):
        line_to_check = '' if line_index == 0 else self.data[line_index - 1][start_index - 1:end_index + 1]
        line_to_check += f'{"" if start_index == 0 else self.data[line_index][start_index - 1]}{"" if end_index == self.line_length else self.data[line_index][end_index]}'
        line_to_check += '' if line_index == len(self.data) - 1 else self.data[line_index + 1][max(0, start_index - 1):min(self.line_length -1, end_index + 1)]
        return not all(c == '.' or c.isdigit() for c in line_to_check)

    def _get_line_result(self, line_index, line):
        line_result = 0
        for match in re.finditer(self.REGEX_NUMBERS, line):
            start_index, end_index = match.span()
            if self._is_part_number(line_index, start_index, end_index):
                line_result += int(match.group())
        return line_result
                     
    def resolve_first_part(self):
        result = 0
        for index, line in enumerate(self.data):
            result += self._get_line_result(index, line)
        return result
    
    def _get_potential_gear_numbers(self, index_line, potential_gear_index, same_line = False):
        numbers = []
        if index_line < 0:
            return []
        try:
            line_to_check = self.data[index_line]
        except IndexError:
            return []
        for match in re.finditer(self.REGEX_NUMBERS, line_to_check):
            start_index, end_index = match.span()
            if same_line:
                if end_index == potential_gear_index or start_index == potential_gear_index + 1:
                    numbers.append(int(match.group()))
            else:
                set_gear = set(range(potential_gear_index - 1, potential_gear_index + 2))
                set_match = set(range(match.start(), match.end()))
                if set_gear & set_match:
                    numbers.append(int(match.group()))
        return numbers
    
    def _get_potential_gear_ratio(self, index_line, potential_gear_index):
        numbers = []
        numbers.extend(self._get_potential_gear_numbers(index_line - 1, potential_gear_index))
        numbers.extend(self._get_potential_gear_numbers(index_line, potential_gear_index, same_line=True))
        numbers.extend(self._get_potential_gear_numbers(index_line + 1, potential_gear_index))
        if len(numbers) == 2:
            return math.prod(numbers)
        return 0

    def resolve_second_part(self):
        result = 0
        for index_line, line in enumerate(self.data):
            for potential_gear_index in [match.start() for match in re.finditer(r'\*', line)]:
                result += self._get_potential_gear_ratio(index_line, potential_gear_index)
        return result


resolver = Resolver()
print(f'Solution 1 = {resolver.resolve_first_part()}')
print(f'Solution 2 = {resolver.resolve_second_part()}')