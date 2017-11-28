import pandas as pd
import subprocess
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import socket

# this little script just runs a problem over and over again to see how consistent the runtime is

# set some parameters
num_runs = 30  # how many times to run the problem
num_events = 10  # how many "events" get run each time
nx = 20  # initial mesh size
num_bins = 10  # number of bins to use in the histogram

# get the hostname so we can do multiple simultaneous runs
hostname = str(socket.gethostname())

# build command line and print to screen
cmd = ['../../PRARIEDOG-opt', '-i', '2d_sink_map_with_refinement.i', 'UserObjects/terminator/expression="num_past_events>='+str(num_events)+'"', 
       'Mesh/nx='+str(nx), 'Mesh/ny='+str(nx), 'Mesh/nz='+str(nx), 'Outputs/exodus=false', 'Outputs/execute_on=final', 'Outputs/file_base=2d_sink_map_with_refinement_out-'+hostname]
print ' '.join(cmd)
print

# store times
times_list = []

# write times to file too
with open('timing_file-'+hostname, 'w') as times_file:
  for i in range(0, num_runs):
    print 'run', i+1, 'of', num_runs, '...'
    subprocess.check_output(cmd)
    df = pd.read_csv('2d_sink_map_with_refinement_out-'+hostname+'.csv')
    total_time = df['total_time'].iloc[-1]
    print total_time
    times_list.append(total_time)
    times_file.write(str(total_time)+'\n')
    times_file.flush()

# print some summary values
time_array = np.array(times_list)
print
print 'total time:', '{:.3f}'.format(np.sum(time_array))
print 'min time:', '{:.3f}'.format(np.min(time_array))
print 'max time:', '{:.3f}'.format(np.max(time_array))
print 'avg time:', '{:.3f}'.format(np.mean(time_array))
print 'std dev:', '{:.3f}'.format(np.std(time_array)), '(', '{:.3f}'.format(np.std(time_array)/np.mean(time_array)*100.0), '% )'
print 'range:', '{:.3f}'.format(np.max(time_array) - np.min(time_array)), '(', '{:.3f}'.format((np.max(time_array) - np.min(time_array))/np.mean(time_array)*100.0), '% )'


quit()

# below here isn't quite ready yet

# fit data to gaussian
mu, sigma = stats.norm.fit(times_list)

# fit data to log-normal
shape, loc, scale = stats.lognorm.fit(times_list)

# plot historgram and collect stats
n, bins, patches = plt.hist(times_list, num_bins)

# plot fitted gaussian, normalized to max histogram count
x_gauss = np.linspace(mu-3.0*sigma, mu+3.0*sigma, 100)
y_gauss = stats.norm.pdf(x_gauss, mu, sigma)
plt.plot(x_gauss, y_gauss/max(y_gauss)*max(n))

# plot fitted log-normal
x_lognorm = np.linspace(min(bins), max(bins), 100)
y_lognorm = stats.lognorm.pdf(x_lognorm, shape, loc, scale)
plt.plot(x_lognorm, y_lognorm/max(y_lognorm)*max(n))

# save figure
plt.savefig('times-histogram.png')
