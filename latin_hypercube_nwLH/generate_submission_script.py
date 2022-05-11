import numpy as np
import sys,os

realizations = 2000

# do a loop over all realizations
for i in range(realizations):

    script = """#!/bin/bash -l
#SBATCH --job-name=nwLH%d
#SBATCH --exclusive  
#SBATCH --export=ALL
#SBATCH -t 7-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH -C rome
#SBATCH -p cmbas --qos=cmbas

root="/mnt/ceph/users/fvillaescusa/Quijote/nwLH/%d"
G3="/mnt/ceph/users/fvillaescusa/Quijote/nwLH/Codes/g3_new_nu/P-Gadget3"
NGenIC="/mnt/ceph/users/fvillaescusa/Quijote/nwLH/Codes/n-genic_growth/N-GenIC"

module purge
module load slurm
module load gcc
module load openmpi
module load fftw/2.1.5-mpi
module load lib/openblas
module load lib/gsl
module load lib/hdf5

cd $root

if [ -f "snapdir_004/snap_004.0.hdf5" ]
then 
    echo $i;
else
    cd ICs;
    srun $NGenIC NGenIC.param > logIC;
    cd ..;
    srun $G3 G3.param > logfile;
fi
    """%(i,i)


    f = open('%d/script.sh'%i, 'w');  f.write(script);  f.close()
