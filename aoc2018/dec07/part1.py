from __future__ import print_function, division, absolute_import

import itertools
import numpy as np

def time_to_do_step(step):
    return ord(step) - 4

class Step(object):

    def __init__(self, name, test=False):
        self.name = name
        self.prereqs = set()
        self.worker = None
        self.time_remaining = time_to_do_step(name)
        if test:
            self.time_remaining -= 60
        self.running = False

def parse_steps(instructions, test=False):
    steps = {}
    for line in instructions:
        prereq_name = line[5]
        step_name = line[-12]

        if step_name in steps:
            steps[step_name].prereqs.add(prereq_name)
        else:
            steps[step_name] = Step(step_name, test=test)
            steps[step_name].prereqs = {prereq_name}

        if prereq_name not in steps:
            steps[prereq_name] = Step(prereq_name, test=test)
    return steps

def get_eligible_steps(steps, completed_steps):
    eligible = []
    if len(completed_steps) == 0:
        eligible = [name for name in steps if not steps[name].prereqs and not steps[name].running]
    else:
        for step_name, step in steps.items():
            # print('    ', step_name)
            if step_name in completed_steps:
                continue
            elif step.running:
                continue
            elif steps[step_name].prereqs.issubset(completed_steps):
                eligible.append(step_name)
    return sorted(eligible)


def part1(instructions):
    steps = parse_steps(instructions)

    # Find the start point
    completed_steps = []

    while len(completed_steps) != len(steps):
        # Find the steps whose prereqs are satisfied and are not already completed
        next = get_eligible_steps(steps, completed_steps)[0]
        completed_steps.append(next)

    print(''.join(completed_steps))

    return completed_steps






if __name__ == '__main__':

    # # print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part1(instructions=lines)

    # print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part1(instructions=lines)
