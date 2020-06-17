import numpy as np
from scipy.integrate import odeint
import sys,os

temp_2LPT = \
"""
Nmesh            {Nm}      % This is the size of the FFT grid used to
                           % compute the displacement field. One
                           % should have Nmesh >= Nsample.

Nsample          {Ns}       % sets the maximum k that the code uses,
                           % i.e. this effectively determines the
                           % Nyquist frequency that the code assumes,
                           % k_Nyquist = 2*PI/Box * Nsample/2
                           % Normally, one chooses Nsample such that
                           % Ntot =  Nsample^3, where Ntot is the
                           % total number of particles


Box              {boxsize}      % Periodic box size of simulation

FileBase         ics            % Base-filename of output files
OutputDir        ./ICs/         % Directory for output

GlassFile        /simons/scratch/fvillaescusa/pdf_information/ICs_codes/2lpt/GLASS/dummy_glass_dmonly_64.dat  % Glass-File
GlassTileFac     {glass_fac}                % Number of times the glass file is
                                  % tiled in each dimension (must be
                                  % an integer)


Omega            {Om}    % Total matter density  (at z=0)
OmegaLambda      {OL}    % Cosmological constant (at z=0)
OmegaBaryon      0.0000    % Baryon density        (at z=0)
OmegaDM_2ndSpecies  0.0    % Omega for a second dark matter species (at z=0)
HubbleParam      {h0}    % Hubble paramater (may be used for power spec parameterization)

Redshift         127       % Starting redshift
Sigma8           1.0       % power spectrum normalization at z=0
Sigma8_rescaling  0        % 0 will ignore the value of Sigma8. 1 will modify the
		  	   % amplitude of the input Pk to match Sigma8


SphereMode       0         % if "1" only modes with |k| < k_Nyquist are
                           % used (i.e. a sphere in k-space), otherwise
			   % modes with
                           % |k_x|,|k_y|,|k_z| < k_Nyquist are used
                           % (i.e. a cube in k-space)


WhichSpectrum    2         % "1" selects Eisenstein & Hu spectrum,
		           % "2" selects a tabulated power spectrum in
                           % the file 'FileWithInputSpectrum'
                           % otherwise, Efstathiou parametrization is used


FileWithInputSpectrum   ../CAMB_TABLES/CAMB_matterpow_0.dat  % filename of tabulated MATTER powerspectrum from CAMB


InputSpectrum_UnitLength_in_cm  3.085678e24 % defines length unit of tabulated
                                            % input spectrum in cm/h.
                                            % Note: This can be chosen different
					    % from UnitLength_in_cm


ShapeGamma       0.201     % only needed for Efstathiou power spectrum
PrimordialIndex  1.0       % may be used to tilt the primordial index
		 	   % (one if tabulated)

Phase_flip          0         % flip phase 0-no 1-yes for paired simulations)
RayleighSampling    1         % whether sampling modes amplitude (1) or not (0)
Seed                {seed}         %  seed for IC-generator


NumFilesWrittenInParallel 32  % limits the number of files that are
                              % written in parallel when outputting


UnitLength_in_cm          3.085678e21  % define output length unit (in cm/h)
UnitMass_in_g             1.989e43     % define output mass unit (in g/cm)
UnitVelocity_in_cm_per_s  1e5          % define output velocity unit (in cm/sec)



WDM_On               0      % Putting a '1' here will enable a WDM small-scale
                            % smoothing of the power spectrum

WDM_Vtherm_On        0      % If set to '1', the (warm) dark matter particles
		     	    % will receive an additional random thermal velocity
                            % corresponding to their particle mass

WDM_PartMass_in_kev  10.0   % This is the particle mass in keV of the WDM
		     	    % particle
"""

