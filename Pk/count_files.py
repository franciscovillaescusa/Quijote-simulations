import numpy as np
import sys,os,glob

######################################### INPUT ########################################
root = '/simons/scratch/fvillaescusa/pdf_information/Pk'
folders = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
           'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
           'Mnu_p', 'Mnu_pp', 'Mnu_ppp', 'fiducial']
########################################################################################

# do a loop over the different folders
for cosmo in folders:
    files = glob.glob('%s/matter/%s/*/Pk_*z=127.txt'%(root,cosmo))
    print 'Found %d files for %s at z=127'%(len(files),cosmo)
