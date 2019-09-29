from mpi4py import MPI
import numpy as np
import sys,os
import readgadget
import cosmology_library as CL

###### MPI DEFINITIONS ######                             
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

##################################### INPUT #############################################
root         = '/simons/scratch/fvillaescusa/pdf_information/'
root_out     = '/simons/scratch/fvillaescusa/pdf_information/displacement_field/matter/'
model        = 'fiducial'
snapnum      = 4      #4(z=0) 3(z=0.5) 2(z=1) 1(z=2) 0(z=3)
ptype        = [1]    #1(CDM) 2(neutrinos)
BoxSize      = 1000.0 #Mpc/h
grid         = 512
realizations = 100

zi      = 127
Omega_m = 0.3175
Omega_l = 0.6825
#########################################################################################

z = {4:0, 3:0.5, 2:1, 1:2, 0:3}[snapnum]

# compute growth factor at z=127 and z_final
Di = CL.linear_growth_factor(zi, Omega_m, Omega_l) 
Df = CL.linear_growth_factor(z,  Omega_m, Omega_l) 

# find the numbers that each cpu will work with                      
numbers = np.where(np.arange(realizations)%nprocs==myrank)[0]

# do a loop over the different realizations
for i in numbers:

    print i

    # if output folder does not exists, create it. Get name of output file
    folder_out = '%s/%s/%d'%(root_out,model,i)
    if not(os.path.exists(folder_out)):  os.system('mkdir %s'%folder_out)
    fout1 = '%s/displacement_field_Nbody_z=%s.npy'%(folder_out,z)
    fout2 = '%s/displacement_field_ZA_z=%s.npy'%(folder_out,z)
    if os.path.exists(fout1) and os.path.exists(fout2):  continue

    # find the name of the ICs and snapshot 
    ICs_snapshot = '%s/Snapshots/%s/%d/ICs/ics'%(root,model,i)
    snapshot     = '%s/Snapshots/%s/%d/snapdir_%03d/snap_%03d'\
                   %(root,model,i,snapnum,snapnum)


    # read the positions and IDs of the ICs
    pos_ICs = readgadget.read_block(ICs_snapshot, "POS ", ptype)/1e3 #Mpc/h
    IDs_ICs = readgadget.read_block(ICs_snapshot, "ID  ", ptype)-1   #IDs begin from 0

    # sort the ICs particles by IDs
    indexes = np.argsort(IDs_ICs)
    pos_ICs = pos_ICs[indexes];  del IDs_ICs



    # find the grid coordinates of the particles
    grid_index = (np.round((pos_ICs/BoxSize)*grid, decimals=0)).astype(np.int32)
    grid_index[np.where(grid_index==grid)]=0
    pos_lag    = grid_index*BoxSize/grid #get the lagrangian coordinates
    grid_index = grid_index[:,0]*grid**2 + grid_index[:,1]*grid + grid_index[:,2]
    indexes2   = np.argsort(grid_index)

    # safety check
    grid_index = grid_index[indexes2]
    diff = grid_index[1:] - grid_index[:-1]
    if np.any(diff!=1):  raise Exception('positions not properly sorted')



    # read the positions and IDs of the z=0 snapshot
    pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #Mpc/h
    IDs = readgadget.read_block(snapshot, "ID  ", ptype)-1   #Make IDs begin from 0

    # sort the particles by IDs
    indexes = np.argsort(IDs)
    pos     = pos[indexes];  del IDs

    
    ##################### N-body ########################
    # compute displacement field
    disp = pos - pos_lag;  del pos

    # take into account periodic boundary conditions
    disp[np.where(disp>BoxSize/2.0)]  -= BoxSize
    disp[np.where(disp<-BoxSize/2.0)] += BoxSize
    disp = disp[indexes2]

    # sort the displacements and save results to file
    np.save(fout1, disp)
    #####################################################

    ####################### ZA ##########################
    # compute displacement field
    disp = pos_ICs - pos_lag;  del pos_ICs

    # take into account periodic boundary conditions
    disp[np.where(disp>BoxSize/2.0)]  -= BoxSize
    disp[np.where(disp<-BoxSize/2.0)] += BoxSize
    disp = disp*Df/Di
    disp = disp[indexes2]

    # sort the displacements and save results to file
    np.save(fout2, disp)
    #####################################################