temp_G3 = \
"""
InitCondFile        ./ICs/ics
OutputDir           ./
OutputListFilename  ../times.txt
%DarkEnergyFile      ../ICs/Hz.txt

CpuTimeBetRestartFile  10800.0   % seconds
TimeLimitCPU           10000000  % seconds

ICFormat     1
SnapFormat   3

NumFilesPerSnapshot       8
NumFilesWrittenInParallel 8

TimeBegin           0.0078125     % z=99
TimeMax	            {time_end}    % end at z=0

Omega0	            {Om}    % total matter density
OmegaLambda         {OL}
OmegaBaryon         0.0     ; maybe there are no baryons
HubbleParam         {h0}    ; only needed for cooling

BoxSize             {boxsize}

SofteningGas           0.0
SofteningHalo          50.0
SofteningDisk          0.0
SofteningBulge         0.0
SofteningStars         0.0
SofteningBndry         0.0

SofteningGasMaxPhys    0.0
SofteningHaloMaxPhys   50.0
SofteningDiskMaxPhys   0.0
SofteningBulgeMaxPhys  0.0
SofteningStarsMaxPhys  0.0
SofteningBndryMaxPhys  0.0

PartAllocFactor        2.5
MaxMemSize	       3800
BufferSize             120

%Time_tree_on_nu        0.09  % tree ON for neutrinos for a<Time_tree_on_nu

CoolingOn       0
StarformationOn 0




%%%%%% Accuracy of time integration %%%%%%%

TypeOfTimestepCriterion  0
ErrTolIntAccuracy        0.025
MaxSizeTimestep          0.025
MinSizeTimestep          0.0


%%%%%%% Tree algorithm and force accuracy %%%%%%%

ErrTolTheta                  0.5
TypeOfOpeningCriterion       1
ErrTolForceAcc               0.005
TreeDomainUpdateFrequency    0.01


%%%%%%%% subfind %%%%%%%%%%

%DesLinkNgb              20
%ErrTolThetaSubfind      0.45


%%%%%%%% Parameters of SPH %%%%%%%%

DesNumNgb           33
MaxNumNgbDeviation  2
ArtBulkViscConst    1.0
InitGasTemp         273.0  % initial gas temp in K, only used if not in ICs
MinGasTemp          10.0
CourantFac          0.15

%%%%%%%%% Star formation and winds %%%%%%%%%%

%CritPhysDensity                    0
%MaxSfrTimescale                    1.5
%CritOverDensity                    1000.0
%TempSupernova                      1e+08
%TempClouds                         1000
%FactorSN                           0.1
%FactorEVP                          1000
%WindEfficiency                     2
%WindFreeTravelLength               20
%WindEnergyFraction                 1
%WindFreeTravelDensFac              0.1


%%%%%%%% miscelanous %%%%%%%%

ComovingIntegrationOn   1    % comoving (1) or physical (0)
PeriodicBoundariesOn    1    % boundary conditions (1) or not (0)
MinGasHsmlFractional    0.1  % min gas SPH in units of the grav softening
OutputListOn            1    % snapshots a values in external file
TimeBetSnapshot         1.   % not used if OutputListOn 1
TimeOfFirstSnapshot     1.   % not used if OutputListOn 1
TimeBetStatistics       0.5  % time interval to compute system potential energy
MaxRMSDisplacementFac   0.25 % limits the PM time step


%%%%%%%%% output files  %%%%%%%%%%

EnergyFile        energy.txt
InfoFile          info.txt
TimingsFile       timings.txt
CpuFile           cpu.txt
TimebinFile       Timebin.txt
SnapshotFileBase  snap
RestartFile       restart


%%%%%%%% Resubmission %%%%%%%%%

ResubmitOn        0
ResubmitCommand   /home/vspringe/autosubmit


%%%%%%%%% Linear response neutrinos %%%%%%%%%%

%OmegaBaryonCAMB    0.049
%KspaceTransferFunction    ./CAMB_TABLES/ics_transfer_99.dat
%TimeTransfer       0.01
%InputSpectrum_UnitLength_in_cm  3.085678e24
%MNue               0.3
%MNum               0.3
%MNut               0.3


%%%%%%%% System of units %%%%%%%%

UnitLength_in_cm         3.085678e21        ;  1.0 kpc
UnitMass_in_g            1.989e43           ;  1.0e10 solar masses
UnitVelocity_in_cm_per_s 1e5                ;  1 km/sec
GravityConstantInternal  0
"""

