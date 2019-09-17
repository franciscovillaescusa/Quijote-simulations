# This script computes the pdf of the matter field in real-space. It takes as input
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
import smoothing_library as SL

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


# This routine computes the PDF in real- and redshift-space
def compute_PDF(snapshot, grid, MAS, threads, NCV, pair, 
                folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter):

    if NCV:  #paired-fixed simulations

        # real-space
        fpdf = '%s/%s/NCV_%d_%d/PDF_%s_%.1f_z=%s.txt'\
               %(folder_out,cosmo,pair,i,suffix,smoothing,z)
        if not(os.path.exists(fpdf)):
            do_RSD, axis = False, 0
            find_pdf(snapshot, grid, MAS, do_RSD, axis, threads, ptype,
                     fpdf, smoothing, Filter)

        # redshift-space
        for axis in [0,1,2]:
            fpdf = '%s/%s/NCV_%d_%d/PDF_%s_RS%d_%.1f_z=%s.txt'\
                   %(folder_out,cosmo,pair,i,suffix,axis,smoothing,z)
            if not(os.path.exists(fpdf)):
                do_RSD = True
                find_pdk(snapshot, grid, MAS, do_RSD, axis, threads, ptype,
                         fpdf, smoothing, Filter)

    else:  #standard simulations

        # real-space
        fpdf = '%s/%s/%d/PDF_%s_%.1f_z=%s.txt'%(folder_out,cosmo,i,suffix,smoothing,z)
        if not(os.path.exists(fpdf)):
            do_RSD, axis = False, 0
            find_pdf(snapshot, grid, MAS, do_RSD, axis, threads, ptype, fpdf,
                     smoothing, Filter)

        # redshift-space
        """
        for axis in [0,1,2]:
            fpdf = '%s/%s/%d/PDF_%s_RS%d_%.1f_z=%s.txt'%(folder_out,cosmo,i,suffix,axis,
                                                         smoothing,z)
            if not(os.path.exists(fpdf)):
                do_RSD = True
                find_pdf(snapshot, grid, MAS, do_RSD, axis, threads, ptype, 
                         fpdf, smoothing, Filter)
        """


# This routine computes and saves the pdf
def find_pdf(snapshot, grid, MAS, do_RSD, axis, threads, ptype, fpdf, smoothing, Filter):

    if os.path.exists(fpdf):  return 0
    
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

    # calculate the overdensity field
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
    delta /= np.mean(delta, dtype=np.float64);  #delta -= 1.0 

    # smooth the overdensity field
    W_k = SL.FT_filter(BoxSize, smoothing, grid, Filter, threads)
    delta_smoothed = SL.field_smoothing(delta, W_k, threads)

    bins = np.logspace(-2,2,100)
    pdf, mean = np.histogram(delta_smoothed, bins=bins)
    mean = 0.5*(mean[1:] + mean[:-1])
    pdf = pdf*1.0/grid**3

    # save results to file
    np.savetxt(fpdf, np.transpose([mean, pdf]), delimiter='\t')



##################################### INPUT #########################################
# folder containing the snapshots
root = '/simons/scratch/fvillaescusa/pdf_information'

# PDF parameters
grid      = 512
MAS       = 'CIC'
threads   = 2
smoothing = 10.0
Filter    = 'Top-Hat' #'Gaussian'

# folder that containts the results
folder_out = '/simons/scratch/fvillaescusa/pdf_information/PDF/matter/'
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
    snapshot = '%s/Snapshots/%s/%d/snapdir_%03d/snap_%03d'%(root,cosmo,i,snapnum,snapnum)
    if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
        continue

    # create output folder if it does not exists
    if not(os.path.exists('%s/%s/%d'%(folder_out,cosmo,i))):
        os.system('mkdir %s/%s/%d'%(folder_out,cosmo,i))

    # neutrinos are special
    if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

        # compute CDM+Baryons PDF
        #NCV, suffix, ptype, pair = False, 'cb', [1], 0
        #compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
        #           folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

        # compute matter PDF
        NCV, suffix, ptype, pair = False, 'm', [1,2], 0
        compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
                    folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

    else:
        # compute matter PDF
        NCV, suffix, ptype, pair = False, 'm', [1], 0
        compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
                    folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

    

###### paired fixed realizations ######
for i in numbers:

    for pair in [0,1]:
        snapshot = '%s/Snapshots/%s/NCV_%d_%d/snapdir_%03d/snap_%03d'\
                   %(root,cosmo,pair,i,snapnum,snapnum)
        if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
            continue

        # create output folder if it does not exists
        if not(os.path.exists('%s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))):
            os.system('mkdir   %s/%s/NCV_%d_%d'%(folder_out,cosmo,pair,i))

        # neutrinos are special
        if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/']:

            # compute CDM+Baryons PDF
            #NCV, suffix, ptype = True, 'cb', [1]
            #compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
            #           folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

            # compute matter PDF
            NCV, suffix, ptype  = True, 'm', [1,2]
            compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
                        folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

        else:
            # compute matter PDF
            NCV, suffix, ptype = True, 'm', [1]
            compute_PDF(snapshot, grid, MAS, threads, NCV, pair,
                        folder_out, cosmo, i, suffix, z, ptype, smoothing, Filter)

