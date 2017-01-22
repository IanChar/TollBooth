""" Class to manage all elements of the simulation. """
from random import random
from math import exp

import Constants as C
from Car import Car
from Road import Road
from SmartCar import SmartCar
from TollBooth import TollBooth

class RoadManager(object):
    def __init__(self, lane_sizes, target_lanes, smart_car_prob,
                 booth_config=None, traffic_speed=C.MED):
        self.smart_car_prob = smart_car_prob
        self.road = Road(lane_sizes, target_lanes)
        self.actors = []
        # Form the booth config if none was given.
        num_lanes = len(lane_sizes)
        if booth_config is None:
            booth_config = [C.FAST] * (num_lanes - 2) + [C.SLOW] * 2
        if num_lanes != len(booth_config):
            raise ValueError('Invalid booth configuration.')
        # Create the different booths.
        self.booths = []
        rate_in = traffic_speed / float(len(booth_config))
        rate_in = 1 - exp(-1* rate_in)
        for booth_id, booth in enumerate(booth_config):
            self.booths.append(TollBooth(booth_id, rate_in, C.BOOTHS[booth]))

        self.collision = 0
        self.speed_collision = 0
        self.total = 0

        self.collisionTime = []
        self.speedCollisionTime = []
        self.totalTime = []

    def tick(self, print_progress=False):
        # Make all the actors act.
        to_remove = []
        for actor_id, actor in enumerate(self.actors):
            act, collision, speed_collision = actor.tick(self.road)
            if not act:
                to_remove.append(actor_id)
            if collision:
                self.collision = self.collision + 1
            if speed_collision:
                self.speed_collision = self.speed_collision + 1

        self.collisionTime.append(self.collision)
        self.speedCollisionTime.append(self.speed_collision)

        # Remove all actors that have left the scene.
        to_remove = to_remove[::-1]
        for actor_id in to_remove:
            del self.actors[actor_id]
        # Check if any actors have entered the scene.
        to_add = []
        for lane_num, booth in enumerate(self.booths):
            if booth.tick(self.road):
                to_add.append(lane_num)
        for lane_num in to_add:
            prob = random()
            if prob < self.smart_car_prob:
                self.actors.append(SmartCar(lane_num, self.road))
            else:
                self.actors.append(Car(lane_num, self.road))
        throughput = self.road.commit_updates()

        self.totalTime.append(self.total)
        self.total = self.total + throughput

        if print_progress:
            self.road.print_road()
        #sys.stdout.write("\033[F\n") # Cursor up one line
        #time.sleep(0.3)
        # Return how many cars left the scene during this tick.
        return throughput
