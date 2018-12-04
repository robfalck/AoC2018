from __future__ import print_function, division, absolute_import

import re
import numpy as np
from datetime import datetime

re_entry = re.compile(r'(\d+)-(\d+)-(\d+) (\d+):(\d+)')


class Entry(object):

    def __init__(self, year, month, day, hour, minute, event_type, id=None):
        self.timestamp = datetime(year, month, day, hour, minute)
        self.id = id
        self.event_type = event_type

    def __lt__(self, other):
        return self.timestamp < other.timestamp

    def __repr__(self):
        return str(self.timestamp) + ' ' + self.event_type + ' ' + str(self.id)


class Shift(object):

    def __init__(self, entries):
        self.id = entries[0].id
        self.entries = entries

    def add_to_sleep_log(self, sleep_log):
        for i in range(1, len(self.entries), 2):
            sleep = self.entries[i].timestamp.minute
            wake = self.entries[i+1].timestamp.minute

            for minute in range(sleep, wake):
                sleep_log[self.id][minute] += 1

def get_sorted_entries(inp):
    """
    Read and sort the input data
    """
    entries = []
    for e in inp:
        match = re_entry.search(e)
        year, month, day, hour, minute = [int(s) for s in match.groups()]

        if '#' in e:
            id = int(e.split('#')[-1].split()[0])
            event_type = 'begin'
        else:
            id = None
            event_type = 'wake' if 'wakes' in e else 'sleep'

        entry = Entry(year, month, day, hour, minute, event_type, id)
        entries.append(entry)
    return sorted(entries)

def get_shifts(log_entries):
    shift_start = 0
    shifts = []
    for i, entry in enumerate(log_entries):
        if i == 0:
            continue
        if entry.event_type == 'begin':
            shift_entries = log_entries[shift_start: i]
            shifts.append(Shift(shift_entries))
            shift_start = i
    else:
        shift_entries = log_entries[shift_start:]
        shifts.append(Shift(shift_entries))

    return shifts

def part1(data):

    entries = get_sorted_entries(data)

    # Initialize the sleep log
    sleep_log = {}
    for entry in entries:
        if entry.id is not None:
            sleep_log[entry.id] = [0]*60

    shifts = get_shifts(entries)
    for shift in shifts:
        shift.add_to_sleep_log(sleep_log)

    # Find the guard with the most minutes of sleep
    max_sleep = -1
    id_max = -1
    for id in sleep_log:
        if sum(sleep_log[id]) > max_sleep:
            max_sleep = int(sum(sleep_log[id]))
            id_max = id
    minute = np.argmax(sleep_log[id_max])
    print(id_max, minute, id_max * minute)



if __name__ == '__main__':

    # with open('test_input.txt', 'r') as f:
    #     lines = [s.strip() for s in f.readlines()]
    #
    # part1(data=lines)


    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part1(data=lines)