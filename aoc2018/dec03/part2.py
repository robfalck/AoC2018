from __future__ import print_function, division, absolute_import

import itertools
import random

def get_claim(inp):
    id_str, tail = inp.split('@')
    pos_str, size_str = tail.split(':')
    pos_x, pos_y = [int(s) for s in pos_str.split(',')]
    width, height = [int(s) for s in size_str.split('x')]
    return int(id_str.strip()[1:]), pos_x, pos_y, width, height

def overlap(a, b):
    a_x, a_y, a_w, a_h = a
    b_x, b_y, b_w, b_h = b

    squares_a = set()
    squares_b = set()

    for i in range(a_w):
        for j in range(a_h):
            squares_a.add((a_x + i, a_y + j))

    for i in range(b_w):
        for j in range(b_h):
            squares_b.add((b_x + i, b_y + j))

    return bool(squares_a.intersection(squares_b))

def part2(data):

    claims = [get_claim(d) for d in data]

    claims_dict = dict([(c[0], c[1:]) for c in claims])

    for a, b in itertools.combinations(claims, 2):
        if overlap(a[1:], b[1:]):
            if a[0] in claims_dict:
                claims_dict.pop(a[0])
                print(len(claims_dict))
            if b[0] in claims_dict:
                claims_dict.pop(b[0])
                print(len(claims_dict))


    print('nonoverlapping claim:', claims_dict)




if __name__ == '__main__':
    test_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split('\n')

    part2(data=test_input)

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(data=lines)
