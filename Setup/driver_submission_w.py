import numpy as np
import sys,os

sims_per_job = 25

for i in xrange(8,10,1):

    a=\
       """#!/bin/bash
#SBATCH -J %d
#SBATCH --exclusive        
#SBATCH -t 1-00:00
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=16
######SBATCH --partition=general
#SBATCH --partition=preempt
#SBATCH --export=ALL
#######SBATCH --qos=double
       
module load intel
module load mvapich2_ib
module load gsl/2.1
module load gmp/6.0.0a
module load fftw/2.1.5
module load hdf5/1.8.14
       
IC_code=/simons/scratch/fvillaescusa/pdf_information/ICs_codes/n-genic_growth/N-GenIC
G3=/simons/scratch/fvillaescusa/Gadget-III_Quijote/g3_new_w/P-Gadget3

root="/simons/scratch/fvillaescusa/pdf_information/Snapshots/"
for cosmo in "w_p/" "w_m/"
do
   for i in {%d..%d}
   do
      folder=$root$cosmo$i
      cd $folder

      if [ ! -f "snapdir_004/snap_004.0.hdf5" ]
      then
         cd $folder"/ICs/"
         srun -n 16 --mpi=pmi2 $IC_code N-GenIC.param >> logIC
         cd ..
         srun -n 512 --mpi=pmi2 $G3 ../G3.param >> logfile
         rm -rf restartfiles
         mkdir extra_files/
         mv balance.txt cpu.txt energy.txt darkenergy.txt drift*.txt growth_*.dat ewald_*.dat free_largest_*.txt free_smallest_*.txt info.txt logfile logIC memory_largest_*.txt memory_smallest_*.txt parameters-usedvalues PIDs.txt processes_largest_*.txt processes_smallest_*.txt ps_file*.txt ps_largest_*.txt ps_smallest_*.txt Timebin.txt timings.txt extra_files/
      fi
   done
done
"""%(i, i*sims_per_job, (i+1)*sims_per_job)

    f = open('dumb_script.sh','w');  f.write(a);  f.close()
    os.system('sbatch dumb_script.sh');  os.system('rm dumb_script.sh')





