import numpy as np
import sys,os

suffix1 = 'void_catalogue_m_z=0.hdf5'
suffix2 = 'void_catalogue_c_z=0.hdf5'

root = '/simons/scratch/fvillaescusa/pdf_information/Voids'

# do a loop over the different cosmologies
for cosmo in ['Mnu_p','Mnu_pp','Mnu_ppp']:
    
    # do a loop over the different realizations
    for i in xrange(500):

        # do a loop over standard and paired fixed simulations
        for prefix in ['%d'%i, 'NCV_0_%d'%i, 'NCV_1_%d'%i]:
            
            fname1 = '%s/%s/%s/%s'%(root,cosmo,prefix,suffix1)
            fname2 = '%s/%s/%s/%s'%(root,cosmo,prefix,suffix2)

            if os.path.exists(fname1):
                os.system('mv %s %s'%(fname1, fname2))
