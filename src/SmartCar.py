""" Class representing a smart_car on the road. """
import random as r

class SmartCar(object):

    def __init__(self, lane, road, val = 0,  dist = 0):
        self.vmax = 3
        self.lane = lane
        self.dist = dist
        self.val = val
        road.update_cell(lane, 0, val)

    def tick(self, road):
        """ calls update_cell """

        currentLane = self._get_lane(self.lane, road)
        #print currentLane
        leftLane = -1
        rightLane = -1

        if self.lane > 0:
            leftLane =  self._get_lane(self.lane - 1, road)
        if self.lane < len(road.lanes) - 1:
            rightLane = self._get_lane(self.lane + 1, road)

        distanceToNextSmartCar, lastSmartCar = self._next_smart_car(currentLane)
        newSpeed, speedCollision = self._get_new_speed(distanceToNextSmartCar, currentLane, lastSmartCar, road)
        newLane = self._should_merge(road, currentLane, leftLane, rightLane)

        if newSpeed >= self.vmax:
            newSpeed = self.vmax
        #print lastSmartCar, self.dist
        tempLane = self.lane

        self._set_lane(newLane)
        self._set_dist(self.dist + newSpeed)
        self._set_val(newSpeed)

        collisionFlag = False
        if self.dist < len(self._get_lane(self.lane, road)):
            if not road.future_lanes[self.lane][self.dist] == -1:
                self._set_lane(tempLane)
                collisionFlag = True

        exit = road.update_cell(self.lane, self.dist, self.val)

        return (exit, collisionFlag, speedCollision)

    def _set_lane(self, lane):
        self.lane = lane

    def _set_dist(self, dist):
        self.dist = dist

    def _set_val(self, val):
        self.val = val

    def _next_smart_car(self, currentLane):
        count = 0
        lastSmartCar = True
        for i in range(self.dist + 1, len(currentLane)):
            count = count + 1
            if currentLane[i] != -1:
                lastSmartCar = False
                break

        return count, lastSmartCar

    def _previous_smart_car_lane_over(self, adjacent):
        count = 0
        noPrevious = True
        val = min(self.dist - 1, len(adjacent))
        for i in range(val, -1, -1):
            count = count + 1
            if adjacent[i] != -1:
                noPrevious = False
                break

        return count - 1, noPrevious


    def _get_new_speed(self, distanceToNextSmartCar, currentLane, lastSmartCar, road):

        currentSpeed = self.val
        if not lastSmartCar:
            nextCarSpeed = currentLane[self.dist + distanceToNextSmartCar]

            if currentSpeed == 0 and distanceToNextSmartCar > 1:
                newSpeed = currentSpeed + 1
            elif currentSpeed == 1 and distanceToNextSmartCar > 2:
                newSpeed = currentSpeed + 1
            elif currentSpeed >= 2 and distanceToNextSmartCar > 3:
                newSpeed = currentSpeed + 1
            else:
                newSpeed = currentSpeed

            if distanceToNextSmartCar >= 2:
                newSpeed = min(nextCarSpeed, currentSpeed + distanceToNextSmartCar)
            elif distanceToNextSmartCar == 1:
                newSpeed = min(2, nextCarSpeed, currentSpeed + distanceToNextSmartCar)
            else:
                newSpeed = min(1, nextCarSpeed, currentSpeed + distanceToNextSmartCar)

        else:
            #Otherwise, just accelerate since you're the last car
            if self.lane in road.target_lanes:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                else:
                    newSpeed = currentLane[self.dist] + 1
            #need to break since the lane is ending
            else:
                if currentLane[self.dist] == self.vmax:
                    newSpeed = self.vmax
                #distance here is the distance until the end of the lane
                if distanceToNextSmartCar <= self.val and distanceToNextSmartCar > 0:
                    newSpeed = distanceToNextSmartCar - 1
                elif distanceToNextSmartCar == 0:
                    newSpeed = 0
                else:
                    newSpeed = currentLane[self.dist] + 1

        if r.random() >= 0.5:
            if newSpeed >= 2:
                newSpeed = newSpeed - 1

        speedCollision = False

        if currentSpeed - newSpeed >= 2:
            speedCollision = True

        return newSpeed, speedCollision

    def _get_lane(self, lane, road):
        length = road.get_lane_size(lane)
        return [road.get_cell(lane, i) for i in range(0, length)]

    def _get_side(self, road):
        if self.lane < min(road.target_lanes):
            side = "left"
        elif self.lane > max(road.target_lanes):
            side = "right"
        else:
            side = "target"

        return side


    def _should_merge(self, road, currentLane, leftLane, rightLane):
        if self._get_side(road) == "left":
            return self._left_merge(road, currentLane, rightLane)
        elif self._get_side(road) == "right":
            return self._right_merge(road, currentLane, leftLane)
        else:
            return self._target_merge(road, currentLane, leftLane, rightLane)

    def _left_merge(self, road, currentLane, rightLane):
        laneToMerge = self.lane
        distanceToPreviousSmartCar, noPrevious = self._previous_smart_car_lane_over(rightLane)
        distanceToNextSmartCarNextLane, lastSmartCar = self._next_smart_car(rightLane)

        if noPrevious:
            laneToMerge = self.lane + 1
        else:
            speed = max(self.val, rightLane[self.dist - distanceToPreviousSmartCar])
            if distanceToPreviousSmartCar - 1 >= speed:
                laneToMerge = self.lane + 1

        return laneToMerge

    def _right_merge(self, road, currentLane, leftLane):
        laneToMerge = self.lane
        distanceToPreviousSmartCar, noPrevious = self._previous_smart_car_lane_over(leftLane)
        distanceToNextSmartCarNextLane, lastSmartCar = self._next_smart_car(leftLane)

        if noPrevious:
            laneToMerge = self.lane - 1
        else:
            speed = max(self.val, leftLane[self.dist - distanceToPreviousSmartCar])
            if distanceToPreviousSmartCar - 1 >= speed:
                laneToMerge = self.lane - 1

        return laneToMerge

    def _target_merge(self, road, currentLane, leftLane, rightLane):
        stay_in_lanes = road.target_lanes
        laneToMerge = self.lane


        if not leftLane == -1 and not rightLane == -1:
            if self.dist > len(leftLane) or self.dist > len(rightLane):
                return laneToMerge


        if self.lane == min(stay_in_lanes):
            distanceToNextSmartCar, lastSmartCar = self._next_smart_car(currentLane)

            if distanceToNextSmartCar < self.vmax:
                laneToMerge = self._left_merge(road, currentLane, rightLane)

        elif self.lane == max(stay_in_lanes):
            distanceToNextSmartCar, lastSmartCar = self._next_smart_car(currentLane)

            if distanceToNextSmartCar < self.vmax:
                laneToMerge = self._right_merge(road, currentLane, leftLane)

        else:
            distanceToNextSmartCar, lastSmartCar = self._next_smart_car(currentLane)

            if distanceToNextSmartCar < self.vmax:
                laneToMerge = self._right_merge(road, currentLane, leftLane)

        return laneToMerge
