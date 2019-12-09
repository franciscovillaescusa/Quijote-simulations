#!/usr/bin/env python3

import sys
import numpy as np
from scipy.integrate import odeint


fid_times = np.array([1/4, 1/3, 1/2, 2/3, 1])


fid_param = dict(
            Np = 512,
            boxsize = 1000.,
            Om = 0.3175,
            Ob = 0.,
            OL = 0.6825,
            h0 = 0.6711,
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
    SU_param['Ob'] *= 1 + 2 * phi
    SU_param['OL'] *= 1 + 2 * phi
    SU_param['h0'] *= 1 - phi

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


if __name__ == '__main__':
    main()
