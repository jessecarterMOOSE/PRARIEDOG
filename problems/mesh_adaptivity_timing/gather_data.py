import glob
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# use this bin width when making histogram instead of number of bins
bin_width = 0.05  # empirically chosen based on falcon run times

# get list of files
file_list = glob.glob('timing_file-r*')

# gather all data
times_list = []
node_times = {}
node_averages = {}
for file in file_list:
  node = file.split('-')[1]
  node_times_array = np.loadtxt(file)
  node_times[node] = node_times_array.tolist()  # put individual runs in a dict
  node_averages[node] = np.mean(node_times_array)  # put average times in a dict
  times_list.append(node_times_array.tolist())

# flatten list of lists into one
times_list = [item for sublist in times_list for item in sublist]
time_array = np.array(times_list)

# print some info
print 'number of data points:', len(times_list)
print 'total time:', '{:.3f}'.format(np.sum(time_array))
print 'min time:', '{:.3f}'.format(np.min(time_array))
print 'max time:', '{:.3f}'.format(np.max(time_array))
print 'avg time:', '{:.3f}'.format(np.mean(time_array))
print 'std dev:', '{:.3f}'.format(np.std(time_array)), '(', '{:.3f}'.format(np.std(time_array)/np.mean(time_array)*100.0), '% )'
print 'range:', '{:.3f}'.format(np.max(time_array) - np.min(time_array)), '(', '{:.3f}'.format((np.max(time_array) - np.min(time_array))/np.mean(time_array)*100.0), '% )'

# make a histogram, but use a bin width
plt.figure(figsize=(8, 6))
n, bins, patches = plt.hist(times_list, bins=np.arange(min(times_list), max(times_list), bin_width), edgecolor='k', linewidth=0.5)
plt.savefig('times-histogram.png')

# summarize data from each node
print
print 'node and average time:'
for node in sorted(node_averages, key=node_averages.get):
  print node, '{:.3f}'.format(node_averages[node])
