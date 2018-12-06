from __future__ import print_function, division, absolute_import

import itertools
import numpy as np


def manhattan_distance(p_x, p_y, grid_x, grid_y):
    return abs(p_x - grid_x) + abs(p_y - grid_y)


def part1(points):

    x = np.array([int(s.split(',')[0]) for s in points])
    y = np.array([int(s.split(',')[1]) for s in points])
    n = len(x)

    # Find the extends of the grid
    i_maxx = np.argmax(x)
    maxx = x[i_maxx]

    i_maxy = np.argmax(y)
    maxy = y[i_maxy]

    grid_x, grid_y = np.meshgrid(np.arange(0, maxx+1, dtype=int),
                                 np.arange(0, maxy+1, dtype=int))

    # md keeps track of the minimum distance to any index
    md = manhattan_distance(x[0], y[0], grid_x, grid_y)

    # eq keeps track of those coordinates which have equal minimum distance to two or more points
    eq = np.zeros_like(md)

    # voronoi keeps track of the closest point by integer index to any given coordinate
    voronoi = 0 * np.ones_like(md, dtype=int)

    for i in range(1, n):
        md_i = manhattan_distance(x[i], y[i], grid_x, grid_y)

        r_eq, c_eq = np.where(md_i == md)
        eq[r_eq, c_eq] = 1

        r_lt, c_lt = np.where(md_i < md)
        eq[r_lt, c_lt] = 0

        md = np.minimum(md_i, md)

        r, c = np.where(md == md_i)
        voronoi[r, c] = i

    # Mark the equidistant coordinates with -1
    r, c = np.nonzero(eq)
    voronoi[r, c] = -1

    top = voronoi[0, :]
    left = voronoi[:, 0]
    right = voronoi[:, -1]
    bottom = voronoi[-1, :]

    # The points which don't contain infinite indices (if its on the boundary, it will be infinite)
    finite_idxs = [i for i in range(n) if i not in np.concatenate((top, left, bottom, right))]

    max_area = -1
    for i in finite_idxs:
        max_area = max(max_area, len(np.where(voronoi == i)[0]))
    print(max_area)

if __name__ == '__main__':

    print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part1(points=lines)

    print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part1(points=lines)