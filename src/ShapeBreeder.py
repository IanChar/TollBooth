""" Forms lane shapes and determines the best shape. """

from random import random

SELECT_SIZE_PROB = 0.34
SIDE_ADD_PROB = 0.25
MID_PROB = 0.25

def evolve(population, minimal_shape, mating_pool_size, offspring_number):
    # Rank the population according to some metric
    # Select what the mating pool will be.
    # Force the mating pool to mate.
    # Return the new population.
    pass

def shape_reproduction(parents, targets, cost):
    child = []

    # Find common genes in the parents.
    mom, dad = parents[0], parents[1]
    for lane_num in range(len(mom)):
        if mom[lane_num] == dad[lane_num]:
            child.append(mom[lane_num])
        else:
            child.append(0)
    print child
    return form_extra_shape(child, targets, cost)

def gen_n_rand_extra(n, size, targets, cost):
    shapes = []

    for _ in range(n):
        extra = form_extra_shape([0 for _ in range(size)], targets, cost)
        shapes.append(extra)
    return shapes

def form_extra_shape(shape, targets, cost):
    low, high = min(targets), max(targets)
    # Make the given shape valid and update remaining available cost.
    _make_extra_valid(shape, low, high)
    cost -= sum(shape)

    iteration = 0
    while iteration < range(cost) and cost > 0:
        prob = random()
        if prob >= 2 * SELECT_SIZE_PROB:
            if cost >= len(targets):
                if _maybe_add_to_mid(shape, low, high):
                    cost -= len(targets)
            else:
                prob = random()
                if prob < 0.5:
                    if _maybe_add_to_left(shape, low):
                        cost -= 1
                else:
                    if _maybe_add_to_right(shape, high):
                        cost -= 1
        elif prob < SELECT_SIZE_PROB:
            if _maybe_add_to_left(shape, low):
                cost -= 1
        else:
            if _maybe_add_to_right(shape, high):
                cost -= 1

    return shape



""" Forms the minimal shape possible given the specifications. """
def form_minimal_shape(num_lanes, targets):
    shape = [1 for _ in range(num_lanes)]
    low, high = min(targets), max(targets)

    # Iterate through until we have a correct solution
    correct = False
    while not correct:
        correct = True
        # Increase target lanes
        for lane in range(low, high + 1):
            shape[lane] += 1
        # Leftward lanes.
        for lane in range(low - 1):
            if shape[lane + 1] <= shape[lane]:
                shape[lane + 1] += 1
                correct = False
        # Rightwardd lanes.
        for lane in range(high + 1, num_lanes - 1):
            if shape[lane + 1] >= shape[lane]:
                shape[lane] += 1
                correct = False
    return shape

""" Checks if the lane shape given abides by the rules. """
def is_correct(lanes, targets):
    low, high = min(targets), max(targets)
    for lane_index in range(len(lanes) - 1):
        if lane_index < low:
            if lanes[lane_index] >= lanes[lane_index + 1]:
                return False
        elif lane_index + 1 <= high:
            if lanes[lane_index] != lanes[lane_index + 1]:
                return False
        else:
            if lanes[lane_index] <= lanes[lane_index + 1]:
                return False
    return True

def _make_extra_valid(shape, low, high):
    # Change the intiail shape so that it is valid.
    left_max, right_max = 0, 0

    # Make sure area to the left of the target is valid.
    for lane_num, lane in enumerate(shape[:low]):
        if lane < left_max:
            shape[lane_num] = left_max
        else:
            left_max = lane
    # Make sure area to the right of the target is valid.
    for lane_num in range(high + 1, len(shape))[::-1]:
        if shape[lane_num] < right_max:
            shape[lane_num] = right_max
        else:
            right_max = shape[lane_num]

    # Make sure target area is valid.
    total_max = max([left_max, right_max, max(shape[low: high + 1])])
    shape[low: high + 1] = [total_max] * (high + 1 - low)

def _maybe_add_to_left(shape, low):
    for lane_num in range(low):
        if shape[lane_num] < shape[lane_num + 1] and random() < SIDE_ADD_PROB:
            shape[lane_num] += 1
            return True
    return False

def _maybe_add_to_right(shape, high):
    for lane_num in range(high, len(shape) - 1):
        if shape[lane_num] > shape[lane_num + 1] and random() < SIDE_ADD_PROB:
            shape[lane_num + 1] += 1
            return True
    return False

def _maybe_add_to_mid(shape, low, high):
    if random() < MID_PROB:
        for lane_num in range(low, high + 1):
            shape[lane_num] += 1
        return True
    return False

if __name__ == '__main__':
    parents = gen_n_rand_extra(2, 5, [1, 2], 30)
    print parents, shape_reproduction(parents, [1, 2], 30)
