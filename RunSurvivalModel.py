import deampy.plots.histogram as Hist
import deampy.plots.sample_paths as Path

from SurvivalModelClasses import Cohort

MORTALITY_PROB = 0.1    # annual probability of death
TIME_STEPS = 100        # years
POP_SIZE = 5000

# create a cohort
myCohort = Cohort(id=1, pop_size=POP_SIZE, mortality_prob=MORTALITY_PROB)

# simulate the cohort over the specified time steps
myCohort.simulate(n_time_steps=TIME_STEPS)

# plot the sample path
Path.plot_sample_path(
    sample_path=myCohort.cohortOutcomes.nLivingPatients,
    title='Survival Curve',
    x_label='Simulation Year',
    y_label='Number Alive',
    figure_size=(4, 3.6),
    file_name='figs/survival_curve.png')

# plot the histogram
Hist.plot_histogram(
    data=myCohort.cohortOutcomes.survivalTimes,
    title='Histogram of Patient Survival Time',
    x_label='Survival Time (Year)',
    y_label='Count',
    bin_width=2,
    figure_size=(4, 3.6),
    file_name='figs/histogram.png')

# print the patient survival time
print('Mean survival time (years):',
      myCohort.cohortOutcomes.meanSurvivalTime)
