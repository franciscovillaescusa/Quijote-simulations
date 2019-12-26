# This script generates 2D density fields of the different simulations
from mpi4py import MPI
import numpy as np
import sys,os
import MAS_library as MASL

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()


####################################### INPUT ##########################################
root     = '/simons/scratch/fvillaescusa/pdf_information/'
root_out = '/simons/scratch/fvillaescusa/pdf_information/density_field_2D/'

cosmologies = ['Om_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p', 
               'Om_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
               'fiducial', 'latin_hypercube']

grid   = 256
ptypes = [1]
MAS    = 'CIC'
########################################################################################


# do a loop over the different cosmologies
for cosmo in cosmologies:

    if   cosmo=='fiducial':         realizations = 15000
    elif cosmo=='latin_hypercube':  realizations = 2000
    else:                           realizations = 500

    # find the numbers that each cpu will work with                  
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

    # create output folder if it does not exists
    folder_out = '%s/%s/'%(root_out,cosmo)
    if myrank==0 and not(os.path.exists(folder_out)):  
        os.system('mkdir %s'%folder_out)
    comm.Barrier()

    # do a loop over all realizations
    for i in numbers:

        if not(os.path.exists('%s/%d/'%(folder_out,i))):
            os.system('mkdir %s/%d/'%(folder_out,i))

        fout = '%s/%d/df_z=0.npy'%(folder_out,i)
        if os.path.exists(fout):  continue
    
        # compute the density field and save it to file
        snapshot = '%s/Snapshots/%s/%d/snapdir_004/snap_004'%(root,cosmo,i)
        if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
            continue
        df = MASL.density_field_gadget(snapshot, ptypes, grid, MAS=MAS,
                                       do_RSD=False, axis=0, verbose=True)
        df = df/np.mean(df, dtype=np.float64) - 1.0

        # project the density field along the z-axis
        df = np.mean(df[:,:,:5], axis=2)
        
        np.save(fout, df)


