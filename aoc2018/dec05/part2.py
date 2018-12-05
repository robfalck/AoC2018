from __future__ import print_function, division, absolute_import

import re

# Precompile all possible regex patterns
patterns = [chr(code) for code in range(97, 97+26)]
patterns = [char + char.upper() for char in patterns]
patterns = patterns + [p[::-1] for p in patterns]
regexes = [re.compile(pattern) for pattern in patterns]


def fully_react_polymer_regex(polymer):
    p = polymer
    while True:
        p_start = p
        for regex in regexes:
            p = regex.sub('', p)
        if len(p) == len(p_start):
            break
    return len(p)


def part2(polymer):

    results = {}

    for unit in range(97, 97+26):
        print(chr(unit))
        test_polymer = polymer.replace(chr(unit), '')
        test_polymer = test_polymer.replace(chr(unit).upper(), '')
        length = fully_react_polymer_regex(test_polymer)
        results[chr(unit)] = length

    minimum = 1E23
    arg_min = 'a'
    for key in results:
        if results[key] < minimum:
            arg_min = key
            minimum = results[key]
    print(arg_min, minimum)


if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(polymer=lines[0])

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(polymer=lines[0])