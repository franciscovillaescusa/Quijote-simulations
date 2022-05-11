#!/bin/bash -l
#SBATCH --job-name=camels
#SBATCH --exclusive  
#SBATCH --export=ALL
#SBATCH -t 7-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH -C rome
######SBATCH -p gen --qos=gen
######SBATCH -p gen --qos=gen
#SBATCH -p cmbas --qos=cmbas


root="/mnt/ceph/users/fvillaescusa/Nbody_systematics/data/Sims/Ramses_HR/"

module load openmpi2

for i in {9..9}
do

    cd $root$i

    if [ -f "output_00006/part_00006.out00128" ]
    then 
	echo $i;
    else
	export DATE=`date +%F_%Hh%M`;
	srun ramses3d dmo.nml > run_$DATE.log;
    fi

done
