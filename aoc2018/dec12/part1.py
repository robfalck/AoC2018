from __future__ import print_function, division, absolute_import

import numpy as np

np.set_printoptions(linewidth=1024, edgeitems=1000)


def solve(initial_state, rules, num_gen=20):
    # print(initial_state)
    padding = 1000
    # print(initial_num_pots)
    pots = {0: padding * '.' + initial_state.split()[-1] + padding * '.'}
    rules = [tuple(s.split(' => ')) for s in rules]

    # print(pots)
    # print(rules)

    # print(0, pots[0])

    for generation in range(1, num_gen+1):
        pots[generation] = pots[generation-1]
        for i in range(2, len(pots[generation-1])):
            # print('i=', i)
            for (seq, result) in rules:
                # print(seq, result, pots[generation - 1][i-2:i+3])
                if pots[generation - 1][i-2:i+3] == seq:
                    # print('match at ', i, seq)
                    # print( pots[generation][:i], pots[generation][i:])
                    # if result == '#':
                    #     print('generate')
                    # else:
                    #     print('die')
                    pots[generation] = pots[generation][:i] + result + pots[generation][i+1:]
                    # print(pots[generation])
                    break
            else:
                # print('die')
                # print('no match at ', i, pots[generation - 1][i-2:i+3])
                # print( pots[generation][:i], pots[generation][i:])
                pots[generation] = pots[generation][:i] + '.' + pots[generation][i+1:]
                # print(pots[generation])

        # Print the total after each generation to see if we find a pattern
        total = 0
        for i in range(len(pots[generation])):
            if pots[generation][i] == '#':
                total += (i - padding)
        # print(generation, total)

    # This code block checks for frequency, but no repetition in the pattern was found
    # # compute frequency of pattern
    # for i in range(1, num_gen):
    #     if pots[0] == pots[i]:
    #         frequency = i
    #     else:
    #         frequency = None

    total = 0
    for i in range(len(pots[num_gen])):
        if pots[num_gen][i] == '#':
            total += (i - padding)

    return total







if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    print('test: ', solve(initial_state=lines[0], rules=lines[2:], num_gen=20))  # 325

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    print('part 1:', solve(initial_state=lines[0], rules=lines[2:], num_gen=20))  # 2542

    # with open('input.txt', 'r') as f:
    #     lines = [s.strip() for s in f.readlines()]
    # print('part 2:', solve(initial_state=lines[0], rules=lines[2:], num_gen=10000))  # 2542

    # pattern in total, same delta after many generations (+51)
    # at generation 150, total is 8533
    # adding 51 for every generation to 50 000 000 000 gives
    print('part 2:', 8533 + 51 * (50000000000 - 150))