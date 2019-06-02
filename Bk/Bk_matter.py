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


# This routine computes the Bk in real- and redshift-space
def compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair, 
               folder_out, cosmo, i, suffix, z, ptype):

    if NCV:  #paired-fixed simulations

        # real-space
        fbk = '%s/%s/NCV_%d_%d/Bk_%s_z=%s.txt'%(folder_out,cosmo,pair,i,suffix,z)
        if not(os.path.exists(fbk)):
            do_RSD, axis = False, 0
            find_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, do_RSD, axis, ptype, fbk)

        # redshift-space
        for axis in [0,1,2]:
            fbk = '%s/%s/NCV_%d_%d/Bk_%s_RS%d_z=%s.txt'\
                  %(folder_out,cosmo,pair,i,suffix,axis,z)
            if not(os.path.exists(fbk)):
                do_RSD = True
                find_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, do_RSD, axis, 
                        ptype, fbk)

    else:  #standard simulations

        # real-space
        fbk = '%s/%s/%d/Bk_%s_z=%s.txt'%(folder_out,cosmo,i,suffix,z)
        if not(os.path.exists(fbk)):
            do_RSD, axis = False, 0
            find_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, do_RSD, axis, ptype, fbk)

        # redshift-space
        for axis in [0,1,2]:
            fbk = '%s/%s/%d/Bk_%s_RS%d_z=%s.txt'%(folder_out,cosmo,i,suffix,axis,z)
            if not(os.path.exists(fbk)):
                do_RSD = True
                find_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, do_RSD, axis, 
                        ptype, fbk)



# This routine computes and saves the bispectrum
def find_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, do_RSD, axis, ptype, fbk):
    
    # read header
    head     = readgadget.header(snapshot)
    BoxSize  = head.boxsize/1e3  #Mpc/h                      
    Omega_m  = head.omega_m
    Omega_l  = head.omega_l
    redshift = head.redshift
    Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#km/s/(Mpc/h)
    h        = head.hubble

    # read the snapshot
    pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #Mpc/h

    # move positions to redshift-space
    if do_RSD:
        vel = readgadget.read_block(snapshot, "VEL ", ptype) #km/s
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



##################################### INPUT #########################################
# folder containing the snapshots
root = '/simons/scratch/fvillaescusa/pdf_information'

# Bk parameters
Ngrid = 360 
Nmax  = 40
Ncut  = 3
step  = 3

# output folder name
folder_out = '/simons/scratch/fvillaescusa/pdf_information/Bk/matter/' 
#####################################################################################

# find the redshift
z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]

# create output folder if it does not exist
if myrank==0 and not(os.path.exists(folder_out+cosmo)):  
    os.system('mkdir %s/%s/'%(folder_out,cosmo))
comm.Barrier()

# get the realizations each cpu works on
numbers = np.where(np.arange(args.first, args.last)%nprocs==myrank)[0]
numbers = np.arange(args.first, args.last)[numbers]


######## standard simulations #########
for i in numbers:

    # find the snapshot name
    snapshot = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)
    if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')): 
        continue

    # create output folder if it does not exists
    if not(os.path.exists('%s/%s/%d'%(folder_out,cosmo,i))):
        os.system('mkdir %s/%s/%d'%(folder_out,cosmo,i))

    # neutrinos are special
    if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

        # compute CDM+Baryons Bk
        NCV, suffix, ptype, pair = False, 'cb', [1], 0
        compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
                   folder_out, cosmo, i, suffix, z, ptype)

        # compute matter Bk
        #NCV, suffix, ptype, pair = False, 'm', [1,2], 0
        #compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
        #           folder_out, cosmo, i, suffix, z, ptype)

    else:
        # compute matter Bk
        NCV, suffix, ptype, pair = False, 'm', [1], 0
        compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
                   folder_out, cosmo, i, suffix, z, ptype)



###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:
        # find the snapshot name
        snapshot = '%s/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                  %(root,cosmo,pair,i,snapnum,snapnum)
        if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')): 
            continue

        # create output folder if it does not exists
        if not(os.path.exists('%s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))):
            os.system('mkdir %s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))

        # neutrinos are special
        if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

            # compute CDM+Baryons Bk
            NCV, suffix, ptype = True, 'cb', [1]
            compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
                       folder_out, cosmo, i, suffix, z, ptype)

            # compute matter Bk
            #NCV, suffix, ptype  = True, 'm', [1,2]
            #compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
            #           folder_out, cosmo, i, suffix, z, ptype)

        else:
            # compute matter Bk
            NCV, suffix, ptype = True, 'm', [1]
            compute_Bk(snapshot, snapnum, Ngrid, Nmax, Ncut, step, NCV, pair,
                       folder_out, cosmo, i, suffix, z, ptype)




        

