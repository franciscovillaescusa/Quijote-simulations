# This script computes the matter CF in real- and redshift-space. It takes as input
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
parser.add_argument("snapnum", help="snapshot number",          type=int)
args = parser.parse_args()
first, last, cosmo, snapnum = args.first, args.last, args.cosmo, args.snapnum


# This routine computes the Pk in real- and redshift-space
def compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair, 
               folder_out, cosmo, i, suffix, z, ptype):

    if NCV:  #paired-fixed simulations

        # real-space
        fcf = '%s/%s/NCV_%d_%d/CF_%s_z=%s.txt'%(folder_out,cosmo,pair,i,suffix,z)
        if not(os.path.exists(fcf)):
            do_RSD, axis, save_multipoles = False, 0, False
            find_CF(snapshot, snapnum, grid, MAS, do_RSD, axis, threads, ptype,
                    fcf, save_multipoles)

        # redshift-space
        """
        for axis in [0,1,2]:
            cfk = '%s/%s/NCV_%d_%d/CF_%s_RS%d_z=%s.txt'\
                  %(folder_out,cosmo,pair,i,suffix,axis,z)
            if not(os.path.exists(fcf)):
                do_RSD, save_multipoles = True, True
                find_CF(snapshot, snapnum, grid, MAS, do_RSD, axis, threads, ptype,
                        fcf, save_multipoles)
        """

    else:  #standard simulations

        # real-space
        fcf = '%s/%s/%d/CF_%s_z=%s.txt'%(folder_out,cosmo,i,suffix,z)
        if not(os.path.exists(fcf)):
            do_RSD, axis, save_multipoles = False, 0, False
            find_CF(snapshot, snapnum, grid, MAS, do_RSD, axis, threads, ptype,
                    fcf, save_multipoles)

        # redshift-space
        """
        for axis in [0,1,2]:
            fcf = '%s/%s/%d/CF_%s_RS%d_z=%s.txt'%(folder_out,cosmo,i,suffix,axis,z)
            if not(os.path.exists(fcf)):
                do_RSD, save_multipoles = True, True
                find_CF(snapshot, snapnum, grid, MAS, do_RSD, axis, threads, ptype,
                        fcf, save_multipoles)
        """


# This routine computes and saves the correlation function
def find_CF(snapshot, snapnum, grid, MAS, do_RSD, axis, threads, ptype,
            fcf, save_multipoles):

    if os.path.exists(fcf):  return 0
    
    # read header
    head     = readgadget.header(snapshot)
    BoxSize  = head.boxsize/1e3  #Mpc/h  
    Nall     = head.nall         #Total number of particles
    Masses   = head.massarr*1e10 #Masses of the particles in Msun/h                    
    Omega_m  = head.omega_m
    Omega_l  = head.omega_l
    redshift = head.redshift
    Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#km/s/(Mpc/h)
    h        = head.hubble

    # read snapshot
    pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #Mpc/h

    # move particles to redshift-space
    if do_RSD:
        vel = readgadget.read_block(snapshot, "VEL ", ptype) #km/s
        RSL.pos_redshift_space(pos, vel, BoxSize, Hubble, redshift, axis)

    # calculate CF
    delta = np.zeros((grid,grid,grid), dtype=np.float32)
    if len(ptype)>1:  #for multiple particles read masses
        mass = np.zeros(pos.shape[0], dtype=np.float32)
        offset = 0
        for j in ptype:
            mass[offset: offset+Nall[j]] = Masses[j]
            offset += Nall[j]
        MASL.MA(pos, delta, BoxSize, MAS, W=mass)
    else:
        MASL.MA(pos, delta, BoxSize, MAS)
    delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0 
    CF  = PKL.Xi(delta, BoxSize, MAS, axis, threads)

    # save results to file
    if save_multipoles:
        np.savetxt(fcf, np.transpose([CF.r3D, CF.xi[:,0], CF.xi[:,1], CF.xi[:,2]]),
                   delimiter='\t')
    else:
        np.savetxt(fcf, np.transpose([CF.r3D, CF.xi[:,0]]), delimiter='\t')



##################################### INPUT #########################################
# folder containing the snapshots
root = '/simons/scratch/fvillaescusa/pdf_information'

# folder that containts the results
folder_out = '/simons/scratch/fvillaescusa/pdf_information/CF/matter/'

# CF parameters
grid    = 1024
MAS     = 'CIC'
threads = 2
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

    # find the snapshot
    snapshot = '%s/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)
    if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
        continue

    # create output folder if it does not exists
    if not(os.path.exists('%s/%s/%d'%(folder_out,cosmo,i))):
        os.system('mkdir %s/%s/%d'%(folder_out,cosmo,i))

    # neutrinos are special
    if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

        # compute CDM+Baryons Pk
        NCV, suffix, ptype, pair = False, 'cb', [1], 0
        compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                   folder_out, cosmo, i, suffix, z, ptype)

        # compute matter Pk
        NCV, suffix, ptype, pair = False, 'm', [1,2], 0
        compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                   folder_out, cosmo, i, suffix, z, ptype)

    else:
        # compute matter Pk
        NCV, suffix, ptype, pair = False, 'm', [1], 0
        compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                   folder_out, cosmo, i, suffix, z, ptype)

    


###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:
        snapshot = '%s/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                   %(root,cosmo,pair,i,snapnum,snapnum)
        if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
            continue

        # create output folder if it does not exists
        if not(os.path.exists('%s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))):
            os.system('mkdir %s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))

        # neutrinos are special
        if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

            # compute CDM+Baryons Pk
            NCV, suffix, ptype = True, 'cb', [1]
            compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                       folder_out, cosmo, i, suffix, z, ptype)

            # compute matter Pk
            NCV, suffix, ptype  = True, 'm', [1,2]
            compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                       folder_out, cosmo, i, suffix, z, ptype)

        else:
            # compute matter Pk
            NCV, suffix, ptype = True, 'm', [1]
            compute_CF(snapshot, snapnum, grid, MAS, threads, NCV, pair,
                       folder_out, cosmo, i, suffix, z, ptype)


        

