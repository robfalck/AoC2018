
import numpy as np
import collections
from operator import itemgetter

np.set_printoptions(linewidth=1024, edgeitems=1000)

delta = {'N': (-1, 0), 'W': (0, -1), 'E': (0, 1), 'S': (1, 0)}
inv_delta = {v: k for k, v in delta.items()}

def distance(p1, p2):
    return np.array(p2) - np.array(p1)

def manhattan_distance(p1, p2):
    return sum(np.abs(distance(p1, p2)))

def build_graph(board):
    # Build the list of neighbors for each square in the grid.  this is our graph.
    graph = {}
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 0:
                graph[i, j] = []
                for direction in 'N', 'E', 'S', 'W':
                    row, col = i + delta[direction][0], j + delta[direction][1]
                    if board[row, col] == 0:
                        graph[i, j].append((row, col))
    return graph

def get_squares_in_range(allies, enemies, graph):
    """
    returns the positions of the squares that are within range of the enemy units
    """
    squares = []

    occupied = get_occupied_squares(allies, enemies)

    for e in enemies:
        if not e.alive:
            continue
        adjacent = graph[e.pos]
        squares.extend([sq for sq in adjacent if sq not in occupied])
    return squares

def get_occupied_squares(allies, enemies):
    occupied = set()
    for unit in allies + enemies:
        if unit.alive:
            occupied.add(unit.pos)
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

def get_cost_map(pos, allies, enemies, graph):
    # Setup the visited set and queue for the BFS
    visited, queue = set(), collections.deque([(0, pos)])

    visited.add(pos)
    cost_map = {}

    # Setup a set of spaces occupied by units
    occupied = get_occupied_squares(allies, enemies)

    # Perform the BFS to find the number of moves required to
    # get to every accessible point on the grid.
    while queue:
        distance, p = queue.popleft()
        cost_map[p] = distance
        for neighbor in graph[p]:
            if neighbor not in visited and neighbor in graph and neighbor not in occupied:
                queue.append((distance+1, neighbor))
            visited.add(neighbor)

    return cost_map


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
                # Found the end, clear the queue and log the previous location\
                prev[neighbor] = loc
                break
            if neighbor not in visited and neighbor in graph and neighbor not in occupied:
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
    path.reverse()

    return path


def print_board(turn, board, elves, goblins):
    g = np.empty(board.shape, dtype=str)
    g[:, :] = '.'
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 1:
                g[i, j] = '#'

    for elf in elves:
        g[elf.pos[0], elf.pos[1]] = 'E'

    for gob in goblins:
        g[gob.pos[0], gob.pos[1]] = 'G'

    print()
    for row in range(board.shape[0]):
        print(''.join(g[row, :]))
    print()


def print_cost_map(turn, board, elves, goblins, cost_map):
    g = np.empty(board.shape, dtype=str)
    g[:, :] = '.'
    for i in range(board.shape[0]):
        for j in range(board.shape[1]):
            if board[i, j] == 1:
                g[i, j] = '#'

    for elf in elves:
        g[elf.pos[0], elf.pos[1]] = 'E'

    for gob in goblins:
        g[gob.pos[0], gob.pos[1]] = 'G'

    for key, val in cost_map.items():
        g[key] = str(val)

    print()
    for row in range(board.shape[0]):
        print(''.join(g[row, :]))
    print()


class Unit(object):

    def __init__(self, pos, attack_power=3):
        self.pos = pos
        self.hit_points = 200
        self.attack_power = attack_power
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
                p = self.pos[0] + delta[direction][0], self.pos[1] + delta[direction][1]
                target_unit = [enemy for enemy in enemies if enemy.pos == p][0]
                if target_unit.hit_points < fewest_target_hit_points:
                    fewest_target_hit_points = target_unit.hit_points
                    target_to_attack = target_unit
        target_to_attack.hit_points -= self.attack_power

        if target_to_attack.hit_points <= 0:
            target_to_attack.alive = False

        return True

    def try_move(self, turn, allies, enemies, board, graph):
        # squares in range of the enemy
        squares = get_squares_in_range(allies, enemies, graph)
        # print(squares)

        # cost_map
        cost_map = get_cost_map(self.pos, allies, enemies, graph)
        # print(cost_map)
        # print_cost_map(turn, board, enemies, allies, cost_map)
        square_costs = {sq: cost_map[sq] for sq in squares if sq in cost_map}
        min_cost_squares = [sq for sq in squares if sq in cost_map and cost_map[sq] == min(square_costs.values())]
        if not min_cost_squares:
            # No viable targets found, do not move
            return False
        target_square = sorted(min_cost_squares, key=itemgetter(0, 1))[0]

        # now build a new cost_map from the targeted squares perspective
        # choose the square adjacent to this unit with the lowest cost for the first move
        # if multiple squares have the lowest cost, choose the first in reading order
        rev_cost_map = get_cost_map(target_square, allies, enemies, graph)
        first_step = None
        for direction in 'N', 'W', 'E', 'S':
            sq = self.pos[0] + delta[direction][0], self.pos[1] + delta[direction][1]
            if sq not in graph or sq not in rev_cost_map:
                continue
            if first_step is None or rev_cost_map[sq] < rev_cost_map[first_step]:
                first_step = sq

        if first_step is not None:
            self.pos = first_step
            return True
        return False

    def take_turn(self, turn, allies, enemies, board, graph):

        # I can't attack if I'm dead
        if not self.alive:
            return

        attack_performed = self.try_attack(enemies)
        if attack_performed:
            # Turn complete
            return

        # No attack performed, do a move
        move_performed = self.try_move(turn, allies, enemies, board, graph)
        if not move_performed:
            # Turn complete
            return

        self.try_attack(enemies)


class Elf(Unit):

    def __init__(self, pos, attack_power=3):
        super(Elf, self).__init__(pos, attack_power)


class Goblin(Unit):

    def __init__(self, pos, attack_power=3):
        super(Goblin, self).__init__(pos, attack_power)


def parse_initial_state(initial_state, elf_attack_power=3):

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
                elves.append(Elf((i, j), attack_power=elf_attack_power))
            elif initial_state[i][j] == 'G':
                goblins.append(Goblin((i, j)))

    return elves, goblins, board


def solve(initial_state):

    elves, goblins, board = parse_initial_state(initial_state)

    graph = build_graph(board)

    units = elves + goblins
    units.sort()

    print('\ninitial setup')
    print_board(0, board, elves, goblins)
    for unit in units:
        print(unit)

    for turn in range(1,1000):
        print('\nstart turn', turn)

        # Sort all units by read-order
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

            unit.take_turn(turn, allies, enemies, board, graph)

            # number of enemies remaining
            num_enemies = len([e for e in enemies if e.alive])

            if num_enemies == 0:
                print('done after', turn-1, 'full turns')
                hp_remaining = sum([unit.hit_points for unit in units if unit.alive])
                print('hitpoints remaining', hp_remaining)
                print('result', (turn-1) * hp_remaining)
                exit(0)

        # clear the dead
        elves = [e for e in elves if e.alive]
        goblins = [g for g in goblins if g.alive]

        print_board(turn, board, elves, goblins)
        for unit in units:
            print(unit)
        print('end turn', turn)
        print()
        print()


if __name__ == '__main__':
    # with open('test_input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(initial_state=lines)


    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(initial_state=lines)