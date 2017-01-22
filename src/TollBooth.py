""" Class representing TollBooth via Markov Chain. """

from random import random

class TollBooth(object):
    def __init__(self, lane_num, rate_in, rate_out):
        self.lane_num = lane_num
        self.rate_in = rate_in
        self.rate_out = rate_out
        self.queue_size = 0

    def tick(self, road):
        emission = False
        queue_change = 0

        rand = random()
        if rand < self.rate_in:
            queue_change += 1

        if road.get_cell(self.lane_num, 0) < 0:
            rand = random()
            if rand < self.rate_out:
                queue_change -= 1
                emission = True
        self.queue_size += queue_change
        return emission
