from __future__ import print_function, division, absolute_import


class Node(object):

    def __init__(self, numbers):
        self.num_children = numbers.pop(0)
        self.num_metadata = numbers.pop(0)
        self.children = []
        self.metadata = []

        for i in range(self.num_children):
            self.children.append(Node(numbers))

        self.metadata = numbers[:self.num_metadata]
        del numbers[:self.num_metadata]

    def sum_metadata(self):
        tally = sum(self.metadata)
        for c in self.children:
            tally += c.sum_metadata()
        return tally

    def get_value(self):
        tally = 0
        if not self.children:
            return self.sum_metadata()
        else:
            for idx in self.metadata:
                try:
                    tally += self.children[idx - 1].get_value()
                except IndexError as e:
                    pass
        return tally


def part1(data):
    numbers = [int(s) for s in data.split()]
    root = Node(numbers)
    print(root.sum_metadata())


if __name__ == '__main__':

    # # print('test result: ', end='')
    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part1(data=lines[0])

    # # print('result: ', end='')
    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]
    part1(data=lines[0])
