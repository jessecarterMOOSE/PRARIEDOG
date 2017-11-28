import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# this time (in seconds) separates "fast" from "slow" times
fast_time = 30

# get list of files
file_list = glob.glob('timing_file-r*')

# gather all data
times_list = []
fast_node_list = []
slow_node_list = []
for file in file_list:
  node = file.split('-')[1]
  node_times_array = np.loadtxt(file)
  if np.mean(node_times_array) > fast_time:
    slow_node_list.append(node)
  else:
    fast_node_list.append(node)
  times_list.append(node_times_array.tolist())

# flatten list of lists into one
times_list = [item for sublist in times_list for item in sublist]

# print some info
print 'number:', len(times_list)
time_array = np.array(times_list)
print 'total time:', '{:.3f}'.format(np.sum(time_array))
print 'min time:', '{:.3f}'.format(np.min(time_array))
print 'max time:', '{:.3f}'.format(np.max(time_array))
print 'avg time:', '{:.3f}'.format(np.mean(time_array))
print 'std dev:', '{:.3f}'.format(np.std(time_array)), '(', '{:.3f}'.format(np.std(time_array)/np.mean(time_array)*100.0), '% )'
print 'range:', '{:.3f}'.format(np.max(time_array) - np.min(time_array)), '(', '{:.3f}'.format((np.max(time_array) - np.min(time_array))/np.mean(time_array)*100.0), '% )'

# report "fast" and "slow" nodes
print
print '"fast" nodes:'
for host in fast_node_list:
  print host
print
print '"slow" nodes:'
for host in slow_node_list:
  print host
print

# make a histogram
for i in [10*i for i in range(1,11)]:
  print 'making histogram using', i, 'bins'
  n, bins, patches = plt.hist(times_list, i)
  plt.savefig('times-histogram-'+str(i)+'.png')
  plt.cla()

print 'making histogram using manual bins'
bins = np.linspace(26,27,21).tolist() + np.linspace(32,33,21).tolist()
n, bins, patches = plt.hist(times_list, bins=bins)
plt.savefig('times-histogram-manual-bins.png')
