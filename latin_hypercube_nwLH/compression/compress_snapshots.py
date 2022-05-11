from mpi4py import MPI
import numpy as np
import sys,os,h5py,glob,time
import functools
import readgadget

###### MPI DEFINITIONS ######                                    
comm   = MPI.COMM_WORLD
nprocs = comm.Get_size()
myrank = comm.Get_rank()

# This function takes a snapshot and compress it
def compress_snapshot(snap_in, snap_out, myrank, nprocs, gzip, check_files):

    # get the compression level
    if gzip==0:  compression_opts = None
    else:        compression_opts = gzip

    # read the number of subfiles in the snapshot
    filenum  = (readgadget.header(snap_in)).filenum
    filenum2 = len(glob.glob('%s.*'%snap_in))
    if filenum!=filenum2:  raise Exception('problem with number of subfiles')

    #################### COMPRESS FILES #################
    # do a loop over all subfiles
    for i in range(filenum):

        # get the names of input and output files
        filename    = '%s.%d.hdf5'%(snap_in, i)
        outfilename = '%s.%d.hdf5'%(snap_out,i)
        if os.path.exists(outfilename):  continue

        # open input and output files
        fs = h5py.File(filename,    'r')
        fd = h5py.File(outfilename, 'w')

        # core call
        copy_datasets = functools.partial(copy_level0, fs, fd, compression_opts)
        fs.visititems(copy_datasets)
        fd.close();  fs.close()
    #####################################################

    # check if files are identical
    if check_files:  os.system('h5diff %s %s'%(filename, outfilename))
    print('Snapshot succesfully compressed')


# This function writes the compressed file
def copy_level0(fs, fd, compression_opts, name, node):
    """full copy of datasets + header: chunking + compressing"""

    if isinstance(node, h5py.Dataset):
        compression = 'gzip'
        if not compression_opts:
            compression = None
        dnew = fd.create_dataset(
            name, data=node, dtype=node.dtype, chunks=True,
            shuffle=True, compression=compression,
            compression_opts=compression_opts, fletcher32=True)

    elif isinstance(node, h5py.Group) and name == 'Header':
        fs.copy(name, fd, name=name)

###################################### INPUT ###########################################
root         = '/mnt/ceph/users/fvillaescusa/Quijote/nwLH'
gzip         = 4
snapnums     = [0,1,2,3,4]
start        = 1500
end          = 2000
check_files  = False
########################################################################################

"""
############################ compress snapshopts ##############################
###############################################################################
# find the numbers that each cpu will work with                  
numbers = np.where(np.arange(start,end)%nprocs==myrank)[0]
numbers = np.arange(start,end)[numbers]

# do a loop over the different realizations
for i in numbers:

    # do a loop over the different snapshots
    for snapnum in snapnums:

        # find the names of the original and compressed snapshot
        folder_out = '%d/snapdir_%03d'%(i,snapnum)
        snap_in    = '%s/%d/snapdir_%03d/snap_%03d'%(root,i,snapnum,snapnum)
        snap_out   = '%s/snap_%03d'%(folder_out,snapnum)

        if not(os.path.exists(folder_out)):  os.makedirs(folder_out)
        print('Compressing %s'%snap_in)
        comm.Barrier()

        # compress the snapshot
        compress_snapshot(snap_in, snap_out, myrank, nprocs, gzip, check_files)
        comm.Barrier()

        # count the number of subfiles
        files1 = len(glob.glob('%s*'%snap_in))
        files2 = len(glob.glob('%s*'%snap_out))
        if files1!=files2:  raise Exception('number of files differ!!!')
comm.Barrier()
if myrank==0:  
    print('All snapshots compressed!!!')
    print('Verifying that files are identical...')
"""


##################################################################
######################## check files #############################
# find the numbers that each cpu will work with                  
numbers = np.where(np.arange(start,end)%nprocs==myrank)[0]
numbers = np.arange(start,end)[numbers]

# do a loop over the different realizations
for i in numbers:

    print(i)

    # do a loop over the different snapshots
    for snapnum in snapnums:

        # do a loop over all subfiles
        for j in range(8):
            file1 = '%s/%d/snapdir_%03d/snap_%03d.%d.hdf5'%(root,i,snapnum,snapnum,j)
            file2 = '%d/snapdir_%03d/snap_%03d.%d.hdf5'%(i,snapnum,snapnum,j)
            os.system('h5diff %s %s'%(file1, file2))

print('Done!!')

