# this script runs several simulations and loops over a range of timesteps to see the convergence
# should be linear since the input file is doing implicit euler

import numpy as np
import matplotlib.pyplot as plt
import os
from subprocess import call

# set some values
end_time = 1.0
sigma = 0.02
D = 0.001
dt_list = np.array([0.1, 0.05, 0.02, 0.01, 0.005, 0.002])

# exact value
target_value = 1.0/np.sqrt(2*np.pi)/np.sqrt(2*D*(end_time + sigma*sigma/2/D))

# open /dev/null for writing
FNULL = open(os.devnull, 'w')

# initialize some things
i = 0
values = np.empty([dt_list.size,1])
errors = np.empty([dt_list.size,1])

# loop over time steps
for dt in dt_list:
  print "running simulation with dt = " + str(dt)

  # run simulation
  call([
    "../../../PRARIEDOG-opt",
    "-i",
    "1d_gaussian_diffusion.i",
    "Executioner/end_time="+str(end_time),
    "Executioner/dt="+str(dt),
    "Functions/gaussian/vals="+str(sigma),
    "Materials/simple/prop_values="+str(D)
  ], stdout=FNULL)

  # get postprocessor output
  for file in os.listdir("."):
    if file.endswith(".csv"):
      csvfile=file

  data = np.loadtxt(csvfile, delimiter=',', skiprows=1)

  # get final value and calculate error
  values[i] = data[1,1]
  errors[i] = np.abs(values[i] - target_value)/target_value

  i = i + 1


# plot errors on log-log plot
plt.loglog(dt_list, errors, '-o')
plt.xlabel('dt')
plt.ylabel('error')
plt.show()