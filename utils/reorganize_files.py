# This script reorganizes the files in each simulation of the latin hypercube
from mpi4py import MPI
import numpy as np
import sys,os
import glob

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

######################################## INPUT ##########################################
root = '/simons/scratch/fvillaescusa/pdf_information/fiducial'

standard_realizations     = 15000
paired_fixed_realizations = 250

files = ['balance.txt', 'cpu.txt', 'energy.txt', 'ewald_spc_table_64.dat',
         'free_largest_*', 'free_smallest_*', 'G3.param', 'G3.param-usedvalues',
         'info.txt', 'inputspec_ics.txt', 'logfile', 'logIC', 'memory_largest_*',
         'memory_smallest_*', 'parameters-usedvalues', 'PIDs.txt',
         'processes_largest_*', 'processes_smallest_*', 'ps_file_*', 'ps_largest_*',
         'ps_smallest_*', 'Timebin.txt', 'timings.txt']
#########################################################################################

# find the numbers that each cpu will work with                  
numbers = np.where(np.arange(standard_realizations)%nprocs==myrank)[0]

# do a loop over the different realizations
for i in numbers:

    ################### ICs ####################
    # create ICs folder if it does not exists
    folder1 = '%s/%d/ICs'%(root,i)
    if not os.path.exists(folder1):  os.system('mkdir %s'%folder1)

    # move ics.* to ICs folder
    ics_files = glob.glob('%s/%d/ics.*'%(root,i))
    if len(ics_files)!=0:

        os.system('mv %s/%d/ics.* %s'%(root,i, folder1))
        os.system('mv %s/%d/2LPT.param %s'%(root,i, folder1))
    ############################################        

    ############### EXTRA FILES ################
    # create extra_files folder if it does not exists
    folder2 = '%s/%d/extra_files'%(root,i)
    if not os.path.exists(folder2):  os.system('mkdir %s'%folder2)

    # move dumb files to extra_files folder
    for f in files:
        fout = '%s/%d/%s'%(root,i,f)
        if len(glob.glob(fout))>0:
            os.system('mv %s %s'%(fout, folder2))
    ############################################

comm.Barrier()
