# This script is used to submit jobs to compute Pk from different realizations/cosmologies
import numpy as np
import sys,os

################################## INPUT #############################################
step    = 500   #number of realizations each cpu will do
offset  = 0    #the count will start from offset
######################################################################################

# do a loop over the different cosmologies
for folder in ['w_p/', 'w_m/']:
#['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/',          
#'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',           
#'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/',
#'w_p/', 'w_m/',
#'fiducial_ZA/', 'fiducial/', 
#'fiducial_LR/', 'fiducial_HR/',
#'latin_hypercube/']:

    # do a loop over the different smoothing scales
    for smoothing in [5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0]:

        # do a loop over the different redshifts
        for snapnum in [0,1,2,3,4]:

            if   folder=='fiducial/':         nodes = int(15000/step)
            elif folder=='latin_hypercube/':  nodes = int(2000/step)
            elif folder=='fiducial_HR/':      nodes = int(100/step)
            elif folder=='fiducial_LR/':      nodes = int(1000/step)
            else:                             nodes = int(500/step)

            # do a loop over the different realizations
            for i in range(nodes):    

                a = """#!/bin/bash
#SBATCH -J pdf
#SBATCH --exclusive        
#SBATCH -t 1-00:00
#SBATCH --nodes=1
#####SBATCH --ntasks-per-node=16
#SBATCH --ntasks-per-node=48
#SBATCH --partition=general
#SBATCH --export=ALL

source ~/Pylians3
        
srun -n 20 --mpi=pmi2 python3 pdf_matter.py %d %d %s %d %s\n
                """%(i*step+offset, (i+1)*step+offset, folder, snapnum, smoothing)
                #srun -n 2 --mpi=pmi2 python pdf_matter_LH_high_resolution.py %d %d %s %d\n
                #srun -n 35 --mpi=pmi2 python variance_pdf.py %d %d %s %d\n
                #srun -n 35 --mpi=pmi2 python pdf_matter.py %d %d %s %d\n
                #srun -n 35 --mpi=pmi2 python Pk_halos.py %d %d %s %d\n

                # create the script.sh file, execute it and remove it
                f = open('script.sh','w');  f.write(a);  f.close()
                os.system('sbatch script.sh');  os.system('rm script.sh')
