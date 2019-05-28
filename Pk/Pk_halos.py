# This script computes the halo bispectrum in real- and redshift-space. It takes as input
# the first and last number of the wanted realizations, the cosmology and the snapnum
# In redshift-space it computes the bispectrum along the 3 different axes. 
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
parser.add_argument("snapnum", help="snapshot number",          type=int)
args = parser.parse_args()
first, last, cosmo, snapnum = args.first, args.last, args.cosmo, args.snapnum

# This routine computes and saves the bispectrum
def find_Pk(folder, snapdir, snapnum, grid, MAS, do_RSD, axis, threads,
            fixed_Mmin, Mmin, Nhalos, fpk, save_multipoles):

    if os.path.exists(fpk):  return 0
    
    # read header
    head     = readgadget.header(snapdir)
    BoxSize  = head.boxsize/1e3  #Mpc/h                      
    Omega_m  = head.omega_m
    Omega_l  = head.omega_l
    redshift = head.redshift
    Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#km/s/(Mpc/h)
    h        = head.hubble

    # read halo catalogue
    FoF   = readfof.FoF_catalog(folder, snapnum, long_ids=False,
                                swap=False, SFR=False, read_IDs=False)
    pos_h = FoF.GroupPos/1e3            #Mpc/h
    mass  = FoF.GroupMass*1e10          #Msun/h
    vel_h = FoF.GroupVel*(1.0+redshift) #km/s
    if fixed_Mmin:
        indexes = np.where(mass>Mmin)[0]
        pos_h = pos_h[indexes];  vel_h = vel_h[indexes];  del indexes
    else:
        indexes = np.argsort(mass)[-Nhalos:] #take the Nhalos most massive halos
        pos_h = pos_h[indexes];  vel_h = vel_h[indexes];  del indexes

    # move halos to redshift-space
    if do_RSD:  RSL.pos_redshift_space(pos_h, vel_h, BoxSize, Hubble, redshift, axis)

    # calculate Pk
    delta = np.zeros((grid,grid,grid), dtype=np.float32)
    MASL.MA(pos_h, delta, BoxSize, MAS)
    delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0 
    Pk = PKL.Pk(delta, BoxSize, axis, MAS, threads)

    # save results to file
    hdr = ('Nhalos=%i BoxSize=%.3f'%(pos_h.shape[0],BoxSize))    
    if save_multipoles:
        np.savetxt(fpk, np.transpose([Pk.k3D, Pk.Pk[:,0], Pk.Pk[:,1], Pk.Pk[:,2]]),
                   delimiter='\t', header=hdr)
    else:
        np.savetxt(fpk, np.transpose([Pk.k3D, Pk.Pk[:,0]]),
                   delimiter='\t', header=hdr)



root = '/simons/scratch/fvillaescusa/pdf_information'
##################################### INPUT #########################################
# Pk parameters
grid    = 1024
MAS     = 'CIC'
threads = 2

# halo parameters
fixed_Mmin = True   #whether fix Mmin or nbar
Mmin       = 3.2e13 #Msun/h; fixed Mmin
Nhalos     = 150000 #also consider the Nhalos more massive of the sim (nbar fixed)

# output folder name
root_out = '/simons/scratch/fvillaescusa/pdf_information/Pk/halos_Mmin_3.2e13/' 
#####################################################################################

# find the redshift
z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]

# create output folder if it does not exist
if myrank==0:
    if not(os.path.exists(root_out+cosmo)):  os.system('mkdir %s/%s/'%(root_out,cosmo))

# get the realizations each cpu works on
numbers = np.where(np.arange(args.first, args.last)%nprocs==myrank)[0]
numbers = np.arange(args.first, args.last)[numbers]


######## standard simulations #########
for i in numbers:

    folder  = '%s/Halos/%s/%d'%(root,cosmo,i) #folder with the halo catalogue
    if not(os.path.exists(folder)):  continue
    snapdir = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)

    # real-space
    fpk = '%s/%s/Pk_%d_z=%s.txt'%(root_out,cosmo,i,z)
    do_RSD, axis, save_multipoles = False, 0, False
    find_Pk(folder, snapdir, snapnum, grid, MAS, do_RSD, axis, threads,
            fixed_Mmin, Mmin, Nhalos, fpk, save_multipoles)

    # redshift-space
    for axis in [0,1,2]:
        fpk = '%s/%s/Pk_RS%d_%d_z=%s.txt'%(root_out,cosmo,axis,i,z)
        do_RSD, save_multipoles = True, True
        find_Pk(folder, snapdir, snapnum, grid, MAS, do_RSD, axis, threads,
                fixed_Mmin, Mmin, Nhalos, fpk, save_multipoles)


###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:
        folder  = '%s/Halos/%s/NCV_%d_%d'%(root,cosmo,pair,i) #halo catalogue folder
        if not(os.path.exists(folder)):  continue
        snapdir = '%s/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                  %(root,cosmo,pair,i,snapnum,snapnum)

        # real-space
        fpk = '%s/%s/Pk_NCV_%d_%d_z=%s.txt'%(root_out,cosmo,pair,i,z)
        do_RSD, axis, save_multipoles = False, 0, False
        find_Pk(folder, snapdir, snapnum, grid, MAS, do_RSD, axis, threads,
                fixed_Mmin, Mmin, Nhalos, fpk, save_multipoles)

        # redshift-space
        for axis in [0,1,2]:
            fpk = '%s/%s/Pk_RS%d_NCV_%d_%d_z=%s.txt'%(root_out,cosmo,axis,pair,i,z)
            do_RSD, save_multipoles = True, True
            find_Pk(folder, snapdir, snapnum, grid, MAS, do_RSD, axis, threads,
                    fixed_Mmin, Mmin, Nhalos, fpk, save_multipoles)



        

