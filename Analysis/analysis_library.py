# This library computes the covariance of each observable and the derivatives wrt
# the different cosmological parameters
from mpi4py import MPI
import numpy as np
import sys,os,h5py
import readfof

###### MPI DEFINITIONS ######
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()


#######################################################################################
# This routine takes a covariance matrix and computes its inverse and conditional number
def Inv_Cov(Cov):

    print '\n####################################################'
    # find eigenvalues and eigenvector of the covariance
    v1,w1 = np.linalg.eig(Cov)
    print 'Max eigenvalue    Cov = %.3e'%np.max(v1)
    print 'Min eigenvalue    Cov = %.3e'%np.min(v1)
    print 'Condition number  Cov = %.3e'%(np.max(v1)/np.min(v1))
    print ' '

    # compute the inverse of the covariance
    ICov = np.linalg.inv(Cov)

    # find eigenvalues and eigenvector of the covariance
    v2,w2 = np.linalg.eig(ICov)
    print 'Max eigenvalue   ICov = %.3e'%np.max(v2)
    print 'Min eigenvalue   ICov = %.3e'%np.min(v2)
    print 'Condition number ICov = %.3e'%(np.max(v2)/np.min(v2))

    #np.savetxt('eigenvalues.txt', 
    #           np.transpose([np.arange(elements), np.sort(v1), np.sort(v2)]))
    
    # check the product of the covariance and its inverse gives the identity matrix
    Equal = np.allclose(np.dot(Cov, ICov), np.eye(Cov.shape[0]))
    print '\nHas the inverse been properly found?',Equal
    print '####################################################\n'
    
    return ICov

# This routine computes the subcovariance of the considered statistics given 
# the full covariance
def subcovariance(Cov, bins, do_Pkm, do_Pkc, do_HMF, do_VSF):
    indexes_Pkm = np.arange(0,                np.sum(bins[:1])) #Pkm indexes
    indexes_Pkc = np.arange(np.sum(bins[:1]), np.sum(bins[:2])) #Pkc indexes
    indexes_HMF = np.arange(np.sum(bins[:2]), np.sum(bins[:3])) #HMF indexes
    indexes_VSF = np.arange(np.sum(bins[:3]), np.sum(bins[:4])) #VSF indexes
    
    # find the indexes of the subcovariance
    indexes = np.array([], dtype=np.int32)
    if do_Pkm: indexes = np.hstack([indexes, indexes_Pkm])
    if do_Pkc: indexes = np.hstack([indexes, indexes_Pkc])
    if do_HMF: indexes = np.hstack([indexes, indexes_HMF])
    if do_VSF: indexes = np.hstack([indexes, indexes_VSF])
    all_bins = len(indexes)

    # fill the subcovariance
    new_Cov  = np.zeros((all_bins,all_bins), dtype=np.float64)
    for i,id1 in enumerate(indexes):
        for j,id2 in enumerate(indexes):
            new_Cov[i,j] = Cov[id1,id2]

    return new_Cov

# This routine reads and returns the covariance matrix
def read_covariance(f_Cov):
    f           = open(f_Cov, 'r') #read the header: number of bins of each probe
    bins_probes = np.array(f.readline().split()[1:], dtype=np.int32);  f.close()
    X1, X2, Cov = np.loadtxt(f_Cov, unpack=True) #read covariance
    bins        = int(round(np.sqrt(len(X1))))   #find the number of bins
    Cov         = np.reshape(Cov, (bins,bins))   #reshape covariance
    X           = X2[:bins]                      #get the values of the X-axis
    return bins_probes, X, Cov

