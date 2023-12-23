import re
import math
import queue
from copy import deepcopy

START = 'S'
FLIP_FLOP = '%'
CONJUNCTION = '&'

ON = 'ON'
OFF = 'OFF'

HIGH_PULSE = 'H'
LOW_PULSE = 'L'

END_MODULE = 'rx'


class Module:

    def __init__(self, module_type, name, targets, *args, **kwargs):
        self.state = OFF
        self.type = module_type or START
        self.name = name
        self.targets = targets.split(', ')
        self.last_pulse_sent = LOW_PULSE
        self.parents = []
    
    def switch(self):
        self.state = ON if self.state == OFF else OFF

class Solver:

    def __init__(self, *args, **kwargs):
        self._initial_modules = {}
        regex = re.compile(r'([%|&]?)(\w+) -> (.+)')
        with open('input.txt') as f:
            for line in f.readlines():
                line = line.strip().replace('\n', '')       
                if not line:
                    continue
                module_type, name, targets = regex.match(line).groups()
                if END_MODULE in targets:
                    self.final_operating_module = name
                self._initial_modules[name] = Module(module_type, name, targets)
        for conjunction_module in [module for module in self._initial_modules.values() if module.type == CONJUNCTION]:
            conjunction_module.parents.extend(module.name for module in self._initial_modules.values() if conjunction_module.name in module.targets)

    def _reset_modules(self):
        self.modules = deepcopy(self._initial_modules)

    def _push_button(self, search_high_pulse_on_conjunction=None):
        nb_low_pulses = nb_high_pulses = 0
        q = queue.Queue()
        q.put(('broadcaster', LOW_PULSE))
        while not q.empty():
            actual_name, pulse = q.get()
            if pulse == LOW_PULSE:
                nb_low_pulses += 1
            else:
                nb_high_pulses += 1
            actual_module = self.modules.get(actual_name)
            if not actual_module:  # Output module
                continue
            if actual_module.type == FLIP_FLOP:
                if pulse == HIGH_PULSE:
                    continue
                else:
                    actual_module.switch()
                    next_pulse = LOW_PULSE if actual_module.state == OFF else HIGH_PULSE
            elif actual_module.type == CONJUNCTION:
                if pulse == LOW_PULSE:
                    next_pulse = HIGH_PULSE
                else:
                    parents_modules = [module for module in self.modules.values() if module.name in actual_module.parents]
                    next_pulse = LOW_PULSE if all(module.last_pulse_sent == HIGH_PULSE for module in parents_modules) else HIGH_PULSE
                if search_high_pulse_on_conjunction and search_high_pulse_on_conjunction == actual_name and next_pulse == HIGH_PULSE:
                    return 0, 0, True
            else: # START
                next_pulse = pulse
            for target_name in actual_module.targets:
                q.put((target_name, next_pulse))
            actual_module.last_pulse_sent = next_pulse
        return nb_low_pulses, nb_high_pulses, False
    

    def solve_first_part(self):
        self._reset_modules()
        nb_low_pulses = nb_high_pulses = 0
        for _ in range(1000):
            nb_low_push, nb_high_push, _junk = self._push_button()
            nb_low_pulses += nb_low_push
            nb_high_pulses += nb_high_push
        return nb_low_pulses * nb_high_pulses

        
    def solve_second_part(self):
        results = []
        for parent in self._initial_modules.get(self.final_operating_module).parents:
            self._reset_modules()
            parent_result = 0
            while True:
                parent_result += 1
                *_, found = self._push_button(search_high_pulse_on_conjunction=parent)
                if found:
                    results.append(parent_result)
                    break
        return math.lcm(*results)
                        
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')