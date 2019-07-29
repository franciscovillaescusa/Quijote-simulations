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

root = '/home/fvillaescusa/data/pdf_information/'
################################## INPUT ##########################################
snapnums = '0 1 2 3 4'

folders = ['fiducial_ZA']
#['Om_p', 'Ob_p', 'h_p', 'ns_p', 's8_p', 'Mnu_p', 'Mnu_pp', 'Mnu_ppp',
#'Om_m', 'Ob_m', 'h_m', 'ns_m', 's8_m', 'fiducial', 'latin_hypercube']
###################################################################################ls

# do a loop over the different cosmologies
for folder in folders:
    if   folder=='fiducial':         realizations, pairs = 15000, False
    elif folder=='latin_hypercube':  realizations, pairs = 2000,  True
    elif folder=='fiducial_ZA':      realizations, pairs = 100,   False
    else:                            realizations, pairs = 500,   False

    # find the numbers that each cpu will work with                    
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

    # do a loop over the different realizations
    for i in numbers:

        if pairs:
            for pair in [0,1]:
                snapdir = '%s/%s/NCV_%d_%d/'%(root,folder,pair,i)
                os.system('FoF_reductor %s %s --no_read_ids'%(snapdir, snapnums))

                # make a consistent check
                for snapnum in snapnums.split():
                    fin = '%s/groups_%03d/'%(snapdir,int(snapnum))
                    file_num = len(os.listdir(fin))
                    if file_num!=1:  
                        raise Exception ('%s %d %d %d'%(folder,i,snapnum,file_num))

        else:
            snapdir = '%s/%s/%d/'%(root,folder,i)
            os.system('FoF_reductor %s %s --no_read_ids'%(snapdir, snapnums))

            # make a consistent check
            for snapnum in snapnums.split():
                fin = '%s/groups_%03d/'%(snapdir,int(snapnum))
                file_num = len(os.listdir(fin))
                if file_num!=1:
                    raise Exception ('%s %d %d %d'%(folder,i,snapnum,file_num))

    comm.Barrier()
