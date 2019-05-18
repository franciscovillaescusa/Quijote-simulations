# This script moves the halo catalogues from their original locations to the halo folder
import numpy as np
import sys,os

root = '/simons/scratch/fvillaescusa/pdf_information/'
##################################### INPUT ############################################
cosmologies = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
               'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
               'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial']
########################################################################################

# do a loop over all different cosmologies
for cosmo in cosmologies:

    # find the number of standard and paired fixed simulations
    paired_fixed_realizations = 250
    if cosmo=='fiducial':  standard_realizations = 15000
    else:                  standard_realizations = 500
     
    # find the name of the output halo folder containing all results
    folder = '%s/Halos/%s'%(root,cosmo)
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    ###### standard realizations ######
    for i in xrange(standard_realizations):

        # create output folder if it does not exists
        folder_out = '%s/%d/'%(folder,i)
        if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

        # do a loop over the different redshifts
        for snapnum in [0,1,2,3,4]:

            folder_in = '%s/%s/%d/groups_%03d'%(root,cosmo,i,snapnum)
            if not(os.path.exists(folder_in)):  continue
            os.system('mv %s %s'%(folder_in, folder_out))


    ###### paired fixed realizations ######
    for i in xrange(paired_fixed_realizations):

        for pair in [0,1]:
            
            # create output folder if it does not exists
            folder_out = '%s/NCV_%d_%d/'%(folder,pair,i)
            if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

            # do a loop over the different redshifts
            for snapnum in [0,1,2,3,4]:

                folder_in = '%s/%s/NCV_%d_%d/groups_%03d'%(root,cosmo,pair,i,snapnum)
                if not(os.path.exists(folder_in)):  continue
                os.system('mv %s %s'%(folder_in, folder_out))



