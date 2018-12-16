from collections import deque


def solve(score, find):

    initial_length = len(str(score))
    recipes = [int(c) for c in str(score)]

    e1 = 0
    e2 = 1

    round = 0
    result = []

    while True:
        round += 1

        # Elf current scores
        e1_score = recipes[e1 % len(recipes)]
        e2_score = recipes[e2 % len(recipes)]

        # Extend the score list
        new_scores = [int(c) for c in str(e1_score + e2_score)]
        recipes.extend(new_scores)

        if find in ''.join([str(i) for i in recipes[-7:]]):
            break

        e1 = (e1 + 1 + recipes[e1]) % len(recipes)
        e2 = (e2 + 1 + recipes[e2]) % len(recipes)

        if round % 100000 == 0:
            print(round, len(recipes))

    s = ''.join([str(i) for i in recipes])
    return s.index(find)


if __name__ == '__main__':
    assert(solve(37, find='51589') == 9)
    assert(solve(37, find='01245') == 5)

    print(solve(37, find='440231'))  # 1052903161
