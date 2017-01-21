""" Class representing TollBooth via Markov Chain. """

from random import random

class TollBooth(object):
    def __init__(self, lane_num, rate_in, rate_out):
        self.lane_num = lane_num
        self.rate_in = rate_in
        self.rate_out = rate_out
        self.processing = 0

    def tick(self, road):
        rand_num = random()
        if rand_num <= self.rate_in:
            self.processing += 1
        elif self.processing > 0 and road.get_cell(self.lane_num, 0) < 0:
            if rand_num <= (self.rate_in + self.rate_out):
                self.processing -= 1
                return True
        return False
