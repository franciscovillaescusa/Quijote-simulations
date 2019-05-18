# This script is used to submit jobs to compute bispectra
import sys,os

################################## INPUT #############################################
realizations = 500 #total number of realizations
step         = 125 #number of realizations each node will do
offset       = 0   #the count will start from offset
snapnum      = 4   #4(z=0), 3(z=0.5), 2(z=1), 1(z=2), 0(z=3)
######################################################################################

# number of nodes needed
nodes = int((realizations-offset)/step)

# do a loop over each node
for i in xrange(nodes):

    for folder in ['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/', 
                   'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',
                   'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/', 'fiducial/']:

        a = """#!/bin/bash
#SBATCH -J Bk
#SBATCH --exclusive        
#SBATCH --nodes=1
####SBATCH --ntasks-per-node=16
#SBATCH --ntasks-per-node=48
#SBATCH --partition=general
#####SBATCH --partition=preempt
#SBATCH --export=ALL

export PYSPEC_CODEDIR="/home/fvillaescusa/data/pdf_information/analysis/Bispectrum/pySpectrum/"
    
srun -n 32 --mpi=pmi2 python Bk_halos.py %d %d %s %d\n
        """%(i*step+offset, (i+1)*step+offset, folder, snapnum)

        # create the script file; execute it and remove it
        f = open('script.sh','w');  f.write(a);  f.close()
        os.system('sbatch script.sh');  os.system('rm script.sh')
