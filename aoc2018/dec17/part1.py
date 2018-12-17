from __future__ import print_function, division, absolute_import

import re
import numpy as np
import collections


def get_shortest_path(start, end, allies, enemies):
    """
    Returns a np array of the board where each element holds
    the number of moves required to get from pos to that element.
    """

    # Setup the visited set and queue for the BFS
    visited, queue = set(), collections.deque([(start)])
    visited.add(start)

    # Setup a set of spaces occupied by units

    # Perform the BFS to get the shortest path
    prev = {start: None}
    while queue:
        loc = queue.popleft()
        for neighbor in graph[loc]:
            if neighbor == end:
                # Found the end, clear the queue and log the previous location
                queue.clear()
                prev[neighbor] = loc
                break
            elif neighbor not in visited and neighbor in graph and neighbor not in occupied:
                queue.append((neighbor))
            prev[neighbor] = loc
            visited.add(neighbor)

    # Reconstruct path
    path = []
    at = end
    for i in range(20):
        path.append(at)
        at = prev[at]
        if at is None:
            break
    else:
        path.reverse()
        print('foo')
        print(path)
    path.reverse()

    return path


def parse_input(data):

    re_x_scalar = re.compile('x=(\d+)')
    re_x_array = re.compile('x=(\d+)\.\.(\d+)')
    re_y_scalar = re.compile('y=(\d+)')
    re_y_array = re.compile('y=(\d+)\.\.(\d+)')

    clay = set()

    for line in data:

        match_x_array = re_x_array.search(line)
        if match_x_array:
            xs = range(int(match_x_array.groups()[0]), int(match_x_array.groups()[1])+1)
            match_y = re_y_scalar.search(line)
            y = int(match_y.groups()[0])
            for x in xs:
                clay.add((x, y))
                
        match_y_arrax = re_y_array.search(line)
        if match_y_arrax:
            ys = range(int(match_y_arrax.groups()[0]), int(match_y_arrax.groups()[1])+1)
            match_x = re_x_scalar.search(line)
            x = int(match_x.groups()[0])
            for y in ys:
                clay.add((x, y))

    list_clay = list(clay)
    min_y = min([c[1] for c in list_clay])
    max_y = max([c[1] for c in list_clay])
    min_x = min([c[0] for c in list_clay])
    max_x = max([c[0] for c in list_clay])

    return clay, min_x, max_x, min_y, max_y


def solve(data):

    clay, min_x, max_x, min_y, max_y = parse_input(data)
    print(clay, min_x, max_x, min_y, max_y)


if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines)

    # with open('input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(data=lines)

