""" Main file to run the simulation. """

from RoadManager import RoadManager

if __name__ == '__main__':

    rd = RoadManager([6, 7], [], 0.5, 0.5)
    for _ in range(10):
        rd.tick(True)
