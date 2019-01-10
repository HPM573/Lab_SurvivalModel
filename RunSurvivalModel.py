import SurvivalModelClasses as Cls
import SimPy.SamplePathClasses as SamplePathSupport
import SimPy.FigureSupport as Fig

MORTALITY_PROB = 0.1
TIME_STEPS = 40

# create a cohort
myCohort = Cls.Cohort(id=1, pop_size=1000, mortality_prob=MORTALITY_PROB)

# simulate the cohort over the specified time steps
myCohort.simulate(TIME_STEPS)

# plot the sample path
SamplePathSupport.graph_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Time-Step (Year)',
    y_label='Number Survived')

# plot the histogram
Fig.graph_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count')

# print the patient survival time
print('Mean survival time (years):',
      myCohort.cohortOutcomes.meanSurvivalTime)