# This routine computes the covariance matrix of all probes
def covariance(realizations, BoxSize, snapnum, root_data, root_results,
               kmax_m=0,                                           #Pkm parameters
               kmax_c=0,                                           #Pkc parameters
               Radii=0,                                            #VSF parameters    
               HMF_bins=0, Nmin=0, Nmax=0):                        #HMF parameters

    # find redshift and define the working folders
    z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]
    folder = '/%s/covariance'%root_results
    if myrank==0 and not(os.path.exists(folder)): 
        os.system('mkdir %s'%folder)
    comm.Barrier()

    # perform checks and compute binning
    Pkm_bins, mean_km      = binning_Pk(root_data+'Pk/fiducial/', z, kmax_m)  #Pkm
    Pkc_bins, mean_kc      = binning_Pk(root_data+'Pk/fiducial/', z, kmax_c)  #Pkc
    bins_HMF, dN, Nmean    = binning_HMF(Nmin, Nmax, HMF_bins)                #HMF
    VSF_bins, dR, Rmean    = binning_VSF(Radii)                               #VSF

    # find the vector with the X-values (only needed to save the covariances)
    mean = np.hstack([mean_km, mean_kc, Nmean, Rmean])

    # find the suffix name
    suffix = '%d_Pkm_%.2f_Pkc_%.2f_HMF_%.1e_%.1e_%d_VSF_%s_z=%s.txt'\
        %(realizations, kmax_m, kmax_c, Nmin, Nmax, HMF_bins, Radii, z)

    # compute the total number of bins
    bins = Pkm_bins + Pkc_bins + HMF_bins + VSF_bins
    if myrank==0:
        print '\n%d bins: %d(Pkm) + %d(Pkcb) + %d(HMF) + %d(VSF)\n'\
            %(bins, Pkm_bins, Pkc_bins, HMF_bins, VSF_bins)

    # find the name of the output files; if they exists, just read them
    fout  = '%s/Cov_%s'%(folder,suffix)
    fout1 = '%s/Cov_norm_%s'%(folder,suffix)
    if os.path.exists(fout):  return read_covariance(fout)

    ########### read all the data ############
    if myrank==0:  print 'Reading data at z=%s...'%z

    # define the array hosting all the data
    data_p = np.zeros((realizations,bins), dtype=np.float64) #data each cpu reads
    data   = np.zeros((realizations,bins), dtype=np.float64) #Matrix with all data

    # each cpu reads its corresponding data
    numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]
    for i in numbers:
        if i%1000==0:  print i
        folder_Pk  = '%s/Pk/fiducial/%d'%(root_data,i)
        folder_HMF = '%s/Halos/fiducial/%d'%(root_data,i)
        folder_VSF = '%s/Voids/fiducial/%d'%(root_data,i)
        dumb = np.array([], dtype=np.float64)
        dumb = np.hstack([dumb, read_Pkm_data(folder_Pk,z,kmax_m)])
        dumb = np.hstack([dumb, read_Pkc_data(folder_Pk,z,kmax_c)])
        dumb = np.hstack([dumb, read_HMF_data(folder_HMF,snapnum,bins_HMF,dN,BoxSize)])
        dumb = np.hstack([dumb, read_VSF_data(folder_VSF,z)])
        data_p[i] = dumb

    # join the data of the different cpus into a single matrix (only for master)
    comm.Reduce(data_p, data, root=0);  del data_p

    # compute the mean and std of the data
    data_mean, data_std = np.mean(data, axis=0), np.std(data,  axis=0)
    ############################################

    ########## compute the covariance ##########
    if myrank>0:  return 0,0,0
    print 'Computing the covariance at z=%s...'%z

    # define the arrays containing the covariance and correlation matrices
    Cov = np.zeros((bins,bins), dtype=np.float64)
    Cor = np.zeros((bins,bins), dtype=np.float64)

    # compute the covariance matrix
    for i in xrange(bins):
        for j in xrange(i,bins):
            Cov[i,j] = np.sum((data[:,i]-data_mean[i])*(data[:,j]-data_mean[j])) 
            if j>i:  Cov[j,i] = Cov[i,j]
    Cov /= (realizations-1.0)

    # compute the normalized covariance matrix
    f = open(fout, 'w');  g = open(fout1, 'w')
    f.write('# %d %d %d %d\n'%(Pkm_bins, Pkc_bins, HMF_bins, VSF_bins2)) #header (#-bins)
    g.write('# %d %d %d %d\n'%(Pkm_bins, Pkc_bins, HMF_bins, VSF_bins2)) #header (#-bins)
    for i in xrange(bins):
        for j in xrange(bins):
            Cor[i,j] = Cov[i,j]/np.sqrt(Cov[i,i]*Cov[j,j])
            f.write('%.8e %.8e %.8e\n'%(mean[i], mean[j], Cov[i,j]))
            g.write('%.8e %.8e %.8e\n'%(mean[i], mean[j], Cor[i,j]))
    f.close();  g.close()

    # read and return the covariance
    return read_covariance(fout)
