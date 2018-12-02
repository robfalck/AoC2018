from __future__ import print_function, division, absolute_import


def part1():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    box_id_tracker = {2: [], 3: []}

    for box_id in lines:
        letter_counts = {}
        for char in box_id:
            if char in letter_counts:
                continue
            letter_counts[char] = box_id.count(char)
        letters_that_appear_twice = [key for key in letter_counts if letter_counts[key] == 2]
        letters_that_appear_thrice = [key for key in letter_counts if letter_counts[key] == 3]

        if letters_that_appear_twice:
            box_id_tracker[2].append(box_id)
        if letters_that_appear_thrice:
            box_id_tracker[3].append(box_id)

    checksum = len(box_id_tracker[2]) * len(box_id_tracker[3])

    print(checksum)


if __name__ == '__main__':
    part1()