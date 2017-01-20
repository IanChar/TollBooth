""" Main file to run the simulation. """

from RoadManager import RoadManager

if __name__ == '__main__':
    rd = RoadManager([3, 4, 3], [1], 1, 1)
    rd.tick(True)
