from __future__ import print_function, division, absolute_import


def part1():
    with open('input1.txt', 'r') as f:
        lines = f.readlines()
    inp = [int(s) for s in lines]
    print(sum(inp))


if __name__ == '__main__':
    part1()