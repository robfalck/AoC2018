from __future__ import print_function, division, absolute_import

def get_claim(inp):
    id_str, tail = inp.split('@')
    pos_str, size_str = tail.split(':')
    pos_x, pos_y = [int(s) for s in pos_str.split(',')]
    width, height = [int(s) for s in size_str.split('x')]
    return id_str.strip()[1:], pos_x, pos_y, width, height

def part1(data):

    fabric = {}

    for d in data:
        id, pos_x, pos_y, width, height = get_claim(d)
        print(pos_x, pos_y, width, height)
        for i in range(width):
            for j in range(height):
                loc = (pos_x + i, pos_y + j)
                if not loc in fabric:
                    fabric[pos_x + i, pos_y + j] = 0
                fabric[pos_x + i, pos_y + j] += 1

    count = 0
    for loc, claims in fabric.items():
        if claims > 1:
            count += 1
    print(count)



if __name__ == '__main__':
    test_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split('\n')

    part1(data=test_input)

    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part1(data=lines)