#######################################################################################


#######################################################################################
# This functions computes the derivatives with respect to the different parameters
def derivatives(realizations, BoxSize, snapnum, root_data, root_results,
                kmax_m=0,                                           #Pkm parameters
                kmax_c=0,                                           #Pkc parameters
                Radii=0,                                            #VSF parameters    
                HMF_bins=0, Nmin=0, Nmax=0):                        #HMF parameters


    cosmologies = ['Om_p/',  'Ob_p/',  'Ob2_p/', 'h_p/', 'ns_p/', 's8_p/', 
                   'Om_m/',  'Ob_m/',  'Ob2_m/', 'h_m/', 'ns_m/', 's8_m/', 
                   'Mnu_p/', 'Mnu_pp/', 'Mnu_ppp/', 'fiducial_NCV/']

    parameters = ['Om',  'Ob',   'Ob2',  'h',   'ns',  's8',   'Mnu']
    diffs      = [0.01,  0.001,  0.002,  0.02,  0.02,  0.015,  0.10]

    # find the corresponding redshift
    z_dict = {4:0, 3:0.5, 2:1, 1:2, 0:3};  z = z_dict[snapnum] 

    # perform checks and compute binning
    Pkm_bins, mean_km      = binning_Pk(root_data+'Pk/fiducial/', z, kmax_m)  #Pkm
    Pkc_bins, mean_kc      = binning_Pk(root_data+'Pk/fiducial/', z, kmax_c)  #Pkc
    bins_HMF, dN, Nmean    = binning_HMF(Nmin, Nmax, HMF_bins)                #HMF
    VSF_bins, dR, Rmean    = binning_VSF(Radii)                               #VSF

    # find the suffixes
    suffix_Pkm = 'Pk_m_%d_%.2f_z=%s.txt'%(realizations, kmax_m, z)
    suffix_Pkc = 'Pk_c_%d_%.2f_z=%s.txt'%(realizations, kmax_c, z)
    suffix_HMF = 'HMF_%d_%.1e_%.1e_%d_z=%s.txt'%(realizations, Nmin, Nmax, HMF_bins, z)
    suffix_VSF = 'VSF_%d_%s_z=%s.txt'%(realizations, Radii, z)

    folder = '%s/derivatives/'%root_results
    if myrank==0 and not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    # do a loop over the different cosmologies
    for cosmo in cosmologies:

        # create output folder if it does not exists
        folder = '%s/derivatives/%s'%(root_results, cosmo)
        if myrank==0 and not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

        # do a loop over the different probes
        for probe in ['Pkm', 'Pkc', 'HMF', 'VSF']: 

            comm.Barrier() #synchronize threads

            if   probe=='Pkm': bins, mean, suffix = Pkm_bins,  mean_km,  suffix_Pkm
            elif probe=='Pkc': bins, mean, suffix = Pkc_bins,  mean_kc,  suffix_Pkc
            elif probe=='HMF': bins, mean, suffix = HMF_bins,  mean_HMF, suffix_HMF
            elif probe=='VSF': bins, mean, suffix = VSF_bins2, mean_VSF, suffix_VSF

            # find output file name
            fout = '%s/mean_%s'%(folder,suffix)
            if os.path.exists(fout):  continue

            # define the array hosting the data
            data_p = np.zeros((2*realizations,bins), dtype=np.float64) 
            data   = np.zeros((2*realizations,bins), dtype=np.float64) 

            # do a loop over the different realizations
            count, count_p = np.array([0]), np.array([0])
            numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]
            for i in numbers:
                for pair in [0,1]:

                    folder1 = '%s/%s/NCV_%d_%d/'%(root_data,cosmo,pair,i)
                    if probe=='Pkm':  
                        data_p[2*i+pair] = read_Pkm_data(folder1, z, kmax_m)
                    elif probe=='Pkc':
                        data_p[2*i+pair] = read_Pkc_data(folder1, z, kmax_c)
                    elif probe=='HMF':
                        data_p[2*i+pair] = \
                            read_HMF_data(folder1, snapnum, bins_HMF, dN, BoxSize)
                    elif probe=='VSF':
                        data_p[2*i+pair] = \
                            read_VSF_data(folder1, z, BoxSize, grid, bins_VSF, dR)
                    count_p[0] += 1

            # join all data into a single matrix (only for master)
            comm.Reduce(data_p,  data,  root=0)
            comm.Reduce(count_p, count, root=0)
            if myrank>0:  continue

            # save results to file (only master)
            data_mean, data_std = np.mean(data, axis=0), np.std(data, axis=0)
            np.savetxt(fout, np.transpose([mean, data_mean, data_std]))
            print '%d realizations found for %s probe %s'%(count,cosmo,probe)


    ##### derivatives #####
    if myrank>0:  return 0
    folder = '%s/derivatives/'%root_results
    if not(os.path.exists(folder)):  os.system('mkdir %s'%folder)

    # do a loop over the different probes
    for probe in ['Pkm', 'Pkc', 'HMF', 'VSF']:
        
        if   probe=='Pkm': suffix = suffix_Pkm
        elif probe=='Pkc': suffix = suffix_Pkc
        elif probe=='HMF': suffix = suffix_HMF
        elif probe=='VSF': suffix = suffix_VSF

        for parameter,diff in zip(parameters,diffs):
            
            # find name of output file
            fout = '%s/derivative_%s_%s'%(folder, parameter, suffix)
            if os.path.exists(fout):  continue

            if parameter=='Mnu':
                f0 = '%s/fiducial_NCV/mean_%s'%(root_results,suffix)
                f1 = '%s/Mnu_p/mean_%s'%(root_results,suffix)
                f2 = '%s/Mnu_pp/mean_%s'%(root_results,suffix)
                f4 = '%s/Mnu_ppp/mean_%s'%(root_results,suffix)
                X, Y0, dY0 = np.loadtxt(f0, unpack=True)
                X, Y1, dY1 = np.loadtxt(f1, unpack=True)
                X, Y2, dY2 = np.loadtxt(f2, unpack=True)
                X, Y4, dY4 = np.loadtxt(f4, unpack=True)
                deriv  = (4.0*Y2 - 3.0*Y0 - Y4)/(2.0*2.0*diff)
                deriv1 = (Y1 - Y0)/(1.0*diff)
                deriv2 = (Y2 - Y0)/(2.0*diff)
                deriv3 = (Y4 - Y0)/(4.0*diff)
                deriv4 = (4.0*Y1 - 3.0*Y0 - Y2)/(2.0*diff)
                np.savetxt('%s/derivative_Mnu_0.1-0.0_%s'%(folder,suffix), 
                           np.transpose([X, deriv1]))
                np.savetxt('%s/derivative_Mnu_0.2-0.0_%s'%(folder,suffix), 
                           np.transpose([X, deriv2]))
                np.savetxt('%s/derivative_Mnu_0.4-0.0_%s'%(folder,suffix), 
                           np.transpose([X, deriv3]))
                np.savetxt('%s/derivative_Mnu_0.2-0.1_0.0_%s'%(folder,suffix), 
                           np.transpose([X, deriv4]))

            else:
                f1 = '%s/%s_m/mean_%s'%(root_results, parameter, suffix)
                f2 = '%s/%s_p/mean_%s'%(root_results, parameter, suffix)
                X, Ym, dYm = np.loadtxt(f1, unpack=True)
                X, Yp, dYp = np.loadtxt(f2, unpack=True)
                deriv = (Yp - Ym)/(2.0*diff)

            np.savetxt('%s/derivative_%s_%s'%(folder, parameter, suffix), 
                       np.transpose([X, deriv]))
