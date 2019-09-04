#!/bin/bash
#SBATCH -J HR
#SBATCH --exclusive        
#SBATCH -o OUTPUT.o%j             
#SBATCH -e OUTPUT.e%j                 
#SBATCH --mail-user=villaescusa.francisco@gmail.com     
#SBATCH --mail-type=ALL  
#SBATCH -t 7-00:00
#SBATCH --nodes=40
#SBATCH --ntasks-per-node=16
#SBATCH --partition=general
#SBATCH --export=ALL
#####SBATCH --qos=double
######SBATCH --partition=preempt
#####SBATCH --partition=interactive

module load intel
module load mvapich2_ib
module load gsl/2.1
module load gmp/6.0.0a
module load fftw/2.1.5
module load hdf5/1.8.14


root="/simons/scratch/fvillaescusa/pdf_information/"

#for i in {0..499}
#do

    #for cosmo in "Om_m/" "Om_p/"
    #for cosmo in "s8_m/" "s8_p/"
    #for cosmo in "h_m/" "h_p/"
    #for cosmo in "Ob_mm/" 
    #for cosmo in "ns_m/" "ns_p/"
    #for cosmo in "fiducial_NCV/"
    #for cosmo in "Mnu_p/"
    #for cosmo in "Mnu_pp/"
    #for cosmo in "Mnu_ppp/"
    #do

	#for suffix in "NCV_0_" "NCV_1_"
	#do
	    #folder=$root$cosmo$suffix$i
	    #cd $folder

	    #if [ ! -f "snapdir_004/snap_004.0" ]
	    #then
		#srun -n 512 --mpi=pmi2 ../../2lpt/2LPTic 2LPT.param >> logIC
		#srun -n 512 --mpi=pmi2 ../../g3_new/P-Gadget3 ../G3.param >> logfile
	    
		#only for neutrino sims
		#srun -n 512 --mpi=pmi2 ../../n-genic_growth/N-GenIC N-GenIC_0.10.param >> logIC
		#srun -n 512 --mpi=pmi2 ../../n-genic_growth/N-GenIC N-GenIC_0.20.param >> logIC
		#srun -n 512 --mpi=pmi2 ../../n-genic_growth/N-GenIC N-GenIC_0.40.param >> logIC
		#srun -n 512 --mpi=pmi2 ../../g3_new_nu/P-Gadget3 ../G3.param >> logfile

		#rm -rf restartfiles ics.{0..512}
		#echo $i
	    #fi
	#done
    #done
#done



root="/simons/scratch/fvillaescusa/pdf_information/fiducial_HR/"
for i in {0..0}
do

    folder=$root$i
    cd $folder

    if [ ! -f "snapdir_004/snap_004.0.hdf5" ]
    then
	cd ICs
	srun -n 640 --mpi=pmi2 ../../../2lpt/2LPTic 2LPT.param >> logIC
	cd ..
	srun -n 640 --mpi=pmi2 ../../g3_new_HR/P-Gadget3 ../G3.param >> logfile
	rm -rf restartfiles
    fi

done
