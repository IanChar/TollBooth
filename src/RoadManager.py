""" Class to manage all elements of the simulation. """

from Road import Road

class RoadManager(object):
    def __init__(self, lane_sizes, target_lanes, rate_in, rate_out):
        self.road = Road(lane_sizes, target_lanes)
        self.actors = []

    def tick():
        pass