temp_camb = \
"""output_root = CAMB
get_scalar_cls = F
get_vector_cls = F
get_tensor_cls = F
CMB_outputscale = 7.4311e12
get_transfer = T
accuracy_boost = 1
l_accuracy_boost = 1
high_accuracy_default =  T
do_nonlinear = 0
w = -1
cs2_lam = 1
hubble = {H0}
use_physical = F
omega_baryon = {Ob}
omega_cdm = {Oc}
omega_lambda = {OL}
omega_neutrino = 0.0
temp_cmb = 2.725
helium_fraction = 0.24
massless_neutrinos = 3.046
nu_mass_eigenstates = 1
massive_neutrinos = 0
transfer_high_precision = T
transfer_kmax = 500
transfer_k_per_logint = 50
transfer_num_redshifts = 11
transfer_interp_matterpower = F
transfer_power_var =            7
transfer_redshift(1) = 127
transfer_filename(1) = transfer_127.dat
transfer_matterpower(1) = matterpow_127.dat
transfer_redshift(2) = 99
transfer_filename(2) = transfer_99.dat
transfer_matterpower(2) = matterpow_99.dat
transfer_redshift(3) = 49
transfer_filename(3) = transfer_49.dat
transfer_matterpower(3) = matterpow_49.dat
transfer_redshift(4) = 24
transfer_filename(4) = transfer_24.dat
transfer_matterpower(4) = matterpow_24.dat
transfer_redshift(5) = 9
transfer_filename(5) = transfer_9.dat
transfer_matterpower(5) = matterpow_9.dat
transfer_redshift(6) = 4
transfer_filename(6) = transfer_4.dat
transfer_matterpower(6) = matterpow_4.dat
transfer_redshift(7) = 3
transfer_filename(7) = transfer_3.dat
transfer_matterpower(7) = matterpow_3.dat
transfer_redshift(8) = 2
transfer_filename(8) = transfer_2.dat
transfer_matterpower(8) = matterpow_2.dat
transfer_redshift(9) = 1
transfer_filename(9) = transfer_1.dat
transfer_matterpower(9) = matterpow_1.dat
transfer_redshift(10) = 0.5
transfer_filename(10) = transfer_0.5.dat
transfer_matterpower(10) = matterpow_0.5.dat
transfer_redshift(11) = 0
transfer_filename(11) = transfer_0.dat
transfer_matterpower(11) = matterpow_0.dat
DebugParam =   0.000000000000000E+000
Alens =    1.00000000000000
reionization = T
re_use_optical_depth = T
re_optical_depth = 0.0925
re_delta_redshift = 0.5
re_ionization_frac = -1
re_helium_redshift =    3.50000000000000
re_helium_delta_redshift =   0.500000000000000
re_helium_redshiftstart =    5.00000000000000
pivot_scalar = 0.05
pivot_tensor = 0.05
initial_power_num = 1
scalar_spectral_index(1) = 0.9624
scalar_nrun(1) = 0
scalar_nrunrun(1) =   0.000000000000000E+000
scalar_amp(1) = 2.13e-09
RECFAST_fudge_He = 0.86
RECFAST_Heswitch = 6
RECFAST_Hswitch = T
RECFAST_fudge = 1.14
AGauss1 =  -0.140000000000000
AGauss2 =   7.900000000000000E-002
zGauss1 =    7.28000000000000
zGauss2 =    6.73000000000000
wGauss1 =   0.180000000000000
wGauss2 =   0.330000000000000
do_lensing_bispectrum =  F
do_primordial_bispectrum =  F
initial_condition = 1
accurate_polarization = T
accurate_reionization = T
accurate_BB = F
derived_parameters =  T
version_check = Jan17
do_late_rad_truncation = T
feedback_level = 1
output_file_headers =  T
massive_nu_approx = 3
number_of_threads = 0
use_spline_template =  T
l_sample_boost = 1
"""

# This function returns the growths given a cosmology and a scale factor
def growthEqns(y, lna, param):
    Om, OL, w = param['Om'], param['OL'], -1
    OK = 1 - Om - OL

    D, F = y
    a = np.exp(lna)
    a3w = a**(-3*w)
    Hfac = - 0.5 * (Om+2*OK*a+(1-3*w)*OL*a3w) / (Om+OK*a+OL*a3w)
    Ofac = 1.5 * Om / (Om+OK*a+OL*a3w)
    Dp = F
    Fp = Hfac * F + Ofac * D

    return Dp, Fp

# This routine computes the growth factor given a cosmology and a scale factor,
# normalized to the scale factor at matter dominated era
def linear_growth(a, param):
    ai = 1e-3 * a
    Di = ai
    Fi = Di
    yi = [Di, Fi]
    lna = np.log([ai, a])

    y = odeint(growthEqns, yi, lna, args=(param,), atol=0)
    D, F = y[-1]

    return D

# This function returns delta_a = a_SU(t) / a(t) - 1 given scale factor & cosmology
def daEqns(y, lna, param):
    Om, OL, w = param['Om'], param['OL'], -1
    OK = 1 - Om - OL

    y1, y2 = y
    a = np.exp(lna)
    a3w = a**(-3*w)
    Hfac = - 0.5 * (Om+2*OK*a+(1-3*w)*OL*a3w) / (Om+OK*a+OL*a3w)
    Ofac = 0.5 * Om / (Om+OK*a+OL*a3w)
    y1p = y2
    y2p = Hfac * y2 + Ofac * y1 * (3+y1*(3+y1)) / (1 + y1)**2

    return y1p, y2p

