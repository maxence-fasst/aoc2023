from itertools import pairwise

class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.patterns = []
            actual_pattern = []
            for line in f.readlines():
                line = line.strip()
                if not line:
                    self.patterns.append(actual_pattern)
                    actual_pattern = []
                    continue
                actual_pattern.append(line)
            self.patterns.append(actual_pattern)

    def _find_reflection_index(self, pattern, original_index=None):
        for index, (line, next_line) in enumerate(pairwise(pattern)):
            if line == next_line:
                len_to_check = min(index, len(pattern) - index - 2)
                left_list = list(reversed(pattern[max(0, index - len_to_check): index]))
                right_list = pattern[index + 2: index + len_to_check + 2]
                if all(left == right for left, right in zip(left_list, right_list)):
                    result = index + 1
                    if original_index:
                        if result != original_index:
                            return result
                    else:
                        return result
        return 0

    def _find_reflection_value(self, pattern, original_value=None):
        # Horizontal
        original_index = original_value // 100 if original_value and original_value >= 100 else None
        horizontal_index = self._find_reflection_index(pattern, original_index=original_index)
        if horizontal_index:
            return horizontal_index * 100

        # Vertical
        new_pattern = [''.join(element) for element in zip(*pattern)]
        original_index = original_value if original_value and original_value < 100 else None
        vertical_index = self._find_reflection_index(new_pattern, original_index=original_index)
        if vertical_index:
            return vertical_index
        return 0
            
    def solve_first_part(self):
        return sum(self._find_reflection_value(pattern) for pattern in self.patterns)
    
    def _solve_with_smudge(self, pattern):
        original_value = self._find_reflection_value(pattern)
        for y, line in enumerate(pattern):
            for x, value in enumerate(line):
                new_pattern = pattern.copy()
                new_pattern[y] = pattern[y][:x] + ('#' if value == '.' else '.') + pattern[y][x + 1:]
                reflection_value = self._find_reflection_value(new_pattern, original_value=original_value)
                if reflection_value:
                    return reflection_value
                 
    def solve_second_part(self):
        return sum(self._solve_with_smudge(pattern) for pattern in self.patterns)


solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')