# We use this script to create the initial condition parameter file when multiple
# realizations of the same cosmology are needed
import numpy as np
import sys,os


############################### INPUT ###################################
root = '/simons/scratch/fvillaescusa/pdf_information/Snapshots/'
cosmologies = ['Om_p', 'Ob2_p', 'h_p', 's8_p', 'ns_p', 
               'Om_m', 'Ob2_m', 'h_m', 's8_m', 'ns_m',
               'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'w_p', 'w_m', 
               'fiducial_LR', 'fiducial_HR', 'fiducial_ZA']

fiducial_seed = 7890 #Seed value in the fiducial file
fiducial_flip = 4567 #Phase_flip value in the fiducial file
fiducial_RS   = 3456 #RayleighSampling value in the fiducial file 
#########################################################################

# do a loop over the different cosmologies
for cosmology in cosmologies:

    # get the name of the folder with the different realizations
    cosmo = '%s/%s'%(root,cosmology)
    
    # fidn the number of realizations for each model
    if   cosmology=='fiducial_LR':  derivatives_realizations = 1000
    elif cosmology=='fiducial_HR':  derivatives_realizations = 100
    elif cosmology=='fiducial_ZA':  derivatives_realizations = 500
    else:                           derivatives_realizations = 500

    # find the example parameter file
    if   cosmology=='Mnu_p':   fiducial_file = 'N-GenIC_0.10.param'
    elif cosmology=='Mnu_pp':  fiducial_file = 'N-GenIC_0.20.param'
    elif cosmology=='Mnu_ppp': fiducial_file = 'N-GenIC_0.40.param'
    elif cosmology=='w_p':     fiducial_file = 'N-GenIC.param'
    elif cosmology=='w_m':     fiducial_file = 'N-GenIC.param'
    else:                      fiducial_file = '2LPT.param'
        
    # do a loop over all standard realizations
    for i in xrange(derivatives_realizations):

        seed = 10*i + 5 #value of the random seed

        # create the folders if they do not exist
        folder = '%s/%d'%(cosmo,i);  ICs_folder = '%s/ICs/'%folder
        if not(os.path.exists(folder)):      os.system('mkdir %s'%folder)
        if not(os.path.exists(ICs_folder)):  os.system('mkdir %s'%ICs_folder)

        # open input and output files
        output_file = '%s/%s'%(ICs_folder, fiducial_file)
        #if os.path.exists(output_file):  continue
        fin  = open('%s/%s'%(cosmo,fiducial_file), 'r')
        fout = open(output_file, 'w')

        for line in fin:
            if str(fiducial_seed) in line.split():
                fout.write(line.replace(str(fiducial_seed), str(seed)))
            elif str(fiducial_RS) in line.split():
                fout.write(line.replace(str(fiducial_RS), str(1)))  #do Rayleigh sampling
            elif str(fiducial_flip) in line.split():
                fout.write(line.replace(str(fiducial_flip), str(0)))
            else:  fout.write(line)
        
        fin.close(); fout.close()


    """
    # do a loop over all paired fixed simulations
    for i in xrange(250):

        seed = 10*i + 1

        # create the folder if it does not exists
        folder1 = '%s/NCV_0_%d'%(cosmo,i);  ICs_folder1 = '%s/ICs/'%folder1
        folder2 = '%s/NCV_1_%d'%(cosmo,i);  ICs_folder2 = '%s/ICs/'%folder2
        if not(os.path.exists(folder1)):      os.system('mkdir %s'%folder1)
        if not(os.path.exists(ICs_folder1)):  os.system('mkdir %s'%ICs_folder1)
        if not(os.path.exists(folder2)):      os.system('mkdir %s'%folder2)
        if not(os.path.exists(ICs_folder2)):  os.system('mkdir %s'%ICs_folder2)

        # open input and output files
        output_file = '%s/%s'%(ICs_folder1, fiducial_file)
        if os.path.exists(output_file):  continue
        fin  = open('%s/%s'%(cosmo,fiducial_file), 'r')
        fout = open(output_file, 'w')

        for line in fin:
            if str(fiducial_seed) in line.split():
                fout.write(line.replace(str(fiducial_seed), str(seed)))
            elif str(fiducial_RS) in line.split():
                fout.write(line.replace(str(fiducial_RS), str(0)))  #NO Rayleigh sampling
            elif str(fiducial_flip) in line.split():
                fout.write(line.replace(str(fiducial_flip), str(0)))
            else:  fout.write(line)
        
        fin.close(); fout.close()

        # open input and output files
        output_file = '%s/%s'%(ICs_folder2, fiducial_file)
        if os.path.exists(output_file):  continue
        fin  = open('%s/%s'%(cosmo,fiducial_file), 'r')
        fout = open(output_file, 'w')

        for line in fin:
            if str(fiducial_seed) in line.split():
                fout.write(line.replace(str(fiducial_seed), str(seed)))
            elif str(fiducial_RS) in line.split():
                fout.write(line.replace(str(fiducial_RS), str(0)))  #NO Rayleigh sampling
            elif str(fiducial_flip) in line.split():
                fout.write(line.replace(str(fiducial_flip), str(1)))
            else:  fout.write(line)
        
        fin.close(); fout.close()
    """



