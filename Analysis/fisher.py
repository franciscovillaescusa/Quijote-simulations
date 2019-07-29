# This scripts computes:
# 1) The covariance matrix for all probes (P_m(k) + P_cb(k) + HMF + VSF)
# 2) The mean of all statistics for all cosmologies
# 3) The derivatives of the statistics with respect to the cosmological parameters
# 4) The Fisher matrix for the considered probes
from mpi4py import MPI
import numpy as np
import sys,os
sys.path.append('/home/fvillaescusa/data/pdf_information/analysis/git_repo/library')
import analysis_library as AL

###### MPI DEFINITIONS ######
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

##################################### INPUT ###########################################
# folders with the data and output files
root_data    = '/simons/scratch/fvillaescusa/pdf_information/'
root_results = '/simons/scratch/fvillaescusa/pdf_information/results/'

# general parameters
parameters       = ['Om', 'Ob2', 'h', 'ns', 's8', 'Mnu']
BoxSize          = 1000.0  #Mpc/h
snapnum          = 4       #z=0
realizations_Cov = 1000   #number of realizations for the covariance
realizations_der = 250     #number of realizations for the derivatives
Volume           = 1.0     #(Gpc/h)^3

# parameters of the Pk_m
kmax_m     = 1.0 #h/Mpc
folder_Pkm = '/simons/scratch/fvillaescusa/pdf_information/Pk/matter/'
do_Pkm     = True

# parameters of the Pk_cb
kmax_c     = 0.2 #h/Mpc
folder_Pkc = '/simons/scratch/fvillaescusa/pdf_information/Pk/matter/'
do_Pkc     = False

# parameters of the VSF
Radii       = np.array([41, 39, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19, 17, 
                        15, 13, 11, 9, 7, 5], dtype=np.float32)*1000.0/768 #Mpc/h
grid        = 1024
VSF_bins    = 29
Rmin        = 4.0   #Mpc/h
Rmax        = 33.0  #Mpc/h
delete_bins = [1,2,3,5,7,9]
folder_VSF  = '/simons/scratch/fvillaescusa/pdf_information/Voids/'
do_VSF      = False

# parameters of the HMF
Nmin       = 100.0    #minimum number of CDM particles in a halo
Nmax       = 10000.0  #maximum number of CDM particles in a halo
HMF_bins   = 15       #number of bins in the HMF
folder_HMF = '/simons/scratch/fvillaescusa/pdf_information/Halos/'
do_HMF     = False
#######################################################################################

# find the corresponding redshift
z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]

######################## COMPUTE/READ FULL COVARIANCE #############################
# read/compute the covariance of all the probes (Pk+HMF+VSF)
# bins is an array with the number of bins in each statistics
# X is an array with the value of the statistics in each bin
# Cov is the covariance matrix with size bins x bins
bins, X, Cov = AL.covariance(realizations_Cov, BoxSize, snapnum, root_data, root_results, 
                             kmax_m, folder_Pkm,
                             kmax_c, folder_Pkc,
                             Radii,  folder_VSF,
                             HMF_bins, Nmin, Nmax, folder_HMF)
sys.exit()
###################################################################################

########################## COMPUTE ALL DERIVATIVES ################################
# compute the mean values of the different statistics for all cosmologies and 
# compute the derivatives of the statistics with respect to the parameters
AL.derivatives(realizations_der, BoxSize, snapnum, root_data, root_results, 
               kmax_m, kmax_c, grid, Rmin, Rmax, VSF_bins, delete_bins, 
               HMF_bins, Nmin, Nmax)
###################################################################################

if myrank>0:  sys.exit() #here finishes the parallelism 

######################## COMPUTE INVERSE OF (SUB)-COVARIANCE ######################
# find the (sub)covariance of the considered observables; invert it
Cov  = AL.subcovariance(Cov, bins, do_Pkm, do_Pkc, do_HMF, do_VSF)
ICov = AL.Inv_Cov(Cov)
###################################################################################

################################# GENERAL THINGS ##################################
# find the k-bins, M-bins and R-bins and the number of cosmo parameter
km = X[np.arange(0,                np.sum(bins[:1]))] #k-modes for P_m(k)
kc = X[np.arange(np.sum(bins[:1]), np.sum(bins[:2]))] #k-modes for P_cb(k)
N  = X[np.arange(np.sum(bins[:2]), np.sum(bins[:3]))] #number of particles bins
R  = X[np.arange(np.sum(bins[:3]), np.sum(bins[:4]))] #radii bins
all_bins   = Cov.shape[0]    #number of bins in the (sub)-covariance matrix
params_num = len(parameters) #number of cosmological parameters

# find the different suffixes
suffix_Pkm = 'Pkm_%d_%.2f_z=%s.txt'%(realizations_der, kmax_m, z)
suffix_Pkc = 'Pkc_%d_%.2f_z=%s.txt'%(realizations_der, kmax_c, z)
suffix_HMF = 'HMF_%d_%.1e_%.1e_%d_z=%s.txt'%(realizations_der, Nmin, Nmax, HMF_bins, z)
suffix_VSF = 'VSF_%d_%.1e_%.1e_%d_%s_z=%s.txt'\
             %(realizations_der, Rmin, Rmax, VSF_bins, delete_bins, z)

# read the HMF of the fiducial cosmology
f = '%s/fiducial_NCV/mean_HMF_%d_%.1e_%.1e_%d_z=%s.txt'\
    %(root_results, realizations_der, Nmin, Nmax, HMF_bins, z)
