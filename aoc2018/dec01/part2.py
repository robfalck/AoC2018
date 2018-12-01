from __future__ import print_function, division, absolute_import

import itertools


def part2():
    with open('input1.txt', 'r') as f:
        lines = f.readlines()

    inp = [int(s) for s in lines]
    seen_freqs = set()

    freq = 0
    for i in itertools.cycle(inp):
        freq += i
        if freq in seen_freqs:
            print('first repeated is', freq)
            break
        seen_freqs.add(freq)


if __name__ == '__main__':
    part2()