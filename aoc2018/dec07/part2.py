from __future__ import print_function, division, absolute_import

from part1 import Step, parse_steps, get_eligible_steps


class Worker(object):
    def __init__(self, id):
        self.id = id
        self.step = None

    def assign(self, step):
        # print('assigned', self.id, step.name)
        self.step = step
        step.worker = self.id
        step.running = True

    def free(self, completed_steps):
        self.step.worker = None
        self.step.running = False
        completed_steps.append(self.step.name)
        self.step = None


def print_iterate(clock, workers, completed_steps):
    print(clock, end='   ')
    for w in workers:
        if w.step is not None:
            print(w.step.name, end='   ')
        else:
            print(None, end='   ')
    print(completed_steps)


def part2(instructions, num_workers, test=False):
    steps = parse_steps(instructions, test=test)
    workers = [Worker(i) for i in range(num_workers)]
    completed_steps = []
    clock = 0

    while len(completed_steps) != len(steps):

        # decrement the timer on any running steps
        for step_name, step in steps.items():
            if step.running:
                step.time_remaining -= 1
                if step.time_remaining == 0:
                    workers[step.worker].free(completed_steps)

        # Get a list of idle workers
        idle_workers = [w for w in workers if w.step is None]

        # Find the steps that can be done
        eligible = get_eligible_steps(steps, completed_steps)

        # Assign tasks to available workers
        for i in range(min(len(idle_workers), len(eligible))):
            # print(clock, 'assigning', eligible[i], 'to', idle_workers[i])
            idle_workers[i].assign(steps[eligible[i]])

        # print the status
        # print_iterate(clock, workers, completed_steps)

        clock += 1

    print(''.join(completed_steps))
    print(clock - 1)



if __name__ == '__main__':

    # print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part2(instructions=lines, num_workers=2, test=True)

    # print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part2(instructions=lines, num_workers=5, test=False)