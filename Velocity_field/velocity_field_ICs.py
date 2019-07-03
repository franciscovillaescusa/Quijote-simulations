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
def compute_vf(snapshot, ptypes, grid, axis, MAS, fout):
    if not(os.path.exists(snapshot+'.0')):  return 0
    
    # read header
    header   = readgadget.header(snapshot)
    BoxSize  = header.boxsize/1e3  #Mpc/h
    Nall     = header.nall         #Total number of particles
    Masses   = header.massarr*1e10 #Masses of the particles in Msun/
    redshift = header.redshift     #redshift of the snapshot

    # read positions and velocities
    pos = readgadget.read_block(snapshot, "POS ", ptypes)/1e3 #Mpc/h
    vel = readgadget.read_block(snapshot, "VEL ", ptypes)     #km/s
    
    # compute density field
    df = np.zeros((grid,grid,grid), dtype=np.float32)
    MASL.MA(pos, df, BoxSize, MAS)
    df[np.where(df==0)]=1e-7 # to avoid dividing by 0

    # compute the velocity field
    vf = np.zeros((grid,grid,grid), dtype=np.float32)
    MASL.MA(pos, vf, BoxSize, MAS, W=vel[:,axis])
    vf = vf/df

    # save results to file
    np.save(fout, df)

####################################### INPUT ##########################################
root         = '/simons/scratch/fvillaescusa/pdf_information'
root_out     = '/simons/scratch/fvillaescusa/pdf_information/velocity_field'
grid         = 512
MAS          = 'CIC'
ptypes       = [1] #this code doesnt work for neutrinos!!!
cosmologies  = ['fiducial']
z            = 127
########################################################################################


# do a loop over the different cosmologies
for cosmo in cosmologies:

    # create output folder if it does not exists
    if myrank==0 and not(os.path.exists('%s/%s'%(root_out,cosmo))):
        os.system('mkdir %s/%s'%(root_out,cosmo))
    comm.Barrier()

    #if   cosmo=='latin_hypercube':  std_realizations, pf_realizations =  2000, 2000
    #elif cosmo=='fiducial':         std_realizations, pf_realizations = 15000,  250
    #else:                           std_realizations, pf_realizations =   500,  250
    std_realizations, pf_realizations = 1000, 0

    # do a loop over the different cosmologies
    numbers = np.where(np.arange(std_realizations)%nprocs==myrank)[0]
    for i in numbers:

        # create output folder if it does not exists
        folder_out = '%s/%s/%d'%(root_out,cosmo,i)
        if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

        # get the name of the snapshot
        snapshot = '%s/%s/%d/ICs/ics'%(root,cosmo,i)

        # find name of output file and compute velocity field
        for axis in [0,1,2]:
            fout = '%s/vf%d_m_z=%s.npy'%(folder_out,axis,z)
            if os.path.exists(fout):  continue
            compute_vf(snapshot, ptypes, grid, axis, MAS, fout)
    comm.Barrier()


    # do a loop over the different cosmologies
    numbers = np.where(np.arange(pf_realizations)%nprocs==myrank)[0]
    for i in numbers:

        # do a loop over the two pairs
        for pair in [0,1]:

            # create output folder if it does not exists
            folder_out = '%s/%s/NCV_%d_%d'%(root_out,cosmo,pair,i)
            if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

            # get the name of the snapshot
            snapshot = '%s/%s/NCV_%d_%d/ICs/ics'%(root,cosmo,pair,i)

            # find name of output file
            for axis in [0,1,2]:
                fout = '%s/vf%d_m_z=%s.npy'%(folder_out,axis,z)
                if os.path.exists(fout):  continue
                compute_vf(snapshot, ptypes, grid, axis, MAS, fout)
