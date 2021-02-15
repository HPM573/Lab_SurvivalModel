from SurvivalModelClasses import Patient

MORTALITY_PROB = 0.1    # annual probability of death
TIME_STEPS = 40         # years

# create a patient
myPatient = Patient(id=1, mortality_prob=MORTALITY_PROB)

# simulate the patient over the specified time steps
myPatient.simulate(n_time_steps=TIME_STEPS)

# print the patient survival time
print(myPatient.survivalTime)
