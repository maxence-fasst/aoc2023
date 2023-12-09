class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.reports = []
            for line in f.readlines():
                self.reports.append([int(value) for value in line.strip().split(' ')])

    def _solve_report(self, report, backwards=False):
        if len(set(report)) == 1:
            return report[0]
        sub_report = [(report[index + 1] - report[index]) for index in range(len(report) - 1)]
        if backwards:
            return report[0] - self._solve_report(sub_report, backwards=backwards)
        return report[-1] + self._solve_report(sub_report, backwards=backwards)

    def solve_first_part(self):
        return sum(self._solve_report(report) for report in self.reports)

    def solve_second_part(self):
        return sum(self._solve_report(report, backwards=True) for report in self.reports)
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')