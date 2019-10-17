# This script is used to submit jobs to compute CF from different realizations/cosmologies
import numpy as np
import sys,os

################################## INPUT #############################################
step             = 500  #number of realizations each cpu will do
offset           = 0    #the count will start from offset
snapnum          = 4    #4(z=0), 3(z=0.5), 2(z=1), 1(z=2), 0(z=3)
######################################################################################


# do a loop over the different cosmologies
for folder in ['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/',          
               'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',           
               'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/', 'fiducial/',
               'latin_hypercube/']:

    if   folder=='fiducial/':         nodes = 15000/step
    elif folder=='latin_hypercube/':  nodes = 2000/step
    else:                             nodes = 500/step

    # do a loop over the different realizations
    for i in xrange(nodes):    

        a = """#!/bin/bash
#SBATCH -J CF
#SBATCH --exclusive        
######SBATCH -t 1-00:00
#SBATCH --nodes=1
#####SBATCH --ntasks-per-node=16
#SBATCH --ntasks-per-node=48
#SBATCH --partition=general
#SBATCH --export=ALL
        
srun -n 30 --mpi=pmi2 python CF_matter.py %d %d %s %d\n
        """%(i*step+offset, (i+1)*step+offset, folder, snapnum)
#srun -n 35 --mpi=pmi2 python Pk_halos.py %d %d %s %d\n

        # create the script.sh file, execute it and remove it
        f = open('script.sh','w');  f.write(a);  f.close()
        os.system('sbatch script.sh');  os.system('rm script.sh')
