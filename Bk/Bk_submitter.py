# This script is used to submit jobs to compute Pk from different realizations/cosmologies
import numpy as np
import sys,os

################################## INPUT #############################################
realizations_fid = 15000
realizations_der = 500
realizations_lh  = 2000 #latin-hypercube
step             = 100 #number of realizations each cpu will do
offset           = 0   #the count will start from offset
snapnum          = 0   #4(z=0), 3(z=0.5), 2(z=1), 1(z=2), 0(z=3)
######################################################################################

# number of nodes needed
nodes_fid = int(realizations_fid/step)
nodes_der = int(realizations_der/step)
nodes_lh  = int(realizations_lh/step)

# do a loop over the different cosmologies
for folder in ['Ob2_m/', 'ns_m/', 'Mnu_pp/','fiducial/']:
#['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/',          
#'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',           
#'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/', 'fiducial/',
#'latin_hypercube/']:

    if   folder=='fiducial/':         nodes = nodes_fid
    elif folder=='latin_hypercube/':  nodes = nodes_lh
    else:                             nodes = nodes_der

    # do a loop over the different realizations
    for i in xrange(nodes):    

        a = """#!/bin/bash
#SBATCH -J Bk
#SBATCH --exclusive        
######SBATCH -t 1-00:00
#SBATCH --nodes=1
#####SBATCH --ntasks-per-node=16
#SBATCH --ntasks-per-node=48
#SBATCH --partition=general
#SBATCH --export=ALL
        
srun -n 35 --mpi=pmi2 python Bk_matter.py %d %d %s %d\n
        """%(i*step+offset, (i+1)*step+offset, folder, snapnum)
#srun -n 35 --mpi=pmi2 python Bk_halos.py %d %d %s %d\n

        # create the script.sh file, execute it and remove it
        f = open('script.sh','w');  f.write(a);  f.close()
        os.system('sbatch script.sh');  os.system('rm script.sh')
