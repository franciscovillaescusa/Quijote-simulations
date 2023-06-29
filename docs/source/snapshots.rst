.. _snapshots:

Snapshots
=========

The snapshots are stored in either Gadget-II format or HDF5. They can be read using the `readgadget.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readgadget.py>`_ and `readsnap.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readsnap.py>`_ scripts. If you have `Pylians <https://github.com/franciscovillaescusa/Pylians3>`_ installed you already have them. The user can find an example on how to read and manipulate Quijote snapshots in :ref:`tutorials`.

The snapshots only contain 4 blocks:

- Header: This block contains general information about the snapshot such as redshift, number of particles, box size, particle masses...etc.
- Positions: This block contains the positions of all particles. Stored as 32-floats
- Velocities: This block contains the velocities of all particles. Stored as 32-floats
- IDs: This block contains the IDs of all particles. Stored as 32-integers. (This block may be removed in the future to reduce the size of the snapshots)

An example on how to read a snapshot is this:

.. code-block:: python
		
    import numpy as np
    import readgadget

    # input files
    snapshot = '/home/fvillaescusa/Quijote/Snapshots/h_p/snapdir_002/snap_002'
    ptype    = [1] #[1](CDM), [2](neutrinos) or [1,2](CDM+neutrinos)

    # read header
    header   = readgadget.header(snapshot)
    BoxSize  = header.boxsize/1e3  #Mpc/h
    Nall     = header.nall         #Total number of particles
    Masses   = header.massarr*1e10 #Masses of the particles in Msun/h
    Omega_m  = header.omega_m      #value of Omega_m
    Omega_l  = header.omega_l      #value of Omega_l
    h        = header.hubble       #value of h
    redshift = header.redshift     #redshift of the snapshot
    Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#Value of H(z) in km/s/(Mpc/h)
    
    # read positions, velocities and IDs of the particles
    pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #positions in Mpc/h
    vel = readgadget.read_block(snapshot, "VEL ", ptype)     #peculiar velocities in km/s
    ids = readgadget.read_block(snapshot, "ID  ", ptype)-1   #IDs starting from 0
    
In the simulations with massive neutrinos it is possible to read the positions, velocities and IDs of the neutrino particles. Notice that the field should contain exactly 4 characters, that can be blank: :code:`"POS "`, :code:`"VEL "`, :code:`"ID  "`. The number in the name of the snapshot represents its redshift:

- 000 ------> z=3
- 001 ------> z=2
- 002 ------> z=1
- 003 ------> z=0.5
- 004 ------> z=0


.. warning::

   In February 2023 we compressed the Qujote snapshots due to storage limitations. While the format is exactly the same, you may enconter problems reading them if you don't use Pylians. In order to read them you will need both hdf5 and hdf5plugin.

   For instance, if you are reading the snapshots using h5py directly, you will need to install hdf5plugin, ``python -m pip install hdf5plugin``, and then import both h5py and hdf5plugin

   .. code-block:: python
   
      import h5py
      import hdf5plugin

   `Reach out <mailto:villaescusa.francisco@gmail.com>`_ if you experience problems.

Initial conditions
------------------

On top of the snapshots at redshifts 0, 0.5, 1, 2, and 3, we also provide the initial conditions for each simulation. Those can be stored as hdf5 files or as Gadget format I files. In both cases, you can read the positions, velocities, and IDs of the particles using the above example just using as snapshot the name of the initial conditions, for instance:

.. code-block:: python
		
   snapshot = '/home/fvillaescusa/Quijote/Snapshots/w_p/ICs/ics'

If you want to use the linear matter power spectrum used to create the initial conditions, take a look at :ref:`linear_Pk`.
   
.. note::
   
   We note that the particle IDs are unique across snapshots. For instance, particles with an ID equal to 43623 at redshifts 0, 0.5, and 127 represent the very same particle at different times. This can be used to track particles back/forward in time; for instance, can be used to identify the Lagrangian region of a halo or a void.


Compression
-----------
The particle positions, velocities, and PID, are stored in HDF5 files, using HDF5 compression filters to reduce the disk usage.  Specifically, the files use the Blosc compression filter, as implemented in the `hdf5plugin <https://github.com/silx-kit/hdf5plugin/>`_ Python package.  Blosc compression applies a transpose to the data then passes it to zstandard, all of which is lossless and transparent to the user.  As a preconditioning step to increase the Blosc compression ratio, we manually null out some bits of the positions and velocities to increase the compression ratio.  This step is lossy.  The typical total compression ratio is 2.5x.

The positions are stored as absolute coordinates in float32 precision.  The lossy preconditioning we apply is to set several of the low bits in the float32 significand to zero.  The number of bits nulled out is B=6 for the 1024^3 simulations, B=7 for 512^3, and B=8 for 256^3.  This introduces a fractional error of 2^(-24+B), which is 3.8e-6 for the 1024^3 simulations.  Since these are 1 Gpc/h simulations, this is 3.8 kpc/h precision worst-case.  The softening length in all cases is 1/40th of the interparticle spacing, or 24.4 kpc/h for 1024^3.  Therefore, the lossiness is 6.4x smaller than the softening length and should have a minimal impact on science analyses.

Likewise, we null out 11 low bits of the velocities, for a fractional precision of 0.01%.  The velocity rarely goes above 6000 km/s in LCDM simulations, so this is a worst case of 0.6 km/s precision.

No lossy compression is applied to the IC files, or to the PIDs.

Each HDF5 file also has a new group called ``/CompressionInfo`` whose attributes contain a JSON string describing the exact compression options used.

The scripts used to do the compression are here: https://github.com/lgarrison/quijote-compression
