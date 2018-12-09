from __future__ import print_function, division, absolute_import

import itertools

class Circle(object):

    def __init__(self):
        self.marbles = [0]
        self.current_marble = 0

    def place_marble(self, i):
        score = 0
        if i % 23 == 0:
            current_idx = self.marbles.index(self.current_marble)
            idx_to_remove = current_idx - 7
            # print('current', self.current_marble, 'current_idx', current_idx, 'idx_to_remove', idx_to_remove)
            self.current_marble = self.marbles[idx_to_remove + 1]
            score = 23 + self.marbles.pop(idx_to_remove)
        else:
            insert_idx = self.get_insertion_idx()
            self.marbles.insert(insert_idx, i)
            self.current_marble = i
        return score

    def get_insertion_idx(self):
        current_idx = self.marbles.index(self.current_marble)
        insertion_idx = current_idx + 2
        if insertion_idx > len(self.marbles):
            insertion_idx = insertion_idx - len(self.marbles)
        return insertion_idx



def part1(num_players, last_marble_score):

    players_scores = dict([(i, 0) for i in range(1, num_players + 1)])
    c = Circle()

    player_iter = itertools.cycle(range(1, num_players + 1))

    for marble in range(1, last_marble_score + 1):
        print(marble)
        players_scores[next(player_iter)] += c.place_marble(marble)
        #print(player, marble, c.marbles, players_scores[player]) #, c.marbles, players_scores[player])

    print('winning score: ', max(players_scores.values()))




if __name__ == '__main__':

    # # # print('test result: ', end='')
    # with open('test_input.txt', 'r') as f:
    #     lines = [s.strip() for s in f.readlines()]
    part1(num_players=9, last_marble_score=25)
    part1(num_players=17, last_marble_score=1104)
    # part1(num_players=10, last_marble_score=1618)


    # part1(num_players=424, last_marble_score=71482)
    # wrong 110783


    # # # print('result: ', end='')
    # with open('input.txt', 'r') as f:
    #     lines = [s.strip() for s in f.readlines()]
    # part1(data=lines[0])
