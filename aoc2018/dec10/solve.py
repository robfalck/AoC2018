from __future__ import print_function, division, absolute_import

import re
import numpy as np

re_posvel = re.compile(r'position=<(.+),(.+)> velocity=<(.+),(.+)>')

np.set_printoptions(linewidth=1024, edgeitems=1000)

def parse(s):
    """
    Parse out the positions and velocities.
    """
    match = (re_posvel.search(s))
    px, py, vx, vy = [int(g) for g in match.groups()]
    return px, py, vx, vy


def print_message(pos):
    """
    Print the message by first populating a numpy.array of the pixels.
    Then transpose it to fix the x-y axes.
    Then loop through each row and col, printing each point in the array if appropriate.
    """
    min_x = np.min(pos[:, 0])
    min_y = np.min(pos[:, 1])
    dx = int(np.max(pos[:, 0]) - min_x)
    dy = int(np.max(pos[:, 1]) - min_y)

    sky = np.zeros((dx + 1, dy + 1), dtype=int)

    for x, y in pos:
        sky[x - min_x, y - min_y] = 1

    sky = sky.T

    r, c = sky.shape
    for i in range(r):
        for j in range(c):
            char = '#' if sky[i, j] == 1 else ' '
            print(char, end='')
        print()


def solve(data):

    # Parse out the data.
    pos = np.zeros((len(data), 2), dtype=int)
    vel = np.zeros((len(data), 2), dtype=int)
    for i, line in enumerate(data):
        px_i, py_i, vx_i, vy_i = parse(line)
        pos[i, :] = px_i, py_i
        vel[i, :] = vx_i, vy_i

    # When the variance in the y position of the points is minimized, we assume the message
    # is ready.  This isn't foolproof but it's probably good enough for our purposes.
    var_prev = 1E23
    for tick in range(1000000):
        var = np.var(pos[:, 1])
        if var > var_prev:
            print('at {0} ticks'.format(tick - 1))
            pos -= vel
            print_message(pos.copy())
            break
        pos += vel
        var_prev = var


if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    solve(data=lines)

    print()

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    solve(data=lines)
