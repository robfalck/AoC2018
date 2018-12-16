"""
Lagrange Four Square Theorem Algorithm from
https://cs.stackexchange.com/questions/2988/how-fast-can-we-find-all-four-square-combinations-that-sum-to-n
"""
from math import sqrt
import itertools


def sqrt_nearest_int(n):
    return int(sqrt(float(n)))


def two_square_sum_less_than(n):
    """
    Returns a list of all sums of two squares less than or equal to n, in order.
    """
    sum_2_sqs = {}
    base_sqrt = sqrt_nearest_int(n)

    for i in range(base_sqrt, -1, -1):
        for j in range(i + 1):
            sum_ = (i * i) + (j * j)
            if sum_ > n:
                break
            else:
                # make the new pair
                sum_2_sqs[sum_] = (i, j)

    # collapse the index array down to a sequential list
    return sum_2_sqs


def find_four_squares_that_sum_to(n):

    sqr_2s = two_square_sum_less_than(n)

    print(sqr_2s)

    # If the number is the sum of two squares, then just return them
    if n in sqr_2s:
        return 0, 0, sqr_2s[n][0], sqr_2s[n][1]

    n_2s = list(sqr_2s.keys())

    # This isn't as efficient as the original authors implementation, but its clean code.
    for a, b in itertools.combinations_with_replacement(n_2s, 2):
        if a * b == n:
            if 0 in sqr_2s[a]:
                k1, k2 = 0, 0
            else:
                k1, k2 = sqr_2s[a]
            if 0 in sqr_2s[b]:
                k3, k4 = 0, 0
            else:
                k3, k4 = sqr_2s[b]
            return k1, k2, k3, k4
    else:
        # It must be the sum of three squares:
        seq = range(n)
        for a, b, c in itertools.combinations_with_replacement(seq, 3):
            if a**2 + b**2 + c**2 == n:
                return 0, a, b, c
        else:
            raise ValueError('wtf')


if __name__ == '__main__':
    a, b, c, d = find_four_squares_that_sum_to(16)
    print(a, b, c, d)
    # for i in range(20):
    #     print(i)
    #     a, b, c, d = find_four_squares_that_sum_to(i)
    #     print(i, ':', a, b, c, d)
    #     # print(a, b, c, d)
