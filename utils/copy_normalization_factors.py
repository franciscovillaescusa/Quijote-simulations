import numpy as np
import sys,os


####################################### INPUT ##########################################
root1 = '/simons/scratch/fvillaescusa/pdf_information/Snapshots'
root2 = '/simons/scratch/fvillaescusa/pdf_information/Linear_Pk'
cosmologies = ['Om_p', 'Ob_p', 'Ob2_p', 'h_p', 'ns_p', 's8_p',
               'Om_m', 'Ob_m', 'Ob2_m', 'h_m', 'ns_m', 's8_m',
               'Mnu_p', 'Mnu_pp', 'Mnu_ppp',
               'fiducial']
########################################################################################

# do a loop over all cosmologies
for cosmo in cosmologies:

    # get the name of the file
    if cosmo in ['Ob_p', 'Ob_m']:
        f_logIC = '%s/%s/NCV_0_0/extra_files/logIC'%(root1,cosmo)
    else:
        f_logIC = '%s/%s/0/extra_files/logIC'%(root1,cosmo)

    # read file
    if cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp']:
        Normfac = 1.0
    else:
        count = 0
        f = open(f_logIC, 'r')
        for line in f.readlines():
            count += 1
            if count==4:  
                Normfac = line.split()[4][9:-1]
                print '%s ----> %s'%(cosmo,Normfac)
            else:  continue
        f.close()
    
    # save number to file
    fout = '%s/%s/Normfac.txt'%(root2,cosmo)
    f = open(fout, 'w');  f.write('%s'%Normfac);  f.close()


# do the latin hypercube here
for i in xrange(2000):

    # get the name of the file
    f_logIC = '%s/latin_hypercube/%d/extra_files/logIC'%(root1,i)

    # read file
    count = 0
    f = open(f_logIC, 'r')
    for line in f.readlines():
        count += 1
        if count==4:  
            Normfac = line.split()[4][9:-1]
            print 'LH %d ----> %s'%(i,Normfac)
        else:  continue
    f.close()
    
    # save number to file
    fout = '%s/latin_hypercube/%d/Normfac.txt'%(root2,i)
    f = open(fout, 'w');  f.write('%s'%Normfac);  f.close()    