#######################################################################################



#######################################################################################
######################################## Pk ###########################################
# This routine determines the number of bins until kmax
def binning_Pk(folder,z,kmax):
    if kmax==0:  raise Exception('kmax have to be larger than 0')
    fin = '%s/0/Pk_m_z=%s.txt'%(folder,z)         #take the first realization
    k, Pk = np.loadtxt(fin, unpack=True)          #read its power spectrum
    indexes = np.where(k<=kmax)[0]
    return len(indexes), k[indexes]

# This routine reads the Pk_m of a given realization
def read_Pkm_data(folder,z,kmax):
    k, Pk_p = np.loadtxt('%s/Pk_m_z=%s.txt'%(folder,z), unpack=True)
    indexes = np.where(k<kmax)[0]
    return Pk_p[indexes]

# This routine reads the Pk_cb of a given realization
def read_Pkc_data(folder,z,kmax):
    f1 = '%s/Pk_cb_z=%s.txt'%(folder,z)
    f2 = '%s/Pk_m_z=%s.txt'%(folder,z)
    if os.path.exists(f1):  k, Pk_p = np.loadtxt(f1, unpack=True)
    else:                   k, Pk_p = np.loadtxt(f2, unpack=True)
    indexes = np.where(k<kmax)[0]
    return Pk_p[indexes]
