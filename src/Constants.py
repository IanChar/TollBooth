# Enums for simplicity
SLOW = 0
MED = 1
FAST = 2

# Probabilities calculated for a given booth.
SLOW_BOOTH = 0.098774
MED_BOOTH = 0.130398
FAST_BOOTH = 0.377742

BOOTHS = [SLOW_BOOTH, MED_BOOTH, FAST_BOOTH]

# Rates for incoming cars at different traffic times.
FAST_LAMBDA = 1.41
MED_LAMBDA = 0.84
SLOW_LAMBDA = 0.28

TRAFFIC = [SLOW_LAMBDA, MED_LAMBDA, FAST_LAMBDA]
