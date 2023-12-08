import math


class Solver:

    def __init__(self, *args, **kwargs):
        example_races = [(7, 9, ), (15, 40, ), (30, 200, )]
        input_races = [(49, 356, ), (87, 1378, ), (78, 1502, ), (95, 1882, )]
        # self.races = example_races
        self.races = input_races
    
    def _solve(self, a,b,c):
        delta = b**2 - 4 * a * c
        racine_delta = math.sqrt(delta)
        return [(-b - racine_delta)/(2 * a),(-b + racine_delta)/(2 * a)]
    
    def _get_race_result(self, race):
        # record beaten => x(t - x) > r => -x2 + tx - r > 0
        time, record = race
        results = self._solve(-1, time, -record)
        start_result, end_result = sorted(results)
        end_is_integer = end_result.is_integer()
        end_result = math.floor(end_result)
        if end_is_integer:
            end_result -= 1
        return end_result - math.floor(start_result)

    def solve_first_part(self):
        return math.prod(self._get_race_result(race) for race in self.races)

    def solve_second_part(self):
        time = record = ''
        for race_time, race_record in self.races:
            time += f'{race_time}'
            record += f'{race_record}'
        return self._get_race_result((int(time), int(record), ))
                    

solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')