# This routine computes a_SU(a) given DC mode, scale factors, and cosmology
def aSU(delta_b, times, param):
    ai = 1e-3 * times[0]  # push it to matter dominated era
    y1i = - 1/3 * delta_b * ai / linear_growth(1, param)  # a_SU / a - 1
    y2i = y1i  # y2 = d y1 / d lna
    yi = [y1i, y2i]
    lna = [np.log(ai)] + list(np.log(times))

    y = odeint(daEqns, yi, lna, args=(param,), atol=0)
    return times * (1 + y[1:, 0])

# This routine computes the value of the cosmological parameters, box size and scale
# factor given the value of the DC mode
# Note that the DC mode should be in its linear value
def get_SU(delta_b, param, times):
    SU_param = param.copy()

    D0 = linear_growth(1., param)
    dlnH2 = - 5 / 3 * param['Om'] * delta_b / D0  # delta(H^2) / H^2
    dlnH = np.sqrt(1 + dlnH2) - 1  # delta(H) / H

    SU_param['Om'] /= 1 + dlnH2
    SU_param['Oc'] /= 1 + dlnH2
    SU_param['Ob'] /= 1 + dlnH2
    SU_param['OL'] /= 1 + dlnH2
    SU_param['Ok'] = dlnH2 / (1 + dlnH2)
    SU_param['h0'] *= 1 + dlnH
    SU_param['H0'] = SU_param['h0'] * 100

    SU_param['boxsize'] *= 1 + dlnH

    SU_times = aSU(delta_b, times, param)
    SU_param['time_end'] = SU_times[-1]

    return SU_param, SU_times

######################################## INPUT #########################################
root = '/simons/scratch/fvillaescusa/pdf_information/Snapshots'

# scale factors to write snapshots
fiducial_times = np.array([1/4, 1/3, 1/2, 2/3, 1])

# fiducial parameter values
fiducial_params = dict(Nm = 1024,
                       Ns = 512,
                       boxsize = 1000000.0,
                       glass_fac = 8,
                       s8 = 0.834,
                       Om = 0.3175,
                       Oc = 0.2685,
                       Ob = 0.049,
                       OL = 0.6825,
                       Ok = 0.,
                       h0 = 0.6711,
                       H0 = 67.11,
                       time_end = fiducial_times[-1])

# DC mode overdensity amplitudes
delta_bs = [-0.035, 0.035]

# number of realizations
realizations = 500
########################################################################################

# do a loop over the two different cosmologies
for delta_b in delta_bs:

    print(delta_b)
    if delta_b>0:  folder = '%s/DC_p'%root
    else:          folder = '%s/DC_m'%root
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    # get the parameters of the Separate Universe cosmology
    SU_param, SU_times = get_SU(delta_b, fiducial_params, fiducial_times)

    # write CAMB parameter file
    folder_CAMB = '%s/CAMB_TABLES'%folder
    if not(os.path.exists(folder_CAMB)):  os.system('mkdir %s'%folder_CAMB)
    f_CAMB = '%s/CAMB_params.ini'%folder_CAMB
    with open(f_CAMB, 'w') as f:
        f.write(temp_camb.format(**SU_param))

    # write file with snapshot times
    with open('%s/times.txt'%folder, 'w') as f:
        f.write('\n'.join(str(a) for a in SU_times[:-1]))

    # write Gadget3 parameter file
    with open('%s/G3.param'%folder, 'w') as f:
        f.write(temp_G3.format(**SU_param))

    # do a loop over all realizations
    for i in range(realizations):

        # find the value of the random seed
        SU_param['seed'] = 10*i + 5

        # find the name of the folder containing the realization
        folder_real = '%s/%d'%(folder,i)
        if not(os.path.exists(folder_real)):  os.system('mkdir %s'%folder_real)

        # find the name of the ICs folder
        folder_ICs = '%s/ICs'%(folder_real)
        if not(os.path.exists(folder_ICs)):  os.system('mkdir %s'%folder_ICs)

        # write 2LPT parameter file
        with open('%s/2LPT.param'%folder_ICs, 'w') as f:
            f.write(temp_2LPT.format(**SU_param))
