import re
import math

ACCEPTED = 'A'
REJECTED = 'R'

WORKFLOW_RESUlTS = [ACCEPTED, REJECTED]

REGEX_INSTRUCTION = re.compile(r'([xmas])(<|>)(\d+)')

class Solver:

    def __init__(self, *args, **kwargs):
        self.workflows = {}
        self.ratings = []
        regex_workflow = re.compile(r'(\w+){(.*)}')
        regex_rating = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')
        with open('input.txt') as f:
            workflow_done = False
            for line in f.readlines():
                line = line.strip().replace('\n', '')       
                if not line:
                    workflow_done = True
                    continue
                if not workflow_done:
                    key, rules = regex_workflow.match(line).groups()
                    self.workflows[key] = rules
                    continue
                self.ratings.append([int(group) for group in regex_rating.match(line).groups()])

    def _solve_workflow(self, rating, workflow='in'):
        rules = self.workflows.get(workflow)
        x, m, a, s = rating
        for instruction in rules.split(','):
            try:
                func, result = instruction.split(':')
                if eval(func):
                    next = result
                    break
            except ValueError:
                next = instruction
        return next if next in WORKFLOW_RESUlTS else self._solve_workflow(rating, next)

    def solve_first_part(self):
        result = 0
        for rating in self.ratings:
            if self._solve_workflow(tuple(rating)) == ACCEPTED:
                result += sum(rating)
        return result
    
    def _get_ranges_product(self, ranges):
        result = 1
        for r in ranges.values():
            start, end = r
            result *= end - start + 1
        return result
    
    def _count_combinations(self, workflow, ranges):
        if workflow == REJECTED:
            return 0
        if workflow == ACCEPTED:
            return self._get_ranges_product(ranges)
        result = 0
        current_workflow = self.workflows.get(workflow)
        for rule in current_workflow.split(','):
            try:
                instruction, next_workflow = rule.split(':')
                check_var, op, value = REGEX_INSTRUCTION.match(instruction).groups()
                value = int(value)
                actual_start, actual_end = ranges.get(check_var)
                if op == '<':
                    accepted_range = (actual_start, value - 1)
                    rejected_range = (value, actual_end)
                else:
                    accepted_range = (value + 1, actual_end)
                    rejected_range = (actual_start, value)
                if sum(accepted_range) >= 0:
                    ranges = ranges | { check_var: accepted_range }  #  ranges = { **ranges, **{ check_var: accepted_range } }
                    result += self._count_combinations(next_workflow, ranges)
                if sum(rejected_range) >= 0:
                    ranges = ranges | { check_var: rejected_range }  #  ranges = { **ranges, **{ check_var: rejected_range } }
            except ValueError:
                # Split(':') failed -> rule = next worklow in that case 
                result += self._count_combinations(rule, ranges)
        return result
        
    def solve_second_part(self):
        return self._count_combinations('in', dict.fromkeys('xmas', (1, 4000)))
                        
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')