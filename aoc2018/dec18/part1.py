from __future__ import print_function, division, absolute_import

def parse_input(data):

    acres = {}
    for i, line in enumerate(data):
        for j in range(len(line)):
            acres[i, j] = line[j]
    return acres, len(data), len(data[0])

def count_adjacent(row, col, acres, char='|'):
    count = 0
    for d_row, d_col in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        if d_row == d_col == 0:
            continue
        try:
            if acres[row + d_row, col + d_col] == char:
                count += 1
        except KeyError:
            pass
    return count


def mutate(acres, num_rows, num_cols):
    acres_new = acres.copy()
    for i in range(num_rows):
        for j in range(num_cols):

            if acres[i, j] == '.':
                if count_adjacent(i, j, acres, '|') >= 3:
                    acres_new[i, j] = '|'

            elif acres[i, j] == '|':
                if count_adjacent(i, j, acres, '#') >= 3:
                    acres_new[i, j] = '#'

            elif acres[i, j] == '#':
                if count_adjacent(i, j, acres, '#') > 0 and count_adjacent(i, j, acres, '|') > 0:
                    acres_new[i, j] = '#'
                else:
                    acres_new[i, j] = '.'

    return acres_new


def print_land(acres, num_rows, num_cols):
    for i in range(num_rows):
        for j in range(num_cols):
            print(acres[i, j], end='')
        print()
    print()



def solve(data, minutes=10):

    acres, num_rows, num_cols = parse_input(data)

    for time in range(minutes):
        acres = mutate(acres, num_rows, num_cols)
        # print()
        # print_land(acres, num_rows, num_cols)

    num_wooded = len([a for a in acres.values() if a == '|'])
    num_lumber_yards = len([a for a in acres.values() if a == '#'])
    num_resources = num_wooded * num_lumber_yards

    print('Wooded acres:', num_wooded)
    print('Lumber yards:', num_lumber_yards)
    print('Total Resources:', num_resources)




if __name__ == '__main__':

    # with open('test_input.txt', 'r') as f:
    #     lines = [s.rstrip() for s in f.readlines()]
    # solve(data=lines)

    # part 1
    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]
    solve(data=lines, minutes=10)

    # part 2
    with open('input.txt', 'r') as f:
        lines = [s.rstrip() for s in f.readlines()]

    # Find how long it takes the pattern to repeat
    for minutes in range(100, 1000, 100):
        print()
        print('After {0} minutes:'.format(minutes))
        solve(data=lines, minutes=minutes)

