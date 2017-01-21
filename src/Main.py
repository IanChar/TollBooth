""" Main file to run the simulation. """
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

from RoadManager import RoadManager

if __name__ == '__main__':
    rd = RoadManager([26,26,26,16,14,12,10,6], [0, 1, 2], 0.5, 0.5)
    #rd = RoadManager([6,10,17,22,22,22,10,6], [3, 4, 5], 0.5, 0.5)
    for _ in range(100):
        rd.tick(True)

    #reg = linear_model.LinearRegression()
    #reg.fit(zip(range(0,100), rd.totalTime), range(0,100))

    #print reg.coef

    print "\n\n\n\n" + str(rd.total)
    plt.plot(range(0, 100), rd.totalTime, "o")
    plt.show()
