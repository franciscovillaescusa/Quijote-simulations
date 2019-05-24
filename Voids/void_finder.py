import argparse
import numpy as np 
import sys,os,time
import void_library as VL
import readgadget
import MAS_library as MASL
import h5py

# read the first and last realization to identify voids
parser = argparse.ArgumentParser(description="This code identifies voids from the realization first to the realization last in the cosmology cosmo")
parser.add_argument("first", help="first realization number", type=int)
parser.add_argument("last",  help="last  realization number", type=int)
parser.add_argument("cosmo", help="folder with the realizations")
args = parser.parse_args()


# This routine find the voids and save them to a file
def find_voids(snapshot, ptypes, grid, MAS, do_RSD, axis, threshold, Radii,
               threads1, threads2, fout):
    
    # read snapshot header and obtain BoxSize and redshift
    head     = readgadget.header(snapshot)
    BoxSize  = head.boxsize/1e3  #Mpc/h                      
    redshift = head.redshift
    
    # compute density field
    delta = MASL.density_field_gadget(snapshot, ptypes, grid, MAS, do_RSD, axis)
    delta /= np.mean(delta, dtype=np.float64);  delta -= 1.0
    
    # identify voids
    V = VL.void_finder(delta, BoxSize, threshold, Radii, 
                       threads1, threads2, void_field=False)

    # void properties and void size function
    void_pos    = V.void_pos
    void_radius = V.void_radius
    VSF_R       = V.Rbins     # bins in radius
    VSF         = V.void_vsf  # void size function
        
    parameters = [grid, MAS, '%s'%ptypes, threshold, '%s'%Radii]

    # save the results to file
    f = h5py.File(fout, 'w')
    f.create_dataset('parameters',    data=parameters)
    f.create_dataset('pos',           data=void_pos)
    f.create_dataset('radius',        data=void_radius)
    f.create_dataset('VSF_Rbins',     data=VSF_R)
    f.create_dataset('VSF',           data=VSF)
    f.close()



root = '/simons/scratch/fvillaescusa/pdf_information/%s'%args.cosmo
################################# INPUT ######################################
# density field parameters
grid    = 768
MAS     = 'PCS'
do_RSD  = False
axis    = 0
snapnum = 4

# void finder parameters
threshold = -0.5
Radii     = np.array([41, 39, 37, 35, 33, 31, 29, 27, 25, 23, 21, 19, 17, 15, 13, 
                      11, 9, 7, 5], dtype=np.float32)*1000.0/768
threads1  = 16
threads2  = 4

root_out = '/simons/scratch/fvillaescusa/pdf_information/Voids/%s'%args.cosmo
##############################################################################

z_dict = {4:0, 3:0.5, 2:1, 1:2, 0:3}

# create output folder if it does not exists
if not(os.path.exists(root_out)):  os.system('mkdir %s'%root_out)

# do a loop over the different realizations
for i in xrange(args.first, args.last):

    # loop over standard and paired fixed simulations
    for prefix in ['%d'%i, 'NCV_0_%d'%i, 'NCV_1_%d'%i]:

        # find the name of the snapshot
        snapshot = '%s/%s/snapdir_%03d/snap_%03d'%(root, prefix, snapnum, snapnum)
        if not(os.path.exists(snapshot+'.0')) and not(os.path.exists(snapshot+'.0.hdf5')):
            continue

        # find output name and create void folder if doesnt exists
        output_folder = '%s/%s/'%(root_out, prefix)
        if not(os.path.exists(output_folder)):  os.system('mkdir %s'%output_folder)

        # find output file name
        fout = '%s/void_catalogue_m_z=%s.hdf5'%(output_folder, z_dict[snapnum])
        if not(os.path.exists(fout)): 

            # for massive neutrinos identify voids in the CDM+baryons field
            if args.cosmo in ['Mnu_p', 'Mnu_pp', 'Mnu_ppp']:

                # identify voids in total matter
                find_voids(snapshot, [-1], grid, MAS, do_RSD, axis, 
                           threshold, Radii, threads1, threads2, fout)

                # identify voids in CDM+baryons
                fout = '%s/void_catalogue_c_z=%s.hdf5'%(output_folder, z_dict[snapnum])
                if not(os.path.exists(fout)): 
                    find_voids(snapshot, [1], grid, MAS, do_RSD, axis, 
                               threshold, Radii, threads1, threads2, fout)

            else:

                # identify voids
                find_voids(snapshot, [1], grid, MAS, do_RSD, axis, 
                           threshold, Radii, threads1, threads2, fout)

