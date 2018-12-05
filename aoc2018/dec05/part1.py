from __future__ import print_function, division, absolute_import

def annihilate_next_match(polymer):
    for i in range(len(polymer)-1):
        char_a = polymer[i]
        char_b = polymer[i+1]

        if (char_b == char_a.upper() and char_a == char_b.lower()) or (char_a == char_b.upper() and char_b == char_a.lower()):
            # Annihilate
            return polymer[:i] + polymer[i+2:]
    else:
        return False


def part1(polymer):

    p = polymer

    while True:
        p = annihilate_next_match(p)
        if not p:
            break
        print(len(p))



if __name__ == '__main__':

    with open('test_input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part1(polymer=lines[0])


    with open('input.txt', 'r') as f:
        lines = [s.strip() for s in f.readlines()]

    part1(polymer=lines[0])