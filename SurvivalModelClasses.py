from enum import Enum

import numpy as np

from deampy.sample_path import PrevalencePathBatchUpdate


class HealthState(Enum):
    """ health status of patients  """
    ALIVE = 1
    DEAD = 0


class Patient:
    def __init__(self, id, mortality_prob):
        """ initiates a patient
        :param id: ID of the patient
        :param mortality_prob: probability of death during a time-step (must be in [0,1])
        """
        self.id = id
        self.mortalityProb = mortality_prob
        self.healthState = HealthState.ALIVE  # assuming all patients are alive at the beginning
        self.survivalTime = None  # won't be observed unless the patient dies

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = np.random.RandomState(seed=self.id)

        k = 1  # current simulation year

        # while the patient is alive and simulation length is not yet reached
        while self.healthState == HealthState.ALIVE and k < n_time_steps:
            # determine if the patient will die during this time-step
            if rng.random_sample() < self.mortalityProb:
                # update the health state to death
                self.healthState = HealthState.DEAD
                # record the survival time (assuming deaths occurs at the end of this period)
                self.survivalTime = k

            # increment time
            k += 1


class Cohort:
    def __init__(self, id, pop_size, mortality_prob):
        """ create a cohort of patients
        :param id: cohort ID
        :param pop_size: population size of this cohort
        :param mortality_prob: probability of death for each patient in this cohort over a time-step (must be in [0,1])
        """
        self.id = id
        self.popSize = pop_size  # initial population size
        self.mortalityProb = mortality_prob
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """

        # populate and simulate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i, mortality_prob=self.mortalityProb)

            # simulate
            patient.simulate(n_time_steps)

            # store outputs of this simulation
            self.cohortOutcomes.extract_outcome(patient)

        # calculate cohort outcomes
        self.cohortOutcomes.calculate_cohort_outcomes(initial_pop_size=self.popSize)


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []    # survival times
        self.meanSurvivalTime = None   # mean survival time
        self.nLivingPatients = None   # survival curve (sample path of number of alive patients over time)

    def extract_outcome(self, simulated_patient):
        """ extracts outcomes of a simulated patient
        :param simulated_patient: a patient after being simulated """

        # record survival times
        if simulated_patient.survivalTime is not None:
            self.survivalTimes.append(simulated_patient.survivalTime)

    def calculate_cohort_outcomes(self, initial_pop_size):
        """ calculates the cohort outcomes
        :param initial_pop_size: initial population size
        """

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes)/len(self.survivalTimes)

        # survival curve
        self.nLivingPatients = PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=initial_pop_size,
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
