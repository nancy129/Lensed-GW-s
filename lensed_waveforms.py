# -*- coding: utf-8 -*-
"""Lensed waveforms

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12PTwgwsANkjs-eECSvDzcqZ-8evAcn-B
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

"""# Restart session"""

import numpy as np
from pycbc import waveform
import pylab
from lgw import *
import random
from pycbc.detector import Detector
import pylab as plt
import numpy as np
import scipy.signal

source_ra= 11.832887635111994 #hours
source_dec=3.3227025819181057 #angle(degree)
lens_ra=0.1
lens_dec=0.2
zs=6.0
zl=3.0
ml=32394331134.34737
lens_model_list=['POINT_MASS']
# can change source frame mass (mass1, mass2)
mass1=97.16603243080469
mass2=25.588296233538138
np.int = int
delta_t=1/4096

f_lower=50

optim='False'
distance=6791.8106
waveform.add_custom_waveform('lensed', lensed_gw_td, 'time', force=True)


pol = 0
inc = 0
d = Detector("H1")

hp_tilde_lensed, hc_tilde_lensed = waveform.get_td_waveform(
                approximant="lensed", source_ra=source_ra, source_dec=source_dec,
                lens_ra=lens_ra, lens_dec=lens_dec, distance=distance,
                zs=zs, zl=zl, ml=ml, lens_model_list=lens_model_list,
                mass1=mass1, mass2=mass2, delta_t=delta_t, f_lower=f_lower, optim=optim)

hp, hc = waveform.get_td_waveform(approximant="IMRPhenomD", mass1=mass1, mass2=mass2,
                         f_lower=f_lower, delta_t=delta_t, inclination=inc,
                         distance=distance)

ht2_ul = d.project_wave(hp, hc, source_ra, source_dec, pol)

ht2_l = d.project_wave(hp_tilde_lensed, hc_tilde_lensed, source_ra, source_dec, pol)


hp.start_time = hc.start_time = hc_tilde_lensed.start_time= hp_tilde_lensed.start_time =  ht2_l.start_time= ht2_ul.start_time

sample_time = ht2_l.get_delta_t()


pylab.plot( ht2_l.sample_times, ht2_l, label='lensed (h+)')
pylab.plot( ht2_ul.sample_times, ht2_ul, label='unlensed (h+)')

# Label the x-axis and y-axis
plt.xlabel('Time [s]')
plt.ylabel('h+')
plt.title('waveform')
#np.savetxt('waveform.txt', waveform)
plt.savefig('waveform1.png')
# Add a legend
pylab.legend(ncol=2, fontsize=12)
pylab.grid()

# Show the plot
pylab.show()


indices = np.where((ht2_l.sample_times >= -0.4) & (ht2_l.sample_times <= 0.4))
# Get the samples within the specified range
samples_l1 = ht2_l[indices]
samples_ul1 = ht2_ul[indices]
# Ensure that there are exactly 409 samples
#print(np.size(samples))
if len(samples_l1) & len(samples_ul1) != 409:
     samples_l = scipy.signal.resample(samples_l1, 409)
     samples_ul = scipy.signal.resample(samples_ul1, 409)
    # Print the samples
#print(samples_l)
#print(samples_ul)
# Store the values in an array
values_array_l = np.array(samples_l)
values_array_ul = np.array(samples_ul)
    # Print or use the values_array as required
#print(values_array)
np.save('values_array_l.npy',values_array_l)
np.save('values_array_ul.npy',values_array_ul)

import numpy as np
array_l = np.load('values_array_l.npy')
array_ul = np.load('values_array_ul.npy')
import matplotlib.pyplot as plt
plt.plot(array_l)
plt.show()
plt.plot(array_ul)
plt.show()
'''
print(np.size(array))
plt.plot(array, marker='o', color='blue', linestyle='None')
plt.show()
'''
#37200-37690=diff trim