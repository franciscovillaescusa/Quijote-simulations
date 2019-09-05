# This file contains different routines used in the BCP (Big Covariance Project)
import numpy as np
import sys,os
import Pk_library as PKL
import cosmology_library as CL
import integration_library as IL

#########################################################################################
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


#########################################################################################
# This routine reads the covariance matrix from a file and returns its inverse up to kmax
# f_Cov -----> file containing the covariance matrix
# kmax ------> the covariance will be trucated at kmax
def Inverse_Cov(f_Cov,kmax):
    print '\n########## Computing inverse of covariance #########'
    
    # read covariance matrix
    k1, k2, Cov = np.loadtxt(f_Cov, unpack=True)

    # find the number of bins in the covariance
    bins = int(round(np.sqrt(len(k1))))

    # reshape covariance
    Cov = np.reshape(Cov, (bins,bins))

    # find the number of elements until kmax
    k = k2[:bins]
    elements = len(np.where(k<kmax)[0])
    k = k[:elements]

    # keep the covariance only until kmax
    Cov = Cov[:elements, :elements]

    # compute the inverse of the covariance
    ICov = Inv_Cov(Cov)

    # save results to file
    #f = open('inverse.txt', 'w')
    #for i in xrange(elements):
    #    for j in xrange(elements):
    #        f.write('%.5e %.5e %.5e \n'\
    #                %(k2[i], k2[j], ICov[i,j]/np.sqrt(ICov[i,i]*ICov[j,j])))
    #f.close()

    return k, ICov
#########################################################################################


#########################################################################################
# This routine computes the Fisher matrix of the matter Pk (linear or non-linear)
# f_Cov -------> File containing the covariance to be used
# root_derv ---> Folder containing the different derivatives
# realizations_der ---> number of realiztions used to compute the derivatives
# z -----------> Redshift at which compute the Fisher
# kmax --------> Maximum k to consider for the Fisher
# parameters --> Array with the name of the considered cosmo parameters ['Om','Ob','ns']
def Fisher_Pk(f_Cov, root_derv, realizations_der, z, kmax, parameters, linear=False):
    
    # find the number of cosmological parameters
    params_num = len(parameters)

    # find the inverse of the covariance matrix
    k, ICov = Inverse_Cov(f_Cov, kmax)
    bins = len(k)

    # define the matrix containing the derivatives
    derivative = np.zeros((params_num, bins), dtype=np.float64)

    # read the derivatives
    for i in xrange(params_num):
        
        if linear:
            k_par, derv, Nmodes = \
            np.loadtxt('%s/derivative_rebin_%s_z=%.1f.txt'%(root_derv,parameters[i],z), 
                           unpack=True)
        else:
            k_par, derv = \
                np.loadtxt('%s/derivative_%s_Pk_m_%d_z=%s.txt'\
                           %(root_derv,parameters[i],realizations_der,z), unpack=True)

        elements = len(np.where(k_par<kmax)[0])
        k_par = k_par[:elements];  derv = derv[:elements]
        
        if np.allclose(k_par, k, rtol=1e-8, atol=1e-10):  derivative[i] = derv
        else:  raise Exception('k-values are different!!!')

    # compute the Fisher matrix
    Fisher = np.zeros((params_num, params_num), dtype=np.float64)

    for i in xrange(params_num):
        for j in xrange(i, params_num):
            if i==j:
                Fisher[i,j] = np.dot(derivative[i], np.dot(ICov, derivative[i]))
            else:
                Fisher[i,j] = 0.5*(np.dot(derivative[i], np.dot(ICov, derivative[j])) + \
                                   np.dot(derivative[j], np.dot(ICov, derivative[i])))
                Fisher[j,i] = Fisher[i,j]

    return Fisher
#########################################################################################

#########################################################################################
# This routine computes the analytic Fisher matrix of a set of parameters
# parameter ------> set of paramters used ['Om', 'Ob', 'h', 'ns', 's8']
# z --------------> considered redshift
# V --------------> considered volume in (Mpc/h)^3
# kmax -----------> maximum considered k in h/Mpc
# root_derv ------> folder containing the analytic derivatives
def analytic_Fisher(parameter, z, V, kmax, root_derv):

    num_params = len(parameter)

    # define the Fisher matrix
    Fisher = np.zeros((num_params,num_params), dtype=np.float64)

    # compute the value of kmin
    kmin = 2.0*np.pi/V**(1.0/3.0)

    # check that all ks are equally spaced in log
    for i in xrange(num_params):
        k, deriv = np.loadtxt('%s/derivative_%s_z=%.1f.txt'%(root_derv,parameter[i],z), 
                              unpack=True)
        dk = np.log10(k[1:]) - np.log10(k[:-1])
        if not(np.allclose(dk, dk[0])):
            raise Exception('k-values not log distributed')

    # compute sub-Fisher matrix
    for i in xrange(num_params):
        for j in xrange(i,num_params):
            #if i==5:
            #    k1, deriv1 = np.loadtxt('%s/log_derivative_%s_cb_z=%.1f.txt'%(root_derv,parameter[i],z), unpack=True)
            #else:
            k1, deriv1 = np.loadtxt('%s/log_derivative_%s_z=%.1f.txt'%(root_derv,parameter[i],z), unpack=True)
            #if j==5:
            #    k2, deriv2 = np.loadtxt('%s/log_derivative_%s_cb_z=%.1f.txt'%(root_derv,parameter[j],z), unpack=True)
            #else:
            k2, deriv2 = np.loadtxt('%s/log_derivative_%s_z=%.1f.txt'%(root_derv,parameter[j],z), unpack=True)

            if np.any(k1!=k2):  raise Exception('k-values are different!')
        
            yinit = np.zeros(1, dtype=np.float64) 
            eps   = 1e-16
            h1    = 1e-18 
            hmin  = 0.0   
            function = 'log'

            I = IL.odeint(yinit, kmin, kmax, eps, h1, hmin,
                          np.log10(k1), k**2*deriv1*deriv2,
                          function, verbose=False)[0]

            Fisher[i,j] = I
            if i!=j:  Fisher[j,i] = Fisher[i,j]

    # add prefactors to subFisher matrix
    Fisher = Fisher*V/(2.0*np.pi)**2

    return Fisher
#########################################################################################

#########################################################################################
# This routines takes a continuous curve and rebin it in the same way as for the Pk
# fin --------> file with the input continuous data
# BoxSize ----> size of the simulation box in Mpc/h
# grid -------> grid^3 is the number of cells in the considered grid
def Pk_binning(fin, BoxSize, grid):

    # read input file
    k_in, Pk_in = np.loadtxt(fin, dtype=np.float32, unpack=True)

    # compute expected Pk
    k, Pk, Nmodes = PKL.expected_Pk(k_in, Pk_in, BoxSize, grid)
    Pk = np.asarray(Pk)
    Nmodes = np.asarray(Nmodes)

    return k, Pk, Nmodes
#########################################################################################
