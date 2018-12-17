
import numpy as np
import collections
from operator import itemgetter

from part1 import Unit, Elf, Goblin, distance, manhattan_distance, build_graph, \
    get_squares_in_range, get_occupied_squares, get_cost_map, get_shortest_path, \
    print_board, print_cost_map, parse_initial_state

np.set_printoptions(linewidth=1024, edgeitems=1000)

delta = {'N': (-1, 0), 'W': (0, -1), 'E': (0, 1), 'S': (1, 0)}
inv_delta = {v: k for k, v in delta.items()}


def solve_inner_loop(elves, goblins, board, graph):

    num_elves_initial = len(elves)
    num_goblins_initial = len(goblins)
    combat_complete = False

    for turn in range(1,10000):
        # print('\nstart turn', turn)

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

            unit.take_turn(turn, allies, enemies, board, graph)

            # number of enemies remaining
            num_enemies = len([e for e in enemies if e.alive])

            if num_enemies == 0:
                print('done after', turn-1, 'full turns')
                hp_remaining = sum([unit.hit_points for unit in units if unit.alive])
                print('hitpoints remaining', hp_remaining)
                print('result', (turn-1) * hp_remaining)
                combat_complete = True
                break

        # clear the dead
        elves = [e for e in elves if e.alive]
        goblins = [g for g in goblins if g.alive]

        if combat_complete:
            break

    elves_remaining = len(elves)
    elves_killed = num_elves_initial - elves_remaining
    goblins_remaining = len(goblins)
    goblins_killed = num_goblins_initial - goblins_remaining

    return turn-1, elves_killed, goblins_killed, elves_remaining, goblins_remaining

def solve_outer_loop(initial_state):

    for attack_power in range(4, 100):
        elves, goblins, board = parse_initial_state(initial_state, elf_attack_power=attack_power)
        graph = build_graph(board)

        turns, elves_killed, goblins_killed, elves_remaining, goblins_remaining = solve_inner_loop(elves, goblins, board, graph)
        print()
        print('turns', turns)
        print('hp remaining', sum([e.hit_points for e in elves if e.alive]))
        print('result', turns * sum([e.hit_points for e in elves if e.alive]))
        print('attack power', attack_power)
        print('elves killed:', elves_killed)
        print('elves remaining:', elves_remaining)
        print('goblins killed:', goblins_killed)
        print('goblins remaining:', goblins_remaining)

        print('\n'.join([str(e) for e in elves]))

        if elves_killed == 0:
            print('minimum necessary attack power = ', attack_power)
            break


if __name__ == '__main__':

    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve_outer_loop(initial_state=lines)