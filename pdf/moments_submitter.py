# This script is used to submit jobs to compute Pk from different realizations/cosmologies
import numpy as np
import sys,os

################################## INPUT #############################################
step    = 100   #number of realizations each cpu will do
offset  = 0    #the count will start from offset
######################################################################################

# do a loop over the different cosmologies
for folder in ['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/']:
#['fiducial_HR/', 'fiducial/', 'fiducial_LR/', 'fiducial_ZA/',
#'Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/',          
#'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',           
#'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/',
#'latin_hypercube/']:

    # do a loop over the different redshifts
    for snapnum in [0,1,2,3,4]:

        if   folder=='fiducial/':         nodes = int(15000/step)
        elif folder=='latin_hypercube/':  nodes = int(2000/step)
        elif folder=='fiducial_HR/':      nodes = int(100/step)
        elif folder=='fiducial_LR/':      nodes = int(1000/step)
        else:                             nodes = int(500/step)
        if nodes==0:  nodes = 1

        # do a loop over the different realizations
        for i in xrange(nodes):    

            a = """#!/bin/bash
#SBATCH -J pdf
#SBATCH --exclusive        
######SBATCH -t 7-00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#####SBATCH --ntasks-per-node=48
#####SBATCH --partition=general
#SBATCH --partition=preempt
#SBATCH --export=ALL
        
srun -n 10 --mpi=pmi2 python moments_pdf.py %d %d %s %d\n
                """%(i*step+offset, (i+1)*step+offset, folder, snapnum)
                
            # create the script.sh file, execute it and remove it
            f = open('script.sh','w');  f.write(a);  f.close()
            os.system('sbatch script.sh');  os.system('rm script.sh')
