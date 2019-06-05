# This script moves halo catalogues from their original folders to the Halos folder
import numpy as np
import sys,os


###################################### INPUT ############################################
root         = '/simons/scratch/fvillaescusa/latin_hypercube/Snapshots'
root_results = '/simons/scratch/fvillaescusa/latin_hypercube/Halos'
realizations = 2000
#########################################################################################

# do a loop over the different realizations
for i in xrange(realizations):

    # create output folder if it does not exists
    folder = '%s/%d'%(root_results, i)
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    # do a loop over the different redshifts
    for snapnum in [0,1,2,3,4]:

        fin = '%s/%d/groups_%03d'%(root, i, snapnum)
        if os.path.exists(fin):  os.system('mv %s %s'%(fin, folder))
