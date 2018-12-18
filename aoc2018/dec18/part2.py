from __future__ import print_function, division, absolute_import

import itertools

from part1 import parse_input, count_adjacent, mutate, print_land


def solve(data, minutes=10):

    acres, num_rows, num_cols = parse_input(data)

    acres_history = {0: acres}

    wooded_history = {}
    lumber_yard_history = {}

    found_repeat = False

    for time in range(1, minutes + 1):
        acres_new = mutate(acres_history[time - 1], num_rows, num_cols)

        for t, a in acres_history.items():
            if acres_new == a:
                # print('time {0} state equal to state at time {1}'.format(time, t))
                # repeat found
                found_repeat = True
                break

        if found_repeat:
            break

        acres_history[time] = acres_new

    print('repeat - {0} is the same as {1}'.format(time, t))
    cycle_length = time - t
    t_final = t + (1000000000 - time) % cycle_length

    print('state at end time will be the same as state at time', t_final)

    num_wooded = len([a for a in acres_history[t_final].values() if a == '|'])
    num_lumber_yards = len([a for a in acres_history[t_final].values() if a == '#'])
    num_resources = num_wooded * num_lumber_yards

    print('Wooded acres:', num_wooded)
    print('Lumber yards:', num_lumber_yards)
    print('Total Resources:', num_resources)



if __name__ == '__main__':

    # with open('test_input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(data=lines)

    # part 1
    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines, minutes=1000000000)

    # # part 2
    # with open('input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    #
    # # Find how long it takes the pattern to repeat
    # for minutes in range(100, 1000, 100):
    #     print()
    #     print('After {0} minutes:'.format(minutes))
    #     solve(data=lines, minutes=minutes)
    #
