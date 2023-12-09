class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.reports = []
            for line in f.readlines():
                self.reports.append([int(value) for value in line.strip().split(' ')])

    def _get_repetitive_elements(self, elements):
        shortest = [] 
        if len(elements) <= 1: 
            return elements
        if len(set(elements)) == len(elements): 
            return elements
        for x in range(len(elements)):
            if elements[0:x] == elements[x:2 * x]:
                shortest = elements[0:x] 
        return shortest 
    
    def _solve_report(self, report, backwards=False):
         if len(set(report)) == 1:
             return report[0]
         pattern = self._get_repetitive_elements(report)
         sub_report = [(pattern[index + 1] - pattern[index]) for index in range(len(pattern) - 1)]
         if len(sub_report) == 0:
             sub_report = [(report[index + 1] - report[index]) for index in range(len(report) - 1)]
             pattern = report
         if backwards:
            return pattern[0] - self._solve_report(sub_report, backwards=backwards)
         return pattern[-1] + self._solve_report(sub_report, backwards=backwards)

    def solve_first_part(self):
        return sum(self._solve_report(report) for report in self.reports)

    def solve_second_part(self):
        return sum(self._solve_report(report, backwards=True) for report in self.reports)
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')