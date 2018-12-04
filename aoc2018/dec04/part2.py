from __future__ import print_function, division, absolute_import


import numpy as np


from part1 import Entry, Shift, get_sorted_entries, get_shifts


def part2(data):

    entries = get_sorted_entries(data)

    # Initialize the sleep log
    sleep_log = {}
    for entry in entries:
        if entry.id is not None:
            sleep_log[entry.id] = [0]*60

    shifts = get_shifts(entries)
    for shift in shifts:
        shift.add_to_sleep_log(sleep_log)

    # Find the minute where a guard slept most
    max_id = -1
    max_minute = -1
    max_value = -1
    for id in sleep_log:
        max_val_for_id = np.max(sleep_log[id])
        if max_val_for_id > max_value:
            max_value = max_val_for_id
            max_minute = np.argmax(sleep_log[id])
            max_id = id
    print(max_id, max_minute, max_value, max_id * max_minute)



if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(data=lines)


    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part2(data=lines)