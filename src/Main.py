""" Main file to run the simulation. """

from RoadManager import RoadManager

if __name__ == '__main__':
    rd = RoadManager([6, 7, 6], [1], 1, 1)
    rd.tick(True)
    rd.tick(True)
