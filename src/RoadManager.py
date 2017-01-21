""" Class to manage all elements of the simulation. """
import time
import sys

from Car import Car
from Road import Road
from TollBooth import TollBooth

class RoadManager(object):
    def __init__(self, lane_sizes, target_lanes, rate_in, rate_out):
        self.road = Road(lane_sizes, target_lanes)
        self.actors = [Car(0, self.road, 0)]
        self.road.commit_updates()
        self.road.print_road()
        self.booths = [TollBooth(lane_num, rate_in, rate_out)
                       for lane_num in range(len(lane_sizes))]

    def tick(self, print_progress=False):
        # Make all the actors act.
        to_remove = []
        for actor_id, actor in enumerate(self.actors):
            if not actor.tick(self.road):
                to_remove.append(actor_id)
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
            # TODO: Alter this if we want different cars.
            self.actors.append(Car(lane_num, self.road))
        throughput = self.road.commit_updates()

        if print_progress:
            self.road.print_road()
        sys.stdout.write("\033[F\n") # Cursor up one line
        time.sleep(0.3)
        # Return how many cars left the scene during this tick.
        return throughput
