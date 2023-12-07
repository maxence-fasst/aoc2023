import re

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIRS = 3
ONE_PAIRS = 2
HIGH_CARD = 1

SORTED_VALUES = {
    'A': 'Z',
    'K': 'Y',
    'Q': 'X',
    'J': 'W',
    'T': 'V'
}

JOKER = 'J'

class Hand:

    def __init__(self, string_value, bid_amount, *args, **kwargs):
        self.string_value = string_value
        self.bid_amount = bid_amount
        self.strength = self._get_hand_strength()
        self.sorted_value = ''.join(SORTED_VALUES.get(c, c) for c in self.string_value)
        self.strength_with_joker = self._get_hand_strength_with_joker()
        self.sorted_value_with_joker = ''.join(SORTED_VALUES.get(c, c) for c in self.string_value.replace(JOKER, '0'))


    def _get_hand_strength(self):
        string_to_check = ''.join(sorted(self.string_value))
        if re.findall(r'((\w)\2{4,})', string_to_check):
            return FIVE_OF_A_KIND
        if re.findall(r'((\w)\2{3,})', string_to_check):
            return FOUR_OF_A_KIND
        pair_regex = r'((\w)\2{1,})'
        is_three_of_a_kind = re.findall(r'((\w)\2{2,})', string_to_check)
        if is_three_of_a_kind:
            match = is_three_of_a_kind[0][0]
            if re.findall(pair_regex, string_to_check.replace(match, '')):
                return FULL_HOUSE
            return THREE_OF_A_KIND
        pairs = re.findall(pair_regex, string_to_check)
        if not pairs:
            return HIGH_CARD
        return TWO_PAIRS if len(pairs) == 2 else ONE_PAIRS
    
    def _get_hand_strength_with_joker(self):
        if self.strength == FIVE_OF_A_KIND:
            return FIVE_OF_A_KIND
        if self.strength == FOUR_OF_A_KIND:
            return FIVE_OF_A_KIND if JOKER in self.string_value else FOUR_OF_A_KIND
        if self.strength == FULL_HOUSE:
            return FIVE_OF_A_KIND if JOKER in self.string_value else FULL_HOUSE
        if self.strength == THREE_OF_A_KIND:
            return FOUR_OF_A_KIND if JOKER in self.string_value else THREE_OF_A_KIND
        if self.strength == TWO_PAIRS:
            nb_jokers = self.string_value.count(JOKER)
            if nb_jokers == 0:
                return TWO_PAIRS
            if nb_jokers == 1:
                return FULL_HOUSE
            if nb_jokers > 1:
                return FOUR_OF_A_KIND
        if self.strength == ONE_PAIRS:
            return THREE_OF_A_KIND if JOKER in self.string_value else ONE_PAIRS
        if self.strength == HIGH_CARD:
            return ONE_PAIRS if JOKER in self.string_value else HIGH_CARD


class Resolver:

    def __init__(self, *args, **kwargs):
        self.hands = []
        with open('input.txt') as f:
            for line in f.readlines():
                hand_value, bid_amount = [match.group() for match in re.finditer(r'[AKQJT\d]+', line)]
                self.hands.append(Hand(hand_value, int(bid_amount)))
                
    def resolve_first_part(self):
        result = 0
        sorted_hands = sorted(self.hands, key=lambda h: (h.strength, h.sorted_value))
        for rank, hand in enumerate(sorted_hands, start=1):
            result += rank * hand.bid_amount
        return result

    def resolve_second_part(self):
        result = 0
        sorted_hands = sorted(self.hands, key=lambda h: (h.strength_with_joker, h.sorted_value_with_joker))
        for rank, hand in enumerate(sorted_hands, start=1):
            result += rank * hand.bid_amount
        return result
        

resolver = Resolver()
print(f'Solution 1 = {resolver.resolve_first_part()}')
print(f'Solution 2 = {resolver.resolve_second_part()}')