# -*- coding: utf-8 -*-
"""injections_shashwat sir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WFSTUS8-EKD_8_nAq1xca60oPXDyIc7M
"""

from numpy import pi, random, savetxt, loadtxt

N = 10000
#sequence of parameters:
# mass_source_1, mass_source_2, ra, dec, polarization, M_lz, y
_min_= [10, 10, 0, 0, 0, 100000000, 1]
_max_ = [100, 100, 24, 2*pi, pi, 1000000000000, 2]

data = random.uniform(low=_min_, high=_max_, size=(N, len(_min_)))
savetxt('./injection.txt', data)