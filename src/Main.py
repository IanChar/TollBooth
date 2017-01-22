""" Main file to run the simulation. """
from RoadSimulator2018 import RoadSimulator2018

SIMS = 100

if __name__ == '__main__':
    RS = RoadSimulator2018()

    throughput, mergeCollision, speedCollision = \
        RS.runSim([6,10,17,22,22,22,10,9], [3, 4, 5], 1, False, SIMS)

    RS.linearTrend(throughput, mergeCollision, speedCollision, SIMS)
