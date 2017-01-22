""" Forms lane shapes and determines the best shape. """

from collections import deque
from random import random, shuffle

from RoadSimulator2018 import RoadSimulator2018 as RoadSimulator

SELECT_SIZE_PROB = 0.34
SIDE_ADD_PROB = 0.25
MID_PROB = 0.25
SIMULATIONS = 60
PERCENT_AUTOMATED = 0

RD = RoadSimulator()

def form_one_step_shape(num_lanes, targets):
    shape = [1 for _ in range(num_lanes)]
    low, high = min(targets), max(targets)

    # Iterate through until we have a correct solution
    left_point, right_point = low, high + 1
    running = True
    while running:
        for index in range(left_point, right_point):
            shape[index] += 1
        if left_point > 0:
            left_point -= 1
        if right_point < num_lanes:
            right_point += 1
        running = left_point > 0 or right_point < num_lanes

    return shape

def breed_best_shape(num_lanes, targets, cost, iterations, population_size,
                     mating_pool_size, offspring_number):
    minimal_shape = form_minimal_shape(num_lanes, targets)
    cost -= sum(minimal_shape)
    population = gen_n_rand_extra(population_size, num_lanes, targets, cost)

    for _ in range(iterations):
        shuffle(population)
        population = evolve(population, targets, cost, minimal_shape,
                            mating_pool_size, offspring_number)

""" --------------------------HELPER FUNCTIONS--------------------"""

def objective_function(throughput, accident_merge, accident_speed):
    return 100 - (accident_merge + accident_speed) / float(throughput)

def evolve(population, targets, cost, minimal_shape, mating_pool_size,
           offspring_number):
    # Rank the population according to some metric
    scores = []
    for shape in population:
        scores.append(get_score(shape, targets, minimal_shape))
    # Print information about this iteration.
    max_score = max(scores)
    best_shape = list(population[scores.index(max_score)])
    for index in range(len(best_shape)):
        best_shape[index] += minimal_shape[index]
    print 'Average Score:', str(sum(scores) / float(len(scores))),
    print 'Max Score:', max_score,
    print 'Best Score:', best_shape
    # Select what the mating pool will be.
    mating_pool = make_mating_pool(population, scores, mating_pool_size)
    # Force the mating pool to mate.
    return make_offspring(mating_pool, offspring_number, targets, cost)

def get_score(shape, targets, minimal_shape):
    true_shape = list(minimal_shape)
    for lane_index in range(len(shape)):
        true_shape[lane_index] += shape[lane_index]
    throughputs, accidents_merge, accidents_speed = \
        RD.runSim(true_shape, targets, PERCENT_AUTOMATED, False, SIMULATIONS)
    return objective_function(throughputs[-1], accidents_merge[-1],
            accidents_speed[-1])

def make_mating_pool(population, scores, mating_pool_size):
    mating_pool = deque()
    section_boundaries = range(0, len(population), mating_pool_size)
    for index in range(len(section_boundaries) - 1):
        max_score = 0
        max_id = 0
        for score_id in range(section_boundaries[index],
                            section_boundaries[index + 1]):
            if max_score < scores[score_id]:
                max_score = scores[score_id]
                max_id = score_id
            mating_pool.append(population[max_id])
    return mating_pool

def make_offspring(mating_pool, offspring_number, targets, cost):
    new_population = []
    while len(mating_pool) > 1:
        mom, dad = mating_pool.pop(), mating_pool.pop()
        new_population.append(mom)
        new_population.append(dad)
        for _ in range(offspring_number):
            new_population.append(shape_reproduction([mom, dad], targets, cost))
    if len(mating_pool) == 1:
        new_population.append(mating_pool[0])
    return new_population

def shape_reproduction(parents, targets, cost):
    child = []

    # Find common genes in the parents.
    mom, dad = parents[0], parents[1]
    for lane_num in range(len(mom)):
        if mom[lane_num] == dad[lane_num]:
            child.append(mom[lane_num])
        else:
            child.append(0)
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
    breed_best_shape(6, [1, 2], 30, 3, 10, 5, 1)
