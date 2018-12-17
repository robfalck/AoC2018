from __future__ import print_function, division, absolute_import

def is_addr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] + initial[b]

def addr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] + regs[b]

def is_addi(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] + b

def addi(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] + b

def is_mulr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] * initial[b]

def mulr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] * regs[b]

def is_muli(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] * b

def muli(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] * b

def is_banr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] & initial[b]

def banr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] & regs[b]

def is_bani(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] & b

def bani(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] & b

def is_borr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] | initial[b]

def borr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] | regs[b]

def is_bori(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a] | b

def bori(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a] | b

def is_setr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == initial[a]

def setr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = regs[a]

def is_seti(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    return after[c] == a

def seti(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    regs[c] = a

def is_gtir(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a > initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def gtir(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a > regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def is_gtri(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] > b:
        return after[c] == 1
    else:
        return after[c] == 0

def gtri(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if regs[a] > b:
        regs[c] = 1
    else:
        regs[c] = 0

def is_gtrr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] > initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def gtrr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if regs[a] > regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def is_eqir(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a == initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def eqir(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if a == regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0

def is_eqri(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] == b:
        return after[c] == 1
    else:
        return after[c] == 0

def eqri(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if regs[a] == b:
        regs[c] = 1
    else:
        regs[c] = 0

def is_eqrr(initial, after, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if initial[a] == initial[b]:
        return after[c] == 1
    else:
        return after[c] == 0

def eqrr(regs, instr):
    a = instr[1]
    b = instr[2]
    c = instr[3]
    if regs[a] == regs[b]:
        regs[c] = 1
    else:
        regs[c] = 0




def solve(data):

    test_map = {'addr': is_addr, 'addi': is_addi,
                'mulr': is_mulr, 'muli': is_muli,
                'banr': is_banr, 'bani': is_bani,
                'borr': is_borr, 'bori': is_bori,
                'setr': is_setr, 'seti': is_seti,
                'gtir': is_gtir, 'gtri': is_gtri, 'gtrr': is_gtrr,
                'eqir': is_eqir, 'eqri': is_eqri, 'eqrr': is_eqrr}

    func_map = {'addr': addr, 'addi': addi,
                'mulr': mulr, 'muli': muli,
                'banr': banr, 'bani': bani,
                'borr': borr, 'bori': bori,
                'setr': setr, 'seti': seti,
                'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
                'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr}

    op_code_map = {i: set() for i in range(16)}

    for i, line in enumerate(data):
        if 'Before' in line:
            initial = eval(line.split(':')[-1])
            instr = [int(s) for s in data[i+1].split()]
            final = eval(data[i+2].split(':')[-1])

            matches = set()
            for instruction, test_func in test_map.items():
                if test_func(initial, final, instr):
                    op_code_map[instr[0]].add(instruction)
                    matches.add(instruction)

                elif instruction in op_code_map[instr[0]]:
                    # print('removing')
                    op_code_map[instr[0]].remove(instruction)

    actual_op_codes = {}

    # At least one code should have only one instruction associated with it
    # Pare down the list by removing that as a candidate from all other op codes
    # Repeat until each op code only has one associated instruction.
    for i in range(16):
        for op_code, possible_instructions in op_code_map.items():
            # print(op_code, possible_instructions)
            if len(possible_instructions) == 1:
                newest = list(possible_instructions)[0]
                actual_op_codes[op_code] = newest
                break

        del(op_code_map[op_code])

        for op_code, possible_instructions in op_code_map.items():
            if newest in possible_instructions:
                # print(newest, op_code, possible_instructions)
                possible_instructions.remove(newest)

    for i in range(16):
        print('{0}: {1}'.format(i, actual_op_codes[i]))

    # Now run the instructions
    registers = [0, 0, 0, 0]

    for line in data[3118:]:
        instr = [int(s) for s in line.split()]
        func_map[actual_op_codes[instr[0]]](registers, instr)
    print(registers)





if __name__ == '__main__':

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)

