# This script computes the matter Pk in real- and redshift-space. It takes as input
# the first and last number of the wanted realizations, the cosmology and the snapnum
# In redshift-space it computes the power spectrum along the 3 different axes. 
import argparse
from mpi4py import MPI
import numpy as np
import sys,os
import readgadget,readfof
import redshift_space_library as RSL
import Pk_library as PKL
import MAS_library as MASL

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

# read the first and last realization to identify voids
parser = argparse.ArgumentParser(description="This script computes the bispectrum")
parser.add_argument("first",   help="first realization number", type=int)
parser.add_argument("last",    help="last  realization number", type=int)
parser.add_argument("cosmo",   help="folder with the realizations")
parser.add_argument("z",       help="redshift")
args = parser.parse_args()
first, last, cosmo, z = args.first, args.last, args.cosmo, args.z


##################################### INPUT #########################################
# folder containing the snapshots
root = '/simons/scratch/fvillaescusa/pdf_information/density_field_2D'

# Pk parameters
BoxSize = 1000.0 #Mpc/h
grid    = 512
MAS     = 'CIC'
threads = 2

# folder that containts the results
folder_out = '/simons/scratch/fvillaescusa/pdf_information/Pk_2D/matter/'
#####################################################################################

# create output folder if it does not exist
if myrank==0 and not(os.path.exists(folder_out+cosmo)):  
    os.system('mkdir %s/%s/'%(folder_out,cosmo))
comm.Barrier()

# get the realizations each cpu works on
numbers = np.where(np.arange(args.first, args.last)%nprocs==myrank)[0]
numbers = np.arange(args.first, args.last)[numbers]


######## standard simulations #########
for i in numbers:

    # get the name of the output file
    fpk = '%s/%s/%d/Pk2D_m_z=%s.txt'%(folder_out,cosmo,i,z)
    if os.path.exists(fpk):  continue

    # find the density field file and read it
    f_df = '%s/%s/%d/df_z=%s.npy'%(root,cosmo,i,z)
    if not(os.path.exists(f_df)):  continue
    df = np.load(f_df)

    # create output folder if it does not exists
    if not(os.path.exists('%s/%s/%d'%(folder_out,cosmo,i))):
        os.system('mkdir %s/%s/%d'%(folder_out,cosmo,i))

    # compute matter Pk
    Pk = PKL.Pk_plane(df,BoxSize,MAS,threads)
    np.savetxt(fpk, np.transpose([Pk.k, Pk.Pk]))



###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:

        # get the name of the output file
        fpk = '%s/%s/NCV_%d_%d/Pk2D_m_z=%s.txt'%(folder_out,cosmo,pair,i,z)
        if os.path.exists(fpk):  continue

        # find the density field file and read it
        f_df = '%s/%s/NCV_%d_%d/df_z=%s.npy'%(root,cosmo,pair,i,z)
        if not(os.path.exists(f_df)):  continue
        df = np.load(f_df)

        # create output folder if it does not exists
        if not(os.path.exists('%s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))):
            os.system('mkdir %s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))

        # compute matter Pk
        Pk = PKL.Pk_plane(df,BoxSize,MAS,threads)
        np.savetxt(fpk, np.transpose([Pk.k, Pk.Pk]))

