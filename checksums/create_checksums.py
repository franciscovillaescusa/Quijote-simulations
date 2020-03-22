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
cosmologies = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p', 'w_p', 'DC_p' 
               'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m', 'w_m', 'DC_m',
               'Mnu_p', 'Mnu_pp', 'Mnu_ppp']
##################################################################################

# do a loop over the different cosmologies
for cosmo in cosmologies:

    if myrank==0:  print(cosmo)

    # find the number of standard and paired fixed sims
    if cosmo=='fiducial':  std, pf = 15000, 250
    elif cosmo=='Ob_p':    std, pd = 0,     250
    elif cosmo=='Ob_m':    std, pf = 0,     250
    elif cosmo=='w_p':     std, pf = 500,   0
    elif cosmo=='w_m':     std, pf = 500,   0
    elif cosmo=='DC_p':    std, pf = 500,   0
    elif cosmo=='DC_m':    std, pf = 500,   0
    else:                  std, pf = 500,   250

    # find the numbers that each cpu will work with
    realizations = max(std, pf)
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

    # do a loop over all realizations
    for i in numbers:

        # consider standard and paired fixed
        for suffix in ['%d'%i, 'NCV_0_%d'%i, 'NCV_1_%d'%i]:
        
            if suffix=='%d'%i       and i>=std:  continue
            if suffix=='NCV_0_%d'%i and i>=pf:   continue
            if suffix=='NCV_1_%d'%i and i>=pf:   continue

            # check if output file exists
            fout = '%s/%s/%s/SHA224SUMS'%(root,cosmo,suffix)
            if os.path.exists(fout):  continue
            
            folder = '%s/%s/%s'%(root,cosmo,suffix)
            if not(os.path.exists(folder)):
                print("%s does not exists"%folder)
            else:
                os.chdir(folder)
                os.system('find -type f \! -name SHA224SUMS -exec sha224sum \{\} \+ > SHA224SUMS')
                #os.system('find -type f -exec sha224sum \{\} \+ > SHA224SUMS')

    comm.Barrier()
