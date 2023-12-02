import re
from itertools import groupby

class Resolver:

    MAX_VALUES = {
        'red': 12,
        'green': 13,
        'blue': 14
    }

    REGEX = re.compile(r'((\d+) (blue|red|green))')

    def __init__(self, *args, **kwargs):
        self.games = {}
        with open('input.txt') as f:
            for index, line in enumerate(f.readlines(), start=1):
                self.games[index] = line.replace('\n', '').split(':')[1]

    def _is_set_possible(self, cube_set):
        for _, number, color in self.REGEX.findall(cube_set):
            if int(number) > self.MAX_VALUES.get(color):
                return False
        return True
                                  
    def resolve_first_part(self):
        result = 0
        for game_id, game in self.games.items():
            if all(self._is_set_possible(cube_set) for cube_set in game.split(';')):
                result += game_id
        return result
    
    def resolve_second_part(self):
        by_color = lambda match: match[2]
        powers = []
        for game in self.games.values():
            matches = sorted(self.REGEX.findall(game), key=by_color)
            power = 1
            for _, items in groupby(matches, key=by_color):
                max_color = max(int(item[1]) for item in list(items))
                power *= max_color
            powers.append(power)
        return sum(powers)


resolver = Resolver()
print(f'Solution 1 = {resolver.resolve_first_part()}')
print(f'Solution 2 = {resolver.resolve_second_part()}')