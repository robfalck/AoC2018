from __future__ import print_function, division, absolute_import

import operator
import re


def print_scan(min_x, max_x, min_y, max_y, clay, flowing_water, standing_water):

    print(min_x, max_x)
    for j in range(0, max_y + 1):
        for i in range(min_x, max_x + 1):
            if (i, j) == (500, 0):
                print('+', end='')
            elif (i, j) in standing_water:
                print('~', end='')
            elif (i, j) in flowing_water:
                print('|', end='')
            elif (i, j) in clay:
                print('#', end='')
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

    flowing_water = set([(500, 1)])
    standing_water = set()

    flowing_water_to_add = set()
    standing_water_to_add = set()

    for it in range(10000):
        for w in flowing_water:
            # If this piece of water is below the max depth, ignore it
            if w[1] >= max_y:
                continue
            # Rules for flowing water
            # 1. If sand is below the water, add that location to water
            if (w[0], w[1] + 1) not in clay.union(standing_water):
                if (w[0], w[1] + 1) not in flowing_water:
                    flowing_water_to_add.add((w[0], w[1] + 1))
            # 2. Else if clay or water is below, add left and right if possible
            else:
                # Left
                if (w[0] - 1, w[1]) not in clay.union(standing_water):
                    if (w[0] - 1, w[1]) not in flowing_water:
                        flowing_water_to_add.add((w[0] - 1, w[1]))
                # Right
                if (w[0] + 1, w[1]) not in clay.union(standing_water):
                    if (w[0] + 1, w[1]) not in flowing_water:
                        flowing_water_to_add.add((w[0] + 1, w[1]))

        # print(flowing_water_to_add)
        flowing_water.update(flowing_water_to_add)

        # Now check any elements in flowing water that should be turned into standing water
        # The rule is: any horizontally contiguous flowing water that is bounded on the
        # left and right by clay or standing water, and is entirely on top of clay or standing water
        # becomes standing water.
        for w in sorted(list(flowing_water), key=operator.itemgetter(1, 0), reverse=True):
            # print(w)
            # print(w == (499, 12))
            # if w == (499, 12):
            #     print('ok')
            if (w[0] - 1, w[1]) in clay.union(standing_water): # left is bounded
                # start moving right until we find clay, standing water, or sand
                dx = 0
                while True:
                    check_pos = w[0] + dx, w[1]
                    under_check_pos = w[0], w[1] + 1
                    if check_pos in flowing_water and under_check_pos in clay.union(standing_water):
                        dx += 1
                        standing_water_to_add.add(check_pos)
                    elif check_pos in clay.union(standing_water):
                        break
                        # everything we just checked becomes standing water
                    else:
                        standing_water_to_add.clear()
                        break

            standing_water.update(standing_water_to_add)

        if not flowing_water_to_add and not standing_water_to_add:
            print('finished after {0} iterations'.format(it))
            break

        flowing_water_to_add.clear()
        standing_water_to_add.clear()

        flowing_water -= standing_water
    else:
        print('iteration limit reached')

    print_scan(min_x, max_x, min_y, max_y, clay, flowing_water, standing_water)

    print('total wetted area', len(flowing_water.union(standing_water)))

    exit(0)





if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)
    assert(num_wetted == 57)

    # with open('input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(data=lines)
    # # #
    # # # 35487 : low

