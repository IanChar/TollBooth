""" Main file to run the simulation. """
import matplotlib.pyplot as plt
import numpy as np
import time

from RoadManager import RoadManager

def f(t, coeff):
    return coeff[1] + t*coeff[0]

if __name__ == '__main__':
    start_time = time.time()
    #rd = RoadManager([26,26,26,16,14,12,10,6], [0, 1, 2], 0.5, 0.5)
    rd = RoadManager([6,10,17,22,22,22,10,6], [3, 4, 5], 0.5, 0.5, 1) #BEST ONE SO FAR
    #rd = RoadManager([63, 63, 63, 63, 63, 63, 63, 63], [0, 1, 2, 3, 4, 5, 6, 7], 0.5, 0.5)
    sims = 100
    for _ in range(sims):
        #rd.tick()
        rd.tick(True)

    

    z = np.polyfit(range(0, sims), rd.totalTime, 1)
    print "\n\n\nSlope of Trend: " + str(z[0])
    print "\nTotal: " + str(rd.total) + "\nMerge Collisions: " + str(rd.collision) + "\nSpeed Collisions: " + str(rd.speed_collision)

    print("--- %s seconds ---" % (time.time() - start_time))

    fig1 = plt.figure()
    fig1.suptitle("Total Throughput")
    plt.plot(np.asarray(range(0, sims)), f(np.asarray(range(0, sims)), z), "r--")
    plt.plot(range(0, sims), rd.totalTime, "o")
    fig2 = plt.figure()
    fig2.suptitle("Merge Collisions")
    plt.plot(range(0, sims), rd.collisionTime, "o")
    fig3 = plt.figure()
    fig3.suptitle("Speed Collisions")
    plt.plot(range(0, sims), rd.speedCollisionTime, "o")
    plt.show()
