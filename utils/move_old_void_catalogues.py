# This script moves the halo catalogues from their original locations to the halo folder
import numpy as np
import sys,os

root = '/simons/scratch/fvillaescusa/pdf_information/'
##################################### INPUT ############################################
cosmologies = ['Mnu_ppp']
#['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
#'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
#'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial', 'fiducial_LR','fiducial_HR',
#'latin_hypercube']
########################################################################################

# do a loop over all different cosmologies
for cosmo in cosmologies:

    # find the number of standard and paired fixed simulations
    paired_fixed_realizations = 250
    standard_realizations = 0
    #if   cosmo=='fiducial':         standard_realizations = 15000
    #elif cosmo=='fiducial_ZA':      standard_realizations = 500
    #elif cosmo=='fiducial_LR':      standard_realizations = 1000
    #elif cosmo=='fiducial_HR':      standard_realizations = 100
    #elif cosmo=='latin_hypercube':  standard_realizations = 2000
    #else:                           standard_realizations = 500
     
    # find the name of the output halo folder containing all results
    folder = '%s/Voids/old/%s'%(root,cosmo)
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    """
    ###### standard realizations ######
    for i in xrange(standard_realizations):

        # create output folder if it does not exists
        folder_out = '%s/%d/'%(folder,i)
        if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

        # move file
        folder_in = '%s/%s/%d/voids/void_catalogue_z=0.hdf5'%(root,cosmo,i)
        if not(os.path.exists(folder_in)):  continue
        os.system('mv %s %s'%(folder_in, folder_out))
    """


    ###### paired fixed realizations ######
    for i in xrange(paired_fixed_realizations):

        for pair in [0,1]:
            
            # create output folder if it does not exists
            folder_out = '%s/NCV_%d_%d/'%(folder,pair,i)
            if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

            # move file
            folder_in = '%s/Snapshots/%s/NCV_%d_%d/voids/void_catalogue_z=0.hdf5'\
                        %(root,cosmo,pair,i)
            if not(os.path.exists(folder_in)):  continue

            # change permissions
            os.system('chmod +w %s/Snapshots/%s'%(root,cosmo))
            os.system('chmod +w %s/Snapshots/%s/NCV_%d_%d/'%(root,cosmo,pair,i))
            os.system('chmod +w %s/Snapshots/%s/NCV_%d_%d/voids'%(root,cosmo,pair,i))

            # move file
            os.system('mv %s %s'%(folder_in, folder_out))

            # remove void folder
            os.system('rm -rf %s/Snapshots/%s/NCV_%d_%d/voids'%(root,cosmo,pair,i))

            # change permissions again
            os.system('chmod -w %s/Snapshots/%s'%(root,cosmo))
            os.system('chmod -w %s/Snapshots/%s/NCV_%d_%d/'%(root,cosmo,pair,i))


