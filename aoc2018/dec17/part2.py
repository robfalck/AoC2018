from __future__ import print_function, division, absolute_import

import itertools
import numpy as np

from part1 import vector_map, Cart, detect_crash, initialize, print_state

np.set_printoptions(linewidth=1024, edgeitems=1000)


def solve(initial_state):
    track, carts = initialize(initial_state)

    print_state(track, carts)

    tick = 0
    while len(carts) > 1:
        tick += 1
        # print(tick)
        carts.sort()

        for cart in carts:
            # print('cart starts at', cart.pos)
            cart.move(track)
            # print('cart moves to', cart.pos)
            crashes = detect_crash(carts)
            if crashes:
                print('crash at', list(crashes[0])[::-1], 'on tick', tick)

        carts = [c for c in carts if c.speed == 1]

        # print_state(track, carts)

        if len(carts) == 1:
            print('last cart at', carts[0].pos[::-1])
            break



if __name__ == '__main__':

    with open('test_input2.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)

