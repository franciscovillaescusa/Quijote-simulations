# This script looks for empty files
from mpi4py import MPI
import numpy as np
import sys,os
import glob

###### MPI DEFINITIONS ######
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

####################################### INPUT ###########################################
root = '/simons/scratch/fvillaescusa/pdf_information/Bk/matter'
cosmologies = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
               'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
               'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial',
               'latin_hypercube']
#########################################################################################

# do a loop over the different cosmologies
for cosmo in cosmologies:
    
    # find the number of standard and paired fixed realizations
    if   cosmo=='fiducial':         real_std, real_NCV = 15000, 250
    elif cosmo=='latin_hypercube':  real_std, real_NCV = 2000, 2000
    else:                           real_std, real_NCV = 500,   250

    # do a loop over the standard realizations
    count, count_p = np.array([0]), np.array([0])
    numbers = np.where(np.arange(real_std)%nprocs==myrank)[0]
    for i in numbers:
        folder = '%s/%s/%d'%(root,cosmo,i)
        files = glob.glob(folder+'/*')
        for f in files:
            if os.stat(f).st_size==0:
                #os.system('rm %s'%f)
                raise Exception('%s seems empty'%f)
            count_p[0] += 1

    # do a loop over paired fixed realizations
    numbers = np.where(np.arange(real_NCV)%nprocs==myrank)[0]
    for i in numbers:
        for pair in [0,1]:
            folder = '%s/%s/NCV_%d_%d'%(root,cosmo,pair,i)
            files = glob.glob(folder+'/*')
            for f in files:
                if os.stat(f).st_size==0:  
                    #os.system('rm %s'%f)
                    raise Exception('%s seems empty'%f)
                count_p[0] += 1

    comm.Reduce(count_p, count, root=0)
    if myrank==0:
        print 'Found %d no-empty files in the %s cosmology'%(count[0],cosmo)

        
