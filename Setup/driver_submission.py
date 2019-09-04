import numpy as np
import sys,os

sims_per_job = 1

for i in xrange(500/sims_per_job+1,0,-1):

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
       
root="/simons/scratch/fvillaescusa/pdf_information/"
for i in {%d..%d}
do
   for cosmo in "Mnu_ppp/"
   do
      folder=$root$cosmo$i
      cd $folder

      if [ ! -f "snapdir_004/snap_004.0.hdf5" ]
      then
         #srun -n 512 --mpi=pmi2 ../../2lpt/2LPTic ICs/2LPT.param >> logIC
         #srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3.param >> logfile
         srun -n 512 --mpi=pmi2 ../../n-genic_growth/N-GenIC ICs/N-GenIC_0.40.param >> logIC
         srun -n 512 --mpi=pmi2 ../../g3_new_nu/P-Gadget3 ../G3.param >> logfile
         rm -rf restartfiles
         mkdir extra_files/
         mv balance.txt cpu.txt energy.txt darkenergy.txt drift*.txt growth_*.dat ewald_*.dat free_largest_*.txt free_smallest_*.txt info.txt logfile logIC memory_largest_*.txt memory_smallest_*.txt parameters-usedvalues PIDs.txt processes_largest_*.txt processes_smallest_*.txt ps_file*.txt ps_largest_*.txt ps_smallest_*.txt Timebin.txt timings.txt extra_files/
      fi
   done
done
"""%(i, i*sims_per_job, (i+1)*sims_per_job)

    f = open('dumb_script.sh','w');  f.write(a);  f.close()
    os.system('sbatch dumb_script.sh');  os.system('rm dumb_script.sh')


"""
      srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3_FoF.param 3 0
      srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3_FoF.param 3 1
      srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3_FoF.param 3 2
      srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3_FoF.param 3 3
      srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3_FoF.param 3 4

      rm balance.txt cpu.txt energy.txt ewald_*.dat free_largest_*.txt free_smallest_*.txt info.txt memory_largest_*.txt memory_smallest_*.txt parameters-usedvalues PIDs.txt processes_largest_*.txt processes_smallest_*.txt ps_file*.txt ps_largest_*.txt ps_smallest_*.txt Timebin.txt timings.txt
"""


