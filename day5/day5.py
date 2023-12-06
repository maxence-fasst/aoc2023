import re

class Range:

    def __init__(self, line, *args, **kwargs):
        corresponding_value, start, length = [int(match.group()) for match in re.finditer(r'\d+', line)]
        self.start = start
        self.end = start + length - 1
        self.value_to_add = corresponding_value - start

class Resolver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.maps = []
            actual_map = []
            for line in [l.replace('\n', '') for l in f.readlines()]:
                if not line:
                    continue
                if line.startswith('seeds'):
                    self.seeds = [int(match.group()) for match in re.finditer(r'\d+', line.split(':')[1])]
                    continue
                if 'map' in line:
                    if actual_map:
                        self.maps.append(actual_map)
                        actual_map = []
                else:
                    actual_map.append(Range(line))
            self.maps.append(actual_map)
                
    def resolve_first_part(self):
        result = []
        for seed in self.seeds:
            actual_value = seed
            for map in self.maps:
                map_found = False
                if map_found:
                    continue
                for range_item in map:
                    if range_item.start <= actual_value <= range_item.end:
                        actual_value += range_item.value_to_add
                        map_found = True
                        break
            result.append(actual_value)
        return min(result)
    
    def _get_mapped_ranges(self, map_index, *ranges):
        maps = sorted(self.maps[map_index], key=lambda m: m.start)
        result = []
        for range_start, range_end in ranges:
            range_result = []
            items = { range_start: 0, range_end: 0 }
            for map in maps:
                items = { **items, **dict.fromkeys([map.start, map.end], map.value_to_add)}
            items = dict(sorted(items.items()))
            items_keys = list(items.keys())
            index_start = items_keys.index(range_start)
            index_end = items_keys.index(range_end)
            
            for index in range(index_start, index_end):
                is_between_range = False
                if index > 0:
                    key_before = items_keys[index_start - 1]
                    value_before = items[key_before]
                    same_value_next_key = list({ k: v for k, v in items.items() if v == value_before }.keys())[-1]
                    if items_keys.index(same_value_next_key) > index:
                        is_between_range = True
                tmp_start_index = index - 1 if is_between_range else index
                tmp_start_key = items_keys[tmp_start_index]
                tmp_value = items[tmp_start_key]
                tmp_end_index = index + 1
                tmp_end_key = items_keys[tmp_end_index if index < index_end else index_end]
                range_result.append((items_keys[index] + tmp_value, tmp_end_key + tmp_value - (0 if tmp_end_index == index_end else 1)))
            result.extend(range_result)
        if map_index == len(self.maps) - 1:
            return result
        return self._get_mapped_ranges(map_index + 1,*result)
            

    def resolve_second_part(self):
        iter_seeds = iter(self.seeds)
        ranges = []
        for seed_start in iter_seeds:
            seed_end = next(iter_seeds) + seed_start - 1
            final_ranges = self._get_mapped_ranges(0, (seed_start, seed_end))
            ranges.extend(final_ranges)
        return sorted(ranges, key=lambda r: r[0])[0][0]
                    

resolver = Resolver()
print(f'Solution 1 = {resolver.resolve_first_part()}')
print(f'Solution 2 = {resolver.resolve_second_part()}')