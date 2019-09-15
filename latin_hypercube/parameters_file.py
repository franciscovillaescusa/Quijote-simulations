from mpi4py import MPI
import numpy as np
import sys,os
import camb
from pyDOE import *

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

#################################### INPUT #############################################
dimensions = 5
points     = 2000

# CAMB parameters
hierarchy    = 'degenerate'
Mnu          = 0.0 #eV
Nnu          = 0   #number of massive neutrinos
Neff         = 3.046
As           = 2.13e-9
tau          = None
Omega_k      = 0.0
pivot_scalar = 0.05
pivot_tensor = 0.05
kmax         = 10.0
k_per_logint = 20
redshifts    = [0]

#              [Om,  Ob,   h,   ns,  s8]
Min = np.array([0.1, 0.03, 0.5, 0.8, 0.6])
Max = np.array([0.5, 0.07, 0.9, 1.2, 1.0])

# whether generate standard or paired fixed simulations
standard = True
########################################################################################

# get latin hypercube
np.random.seed(1)
coords = lhs(dimensions, samples=points, criterion='c')

# check if the generated parameters are the same as the saved ones
params = np.loadtxt('latin_hypercube_params.txt')
equal  = (Min + coords*(Max-Min))==params
if np.any(equal==False):  
    raise Exception('Cosmological parameters are different!!!')
#np.savetxt('latin_hypercube_params.txt', Min+coords*(Max-Min))


# get the numbers each cpu will work on
numbers = np.where(np.arange(points)%nprocs==myrank)[0]


