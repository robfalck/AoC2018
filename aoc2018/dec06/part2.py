from __future__ import print_function, division, absolute_import

import numpy as np

def manhattan_distance(p_x, p_y, grid_x, grid_y):
    return abs(p_x - grid_x) + abs(p_y - grid_y)

def part2(points, delta):

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

    md_sum = manhattan_distance(x[0], y[0], grid_x, grid_y)

    for i in range(1, n):
        md_i = manhattan_distance(x[i], y[i], grid_x, grid_y)
        md_sum += md_i

    print(len(np.where(md_sum < delta)[0]))



if __name__ == '__main__':

    print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part2(points=lines, delta=32)


    print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(points=lines, delta=10000)