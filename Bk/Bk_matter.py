# This script computes the matter bispectrum in real- and redshift-space. It takes as 
# input the first and last number of the wanted realizations, the cosmology and the 
# snapnum. In redshift-space it computes the bispectrum along the 3 different axes. 
import argparse
from mpi4py import MPI
import numpy as np
import sys,os
import readgadget,readfof
import redshift_space_library as RSL
from pyspectrum import pyspectrum as pySpec

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
def find_Bk(snapdir, snapnum, axis, Ngrid, step, Ncut, Nmax, do_RSD):
    
    # read header
    head     = readgadget.header(snapdir)
    BoxSize  = head.boxsize/1e3  #Mpc/h                      
    Omega_m  = head.omega_m
    Omega_l  = head.omega_l
    redshift = head.redshift
    Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#km/s/(Mpc/h)
    h        = head.hubble

    # read the snapshot
    pos = readgadget.read_block(snapdir, "POS ", [1])/1e3 #Mpc/h

    # move positions to redshift-space
    if do_RSD:
        vel = readgadget.read_block(snapdir, "VEL ", [1]) #km/s
        RSL.pos_redshift_space(pos, vel, BoxSize, Hubble, redshift, axis)

    # calculate bispectrum
    b123out = pySpec.Bk_periodic(pos.T, Lbox=BoxSize, Ngrid=Ngrid, step=step, 
                                 Ncut=Ncut, Nmax=Nmax, fft='pyfftw', 
                                 nthreads=1, silent=False)

    i_k  = b123out['i_k1']
    j_k  = b123out['i_k2']
    l_k  = b123out['i_k3']
    p0k1 = b123out['p0k1']
    p0k2 = b123out['p0k2']
    p0k3 = b123out['p0k3']
    b123 = b123out['b123']
    b_sn = b123out['b123_sn']
    q123 = b123out['q123']
    cnts = b123out['counts']

    hdr = ('matter bispectrum; k_f = 2pi/%.1f, Nhalo=%i'%(BoxSize, pos.shape[0]))
    np.savetxt(fbk, np.array([i_k, j_k, l_k, p0k1, p0k2, p0k3, b123, q123, b_sn, cnts]).T,
               fmt='%i %i %i %.5e %.5e %.5e %.5e %.5e %.5e %.5e', 
               delimiter='\t', header=hdr)


root = '/simons/scratch/fvillaescusa/pdf_information'
##################################### INPUT #########################################
# Bk parameters
Ngrid = 360 
Nmax  = 40
Ncut  = 3
step  = 3

# output folder name
root_out = '/simons/scratch/fvillaescusa/pdf_information/Bk/matter/' 
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

    # find the snapshot name
    snapdir = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)
    if not(os.path.exists(snapdir+'.0')) and not(os.path.exists(snapdir+'.0.hdf5')): 
        continue

    # real-space
    fbk = '%s/%s/Bk_m_%d_z=%s.txt'%(root_out,cosmo,i,z)
    if not(os.path.exists(fbk)):  
        do_RSD, axis = False, 0
        find_Bk(snapdir, snapnum, axis, Ngrid, step, Ncut, Nmax, do_RSD)

    # redshift-space
    for axis in [0,1,2]:
        fbk = '%s/%s/Bk_m_RS%d_%d_z=%s.txt'%(root_out,cosmo,axis,i,z)
        if not(os.path.exists(fbk)):
            do_RSD = True
            find_Bk(snapdir, snapnum, axis, Ngrid, step, Ncut, Nmax, do_RSD)


###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:
        # find the snapshot name
        snapdir = '%s/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                  %(root,cosmo,pair,i,snapnum,snapnum)
        if not(os.path.exists(snapdir+'.0')) and not(os.path.exists(snapdir+'.0.hdf5')): 
            continue

        # real-space
        fbk = '%s/%s/Bk_m_NCV_%d_%d_z=%s.txt'%(root_out,cosmo,pair,i,z)
        if not(os.path.exists(fbk)):  
            do_RSD, axis = False, 0
            find_Bk(snapdir, snapnum, axis, Ngrid, step, Ncut, Nmax, do_RSD)

        # redshift-space
        for axis in [0,1,2]:
            fbk = '%s/%s/Bk_m_RS%d_NCV_%d_%d_z=%s.txt'%(root_out,cosmo,axis,pair,i,z)
            if not(os.path.exists(fbk)):  
                do_RSD = True
                find_Bk(snapdir, snapnum, axis, Ngrid, step, Ncut, Nmax, do_RSD)



        

