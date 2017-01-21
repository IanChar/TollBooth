""" Main file to run the simulation. """

from RoadManager import RoadManager

if __name__ == '__main__':

    rd = RoadManager([20,22,22,21,20], [1,2], 0.5, 0.5)
    for _ in range(100):
        rd.tick(True)
    for _ in range(5):
        rd.tick(True)
