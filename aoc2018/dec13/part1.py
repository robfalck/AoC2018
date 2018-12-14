from __future__ import print_function, division, absolute_import

import itertools
import numpy as np

np.set_printoptions(linewidth=1024, edgeitems=1000)

# Map of headings to velocities
vector_map = {'^': [-1, 0],
              'v': [1, 0],
              '<': [0, -1],
              '>': [0, 1]}

class Cart(object):

    def __init__(self, char, pos):
        self.heading = char
        self.pos = np.array(pos, dtype=int)
        self.speed = 1
        self.turn_iter = itertools.cycle(['left', 'straight', 'right'])

    def __lt__(self, other):
        """
        Sort carts by row, then by column
        """
        if self.pos[1] == other.pos[1]:
            return self.pos[0] < other.pos[0]
        return self.pos[1] < other.pos[1]

    def move(self, track):
        if self.speed == 0:
            return

        # Check the track at the current position, if its a turn, adjust our heading accordingly
        y, x = self.pos
        t = track[y, x]
        # print(self.pos, self.heading, t)
        if t == '+':
            turn = next(self.turn_iter)
            if turn == 'left':
                if self.heading == '^':
                    self.heading = '<'
                elif self.heading == '>':
                    self.heading = '^'
                elif self.heading == 'v':
                    self.heading = '>'
                else:
                    self.heading = 'v'
            elif turn == 'right':
                if self.heading == '^':
                    self.heading = '>'
                elif self.heading == '>':
                    self.heading = 'v'
                elif self.heading == 'v':
                    self.heading = '<'
                else:
                    self.heading = '^'
        elif t == '/':
            if self.heading == '^':
                self.heading = '>'
            elif self.heading == '>':
                self.heading = '^'
            elif self.heading == 'v':
                self.heading = '<'
            else:
                self.heading = 'v'
        elif t == '\\':
            if self.heading == '^':
                self.heading = '<'
            elif self.heading == '>':
                self.heading = 'v'
            elif self.heading == 'v':
                self.heading = '>'
            else:
                self.heading = '^'

        # Now advance position
        self.pos += vector_map[self.heading]
        # print(self.pos, self.heading, t)
        # print()


def detect_crash(carts):
    crashes = []
    for cart_a, cart_b in itertools.combinations(carts, 2):
        if np.all(cart_a.pos == cart_b.pos):
            # crash!
            cart_a.speed = 0
            cart_b.speed = 0
            crashes.append(cart_a.pos)
    return crashes


def initialize(initial_state):
    # How big does the map have to be?
    num_rows = len(initial_state)
    num_cols = max([len(line) for line in initial_state])
    track = np.empty((num_rows, num_cols), dtype=str)
    track[...] = ' '
    carts = []

    for y, line in enumerate(initial_state):
        for x, char in enumerate(line):
            if char in '<>':
                track[y, x] = '-'
                carts.append(Cart(char, (y, x)))
            elif char in '^v':
                track[y, x] = '|'
                carts.append(Cart(char, (y, x)))
            else:
                track[y, x] = char

    return track, carts


def print_state(track, carts):
    t = track.copy()
    for c in carts:
        y, x = c.pos
        t[y, x] = c.heading
    r, c = t.shape
    for y in range(r):
        print(''.join(t[y, :]))
    print('\n\n')


def solve(initial_state):
    track, carts = initialize(initial_state)

    print_state(track, carts)

    for tick in range(1000):
        # print(tick)
        carts.sort()

        for cart in carts:
            # print('cart starts at', cart.pos)
            cart.move(track)
            # print('cart moves to', cart.pos)
            crashes = detect_crash(carts)
            if crashes:
                print('crash at', list(crashes[0])[::-1], 'on tick', tick)
                return

        print_state(track, carts)



if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)

