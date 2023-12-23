from shapely import LineString

class Brick:

    def __init__(self, name, line, *args, **kwargs):
        self.name = str(name)
        start, end = line.replace('\n', '').split('~')
        self.start_x, self.start_y, self.start_z = [int(value) for value in start.split(',')]
        self.end_x, self.end_y, self.end_z = [int(value) for value in end.split(',')]
        self.supports = set()
        self.supporters = set()

    def get_min_height(self):
        return min(self.start_z, self.end_z)
    
    def get_max_height(self):
        return max(self.start_z, self.end_z)
    
    def _to_geom(self, test_fall=False):
        return LineString([(self.start_x, self.start_y, self.start_z - int(test_fall)), (self.end_x, self.end_y, self.end_z - int(test_fall))])
    
    def _intersects(self, other_brick):
        brick_geom = self._to_geom(test_fall=True)
        other_brick_geom = other_brick._to_geom()
        return brick_geom.intersects(other_brick_geom) or brick_geom.envelope.intersects(other_brick_geom.envelope)
    
    def can_go_down(self, placed_bricks):
        for other_brick in placed_bricks:
            if other_brick.get_max_height() != self.get_min_height() - 1:
                continue
            if self._intersects(other_brick):
                self.supporters.add(other_brick.name)
                other_brick.supports.add(self.name)
        return len(self.supporters) == 0
          
    def fall(self):
        self.start_z -= 1
        self.end_z -= 1

class Solver:

    def __init__(self, *args, **kwargs):
        with open('input.txt') as f:
            self.bricks = { str(name): Brick(name, line) for name, line in enumerate(f.readlines(), start=1) }
        # Execute fall
        self._run()
        self.safe_bricks = set()

    def _run(self):
        bricks_in_place = set()
        for brick in sorted(self.bricks.values(), key=lambda b: b.get_min_height()):
            while brick.get_min_height() > 1:
                if brick.can_go_down(bricks_in_place):
                    brick.fall()
                else:
                    break
            bricks_in_place.add(brick)

    def solve_first_part(self):
        for brick in self.bricks.values():
            if not brick.supports:  # Brick supports no other bricks, can be removed
                self.safe_bricks.add(brick.name)
                continue
            if all(len(self.bricks.get(supported_brick_name).supporters) > 1 for supported_brick_name in brick.supports): 
                # All supported bricks have an other supports, actual brick can be removed
                self.safe_bricks.add(brick.name)
        return len(self.safe_bricks)
    
    def _get_bricks_that_would_fall(self, brick, falling=None):
        falling = falling or set()
        falling.add(brick.name)
        for supported_brick_name in brick.supports:
            supported_brick = self.bricks.get(supported_brick_name)
            if len(supported_brick.supporters - falling) == 0:
                falling |= self._get_bricks_that_would_fall(supported_brick, falling)
        return falling
           
    def solve_second_part(self):
        result = 0
        for brick_name, brick in self.bricks.items():
            if brick_name in self.safe_bricks:
                continue
            result += len(self._get_bricks_that_would_fall(brick)) - 1  # - 1 => Remove desintegrated brick from falling bricks
        return result
        
solver = Solver()
print(f'Solution 1 = {solver.solve_first_part()}')
print(f'Solution 2 = {solver.solve_second_part()}')