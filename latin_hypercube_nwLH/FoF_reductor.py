# This script reads the original FoF files and compress them into a single file.
# This helps reducing the size of the files and make its reading much faster
from mpi4py import MPI
import numpy as np
import sys,os
import readfof

###### MPI DEFINITIONS ######                        
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

root = '/mnt/ceph/users/fvillaescusa/Quijote/nwLH'
################################## INPUT ##########################################
snapnums     = '0 1 2 3 4'
realizations = 2000
###################################################################################ls

# find the numbers that each cpu will work with                    
numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

# do a loop over the different realizations
for i in numbers:

    print('realization:',i)
    snapdir = '%s/%d/'%(root,i)
    os.system('FoF_reductor %s %s --no_read_ids'%(snapdir, snapnums))

    # make a consistent check
    for snapnum in snapnums.split():
        fin = '%s/groups_%03d/'%(snapdir,int(snapnum))
        file_num = len(os.listdir(fin))
        if file_num!=1:  raise Exception('%d %s %d'%(i,snapnum,file_num))

comm.Barrier()
