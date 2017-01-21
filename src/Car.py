""" Class representing a car on the road. """
import random as r

class Car(object):

    def __init__(self, lane, road, val = 0):
        self.vmax = 4
        self.lane = lane
        self.dist = 0
        self.val = val
        road.update_cell(lane, 0, val)

    def tick(self, road):
        """ calls update_cell """

        currentLane = self._get_lane(self.lane, road)
        leftLane = -1
        rightLane = -1

        if self.lane > 0:
            leftLane =  self._get_lane(self.lane - 1, road)
        if self.lane < len(road.lanes) - 1:
            rightLane = self._get_lane(self.lane + 1, road)

        distanceToNextCar, lastCar = self._next_car(currentLane)

        newSpeed = self._get_new_speed(distanceToNextCar, currentLane, lastCar)


        exit = road.update_cell(self.lane, self.dist + newSpeed, newSpeed)

        return exit

    def _next_car(self, currentLane):
        count = 0
        lastCar = False
        for i in range(self.dist + 1, len(currentLane)):
            if currentLane[i] != -1:
                break
            count = count + 1

        #last car in the lane
        if count == (len(currentLane) - (self.dist + 1)):
            lastCar = True
        return count, lastCar

    def _get_new_speed(self, distanceToNextCar, currentLane, lastCar):
        if not lastCar:
            if distanceToNextCar > currentLane[self.dist] + 1:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                else:
                    newSpeed = currentLane[self.dist] + 1
            else:
                newSpeed = distanceToNextCar - 1
        else:
            if currentLane[self.dist] == self.vmax:
                newSpeed = self.vmax
            else:
                newSpeed = currentLane[self.dist] + 1
            print newSpeed

        if r.random() >= 1:
            if newSpeed >= 1:
                newSpeed = newSpeed - 1

        return newSpeed

    def _get_lane(self, lane, road):
        length = road.get_lane_size(lane)
        return [road.get_cell(lane, i) for i in range(0, length)]


    def _merge(self):
        pass
