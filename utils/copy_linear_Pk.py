import numpy as np
import sys,os

##################################### INPUT ############################################
realizations = 2000
########################################################################################

root1 = '/simons/scratch/fvillaescusa/pdf_information/Snapshots/latin_hypercube'
root2 = '/simons/scratch/fvillaescusa/pdf_information/Linear_Pk/latin_hypercube'

# do a loop over all realizations
for i in xrange(realizations):

    folder_in  = '%s/%d'%(root1,i)
    folder_out = '%s/%d'%(root2,i)

    if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)

    os.system('cp %s/CAMB.params %s/'%(folder_in, folder_out))
    os.system('cp %s/ICs/Pk_mm_z=0.000.txt %s/'%(folder_in, folder_out))