N_fiducial, HMF_fiducial, dHMF_fiducial = np.loadtxt(f, unpack=True)
if not(np.allclose(N_fiducial, N, rtol=1e-8, atol=1e-10)):  
    raise Exception('N-values differ in the fiducial HMF!!!')
###################################################################################

############################## READ DERIVATIVES ###################################
# define the matrix containing the derivatives
derivative = np.zeros((params_num, all_bins), dtype=np.float64)

# do a loop over all the parameters
for i,parameter in enumerate(parameters):

    # temporary array storing the derivatives
    derivat = np.array([], dtype=np.float64)
        
    if do_Pkm:  #read the P_m(k) derivatives
        f = '%s/derivatives/derivative_%s_%s'%(root_results, parameter, suffix_Pkm)
        k_der, der_Pk = np.loadtxt(f, unpack=True)
        if not(np.allclose(k_der, km, rtol=1e-8, atol=1e-10)):  
            raise Exception('k-values differ in the Pk derivatives!!!')
        derivat = np.hstack([derivat, der_Pk])

    if do_Pkc:  #read the P_cb(k) derivatives
        f = '%s/derivatives/derivative_%s_%s'%(root_results, parameter, suffix_Pkc)
        k_der, der_Pk = np.loadtxt(f, unpack=True)
        if not(np.allclose(k_der, kc, rtol=1e-8, atol=1e-10)):  
            raise Exception('k-values differ in the Pk derivatives!!!')
        derivat = np.hstack([derivat, der_Pk])

    if do_HMF:  #read the HMF derivatives
        #if parameter in ['Ob','h','ns','s8']:
        #f = '%s/derivatives/derivative_%s_%s'%(root_results, parameter, suffix_HMF)
        #else:
        #f = '../HMF/HMF_theory/derivatives_dndN/derivative_HMF_rebin_%s_z=0.txt'%parameter
        f = '../HMF/HMF_theory/dndN/derivative_dndN_%s_z=0.txt'%parameter
        N_der, der_HMF = np.loadtxt(f, unpack=True)
        if not(np.allclose(N_der, N, rtol=1e-8, atol=1e-10)):  
            raise Exception('N-values differ in the HMF derivatives!!!')
        #if parameter=='Om':   der_HMF = der_HMF - HMF_fiducial/0.3175
        #if parameter=='Mnu':  der_HMF = der_HMF + HMF_fiducial/(0.3175*93.14*0.6711**2)
        derivat = np.hstack([derivat, der_HMF])

    if do_VSF:  #read the VSF derivatives
        f = '%s/derivatives/derivative_%s_%s'%(root_results, parameter, suffix_VSF)
        R_der, der_VSF = np.loadtxt(f, unpack=True)
        if not(np.allclose(R_der, R, rtol=1e-8, atol=1e-10)):  
            raise Exception('k-values differ in the Pk derivatives!!!')
        derivat = np.hstack([derivat, der_VSF])

    derivative[i] = derivat
###################################################################################

#################################### FISHER #######################################
# compute the Fisher matrix
Fisher = np.zeros((params_num, params_num), dtype=np.float64)
for i in xrange(params_num):
    for j in xrange(i, params_num):
        if i==j:
            Fisher[i,j] = np.dot(derivative[i], np.dot(ICov, derivative[i]))
        else:
            Fisher[i,j] = 0.5*(np.dot(derivative[i], np.dot(ICov, derivative[j])) + \
                               np.dot(derivative[j], np.dot(ICov, derivative[i])))
            Fisher[j,i] = Fisher[i,j]
Fisher *= Volume

CAMB_Fisher = np.array([
    [2.13080592e+05, -1.20573100e+06, 1.48016560e+05, 2.93458548e+04, 
     -2.06713944e+04, -1.65766154e+03],
    [-1.20573100e+06, 1.35133806e+07, -2.18303421e+05, -1.26270926e+04,
     -1.61514959e+04, -5.92496230e+04],
    [ 1.48016560e+05, -2.18303421e+05,  2.03038428e+05, -1.38685185e+04,
      -1.61497519e+04, -1.55300001e+03],
    [ 2.93458548e+04, -1.26270926e+04, -1.38685185e+04,  1.02172866e+05,
      -6.36387231e+03, -5.65461481e+03],
    [-2.06713944e+04, -1.61514959e+04, -1.61497519e+04, -6.36387231e+03,
     2.29958884e+04,  6.30418193e+03],
    [-1.65766154e+03, -5.92496230e+04, -1.55300001e+03, -5.65461481e+03,
     6.30418193e+03,  2.27796421e+03]])

# compute the marginalized error on the parameters
IFisher = np.linalg.inv(Fisher)
for i in xrange(params_num):
    print 'Error on %03s = %.5f'%(parameters[i], np.sqrt(IFisher[i,i]))

# save results to file
fout = 'Fisher_%d_%d'%(realizations_der, realizations_Cov)
if do_Pkm:  fout += '_Pkm_%.2f'%kmax_m
if do_Pkc:  fout += '_Pkc_%.2f'%kmax_c
if do_HMF:  fout += '_HMF_%.1e_%.1e_%d'%(Nmin, Nmax, HMF_bins)
if do_VSF:  fout += '_VSF_%.1e_%.1e_%d_%s'%(Rmin, Rmax, VSF_bins, delete_bins)
fout += '_z=%s.npy'%z
np.save(fout, Fisher)
###################################################################################


