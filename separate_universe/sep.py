#!/usr/bin/env python3

import sys
import numpy as np
from scipy.integrate import odeint


fid_times = np.array([1/4, 1/3, 1/2, 2/3, 1])


fid_param = dict(
            Np = 512,
            boxsize = 1000.,
            Om = 0.3175,
            Oc = 0.2685,
            Ob = 0.049,
            OL = 0.6825,
            Ok = 0.,
            h0 = 0.6711,
            H0 = 67.11,
            time_end = fid_times[-1],
        )


def main():
    delta_b = float(sys.argv[1])
    i = int(sys.argv[2])

    SU_param, SU_times = get_SU(delta_b, fid_param, fid_times)
    seed_ICs(i, SU_param)

    write_param_files(SU_param, SU_times)


def get_SU(delta_b, param, times):
    SU_param = param.copy()

    D0 = linear_growth([1.], param).squeeze()
    phi = 5 / 6 * param['Om'] * delta_b / D0
    SU_param['Om'] *= 1 + 2 * phi
    SU_param['Oc'] *= 1 + 2 * phi
    SU_param['Ob'] *= 1 + 2 * phi
    SU_param['OL'] *= 1 + 2 * phi
    SU_param['Ok'] = - 2 * phi
    SU_param['h0'] *= 1 - phi
    SU_param['H0'] = SU_param['h0'] * 100

    SU_param['boxsize'] *= 1 - phi

    D = linear_growth(times, param)
    SU_times = times * (1 - D / D0 * delta_b / 3)
    SU_param['time_end'] = SU_times[-1]

    return SU_param, SU_times


def seed_ICs(i, param):
    param['seed'] = 10 * i + 5


def write_param_files(param, times):
    with open('2lpt.param', 'w') as f:
        f.write(temp_2lpt.format(**param))

    with open('gadget.param', 'w') as f:
        f.write(temp_gadget.format(**param))

    with open('camb.param', 'w') as f:
        f.write(temp_camb.format(**param))

    with open('times.txt', 'w') as f:
        f.write('\n'.join(str(a) for a in times[:-1]))


def linear_growth(times, param):
    ai = 1e-3 * times[0]
    Di = ai
    Fi = Di
    yi = [Di, Fi]
    lna = [np.log(ai)] + list(np.log(times))

    y = odeint(growthEqns, yi, lna, args=(param,), atol=0)
    y = y[1:]
    D, F = y.T

    return D


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


temp_2lpt = \
"""Nmesh           {Np}
Nsample         {Np}
Box             {boxsize}
FileBase        ics
OutputDir       ./
GlassFile       ../../single_particle.glass
GlassTileFac    {Np}
Omega           {Om}
OmegaLambda     {OL}
OmegaBaryon     {Ob}
OmegaDM_2ndSpecies  0
HubbleParam     {h0}
Redshift        127
SphereMode      0
WhichSpectrum   2
FileWithInputSpectrum   ../../matterpower.txt
InputSpectrum_UnitLength_in_cm  3.085678e24
ShapeGamma          0.21
PrimordialIndex     1.000
Phase_flip          0
RayleighSampling    1
Seed                {seed}
NumFilesWrittenInParallel   64
UnitLength_in_cm    3.085678e24
UnitMass_in_g       1.989e43
UnitVelocity_in_cm_per_s    1e5
WDM_On              0
WDM_Vtherm_On       0
WDM_PartMass_in_kev 10.0
"""


temp_gadget = \
"""InitCondFile    path/to/ics_file
OutputDir       path/to/out_dir
EnergyFile      energy.txt
InfoFile        info.txt
TimingsFile     timings.txt
CpuFile         cpu.txt
RestartFile     restart
SnapshotFileBase    snapshot
TimeLimitCPU    86400
ResubmitOn      0
ResubmitCommand ./resub.sh
MaxMemSize      1500
CpuTimeBetRestartFile   82800
ICFormat        1
SnapFormat      1
TimeBegin       0.0078125
TimeMax         {time_end}
Omega0          {Om}
OmegaLambda     {OL}
OmegaBaryon     {Ob}
HubbleParam     {h0}
BoxSize         {boxsize}
Softening           0.05300
SofteningMaxPhys    0.05300
OutputListFilename  ./times.txt
OutputListOn        1
TimeBetSnapshot     0
TimeOfFirstSnapshot 0
TimeBetStatistics   0.1
NumFilesWrittenInParallel   2
ErrTolIntAccuracy           0.025
MaxRMSDisplacementFac       0.2
MaxSizeTimestep     0.025
MinSizeTimestep     0.0
ErrTolTheta         0.5
TypeOfOpeningCriterion  1
ErrTolForceAcc      0.002
PartAllocFactor     2
TreeAllocFactor     0.9
BufferSize          150
UnitLength_in_cm    3.085678e24
UnitMass_in_g       1.989e43
UnitVelocity_in_cm_per_s    1e5
GravityConstantInternal     0
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


if __name__ == '__main__':
    main()
