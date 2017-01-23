""" Main file to run the simulation. """
from RoadSimulator2018 import RoadSimulator2018
import ShapeBreeder

from matplotlib import pyplot as plt
import numpy as np

SIMS = 100

def plot_target_loc(trials, y_measure):
    scores = ShapeBreeder.breed_best_loc(trials, ShapeBreeder.objective2)
    plt.errorbar(range(1, 7), [np.average(score) for score in scores],
                 yerr=[np.var(score) for score in scores], fmt='o')
    plt.title(y_measure + ' vs. Starting Exit Lane Index (%d Trials)' % trials)
    plt.ylabel(y_measure)
    plt.xlabel('Starting Exit Lane Index')
    plt.xlim([0, 7])
    plt.show()

if __name__ == '__main__':
    # plot_target_loc(30, 'Throughput')
    ShapeBreeder.breed_best_shape(9, [1, 2, 3, 4], 136, 5, 32, 4, 3,
                                  ShapeBreeder.objective1)
    # Just throughput
    ShapeBreeder.breed_best_shape(9, [1, 2, 3, 4], 136, 5, 32, 4, 3,
                                  ShapeBreeder.objective2)
    # RS = RoadSimulator2018()
    #
    # throughput, mergeCollision, speedCollision = \
    #     RS.runSim([6,10,17,22,22,22,10,9], [3, 4, 5], 1, False, SIMS)
    #
    # RS.linearTrend(throughput, mergeCollision, speedCollision, SIMS)
