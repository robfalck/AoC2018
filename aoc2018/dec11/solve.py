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


def solve(serial_number):
    # Initialize grid
    grid = {}
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x, y] = power_level(x, y, serial_number)

    # Analyze each 3x3 square, keeping track of the one with the most power as we go
    max_p3x3 = 1E-16
    max_coords = (-1, -1)
    for x in range(1, 298):
        for y in range(1, 298):
            p3x3 = compute_3x3_power_level(grid, x, y)
            if p3x3 > max_p3x3:
                max_p3x3 = p3x3
                max_coords = (x, y)
    print(max_coords, max_p3x3)
    return max_coords, max_p3x3





if __name__ == '__main__':
    loc, power = solve(serial_number=18)
    assert(loc == (33,45))
    assert(power == 29)

    loc, power = solve(serial_number=42)
    assert(loc == (21, 61))
    assert(power == 30)

    solve(serial_number=6878)  # part 1: 20x34

