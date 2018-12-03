from __future__ import print_function, division, absolute_import

import itertools
import difflib


def differs_by_1_letter(a, b):
    common = ''
    num_diffs = 0
    for i in range(len(a)):
        if a[i] == b[i]:
            common += a[i]
        else:
            num_diffs += 1
        if num_diffs > 1:
            break
    return num_diffs == 1, common


def part2(data):

    for id_a, id_b in itertools.combinations(data, 2):
        diff_by_one, common_letters = differs_by_1_letter(id_a, id_b)
        if diff_by_one:
            print('ID a:', id_a, 'ID b:', id_b, 'Common:', common_letters)


if __name__ == '__main__':

    test_input = 'abcde fghij klmno pqrst fguij axcye wvxyz'.split()

    part2(data=test_input)

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(data=lines)