""" Class representing a car on the road. """
import random as r

class Car(object):

    def __init__(self, lane, road, val = 0,  dist = 0):
        self.vmax = 4
        self.lane = lane
        self.dist = dist
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
        newSpeed = self._get_new_speed(distanceToNextCar, currentLane, lastCar, road)

        self._set_dist(self.dist + newSpeed)
        self._set_val(newSpeed)

        exit = road.update_cell(self.lane, self.dist, self.val)

        return exit

    def _set_dist(self, dist):
        self.dist = dist

    def _set_val(self, val):
        self.val = val

    def _next_car(self, currentLane):
        count = 0
        lastCar = False
        for i in range(self.dist + 1, len(currentLane)):
            count = count + 1
            if currentLane[i] != -1:
                break

        #last car in the lane
        if (count == (len(currentLane) - (self.dist + 1))):
            lastCar = True

        return count, lastCar

    def _get_new_speed(self, distanceToNextCar, currentLane, lastCar, road):
        if not lastCar:
            if distanceToNextCar > currentLane[self.dist] + 1:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                else:
                    newSpeed = currentLane[self.dist] + 1
            else:
                newSpeed = distanceToNextCar - 1
        else:
            if self.lane in road.target_lanes:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                else:
                    newSpeed = currentLane[self.dist] + 1
            else:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                if distanceToNextCar <= self.val and distanceToNextCar > 0:
                    newSpeed = distanceToNextCar - 1
                elif distanceToNextCar == 0:
                    newSpeed = 0
                else:
                    newSpeed = currentLane[self.dist] + 1

        if r.random() >= 1:
            if newSpeed >= 1:
                newSpeed = newSpeed - 1

        return newSpeed

    def _get_lane(self, lane, road):
        length = road.get_lane_size(lane)
        return [road.get_cell(lane, i) for i in range(0, length)]


    def _merge(self):
        pass
