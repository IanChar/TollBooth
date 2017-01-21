""" Main file to run the simulation. """
import matplotlib.pyplot as plt
import plotly.plotly as py

from RoadManager import RoadManager

if __name__ == '__main__':
    rd = RoadManager([25,27,27,25,24], [1, 2], 0.5, 0.5)
    for _ in range(100):
        rd.tick(True)


    print rd.total
    plt.plot(range(0, 100), rd.totalTime, "o")
    plt.show()
