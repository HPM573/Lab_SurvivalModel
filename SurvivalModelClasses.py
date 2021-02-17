from enum import Enum
import numpy as np
import SimPy.SamplePath as PathCls


class HealthStat(Enum):
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
        self.healthState = HealthStat.ALIVE  # assuming all patients are alive at the beginning
        self.survivalTime = None  # won't be observed unless the patient dies

    def simulate(self, n_time_steps):
        """ simulate the patient over the specified simulation length """

        # random number generator
        rng = np.random.RandomState(seed=self.id)

        t = 0  # current time step

        # while the patient is alive and simulation length is not yet reached
        while self.healthState == HealthStat.ALIVE and t < n_time_steps:
            # determine if the patient will die during this time-step
            if rng.random_sample() < self.mortalityProb:
                # update the health state to death
                self.healthState = HealthStat.DEAD
                # record the survival time (assuming deaths occurs at the end of this period)
                self.survivalTime = t + 1

            # increment time
            t += 1


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
        self.patients = []  # list of patients
        self.cohortOutcomes = CohortOutcomes()  # outcomes of the this simulated cohort

    def simulate(self, n_time_steps):
        """ simulate the cohort of patients over the specified number of time-steps
        :param n_time_steps: number of time steps to simulate the cohort
        """

        # populate the cohort
        for i in range(self.popSize):
            # create a new patient (use id * pop_size + n as patient id)
            patient = Patient(id=self.id * self.popSize + i, mortality_prob=self.mortalityProb)
            # add the patient to the cohort
            self.patients.append(patient)

        # simulate all patients
        for patient in self.patients:
            # simulate
            patient.simulate(n_time_steps)

        # store outputs of this simulation
        self.cohortOutcomes.extract_outcomes(self.patients)

        # clear the patients
        self.patients.clear()


class CohortOutcomes:
    def __init__(self):

        self.survivalTimes = []    # survival times
        self.meanSurvivalTime = None   # mean survival time
        self.nLivingPatients = None   # survival curve (sample path of number of alive patients over time)

    def extract_outcomes(self, simulated_patients):
        """ extracts outcomes of a simulated cohort
        :param simulated_patients: (list) of patients after being simulated """

        # record survival times
        for patient in simulated_patients:
            if patient.survivalTime is not None:
                self.survivalTimes.append(patient.survivalTime)

        # calculate mean survival time
        self.meanSurvivalTime = sum(self.survivalTimes)/len(self.survivalTimes)

        # survival curve
        self.nLivingPatients = PathCls.PrevalencePathBatchUpdate(
            name='# of living patients',
            initial_size=len(simulated_patients),
            times_of_changes=self.survivalTimes,
            increments=[-1]*len(self.survivalTimes)
        )
