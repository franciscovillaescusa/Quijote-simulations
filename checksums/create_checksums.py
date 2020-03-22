# This script loops over all simulations in Quijote, and creates a checksum for them
# I use this mainly to make sure that files have been properly transfered 
from mpi4py import MPI
import numpy as np
import sys,os

###### MPI DEFINITIONS ###### 
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

#################################### INPUT #######################################
root = '/simons/scratch/fvillaescusa/pdf_information/Snapshots'
cosmologies = ['s8_m', 's8_p']
##################################################################################

# do a loop over the different cosmologies
for cosmo in cosmologies:

    if cosmo=='fiducial':  realizations = 15000
    else:                  realizations = 500

    # find the numbers that each cpu will work with
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

    # do a loop over all realizations
    for i in numbers:

        # consider standard and paired fixed
        for suffix in ['%d'%i, 'NCV_0_%d'%i, 'NCV_1_%d'%i]:
        
            folder = '%s/%s/%s'%(root,cosmo,suffix)
            if not(os.path.exists(folder)):
                print("%s does not exists"%folder)
            else:
                os.chdir(folder)
                os.system('find -type f \! -name SHA224SUMS -exec sha224sum \{\} \+ > SHA224SUMS')
                #os.system('find -type f -exec sha224sum \{\} \+ > SHA224SUMS')

    comm.Barrier()
