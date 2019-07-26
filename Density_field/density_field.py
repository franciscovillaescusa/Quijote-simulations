# This script generates 3D coarse density fields from the simulation snapshots 
from mpi4py import MPI
import numpy as np
import sys,os
import readgadget
import MAS_library as MASL

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

# This routine computes the density field and save results to file
def compute_df(snapshot, ptypes, grid, fout):
    if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
        return 0
    df = MASL.density_field_gadget(snapshot, ptypes, grid, MAS='CIC',
                                   do_RSD=False, axis=0, verbose=True)
    df = df/np.mean(df, dtype=np.float64)-1.0
    np.save(fout, df)

####################################### INPUT ##########################################
root         = '/simons/scratch/fvillaescusa/pdf_information'
root_out     = '/simons/scratch/fvillaescusa/pdf_information/density_field'
grid         = 128
ptypes       = [1]
snapnum      = 4
cosmologies  = ['latin_hypercube']
########################################################################################

# find the redshift
z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]


# do a loop over the different cosmologies
for cosmo in cosmologies:

    # create output folder if it does not exists
    if myrank==0 and not(os.path.exists('%s/%s'%(root_out,cosmo))):
        os.system('mkdir %s/%s'%(root_out,cosmo))
    comm.Barrier()

    if   cosmo=='latin_hypercube':  std_realizations, pf_realizations =  2000, 2000
    elif cosmo=='fiducial':         std_realizations, pf_realizations = 15000,  500
    else:                           std_realizations, pf_realizations =   500,  500

    # do a loop over the different cosmologies
    numbers = np.where(np.arange(std_realizations)%nprocs==myrank)[0]
    for i in numbers:

        # create output folder if it does not exists
        folder_out = '%s/%s/%d'%(root_out,cosmo,i)
        if not(os.path.exists(folder_out)):  
            os.system('mkdir %s'%folder_out)

        # find name of output file
        fout = '%s/df_m_%d_z=%s.npy'%(folder_out,grid,z)
        if os.path.exists(fout):  continue
    
        # compute the density field and save it to file
        snapshot = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)
        compute_df(snapshot, ptypes, grid, fout)
    comm.Barrier()


    # do a loop over the different cosmologies
    numbers = np.where(np.arange(pf_realizations)%nprocs==myrank)[0]
    for i in numbers:

        # do a loop over the two pairs
        for pair in [0,1]:

            # create output folder if it does not exists
            folder_out = '%s/%s/NCV_%d_%d'%(root_out,cosmo,pair,i)
            if not(os.path.exists(folder_out)):  
                os.system('mkdir %s'%folder_out)

            # find name of output file
            fout = '%s/df_m_%d_z=%s.npy'%(folder_out,grid,z)
            if os.path.exists(fout):  continue
    
            # compute the density field and save it to file
            snapshot = '%s/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                       %(root,cosmo,pair,i,snapnum,snapnum)
            compute_df(snapshot, ptypes, grid, fout)
