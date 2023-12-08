import re


class Card:

    REGEX_NUMBERS = r'\d+'

    def __init__(self, string_value, *args, **kwargs):
        winning_numbers, numbers = string_value.split(':')[1].split('|')
        self.winning_numbers = {int(match.group()) for match in re.finditer(self.REGEX_NUMBERS, winning_numbers)}
        self.numbers = {int(match.group()) for match in re.finditer(self.REGEX_NUMBERS, numbers)}

    def get_corresponding_numbers_count(self):
        return len(self.winning_numbers & self.numbers)

    def get_score(self):
        corresponding_numbers = self.get_corresponding_numbers_count()
        return 0 if corresponding_numbers == 0 else 2**(corresponding_numbers - 1)


class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.cards = [Card(line.replace('\n', '')) for line in f.readlines()]
              
    def solve_first_part(self):
        return sum(card.get_score() for card in self.cards)

    def solve_second_part(self):
        cards_with_copy = { index: 1 for index in range(len(self.cards))}
        for index, card in enumerate(self.cards):
            corresponding_numbers = card.get_corresponding_numbers_count()
            for i in range(corresponding_numbers):
                number_of_copies = cards_with_copy.get(index + i + 1)
                if not number_of_copies:
                    break
                cards_with_copy[index + i + 1] = number_of_copies + cards_with_copy.get(index)
        return sum(cards_with_copy.values())



solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')