from __future__ import print_function, division, absolute_import

import itertools


def is_addr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] + initial[b]

def is_addi(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] + b

def is_mulr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] * initial[b]

def is_muli(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] * b

def is_banr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] & initial[b]

def is_bani(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] & b

def is_borr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] | initial[b]

def is_bori(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] | b

def is_setr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a]

def is_seti(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == a

def is_gtir(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a > initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def is_gtri(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] > b:
        return after[c] == 1
    else:
        return after[c] == 0

def is_gtrr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] > initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def is_eqir(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a == initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def is_eqri(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] == b:
        return after[c] == 1
    else:
        return after[c] == 0

def is_eqrr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] == initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0




def solve(data):

    test_map = {'addr': is_addr, 'addi': is_addi,
                'mulr': is_mulr, 'muli': is_muli,
                'banr': is_banr, 'bani': is_bani,
                'borr': is_borr, 'bori': is_bori,
                'setr': is_setr, 'seti': is_seti,
                'gtir': is_gtir, 'gtri': is_gtri, 'gtrr': is_gtrr,
                'eqir': is_eqir, 'eqri': is_eqri, 'eqrr': is_eqrr}

    op_code_map = {i: set() for i in range(16)}

    count_of_tests_that_match_three_or_more = 0
    for i, line in enumerate(data):
        if 'Before' in line:
            initial = eval(line.split(':')[-1])
            print(initial)
            instr = [int(s) for s in data[i+1].split()]
            print(instr)
            final = eval(data[i+2].split(':')[-1])
            print(final)

            matches = set()
            for instruction, test_func in test_map.items():
                if test_func(initial, final, instr):
                    op_code_map[instr[0]].add(instruction)
                    matches.add(instruction)
                else:
                    if instruction in op_code_map[instr[0]]:
                        op_code_map[instr[0]].remove(instruction)
            if len(matches) >= 3:
                count_of_tests_that_match_three_or_more += 1

    print(count_of_tests_that_match_three_or_more)








if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)

