

def solve(score, take_digits, after):

    initial_length = len(str(score))
    recipes = [int(c) for c in str(score)]

    e1 = 0
    e2 = 1

    round = 0
    result = []
    while len(recipes) < take_digits + after:
        round += 1

        # Elf current scores
        e1_score = recipes[e1]
        e2_score = recipes[e2]

        # Extend the score list
        new_scores = [int(c) for c in str(e1_score + e2_score)]
        recipes.extend(new_scores)
        # print(recipes)

        e1 = e1 + e1_score + 1
        while e1 >= len(recipes):
            e1 -= len(recipes)

        e2 = e2 + e2_score + 1
        while e2 >= len(recipes):
            e2 -= len(recipes)

    result = [recipes[i] for i in range(after, after + take_digits)]
    result = ''.join([str(i) for i in result])
    return result


if __name__ == '__main__':
    assert(solve(37, take_digits=10, after=9) == '5158916779')
    assert(solve(37, take_digits=10, after=5) == '0124515891')

    print(solve(37, take_digits=10, after=440231))  # 1052903161