# do a loop over all the points in the latin hypercube
for i in numbers:

    # create output folder in case it does not exists
    folder = '%s/'%i
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    # create initial conditions folder if it does not exists
    folder_ICs = '%s/ICs'%i 
    if not(os.path.exists(folder_ICs)):  os.system('mkdir %s'%folder_ICs)

    # find the values of the cosmological parameters
    coord = Min + coords[i]*(Max-Min)

    Omega_m = coord[0]
    Omega_b = coord[1]
    h       = coord[2]
    ns      = coord[3]
    s8      = coord[4]

    g = open('%s/Cosmo_params.dat'%folder, 'w')
    g.write('%.5f %.5f %.5f %.5f %.5f\n'%(Omega_m, Omega_b, h, ns, s8))
    g.close()

    print 'realization %d'%i
    print 'Omega_m = %.4f'%Omega_m
    print 'Omega_b = %.4f'%Omega_b
    print 'h       = %.4f'%h
    print 'ns      = %.4f'%ns
    print 's8      = %.4f'%s8

    ##### run CAMB #####
    Omega_c  = Omega_m - Omega_b
    pars     = camb.CAMBparams()

    # set accuracy of the calculation
    pars.set_accuracy(AccuracyBoost=5.0, lSampleBoost=5.0, lAccuracyBoost=5.0, 
                      HighAccuracyDefault=True, DoLateRadTruncation=True)

    # set value of the cosmological parameters
    pars.set_cosmology(H0=h*100.0, ombh2=Omega_b*h**2, omch2=Omega_c*h**2, 
                       mnu=Mnu, omk=Omega_k, neutrino_hierarchy=hierarchy, 
                       num_massive_neutrinos=Nnu, nnu=Neff, tau=tau)
                   
    # set the value of the primordial power spectrum parameters
    pars.InitPower.set_params(As=As, ns=ns, 
                              pivot_scalar=pivot_scalar, pivot_tensor=pivot_tensor)

    # set redshifts, k-range and k-sampling
    pars.set_matter_power(redshifts=redshifts, kmax=kmax, k_per_logint=k_per_logint)

    # compute results
    results = camb.get_results(pars)

    # save parameter values to file
    f = open('%s/CAMB.params'%folder,'w');  f.write('%s'%pars);  f.close()

    # interpolate to get Pmm, Pcc...etc
    k, zs, Pkmm = results.get_matter_power_spectrum(minkh=2e-5, maxkh=kmax, 
                                                    npoints=400, var1=7, var2=7, 
                                                    have_power_spectra=True, 
                                                    params=None)

    # do a loop over all redshifts
    for j,z in enumerate(zs):
        fout = '%s/Pk_mm_z=%.3f.txt'%(folder_ICs,z)
        np.savetxt(fout, np.transpose([k,Pkmm[j,:]]))




    ########################## write 2LPT parameter file #######################
    # parameter file for standard simulations
    a="""
    Nmesh            1024      
    Nsample          512       
    Box              1000000.0   
    FileBase         ics         
    OutputDir        ./ICs/          
    GlassFile        ../../2lpt/GLASS/dummy_glass_dmonly_64.dat 
    GlassTileFac     8         
    Omega            %.4f    
    OmegaLambda      %.4f    
    OmegaBaryon      0.0000    
    OmegaDM_2ndSpecies  0.0    
    HubbleParam      %.4f    
    Redshift         127       
    Sigma8           %.4f       
    SphereMode       0         
    WhichSpectrum    2         
    FileWithInputSpectrum   ./ICs/Pk_mm_z=0.000.txt
    InputSpectrum_UnitLength_in_cm  3.085678e24 
    ShapeGamma       0.201     
    PrimordialIndex  1.0       
    
    Phase_flip          0      
    RayleighSampling    1      
    Seed                %d      
    
    NumFilesWrittenInParallel 8  
    UnitLength_in_cm          3.085678e21  
    UnitMass_in_g             1.989e43     
    UnitVelocity_in_cm_per_s  1e5          
    
    WDM_On               0      
    WDM_Vtherm_On        0      
    WDM_PartMass_in_kev  10.0   
    """%(Omega_m, 1.0-Omega_m, h, s8, i)

    # parameter file for paired fixed simulations
    b="""  
    Nmesh            1024      
    Nsample          512       
    Box              1000000.0   
    FileBase         ics         
    OutputDir        ./ICs/          
    GlassFile        ../../2lpt/GLASS/dummy_glass_dmonly_64.dat 
    GlassTileFac     8         
    Omega            %.4f    
    OmegaLambda      %.4f    
    OmegaBaryon      0.0000    
    OmegaDM_2ndSpecies  0.0    
    HubbleParam      %.4f    
    Redshift         127       
    Sigma8           %.4f       
    SphereMode       0         
    WhichSpectrum    2         
    FileWithInputSpectrum   ./ICs/Pk_mm_z=0.000.txt
    InputSpectrum_UnitLength_in_cm  3.085678e24 
    ShapeGamma       0.201     
    PrimordialIndex  1.0       
    
    Phase_flip          0      
    RayleighSampling    0      
    Seed                467      
    
    NumFilesWrittenInParallel 8  
    UnitLength_in_cm          3.085678e21  
    UnitMass_in_g             1.989e43     
    UnitVelocity_in_cm_per_s  1e5          
    
    WDM_On               0      
    WDM_Vtherm_On        0      
    WDM_PartMass_in_kev  10.0   
    """%(Omega_m, 1.0-Omega_m, h, s8)
    
    # save parameters to file
    f = open('%s/2LPT.param'%folder_ICs, 'w')
    if standard:  f.write(a)
    else:         f.write(b)
    f.close()
    #############################################################################

    ####################### write Gadget3 parameter file ########################

    a="""InitCondFile              ./ICs/ics
    OutputDir                 ./
    OutputListFilename        ../../times.txt
    NumFilesPerSnapshot       8
    NumFilesWrittenInParallel 8
    CpuTimeBetRestartFile     10800.0   
    TimeLimitCPU              10000000  
    ICFormat                  1
    SnapFormat                3
    TimeBegin                 0.0078125     
    TimeMax	              1.00          
    Omega0	              %.4f    
    OmegaLambda               %.4f
    OmegaBaryon               0.0000     
    HubbleParam               %.4f     
    BoxSize                   1000000.0

    SofteningGas              0.0
    SofteningHalo             50.0   
    SofteningDisk             0.0
    SofteningBulge            0.0
    SofteningStars            0.0
    SofteningBndry            0.0
    SofteningGasMaxPhys       0.0
    SofteningHaloMaxPhys      50.0
    SofteningDiskMaxPhys      0.0
    SofteningBulgeMaxPhys     0.0
    SofteningStarsMaxPhys     0.0
    SofteningBndryMaxPhys     0.0

    PartAllocFactor           2.5  
    MaxMemSize	              3800
    BufferSize                120
    CoolingOn                 0
    StarformationOn           0

    TypeOfTimestepCriterion   0   	                    
    ErrTolIntAccuracy         0.025  
    MaxSizeTimestep           0.025
    MinSizeTimestep           0.0

    ErrTolTheta               0.5
    TypeOfOpeningCriterion    1
    ErrTolForceAcc            0.005
    TreeDomainUpdateFrequency 0.01
 
    DesNumNgb                 33
    MaxNumNgbDeviation        2
    ArtBulkViscConst          1.0
    InitGasTemp               273.0  
    MinGasTemp                10.0    
    CourantFac                0.15
    ComovingIntegrationOn     1    
    PeriodicBoundariesOn      1    
    MinGasHsmlFractional      0.1  
    OutputListOn              1    
    TimeBetSnapshot           1.   
    TimeOfFirstSnapshot       1.   
    TimeBetStatistics         0.5  
    MaxRMSDisplacementFac     0.25 
    EnergyFile                energy.txt
    InfoFile                  info.txt
    TimingsFile               timings.txt
    CpuFile                   cpu.txt
    TimebinFile               Timebin.txt
    SnapshotFileBase          snap
    RestartFile               restart
    ResubmitOn                0
    ResubmitCommand           /home/vspringe/autosubmit
    UnitLength_in_cm          3.085678e21      
    UnitMass_in_g             1.989e43         
    UnitVelocity_in_cm_per_s  1e5              
    GravityConstantInternal   0
    """%(Omega_m, 1.0-Omega_m, h)

    f = open('%s/G3.param'%folder, 'w');  f.write(a);  f.close()
    #############################################################################
