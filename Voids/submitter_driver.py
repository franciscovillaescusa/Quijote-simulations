# This script is used to submit jobs to identify voids in different snapshots
import numpy as np
import sys,os


################################## INPUT #############################################
realizations = 500

step = 15 #number of realizations each cpu will do

offset = 0 #the count will start from offset
######################################################################################

# number of nodes needed
nodes = int(realizations/step)

# do a loop over each node
for i in xrange(nodes):

    for folder in ['Om_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
                   'Om_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
                   'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial']:


        a = """#!/bin/bash
#SBATCH -J void_finder
#SBATCH --exclusive        
#SBATCH -t 7-00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --partition=general
######SBATCH --partition=preempt
#SBATCH --export=ALL
       

python void_finder.py %d %d %s\n
        """%(i*step+offset,(i+1)*step+offset,folder)

        # create the script.sh file with the above instructions
        f = open('script.sh','w');  f.write(a);  f.close()

        # execute the script and remove it
        os.system('sbatch script.sh');  os.system('rm script.sh')
