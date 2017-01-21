""" Main file to run the simulation. """
from RoadSimulator2018 import RoadSimulator2018

SIMS = 1000

if __name__ == '__main__':
    RS = RoadSimulator2018()

    throughput, mergeCollision, speedCollision = \
        RS.runSim([6,10,17,22,22,22,10,6], [3, 4, 5], 0.5, 0.5, 1, SIMS)

    RS.linearTrend(throughput, mergeCollision, speedCollision, SIMS)