#######################################################################################
#######################################################################################

#######################################################################################
####################################### VSF ###########################################
# This function computes the binning of the VSF
def binning_VSF(Radii):
    dR    = Radii[1:] - Radii[:-1]       #size of the bin
    Rmean = 0.5*(Radii[1:] + Radii[:-1]) #value of R in the intervals
    return len(Radii), dR, Rmean

# This routine computes the VSF for a given realization
def read_VSF_data(folder, z):
    f = h5py.File('%s/void_catalogue_m_z=%s.hdf5'%(folder,z), 'r')
    VSF_p = f['VSF'][:];  f.close()    
    return VSF_p*1e9
#######################################################################################
#######################################################################################

#######################################################################################
####################################### HMF ###########################################
# This function computes the binning of the HMF
def binning_HMF(Nmin, Nmax, HMF_bins):
    if HMF_bins==0 or Nmin==0 or Nmax==0:
        raise Exception('HMF_bins, Nmin and Nmax have to be larger than 0')
    bins_HMF = np.logspace(np.log10(Nmin), np.log10(Nmax), HMF_bins+1)
    dN       = bins_HMF[1:] - bins_HMF[:-1]       #size of the bin
    Nmean    = 0.5*(bins_HMF[1:] + bins_HMF[:-1]) #mean of the bin
    return bins_HMF,dN,Nmean

# This routine computes the HMF for a given realization
def read_HMF_data(snapdir, snapnum, bins_HMF, dN, BoxSize):
    FoF     = readfof.FoF_catalog(snapdir,snapnum,long_ids=False,
                                  swap=False,SFR=False,read_IDs=False)
    mass    = FoF.GroupMass*1e10  #Msun/h  
    part    = FoF.GroupLen        #number of particles in the halo
    p_mass  = mass[0]/part[0]     #mass of a single particle in Msun/h
    mass    = p_mass*(part*(1.0-part**(-0.6))) #corect FoF masses
    return np.histogram(part, bins=bins_HMF)[0]/(dN*BoxSize**3)*1e12
#######################################################################################
#######################################################################################
