from __future__ import print_function, division, absolute_import


def part2(data):
    numbers = [int(s) for s in data.split()]


if __name__ == '__main__':
    # # print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part2(data=lines[0])

    # # print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part2(data=lines[0])
