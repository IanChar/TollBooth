""" Class representing TollBooth via Markov Chain. """

class TollBooth(object):
    def __init__(self, rate_in, rate_out):
        self.rate_in = rate_in
        self.rate_out = rate_out

    def tick(self):
        # TODO: Implement logic to see if we should emmit a car.
        return False
