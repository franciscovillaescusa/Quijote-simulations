import numpy as np
import sys,os


f_params = 'latin_hypercube_params.txt'

Om, Ob, h, ns, s8 = np.loadtxt(f_params, unpack=True)

print '%.3f < Om < %.3f'%(np.min(Om), np.max(Om))
print '%.3f < Ob < %.3f'%(np.min(Ob), np.max(Ob))
print '%.3f < h  < %.3f'%(np.min(h),  np.max(h))
print '%.3f < ns < %.3f'%(np.min(ns), np.max(ns))
print '%.3f < s8 < %.3f'%(np.min(s8), np.max(s8))

dist = np.sqrt((Om-0.3175)**2 +\
               (Ob-0.049)**2 +\
               (h-0.6711)**2 +\
               (ns-0.9624)**2 +\
               (s8-0.834)**2)

print np.min(dist)
index = np.where(dist==np.min(dist))[0]
print index
print Om[index], Ob[index], h[index], ns[index], s8[index]

for index in [95,99,107,125,2]:
    print Om[index], Ob[index], h[index], ns[index], s8[index]
