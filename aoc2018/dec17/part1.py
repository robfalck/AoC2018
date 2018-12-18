from __future__ import print_function, division, absolute_import

import random
import re

# The change in position associated with every direction
headings = {'left': (-1, 0),
            'right': (1, 0),
            'down': (0, 1)}



class WaterBlock(object):

    def __init__(self):
        self.pos = (500, 1)
        # self.wetted_locs = set()
        self.dx = 0
        self.dy = 1
        self.stopped = False
        self.heading = random.choice(('left', 'right'))
        self.num_heading_changes = 0

    def sim_step(self, clay, standing_water, wetted, max_y):
        if self.stopped:
            return

        # Add the current location to the global wetted set and this block's wetted set.
        wetted.add(self.pos)
        # self.wetted_locs.add(self.pos)

        # If the block of water can fall, it should fall.
        next_square = self.pos[0], self.pos[1] + 1
        if next_square not in clay and next_square not in standing_water:
            # Fall one square
            self.pos = next_square

            # Reset the number of heading changes so we start counting again at the next horizontal flow
            self.num_heading_changes = 0
            # Reset the heading so that we could flow left or right at the next level we fall to.
            self.heading = random.choice(('left', 'right'))

            # Check if we've dropped out the bottom of the scan
            if self.pos[1] > max_y:
                self.stopped = True
        else:
            # the square below this water is either water or clay
            # flow sideways, starting with a random direction 'left' or 'right'
            dx = 1 if self.heading == 'right' else -1
            next_square = self.pos[0] + dx, self.pos[1]
            if next_square in clay or next_square in standing_water:
                # change heading
                self.heading = 'left' if self.heading == 'right' else 'right'
                self.num_heading_changes += 1
                if self.num_heading_changes > 2:
                    # Don't bounce back and forth forever
                    self.stopped = True
            else:
                self.pos = next_square


def print_scan(min_x, max_x, min_y, max_y, clay, spring=(500, 0), wetted=None, standing_water=None):
    standing_water = set() if standing_water is None else standing_water
    wetted = set() if wetted is None else wetted

    for j in range(0, max_y + 1):
        for i in range(min_x, max_x + 1):
            if (i, j) == spring:
                print('+', end='')
            elif (i, j) in clay:
                print('#', end='')
            elif (i, j) in standing_water:
                print('~', end='')
            elif (i, j) in wetted:
                print('|', end='')
            else:
                print('.', end='')
        print()





def parse_input(data):

    re_x_scalar = re.compile('x=(\d+)')
    re_x_array = re.compile('x=(\d+)\.\.(\d+)')
    re_y_scalar = re.compile('y=(\d+)')
    re_y_array = re.compile('y=(\d+)\.\.(\d+)')

    clay = set()

    for line in data:

        match_x_array = re_x_array.search(line)
        if match_x_array:
            xs = range(int(match_x_array.groups()[0]), int(match_x_array.groups()[1])+1)
            match_y = re_y_scalar.search(line)
            y = int(match_y.groups()[0])
            for x in xs:
                clay.add((x, y))
                
        match_y_arrax = re_y_array.search(line)
        if match_y_arrax:
            ys = range(int(match_y_arrax.groups()[0]), int(match_y_arrax.groups()[1])+1)
            match_x = re_x_scalar.search(line)
            x = int(match_x.groups()[0])
            for y in ys:
                clay.add((x, y))

    list_clay = list(clay)
    min_y = min([c[1] for c in list_clay])
    max_y = max([c[1] for c in list_clay])
    min_x = min([c[0] for c in list_clay])
    max_x = max([c[0] for c in list_clay])

    return clay, min_x, max_x, min_y, max_y


def solve(data):

    clay, min_x, max_x, min_y, max_y = parse_input(data)

    wetted = set()
    standing_water = set()
    water_blocks = []

    for i in range(200000):
        water_blocks.append(WaterBlock())
        w = water_blocks[-1]
        while not w.stopped:
            w.sim_step(clay, standing_water, wetted, max_y)
        if w.pos[1] <= max_y:
            standing_water.add(w.pos)
        print(i, len(wetted))

    print_scan(min_x, max_x, min_y, max_y, clay, wetted=wetted, standing_water=standing_water)

    print('standing water tiles:', len(standing_water))
    print('wetted tiles:', len(wetted))

    return len(wetted), len(standing_water)


if __name__ == '__main__':

    # with open('test_input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # num_wetted, num_standing_water = solve(data=lines)
    # assert(num_wetted == 57)

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)

    # 35487 : low

