from SurvivalModelClasses import Cohort

MORTALITY_PROB = 0.1    # annual probability of death
TIME_STEPS = 100        # years
POP_SIZE = 5000

# create a cohort
myCohort = Cohort(id=1, pop_size=POP_SIZE, mortality_prob=MORTALITY_PROB)

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=TIME_STEPS)

# print mean survival time
print('Mean survival time:', myCohort.meanSurvivalTime)

