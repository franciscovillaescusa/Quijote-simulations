import numpy as np
from scipy.integrate import odeint
import sys, os
from SU_utils import SU_utils

#--------------------------------------#
# Generates input files for
#     CAMB, 2LPT, Gadget-4
#
# Folder structure :
#     root/
#       CAMB/
#       { abs(delta_b)<p/m> }/
#         2LPT/
#         G4/
#         slurm/
#--------------------------------------#

# read the template files
with open('temp_2LPT.txt', 'r') as f :
    temp_2LPT = eval('"""'+f.read()+'"""')

with open('temp_G4.txt', 'r') as f :
    temp_G4 = eval('"""'+f.read()+'"""')

with open('temp_camb.txt', 'r') as f :
    temp_camb = eval('"""'+f.read()+'"""')

with open('temp_sbatch.txt', 'r') as f :
    temp_sbatch = eval('"""'+f.read()+'"""')


######################################## INPUT #########################################

root = '/projects/QUIJOTE/Leander/SU/CAMELS_like/CV'

# scale factors to write snapshots
# fiducial_times = np.linspace(0.01, 1.0, num=60) 
fiducial_times = np.array([1/4, 1/3, 1/2, 2/3, 1])

# fiducial parameter values
fiducial_params = dict(IC_Nm = 512, # mesh elements (2xNs is good)
                       IC_Ns = 256, # particle number
                       IC_glass_fac = 4, # Ns = fac * 64
                       boxsize = 25000.0, # 25 Mpc
                       Om = 0.3,
                       h0 = 0.6711,
                       H0 = 67.11,
                       Ob = 0.049,
                       OL = 0.7,
                       Oc = 0.251,
                       Ok = 0.0,
                       s8 = 0.8000, # derived parameter from As=2.136e-9
                       time_end = fiducial_times[-1])

seeds = [ii + 2 for ii in range(10)]
delta_bs = [0.1, 0.2, 0.5, 0.8, 1.2]

########################################################################################

# produce the matter power spectrum at the fiducial cosmology
folder_CAMB = '%s/CAMB'%root
os.system('mkdir -p %s'%folder_CAMB)
fiducial_params['folder_CAMB'] = folder_CAMB
f_CAMB = '%s/CAMB_params.ini'%folder_CAMB
log_CAMB = '%s/CAMB_output.txt'%folder_CAMB
with open(f_CAMB, 'w') as f :
    f.write(temp_camb.format(**fiducial_params))
os.system('bash run_camb.sh %s %s'%(f_CAMB, log_CAMB))

# prepare array for easy submission
slurm_scripts = []


# do a loop over the different ICs
for seed in seeds :

    # do a loop over the different cosmologies
    for delta_b in delta_bs :

        this_root = '%s/seed%d'%(root, seed)
        fiducial_params['IC_seed'] = seed

        # get the parameters of the Separate Universe cosmology
        SU_param, SU_times = SU_utils.get_SU(delta_b, fiducial_params, fiducial_times)

        print(delta_b)
        folder = '%s/%.8f%s'%(this_root, abs(delta_b), 'm' if delta_b < 0 else 'p')
        os.system('mkdir -p %s'%folder)

        folder_G4 = '%s/G4'%folder
        os.system('mkdir -p %s'%folder_G4)

        folder_2LPT = '%s/2LPT'%folder
        os.system('mkdir -p %s'%folder_2LPT)

        # rescale the matter power spectrum
        k, P = np.loadtxt('%s/CAMB_matterpow_0.dat'%folder_CAMB, unpack=True)
        k *= fiducial_params['h0'] / SU_param['h0']
        P *= (SU_param['h0'] / fiducial_params['h0'])**3
        P *= (SU_utils.linear_growth(1, SU_param)
              / SU_utils.linear_growth(1, fiducial_params))**2
        SU_param['IC_CAMB_Pk']   = '%s/CAMB_matterpow_0_headerremoved.dat'%folder_CAMB
        np.savetxt(SU_param['IC_CAMB_Pk'], np.stack([k,P], axis=1))

        # write Gadget4 times file
        with open('%s/times.txt'%folder_G4, 'w') as f :
            # LFT removed [:-1] from SU_times to hopefully get halo catalog at z=0
            f.write('\n'.join(str(a) for a in SU_times))

        # add specifics for Gadget-4
        SU_param['G4_ics_file'] = '%s/ics'%folder_2LPT
        SU_param['G4_SU_scale_file'] = '%s/SU_scale_file.dat'%folder_G4
        # write the scale file (for linking length)
        a_global = np.linspace(0.95*fiducial_times[0], 1.05*fiducial_times[-1], num=10000)
        a_SU = SU_utils.aSU(delta_b, a_global, fiducial_params)
        # this is perhaps paranoid, but we need to make sure that the SU scale factors are ordered!
        sort_idx = np.argsort(a_SU)
        a_global = a_global[sort_idx]
        a_SU = a_SU[sort_idx]
        np.savetxt(SU_param['G4_SU_scale_file'], np.stack([a_SU, a_global], axis=1))

        SU_param['G4_wrk_dir']  = folder_G4
        # write Gadget4 parameter file
        f_G4 = '%s/G4.param'%folder_G4
        with open(f_G4, 'w') as f :
            f.write(temp_G4.format(**SU_param))
        
        # write random seed to file for reference
        with open('%s/seed.txt'%folder_2LPT, 'w') as f :
            f.write('%d'%SU_param['IC_seed'])

        # add specifics for 2LPT
        SU_param['IC_outputdir'] = folder_2LPT
        # write 2LPT parameter files
        f_2LPT = '%s/2LPT.param'%folder_2LPT
        with open(f_2LPT, 'w') as f :
            f.write(temp_2LPT.format(**SU_param))
        
        # write slurm file
        folder_slurm = '%s/slurm'%folder
        os.system('mkdir -p %s'%folder_slurm)
        SBATCH_param = dict(sbatch_output = '%s/slurm.out.txt'%folder_slurm,
                            sbatch_name = os.path.basename(this_root) + '-' + os.path.basename(folder),
                            folder_CAMB = folder_CAMB,
                            folder_2LPT = folder_2LPT,
                            folder_G4 = folder_G4)
        f_slurm = '%s/in.sh'%folder_slurm
        with open(f_slurm, 'w') as f :
            f.write(temp_sbatch.format(**SBATCH_param))

        slurm_scripts.append(f_slurm)

# prepare a nice file for easy submission
with open('submit.sh', 'w') as f :
    for s in slurm_scripts :
        f.write('sbatch %s\n'%s)
