import matplotlib.pyplot as plt
import numpy as np
import time

from RoadManager import RoadManager

class RoadSimulator2018(object):

    def __init__(self):
        self.start_time = time.time()
        self.rd = object()

    def reachSteadyState(self):
        for _ in range(50):
            self.rd.tick()

        self.rd.collision = 0
        self.rd.speed_collision = 0
        self.rd.total = 0

        self.rd.collisionTime = []
        self.rd.speedCollisionTime = []
        self.rd.totalTime = []

    def runSim(self, lanes, target_lanes, rate_in, rate_out, smart_car_prob, sims):

        self.rd = RoadManager(lanes, target_lanes, rate_in, rate_out, smart_car_prob) #BEST ONE SO FAR
        #rd = RoadManager([26,26,26,16,14,12,10,6], [0, 1, 2], 0.5, 0.5)
        #rd = RoadManager([63, 63, 63, 63, 63, 63, 63, 63], [0, 1, 2, 3, 4, 5, 6, 7], 0.5, 0.5)

        self.reachSteadyState()

        for _ in range(sims):
            self.rd.tick()

        return self.rd.totalTime, self.rd.collisionTime, self.rd.speedCollisionTime

    def f(self, t, coeff):
        return coeff[1] + t*coeff[0]

    def linearTrend(self, throughput, mergeCollision, speedCollision, sims):

        z = np.polyfit(range(0, sims), throughput, 1)
        print "\n\n\nSlope of Trend: " + str(z[0])
        print "\nTotal: " + str(throughput[-1]) + "\nMerge Collisions: " + str(mergeCollision[-1]) + "\nSpeed Collisions: " + str(speedCollision[-1])

        print("--- %s seconds ---" % (time.time() - self.start_time))

        fig1 = plt.figure()
        fig1.suptitle("Total Throughput")
        plt.plot(np.asarray(range(0, sims)), self.f(np.asarray(range(0, sims)), z), "r--")
        plt.plot(range(0, sims), throughput, "o")
        fig2 = plt.figure()
        fig2.suptitle("Merge Collisions")
        plt.plot(range(0, sims), mergeCollision, "o")
        fig3 = plt.figure()
        fig3.suptitle("Speed Collisions")
        plt.plot(range(0, sims), speedCollision, "o")
        plt.show()
