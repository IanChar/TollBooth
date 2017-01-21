""" Forms lane shapes and determines the best shape. """

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

if __name__ == '__main__':
    tst = form_minimal_shape(16, [5, 6, 7, 8])
    print tst, is_correct(tst, [5, 6, 7, 8])
