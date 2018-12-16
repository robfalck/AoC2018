
import numpy as np
import networkx as nx

delta = {'up': (-1, 0), 'left': (0, -1), 'right': (0, 1), 'down': (1, 0)}
inv_delta = {v: k for k, v in delta.items()}


def distance(p1, p2):
    return p2 - p1


def manhattan_distance(p1, p2):
    return sum(np.abs(distance(p1, p2)))


def get_squares_in_range(targets, board):
    """
    returns the positions of the squares that are within range of the enemy units
    """
    squares = []

    for t in targets:
        for direction in ('up', 'down', 'left', 'right'):
            p = t.pos + delta[direction]

            if board[p] == 1:
                # this square is occupied by a wall
                continue
            else:
                for t2 in targets:
                    if manhattan_distance(p, t2.pos) == 0:
                        break
                else:
                    # this square is not occupied
                    squares.append(p)
    return squares


def reachable_squares(in_range, board, elves, goblins):
    pass


def build_cost_grid(unit, targets, board):
    cost_grid = np.zeros_like(board)


class Unit(object):

    def __init__(self, pos):
        self.pos = np.array(pos, dtype=int)
        self.hit_points = 200
        self.attack_power = 3

    def get_attack_options(self, enemies):
        attack_directions = []
        for t in enemies:
            if tuple(distance(self.pos, t.pos)) in delta.values():
                attack_directions.append(inv_delta[tuple(distance(self.pos, t.pos))])
        return attack_directions

    def find_all_move_paths(self, squares_in_range):
        pass

    def take_turn(self, enemies, board):

        # Can this unit attack this turn?
        attack_directions = self.get_attack_options(enemies)

        # If we can attack, don't bother moving
        if not attack_directions:
            possible = enemies

            # is a target in range?
            squares_in_range = get_squares_in_range(possible, board)





class Elf(Unit):

    def __init__(self, pos):
        super(Elf, self).__init__(pos)


class Goblin(Unit):

    def __init__(self, pos):
        super(Goblin, self).__init__(pos)


def parse_initial_state(initial_state):

    rows = len(initial_state)
    cols = len(initial_state[0])

    board = np.zeros((rows, cols), dtype=int)

    elves = []
    goblins = []

    for i in range(rows):
        for j in range(cols):
            if initial_state[i][j] == '#':
                board[i, j] = 1
            elif initial_state[i][j] == 'E':
                elves.append(Elf((i, j)))
            elif initial_state[i][j] == 'G':
                goblins.append(Goblin((i, j)))

    return elves, goblins, board




def solve(initial_state):

    elves, goblins, board = parse_initial_state(initial_state)

    for elf in elves:
        print(elf.pos, elf.get_attack_options(goblins))
    print()

    for gob in goblins:
        print(gob.pos, gob.get_attack_options(elves))

    print(len(elves))
    print(len(goblins))


if __name__ == '__main__':
    with open('test_input.txt', 'r') as f:
        lines = [s for s in f.readlines()]
    solve(initial_state=lines)