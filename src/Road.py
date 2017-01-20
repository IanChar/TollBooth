""" Class representing the road. """

import gc

"""
Properties:
    - lane_sizes: list of sizes.
    - target_lanes: The lanes that the cars should head towards.
    - lanes: The lanes represented as a nested list where -1 is empty.
    - future_lanes: What the lanes will be once we have commmited.
    - exiting: The number of cars that will be exiting off to the right.
 """
class Road(object):

    def __init__(self, lane_sizes, target_lanes):
        self.lane_sizes = lane_sizes
        # Check if target_lanes valid, and set it if it is.
        for target in target_lanes:
            if target > len(lane_sizes):
                raise ValueError('Target outside of available lanes.')
        self.target_lanes = target_lanes
        # Generate lanes and future_lanes
        self.lanes = self._create_blank_lanes()
        self.future_lanes = self._create_blank_lanes()
        # Set exiting to 0
        self.exiting = 0

    """ Get a cell in current lanes. """
    def get_cell(self, lane, dist):
        return self.lanes[lane][dist]

    def get_lane_size(self, lane):
        return self.lane_sizes[lane]

    """ Change one of the values in future lane.

        Returns: True if we are still on the road, False if not.
    """
    def update_cell(self, lane, dist, val):
        if dist >= len(self.future_lanes[lane]):
            self.exiting += 1
            return False
        else:
            self.future_lanes[lane][dist] = val
            return True

    """ Commit the updates we have made and clear future_lanes.

        Returns: The number of cars that exited off to the right.
    """
    def commit_updates(self):
        del self.lanes
        gc.collect()
        self.lanes = self.future_lanes

        exited = self.exiting
        self.exiting = 0
        return exited

    def print_road(self):
        for lane in self.lanes:
            print '\t'.join([str(speed) if speed >= 0 else '-'
                             for speed in lane])

    def _create_blank_lanes(self):
        return [[-1 for _ in range(size)] for size in self.lane_sizes]

if __name__ == '__main__':
    road = Road([4, 5, 3], [1])
    road.update_cell(0, 0, 0)
    road.update_cell(1, 1, 1)
    road.update_cell(1, 3, 2)
    road.update_cell(2, 2, 2)
    road.commit_updates()
    road.print_road()
