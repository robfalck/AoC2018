from __future__ import print_function, division, absolute_import

import numpy as np

np.set_printoptions(linewidth=1024, edgeitems=1000)


def rack_id(x):
    return x + 10


def power_level(x, y, serial_number):
    r_id = rack_id(x)
    p = r_id * y
    p += serial_number
    p *= r_id
    p = int(str(p)[-3]) - 5
    return p

def compute_3x3_power_level(grid, x, y):
    p = 0
    for i in range(x, x+3):
        for j in range(y, y+3):
            p += grid[i, j]
    return p


def compute_nxn_power_level(grid, x, y, n):
    p = 0
    for i in range(x, x+n):
        for j in range(y, y+n):
            p += grid[i, j]
    return p

def find_best_nxn_power(grid, size):
    max_pnxn = 1E-16
    max_coords = (-1, -1)
    for x in range(1, 301-size):
        for y in range(1, 301-size):
            pnxn = compute_nxn_power_level(grid, x, y, n=size)
            if pnxn > max_pnxn:
                max_pnxn = pnxn
                max_coords = (x, y)
    return max_coords, max_pnxn

def solve_part1(serial_number, size):
    # Initialize grid
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x, y] = power_level(x, y, serial_number)

    # Analyze each nxn square, keeping track of the one with the most power as we go
    max_coords, max_p_nxn = find_best_nxn_power(grid, size)
    return max_coords, max_p_nxn


def solve_part2(serial_number, max_size=300):
    # Initialize grid
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x, y] = power_level(x, y, serial_number)

    # Analyze each nxn square, keeping track of the one with the most power as we go
    max_coords = (-1, -1)
    max_p_nxn = -1E16
    max_gridsize = 0
    for size in range(2, max_size):
        print(size)
        coords, p_nxn = find_best_nxn_power(grid, size)
        if p_nxn > max_p_nxn:
            max_p_nxn = p_nxn
            max_coords = coords
            max_gridsize = size
            print('new best power', max_p_nxn, 'at', max_coords, 'with size', max_gridsize)
    print()
    return max_coords, max_p_nxn, max_gridsize


if __name__ == '__main__':
    loc, power = solve_part1(serial_number=18, size=3)
    print(loc, power)
    assert(loc == (33,45))
    assert(power == 29)

    loc, power = solve_part1(serial_number=42, size=3)
    print(loc, power)
    assert(loc == (21, 61))
    assert(power == 30)

    loc, power = solve_part1(serial_number=6878, size=3)  # part 1: 20x34
    print(loc, power)

    loc, power, gridsize = solve_part2(18, max_size=20)
    print(loc, power, gridsize)
    assert(loc == (90, 269))
    assert(power == 113)
    assert(gridsize == 16)

    loc, power = solve_part2(serial_number=6878)  # part 2:
    print(loc, power)
