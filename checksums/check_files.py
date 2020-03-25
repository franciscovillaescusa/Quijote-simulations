# We use this script to verify the integrity of the transfer
#import h5py
from mpi4py import MPI
import numpy as np
import sys,os

###### MPI DEFINITIONS ###### 
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

################################## INPUT #######################################
root = '/projects/QUIJOTE/Snapshots'

cosmologies = ['Om_p', 'Om_p']
################################################################################

# do a loop over the different cosmologies
for cosmo in cosmologies:

    # find the number of standard and paired fixed sims
    if cosmo=='fiducial':  std, pf = 15000, 250
    elif cosmo=='Ob_p':    std, pd = 0,     250
    elif cosmo=='Ob_m':    std, pf = 0,     250
    elif cosmo=='w_p':     std, pf = 500,   0
    elif cosmo=='w_m':     std, pf = 500,   0
    elif cosmo=='DC_p':    std, pf = 500,   0
    elif cosmo=='DC_m':    std, pf = 500,   0
    else:                  std, pf = 500,   250    
    realizations = max(std,pf)

    # find the numbers that each cpu will work with
    realizations = max(std, pf)
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

    # do a loop over all realizations
    count = 0
    for i in numbers:

        # consider standard and paired fixed
        for suffix in ['%d'%i, 'NCV_0_%d'%i, 'NCV_1_%d'%i]:
        
            if suffix=='%d'%i       and i>=std:  continue
            if suffix=='NCV_0_%d'%i and i>=pf:   continue
            if suffix=='NCV_1_%d'%i and i>=pf:   continue

            # check if output file exists
            fout = '%s/%s/%s/SHA224SUMS'%(root,cosmo,suffix)
            if not(os.path.exists(fout)):  raise Exception('%s doesnt exists'%fout)

            folder = '%s/%s/%s'%(root,cosmo,suffix)
            os.chdir('%s'%folder)
            os.system('sha224sum -c SHA224SUMS --quiet')
            count += 1
    count_partial = np.array(count, dtype=np.int64)
    count_total   = np.array(0,     dtype=np.int64)
    
    comm.Reduce(count_partial, count_total, root=0)
    if myrank==0:  print((count_total,cosmo))
