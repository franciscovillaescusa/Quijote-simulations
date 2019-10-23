import numpy as np
import sys,os,glob



######################################## INPUT ##########################################
root   = '/simons/scratch/fvillaescusa/pdf_information/PDF/matter/'
cosmos = ['Om_p/', 'Ob_p/', 'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/',          
          'Om_m/', 'Ob_m/', 'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/',           
          'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/',
          'fiducial_ZA/', 'fiducial/',
          'latin_hypercube/']
zs     = [0, 0.5, 1, 2, 3]
scales = [5, 10, 15, 20, 25, 30, 35]
#########################################################################################

# do a loop over the different cosmologies
for cosmo in cosmos:

    files = glob.glob('%s/%s/*/PDF_m_*'%(root,cosmo))
    print 'Found %d files for %s'%(len(files),cosmo)
    continue

    # do a loop over the different redshifts
    for z in zs:

        files = glob.glob('%s/%s/*/variance_PDF_m_z=%s.txt'%(root,cosmo,z))
        print 'Found %d var files for %s at z=%d'%(len(files),cosmo,z)

        # do a loop over the different scales
        for scale in scales:
        
            files = glob.glob('%s/%s/*/PDF_m_%.1f_z=%s.txt'%(root,cosmo,scale,z))
            print 'Found %d files for %s with %d at z=%d'%(len(files),cosmo,scale,z)



