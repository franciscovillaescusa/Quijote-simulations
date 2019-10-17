import numpy as np
import sys,os,glob

######################################### INPUT ########################################
root = '/simons/scratch/fvillaescusa/pdf_information/CF'

folders = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
           'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
           'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial',
           'latin_hypercube']

zs = [0, 0.5, 1, 2, 3]
########################################################################################

# do a loop over the different folders
for cosmo in folders:

    # do a loop over the different redshifts
    for z in zs:

        files = glob.glob('%s/matter/%s/*/CF_m_*z=%s.txt'%(root,cosmo,z))
        print 'Found %d files for %s at z=%s'%(len(files),cosmo,z)

        for f in files:
            if os.stat(f).st_size==0:
                print '%s seems empty'%f
    print ''
