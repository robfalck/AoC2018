
import numpy as np
import collections
from operator import itemgetter

np.set_printoptions(linewidth=1024, edgeitems=1000)

delta = {'N': (-1, 0), 'W': (0, -1), 'E': (0, 1), 'S': (1, 0)}
inv_delta = {v: k for k, v in delta.items()}

graph = {}

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
        if not t.alive:
            continue
        for direction in ('N', 'E', 'S', 'W'):
            p = t.pos + delta[direction]
            if board[p[0], p[1]] == 1:
                # this square is occupied by a wall
                continue
            else:
                for t2 in targets:
                    if manhattan_distance(p, t2.pos) == 0:
                        break
                else:
                    # this square is not occupied
                    squares.append(tuple(p.tolist()))
    return squares

def get_occupied_squares(allies, enemies):
    occupied = set()
    for unit in allies + enemies:
        if unit.alive:
            tpos = tuple(unit.pos.tolist())
            occupied.add(tpos)
    return occupied

def get_num_moves(pos, board, allies, enemies):
    """
    Returns a np array of the board where each element holds
    the number of moves required to get from pos to that element.
    """

    # Setup the visited set and queue for the BFS
    visited, queue = set(), collections.deque([(0, pos)])

    grid = np.zeros_like(board) - 1
    visited.add(pos)

    # Setup a set of spaces occupied by units
    occupied = get_occupied_squares(allies, enemies)

    # Perform the BFS to find the number of moves required to
    # get to every accessible point on the grid.
    while queue:
        distance, p = queue.popleft()
        grid[p] = distance
        for neighbor in graph[p]:
            if neighbor not in visited and neighbor in graph and neighbor not in occupied:
                queue.append((distance+1, neighbor))
            visited.add(neighbor)

    return grid

def get_shortest_path(start, end, allies, enemies):
    """
    Returns a np array of the board where each element holds
    the number of moves required to get from pos to that element.
    """

    # Setup the visited set and queue for the BFS
    visited, queue = set(), collections.deque([(start)])
    visited.add(start)

    # Setup a set of spaces occupied by units
    occupied = get_occupied_squares(allies, enemies)

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


def print_board(turn, board, elves, goblins):
    g = np.empty(board.shape, dtype=str)
    g[:, :] = ' '
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 1:
                g[i, j] = '#'

    for elf in elves:
        g[elf.pos[0], elf.pos[1]] = 'E'

    for gob in goblins:
        g[gob.pos[0], gob.pos[1]] = 'G'

    print(' turn {0}'.format(turn))
    for row in range(board.shape[0]):
        print(''.join(g[row, :]))



class Unit(object):

    def __init__(self, pos):
        self.pos = np.array(pos, dtype=int)
        self.hit_points = 200
        self.attack_power = 3
        self.alive = True

    def __repr__(self):
        return '{0:6s}: pos:{1:10s}  hp:{2:03d}  {3}'.format(type(self).__name__, str(self.pos), self.hit_points, ' ' if self.alive else 'X')

    def get_attack_options(self, enemies):
        attack_directions = []
        for t in enemies:
            if not t.alive:
                continue
            if tuple(distance(self.pos, t.pos)) in delta.values():
                attack_directions.append(inv_delta[tuple(distance(self.pos, t.pos))])
        return attack_directions

    def __lt__(self, other):
        self_row, self_col = self.pos
        other_row, other_col = other.pos
        if self_row == other_row:
            return self_col < other_col
        return self_row < other_row

    def try_attack(self, enemies):
        # Can this unit attack this turn?
        attack_directions = self.get_attack_options(enemies)

        if not attack_directions:
            return False

        fewest_target_hit_points = 1E16
        target_to_attack = None
        for direction in ('N', 'W', 'E', 'S'):
            if direction in attack_directions:
                tpos = tuple((self.pos + delta[direction]).tolist())
                target_unit = [enemy for enemy in enemies if tuple(enemy.pos.tolist()) == tpos][0]
                if target_unit.hit_points < fewest_target_hit_points:
                    fewest_target_hit_points = target_unit.hit_points
                    target_to_attack = target_unit
        target_to_attack.hit_points -= self.attack_power

        if target_to_attack.hit_points <= 0:
            target_to_attack.alive = False

        return True

    def take_turn(self, turn, allies, enemies, board):

        if turn == 2:
            print('turn 2')

        # I can't attack if I'm dead
        if not self.alive:
            return

        attack_performed = self.try_attack(enemies)
        if attack_performed:
            # Turn complete
            return 'attacked'

        # No attack performed, do a move
        # Get the number of movements to move to any point in the grid
        distance_grid = get_num_moves(tuple(self.pos.tolist()), board, allies, enemies)
        # print(distance_grid)

        # Find all squares within range of the enemy
        squares_in_range = get_squares_in_range(enemies, board)
        # print(squares_in_range)

        # Find the closest square in range of the enemy
        distances = {s: distance_grid[s] for s in squares_in_range if distance_grid[s] > 0}
        if not distances:
            return 'no enemies'
        min_distance = min(distances.values())
        # print(min_distance)

        # find nearest
        nearest = [loc for loc in distances if distances[loc] == min_distance]
        target = sorted(nearest, key=itemgetter(0, 1))[0]

        # find shortest path to target
        path = get_shortest_path(tuple(self.pos.tolist()), target, allies, enemies)

        # move along the chosen direction
        self.pos[...] = path[1]

        self.try_attack(enemies)

        return 'move and attacked'

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

    # Build the list of neighbors for each square in the grid.  this is our graph.
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 0:
                graph[i, j] = []
                for direction in 'N', 'E', 'S', 'W':
                    graph[i, j].append(tuple((np.asarray((i, j), dtype=int) + delta[direction]).tolist()))

    print_board(0, board, elves, goblins)
    print()

    units = elves + goblins
    units.sort()

    for unit in units:
        print(unit)

    for turn in range(1,1000):
        units = elves + goblins
        units.sort()
        for unit in units:
            if isinstance(unit, Elf):
                allies = elves
                enemies = goblins
            else:
                allies = goblins
                enemies = elves

            if unit is goblins[0] and turn == 2:
                print(unit.pos)

            exit_status = unit.take_turn(turn, allies, enemies, board)

            if exit_status == 'no enemies':
                print('done after', turn-1, 'full turns')
                hp_remaining = sum([unit.hit_points for unit in units if unit.alive])
                print('hitpoints remaining', hp_remaining)
                print('result', (turn-1) * hp_remaining)
                exit(0)

        print(turn)
        print_board(turn, board, elves, goblins)
        print()
        for unit in units:
            print(unit)


if __name__ == '__main__':
    with open('test_input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)


    # with open('input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(initial_state=lines)