# -*- coding: utf-8 -*-
"""lensed_waveforms.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1JsCQmvcAn6xQnQMydD3ZuhzZsLAg8v0O
"""

import sys
!{sys.executable} -m pip install pycbc ligo-common emcee==2.2.1 --no-cache-dir

# Commented out IPython magic to ensure Python compatibility.
# %%shell
# git clone https://github.com/SSingh087/lensotronomy-1.7.0.git
# cd lensotronomy-1.7.0/
# python setup.py install
# cd ..
# #git clone https://github.com/SSingh087/lensGW.git
# git clone  https://github.com/Nancyjikadra/lensGW.git
# cd lensGW
# python setup.py install
# cd ..
# git clone https://github.com/SSingh087/lensGW-PyCBC-plugin.git
# cd lensGW-PyCBC-plugin
# python setup.py install
# cd ..
# git clone https://github.com/SSingh087/sensitivity-curves.git

''' RESTART SESSION '''

import numpy as np
from pycbc import waveform
import pylab
from lgw import *
import random
from pycbc.detector import Detector
import pylab as plt
import numpy as np
import scipy.signal
import zipfile
import os

import logging
#STRAIN

# Create a new folder to save the .npy files
folder_name = 'LNNdata'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

pol = 0
inc = 0
source_ra=0.1
source_dec=0.2
zs=6.0
zl=2.0
lens_model_list=['POINT_MASS']
delta_t=1/4096
f_lower=50
optim='False'
distance=6791.8106

params = []
np.int = int

# Load the parameters from the .npy file
save_file = '/content/parameters.npy'
parameters_list = np.load(save_file, allow_pickle=True)

# Loop over the parameter lists
for parameters in parameters_list:
  # Unpack the parameters
  mass1, mass2, lens_ra, lens_dec, ml = parameters

for i in range(5000):
  # Loop over all .npy files in the data folder
 for file_name in os.listdir('/content'):
  if file_name.endswith('.npy'):
     file_path = os.path.join('/content', file_name)
     data = np.load(file_path)
     waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)

     d = Detector("H1")

     hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(approximant="lensed", source_ra=source_ra,source_dec=source_dec, lens_ra=lens_ra,lens_dec=lens_dec, distance=distance, zs=zs,zl=zl, ml=ml, lens_model_list=lens_model_list,mass1=mass1, mass2=mass2, delta_t=delta_t,f_lower=f_lower, optim=optim)
     hp, hc = waveform.get_td_waveform(approximant="IMRPhenomD", mass1=mass1, mass2=mass2, f_lower=f_lower,delta_t=delta_t, inclination=inc, distance=distance)

     if hp_tilde_lensed is None or hc_tilde_lensed is None:
       print("Skipping iteration {} due to missing data".format(i + 1))
     continue

     ht2_l = d.project_wave(hp_tilde_lensed, hc_tilde_lensed, source_ra, source_dec, pol)
     ht2_l = d.project_wave(hp_tilde_lensed, hc_tilde_lensed, source_ra, source_dec, pol)
     if ht2_l is not None:
        ht2_l = ht2_l.astype(np.complex64)
     else:
     # Handle the case when ht2_l is None
         print("ht2_l is None")

     hp.start_time = hc.start_time = hc_tilde_lensed.start_time = hp_tilde_lensed.start_time = ht2_l.start_time

     sample_time = ht2_l.get_delta_t()

     indices = np.where((ht2_l.sample_times >= -0.4) & (ht2_l.sample_times <= 0.4))
     # Get the samples within the specified range
     samples_l1 = ht2_l[indices]

     # Ensure that there are exactly 409 samples
     if len(samples_l1) != 409:
        samples_l = scipy.signal.resample(samples_l1, 409)
     # Create a new sample_times array that has the same length as the resampled signal
        sample_times_l = np.linspace(samples_l1[0], samples_l1[-1], 409)
     else:
         samples_l = samples_l1
         sample_times_l = ht_l.sample_times[indices]
     # Store the values in an array
     values_array_l = np.array(samples_l)

 # Save the data as .npy files with names L1.npy, L2.npy, ..., L5000.npy and U1.npy, U2.npy, ..., U5000.npy
 #file_name_UL = os.path.join(folder_name, 'L{:03d}_{:03d}.npy'.format(i + 1, i))
 #np.save(file_name_UL, values_array_l)

     fname = 'L{:05d}'.format(i) + '.npy'
     np.save(os.path.join(folder_name, fname), values_array_l)

import google.colab
google.colab.drive.mount('/content/drive')
drive_location = '/content/drive/MyDrive/parameters.npy'
np.save(drive_location, folder_name)
#np.save(drive_location, fname)



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
save_file = '/content/parameters.npy'
parameters_list = np.load(save_file, allow_pickle=True)

# Loop over the parameter lists
for parameters in parameters_list:
  # Unpack the parameters
  mass1, mass2, source_ra, source_dec, lens_mass = parameters

import numpy as np
import matplotlib.pyplot as plt

# Load the saved parameters
parameters_list = np.load('parameters.npy')

# Sort the parameters_list array based on the first column (m1_values)
parameters_list_sorted = sorted(parameters_list, key=lambda x: x[0])

# Save the sorted parameters
np.save('parameters_sorted.npy', parameters_list_sorted)

# Extract each parameter
m1_values = [params[0] for params in parameters_list_sorted]
m2_values = [params[1] for params in parameters_list_sorted]
lensed_ra_values = [params[2] for params in parameters_list_sorted]
lensed_dec_values = [params[3] for params in parameters_list_sorted]
lens_mass_values = [params[4] for params in parameters_list_sorted]

# Plot histograms for each parameter
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
plt.hist(m1_values, bins=30, color='skyblue', edgecolor='black')
plt.title('m1')

plt.subplot(2, 3, 2)
plt.hist(m2_values, bins=30, color='salmon', edgecolor='black')
plt.title('m2')

plt.subplot(2, 3, 3)
plt.hist(lensed_ra_values, bins=30, color='lightgreen', edgecolor='black')
plt.title('lensed_ra')

plt.subplot(2, 3, 4)
plt.hist(lensed_dec_values, bins=30, color='gold', edgecolor='black')
plt.title('lensed_dec')

plt.subplot(2, 3, 5)
plt.hist(lens_mass_values, bins=30, color='orchid', edgecolor='black')
plt.title('lens_mass')

plt.tight_layout()
plt.show()

import random
import numpy as np
import os
import shutil
import scipy.signal

# Define the range of parameters
#m1,m2,lensed_ra,lensed_dec,lens mass   = 5 parameters
#source_ra=0,source_dec=0

# Set the drive location
drive_location = '/content/rawdata'


# Create the directory if it doesn't exist
if not os.path.exists(drive_location):
    os.makedirs(drive_location)

min_value = [20, 20, 0, 0, 1e9]
max_value = [100, 100, 4, np.pi/45, 1e16]


# Create a function to generate a list of 5 parameters
def generate_parameters():
  # Create an empty list to store the parameters
  parameters = []
  # Iterate over the range of parameters
  for i in range(5):
    # Generate a random value within the range
    value = random.uniform(min_value[i], max_value[i])
    # Add the value to the list of parameters
    parameters.append(value)
  # Return the list of parameters
  return parameters
# Generate 5000 lists of 5 parameters
parameters_list = []
for i in range(5000):
  parameters = generate_parameters()
  parameters_list.append(parameters)
  # Add leading zeros to the file name
  fname = '{:05d}'.format(i) + '.npy'
  np.save(os.path.join(drive_location, fname), parameters)

# Print the list of parameters
print(parameters_list)
np.save('parameters.npy', parameters_list)