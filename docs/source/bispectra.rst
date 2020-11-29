Bispectra
=========

The format of the individual bispectra files are:

- k1/kf | k2/kf | k3/kf | P0(k1) | P0(k2) | P0(k3) | B0(k1,k2,k3) | Q(k1,k2,k3) | B_SN(k1,k2,k3) | counts 

where k1, k2, k3 specify the length of the triangle sides, P0(k) is the power spectrum monopole, 
B0(k1,k2,k3) is the bispectrum monopole, Q(k1,k2,k3) is the reduced bipsectrum, B_SN is the 
bispectrum shot noise correction, and counts is the number of triangles in the bin. 
B0 is already shot-noise corrected. The header specifies kf, the fundamental mode, and Nhalo, 
the number of halos. 

The individual bispectra files can be read in python as follows, 

.. code-block:: python
		
    import numpy as np 

    k1, k2, k3, p0k1, p0k2, p0k3, b123, q123, b_sn, cnts = np.loadtxt(FILENAME, skiprows=1, unpack=True, usecols=range(10))

    # read header to get Nhalo 
    hdr   = open(FILENAME).readline().rstrip()
    Nhalo = int(hdr.split('Nhalo=')[-1])

Alternatively, sets of bispectra files for a specific redshift and cosmology can easily be accessed

.. code-block:: python
		
    import h5py 

    fbk    = h5py.File(FILENAME, 'r') 
    k1     = fbk['k1'][...]
    k2     = fbk['k2'][...]
    k3     = fbk['k3'][...]
    p0k1   = fbk['p0k1'][...]
    p0k2   = fbk['p0k2'][...]
    p0k3   = fbk['p0k3'][...]
    b123   = fbk['b123'][...] 
    q123   = fbk['q123'][...]
    b_sn   = fbk['b_sn'][...]
    cnts   = fbk['counts'][...] # triange counts
    Nhalos = fbk['Nhalos'][...] # number of halos 
    files  = fbk['files'][...]  # names of individual files. 
