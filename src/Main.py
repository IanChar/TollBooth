""" Main file to run the simulation. """

from RoadManager import RoadManager

if __name__ == '__main__':
    rd = RoadManager([5, 7, 5], [1], 1, 1)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
    rd.tick(True)
