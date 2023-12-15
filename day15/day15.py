import math
import re

class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.sequences = f.read().replace('\n', '').split(',')

    def _hash_sequence(self, sequence):
        result = 0
        for value in sequence:
            result += ord(value) 
            result *= 17
            result %= 256
        return result

    def solve_first_part(self):
        return sum(self._hash_sequence(sequence) for sequence in self.sequences)

    def solve_second_part(self):
        boxes = {}
        regex = re.compile(r'(\w+)(=|-)(\d+)?')
        for sequence in self.sequences:
            label, operator, value = regex.match(sequence).groups()
            box = boxes.setdefault(self._hash_sequence(label), {})
            if operator == '-':
                box.pop(label, None)
                continue
            box[label] = int(value)
        result = 0
        for box, lenses in boxes.items():
            result += sum((box + 1) * index * value for index, value in enumerate(lenses.values(), start=1))
        return result 
            
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')