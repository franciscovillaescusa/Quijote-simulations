import numpy as np
import sys,os


##################################### INPUT ############################################
root_2LPT = '/simons/scratch/fvillaescusa/pdf_information/Pk/matter/fiducial/'
root_ZA   = '/simons/scratch/fvillaescusa/pdf_information/Pk/matter/fiducial_ZA/'
realizations = 100
bins         = 886

BoxSize = 1000.0 #Mpc/h
########################################################################################

# do a loop over the different redshifts
for z in [0, 0.5, 1, 2, 3]:

    ################ REAL-SPACE ###############
    Pk_2LPT = np.zeros((realizations,bins), dtype=np.float64)
    Pk_ZA   = np.zeros((realizations,bins), dtype=np.float64)

    # do a loop over the different realizations
    for i in xrange(realizations):
        f1 = '%s/%d/Pk_m_z=%s.txt'%(root_2LPT,i,z)
        f2 = '%s/%d/Pk_m_z=%s.txt'%(root_ZA,  i,z)

        # read the two power spectra
        k, Pk_2LPT[i] = np.loadtxt(f1, unpack=True)
        k, Pk_ZA[i]   = np.loadtxt(f2, unpack=True)

    Pk_2LPT = np.mean(Pk_2LPT, axis=0)
    Pk_ZA   = np.mean(Pk_ZA,   axis=0)

    np.savetxt('mean_Pk_m_2LPT_z=%s.txt'%z, np.transpose([k, Pk_2LPT]))
    np.savetxt('mean_Pk_m_ZA_z=%s.txt'%z,   np.transpose([k, Pk_ZA]))


    ################ REDSHIFT-SPACE ###############
    Pk_2LPT = np.zeros((3*realizations,bins), dtype=np.float64)
    Pk_ZA   = np.zeros((3*realizations,bins), dtype=np.float64)

    # do a loop over the different realizations
    j = 0
    for i in xrange(realizations):

        # do a loop over the different RSD axes
        for axis in [0,1,2]:
            f1 = '%s/%d/Pk_m_RS%d_z=%s.txt'%(root_2LPT,i,axis,z)
            f2 = '%s/%d/Pk_m_RS%d_z=%s.txt'%(root_ZA,  i,axis,z)
        
            # read the two power spectra
            k,Pk_2LPT[j],a,b=np.loadtxt(f1, unpack=True)
            k,Pk_ZA[j],a,b  =np.loadtxt(f2, unpack=True)
            j += 1

    Pk_2LPT = np.mean(Pk_2LPT, axis=0)
    Pk_ZA   = np.mean(Pk_ZA,   axis=0)

    np.savetxt('mean_Pk_m_RS_2LPT_z=%s.txt'%z, np.transpose([k, Pk_2LPT]))
    np.savetxt('mean_Pk_m_RS_ZA_z=%s.txt'%z,   np.transpose([k, Pk_ZA]))
