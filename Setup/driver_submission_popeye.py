import numpy as np
import sys,os

sims_per_job = 5

for i in xrange(0,450/sims_per_job+1):

    a=\
       """#!/bin/bash
#SBATCH -J %d
#SBATCH --exclusive        
#SBATCH -t 1-00:00
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=48
#SBATCH --partition=general
######SBATCH --partition=preempt
#SBATCH --export=ALL

module load slurm
module load gcc
module load openmpi
module load lib/fftw2/2.1.5-openmpi1
module load lib/gsl
module load lib/hdf5

       
root="/simons/scratch/fvillaescusa/pdf_information/"
for i in {%d..%d}
do
   for cosmo in "Mnu_pp/"
   do
      folder=$root$cosmo$i
      cd $folder

      if [ ! -f "snapdir_004/snap_004.0.hdf5" ]
      then

         srun -n 144 --mpi=pmi2 ../../n-genic_growth_popeye/N-GenIC ICs/N-GenIC_0.20.param >> logIC
         srun -n 144 --mpi=pmi2 ../../g3_new_nu_popeye/P-Gadget3 ../G3.param >> logfile
         rm -rf restartfiles
         mkdir extra_files/
         mv balance.txt cpu.txt energy.txt darkenergy.txt drift*.txt growth_*.dat ewald_*.dat free_largest_*.txt free_smallest_*.txt info.txt logfile logIC memory_largest_*.txt memory_smallest_*.txt parameters-usedvalues PIDs.txt processes_largest_*.txt processes_smallest_*.txt ps_file*.txt ps_largest_*.txt ps_smallest_*.txt Timebin.txt timings.txt extra_files/
      fi
   done
done
"""%(i, i*sims_per_job, (i+1)*sims_per_job)

    f = open('dumb_script.sh','w');  f.write(a);  f.close()
    os.system('sbatch dumb_script.sh');  os.system('rm dumb_script.sh')




