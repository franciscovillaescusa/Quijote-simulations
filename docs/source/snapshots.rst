Snapshots
=========

The snapshots are stored in either Gadget-II format or HDF5. They can be read using the `readgadget.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readgadget.py>`_ and `readsnap.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readsnap.py>`_ scripts. If you have `Pylians <https://github.com/franciscovillaescusa/Pylians3>`_ installed you already have them.

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
