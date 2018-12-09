from __future__ import print_function, division, absolute_import

from collections import deque
import itertools


def solve(num_players, last_marble):
    circle = deque([0])

    scores = dict([(i, 0) for i in range(num_players)])
    player_iter = itertools.cycle(range(num_players))

    for marble in range(1, last_marble + 1):
        player = next(player_iter)
        if marble % 23 == 0:
            # rotate the deque 7 units CCW
            circle.rotate(7)
            scores[player] += marble + circle.popleft()
        else:
            circle.rotate(-2)
            circle.appendleft(marble)

    print(max(scores.values()))


if __name__ == '__main__':
    #
    #
    # part1(num_players=9, last_marble=25)
    # part1(num_players=10, last_marble=1618)

    print('part 1: ', end='')
    solve(num_players=424, last_marble=71482) # 408679

    # part 2
    print('part 2: ', end='')
    solve(num_players=424, last_marble=71482 * 100)

