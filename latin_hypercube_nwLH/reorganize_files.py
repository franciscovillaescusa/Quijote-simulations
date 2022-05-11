# This script reorganizes the files in each simulation of the latin hypercube
from mpi4py import MPI
import numpy as np
import sys,os
import glob

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

###################################### INPUT ##########################################
root = '/mnt/ceph/users/fvillaescusa/Quijote/nwLH'

standard_realizations = 2000

files = ['balance.txt', 'cpu.txt', 'energy.txt', 'ewald_spc_table_64.dat',
         'free_largest_*', 'free_smallest_*', 'G3.param', 'G3.param-usedvalues',
         'info.txt', 'inputspec_ics.txt', 'logfile', 'logIC', 'memory_largest_*',
         'memory_smallest_*', 'parameters-usedvalues', 'PIDs.txt',
         'processes_largest_*', 'processes_smallest_*', 'ps_file_*', 'ps_largest_*',
         'ps_smallest_*', 'Timebin.txt', 'timings.txt', 'script.sh*', 'slurm*',
         'darkenergy.txt','driftkickfac.txt']
#######################################################################################


# do a loop over the different standard realizations
numbers = np.where(np.arange(standard_realizations)%nprocs==myrank)[0]
for i in numbers:

    ################ PERMISSIONS ###############
    os.system('chmod -R ugo-w %s/%d/snapdir_*'%(root,i))
    ############################################

    ################### ICs ####################
    # create ICs folder if it does not exists
    folder1 = '%s/%d/ICs'%(root,i)
    if not(os.path.exists(folder1)):  os.system('mkdir %s'%folder1)

    # move ics.* to ICs folder
    ics_files = glob.glob('%s/%d/ics.*'%(root,i))
    if len(ics_files)!=0:
        os.system('mv  %s/%d/ics.* %s'%(root,i, folder1))
    if os.path.exists('%s/%d/2LPT.param'%(root,i)):
        os.system('mv  %s/%d/2LPT.param %s'%(root,i, folder1))
    ############################################        

    ############### EXTRA FILES ################
    # create extra_files folder if it does not exists
    folder2 = '%s/%d/extra_files'%(root,i)
    if not(os.path.exists(folder2)):  os.system('mkdir %s'%folder2)

    # move dumb files to extra_files folder
    for f in files:
        fout = '%s/%d/%s'%(root,i,f)
        if len(glob.glob(fout))>0:
            os.system('mv %s %s'%(fout, folder2))
    ############################################

    ############## DELETE FILES ################
    Pk_files =              glob.glob('%s/%d/Pk_m_*.txt'%(root,i))
    if len(Pk_files)>0:  os.system('rm %s/%d/Pk_m_*.txt'%(root,i))

    FoF_files =                  glob.glob('%s/%d/original_groups_*'%(root,i))
    if len(FoF_files)>0:  os.system('rm -rf %s/%d/original_groups_*'%(root,i))
    ############################################
comm.Barrier()


