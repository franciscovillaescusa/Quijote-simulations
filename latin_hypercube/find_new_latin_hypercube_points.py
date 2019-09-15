import numpy as np
import sys,os


#################################### INPUT ##############################################
fin = 'latin_hypercube_params.txt'
Mmin = np.array([0.1, 0.03, 0.5, 0.8, 0.6])
Mmax = np.array([0.5, 0.07, 0.9, 1.2, 1.0])
#########################################################################################

# read the value of the cosmological parameters
pos_lh = np.loadtxt(fin)
pos_lh = np.vstack((pos_lh, [0.49679489, 0.05469354, 0.89481701, 1.19727631, 0.62104751]))


# generate new points
dmax = 0.0
for i in xrange(10000000):
    pos = Mmin + np.random.random(5)*(Mmax-Mmin)
    d = np.sum((pos-pos_lh)**2, axis=1)
    dmin = np.min(d)
    if dmin>dmax:
        index = np.where(d==dmin)[0]
        print i,dmin
        print pos
        print pos_lh[index][0]
        dmax = dmin
    
