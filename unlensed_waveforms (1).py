# -*- coding: utf-8 -*-
"""Unlensed waveforms

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1viq9Hbi_zObC3msfZvKgeYse-WawP3v8
"""

import sys
!{sys.executable} -m pip install pycbc ligo-common emcee==2.2.1 --no-cache-dir

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# git clone https://github.com/SSingh087/lensotronomy-1.7.0.git
# cd lensotronomy-1.7.0/
# python setup.py install
# cd ..
# git clone https://github.com/SSingh087/lensGW.git
# cd lensGW
# python setup.py install
# cd ..
# git clone https://github.com/SSingh087/lensGW-PyCBC-plugin.git
# cd lensGW-PyCBC-plugin
# python setup.py install
# cd ..
# git clone https://github.com/SSingh087/sensitivity-curves.git

import numpy as np
from pycbc import waveform
import pylab
import random
from pycbc.detector import Detector
import pylab as plt
import numpy as np
import scipy.signal
import zipfile
import os

delta_t=1/4096
f_lower=50
optim='False'
distance=6791.8106
pol = 0

params = []
np.int = int

# Load the parameters from the .npy file
save_file = '/content/parameters .npy'
parameters_list = np.load(save_file, allow_pickle=True)

# Loop over the parameter lists
for parameters in parameters_list:
  # Unpack the parameters
  mass1, mass2, source_ra, source_dec, lens_mass = parameters

#STRAIN

#file save
# Create a new folder to save the .npy files

for i in range(5000):
  # Loop over all .npy files in the data folder
 for file_name in os.listdir('/content'):
  if file_name.endswith('.npy'):
     file_path = os.path.join('/content', file_name)
     data = np.load(file_path)

     d = Detector("H1")
     hp, hc = waveform.get_td_waveform(approximant='TaylorF2', mass1=mass1, mass2=mass2, delta_t=delta_t, f_lower=f_lower)
     ht_ul = d.project_wave(hp, hc, source_ra, source_dec, pol)
     hp.start_time = hc.start_time = ht_ul.start_time

     sample_time = ht_ul.get_delta_t()
     # TRIMMING
     indices = np.where((ht_ul.sample_times >= -0.4) & (ht_ul.sample_times <= 0.4))
     # Get the samples within the specified range
     samples_ul1 = ht_ul[indices]
     if len(samples_ul1) != 409:
            samples_ul = scipy.signal.resample(samples_ul1, 409)
                # Create a new sample_times array that has the same length as the resampled signal
            sample_times_ul = np.linspace(samples_ul1[0], samples_ul1[-1], 409)
     else:
            samples_ul = samples_ul1
            sample_times_ul = ht_ul.sample_times[indices]

     values_array_ul = np.array(samples_ul)
     np.save('values_array_ul.npy',values_array_ul)
     array_ul = np.load('values_array_ul.npy')

     file_name_UL = os.path.join(folder_name, 'UL{:03d}.npy'.format(i + 1))
     np.save(file_name_UL, values_array_ul)
#plt.plot(array_ul)
#plt.show()
x = len(array_ul)
print(x)

'''import numpy as np
from pycbc import waveform
import pylab
import random
from pycbc.detector import Detector
import pylab as plt
import numpy as np
import scipy.signal
import zipfile
import os


# Create a new folder to save the .npy files
folder_name = 'UNLdata'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
folder_name ='/content/' + folder_name

delta_t=1/4096
f_lower=50
optim='False'
distance=6791.8106


params = []
np.int = int

# Open the zip file
with zipfile.ZipFile('/content/rawdata_1028.zip', 'r') as zip_ref:
    # Extract all files from the zip folder
    zip_ref.extractall('/content')

for i in range(5000):
  # Loop over all .npy files in the data folder
 for file_name in os.listdir('/content'):
  if file_name.endswith('.npy'):
      file_path = os.path.join('/content', file_name)
      data = np.load(file_path)

      mass1 = data[0]
      mass2 = data[1]
      source_ra = data[2]
      source_dec = data[3]
      pol = 0

'''# Generate the waveform
  hp, hc = waveform.get_fd_waveform(approximant='TaylorF2',mass1=mass1, mass2=mass2, f_lower=f_lower, distance=distance, optim=optim)

  # Generate the time array
  t = np.arange(0, len(hp), 1) * delta_t

  # Save the waveform to a .npy file
  save_file = os.path.join(folder_name, f'waveform_{mass1}_{mass2}_{source_ra}_{source_dec}_{lens_mass}.npy')
  np.save(save_file, hp)

  # Save the time array to a .npy file
  save_file = os.path.join(folder_name, f'time_{mass1}_{mass2}_{source_ra}_{source_dec}_{lens_mass}.npy')
  np.save(save_file, t)

  # Print the progress
  print(f"Generated waveform for parameters: {parameters}")

''' import numpy as np
from pycbc import waveform
import pylab
import random
from pycbc.detector import Detector
import pylab as plt
import numpy as np
import scipy.signal
import zipfile
import os


# Create a new folder to save the .npy files
folder_name = 'UNLdata'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
folder_name ='/content/' + folder_name

delta_t=1/4096
f_lower=50
optim='False'
distance=6791.8106
params = []
np.int = int
# Open the zip file
with zipfile.ZipFile('/content/rawdata_1028.zip', 'r') as zip_ref:
    # Extract all files from the zip folder
    zip_ref.extractall('/content')

for i in range(5000):
  # Loop over all .npy files in the data folder
 for file_name in os.listdir('/content'):
  if file_name.endswith('.npy'):
      file_path = os.path.join('/content', file_name)
      data = np.load(file_path)

      mass1 = data[0]
      mass2 = data[1]
      source_ra = data[2]
      source_dec = data[3]
      pol = 0
      waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)

      d = Detector("H1")
      hp, hc = waveform.get_td_waveform(approximant='TaylorF2', mass1=mass1, mass2=mass2, delta_t=delta_t, f_lower=f_lower)
      ht_ul = d.project_wave(hp, hc, source_ra, source_dec, pol)
      hp.start_time = hc.start_time = ht_ul.start_time

      sample_time = ht_ul.get_delta_t()

      indices = np.where((ht_ul.sample_times >= -0.4) & (ht_ul.sample_times <= 0.4))
        # Get the samples within the specified range
      samples_ul1 = ht_ul[indices]

      # Ensure that there are exactly 409 samples
      #print(np.size(samples))
      if len(samples_ul1) != 409:
       samples_ul = scipy.signal.resample(samples_ul1, 409)
       #Print the samples
       #print(samples_l)
       #print(samples_ul)
       #Store the values in an array
      values_array_ul = np.array(samples_ul)


       # Save the data as .npy files with names L1.npy, L2.npy, ..., L5000.npy and U1.npy, U2.npy, ..., U5000.npy

      file_name_UL = os.path.join(folder_name, 'UL{:03d}.npy'.format(i+1))
      np.save(file_name_UL, values_array_ul)   "''