.. _halo_catalogues:

Halo catalogs
=============

Quijote contains FoF and Rockstar halo catalogs. The ``Halo`` folder contains three folders:

FoF
~~~

The FoF halo catalogs can be read through the `readfof.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readfof.py>`_ script. If you have `Pylians <https://github.com/franciscovillaescusa/Pylians3>`_ installed you already have it. An example on how to read a halo catalog is this (we provide further details on how to read and manipulate these catalogs in :ref:`tutorials`):

.. code-block:: python
		
    import readfof 

    # input files
    snapdir = '/home/fvillaescusa/Quijote/Halos/FoF/s8_p/145/' #folder hosting the catalogue
    snapnum = 4                                            #redshift 0

    # determine the redshift of the catalogue
    z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
    redshift = z_dict[snapnum]

    # read the halo catalogue
    FoF = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
		              swap=False, SFR=False, read_IDs=False)
										
    # get the properties of the halos
    pos_h = FoF.GroupPos/1e3            #Halo positions in Mpc/h
    mass  = FoF.GroupMass*1e10          #Halo masses in Msun/h
    vel_h = FoF.GroupVel*(1.0+redshift) #Halo peculiar velocities in km/s
    Npart = FoF.GroupLen                #Number of CDM particles in the halo

The number in the name of the halo catalogue represents its redshift:

- 000 ------> z=3
- 001 ------> z=2
- 002 ------> z=1
- 003 ------> z=0.5
- 004 ------> z=0

.. Note::

   The above correspondence applies to the majority of the simulations but not to all of them. For instance, for Quijote-ODD, 000 represents redshift 1 while 001 corresponds to redshift 0. Thus, we always recommend reading the redshift of the correspond snapshot.

FoF_id
~~~~~~

This folder contains FoF halo catalogs. There are two differences with respect to the above ``FoF`` folder. First, these halo catalogs contain the IDs of the particles belonging to the halos and second, it has been run over the compressed snapshots. Thus, there may be some small (likely negligible) differences among with respect to the halo catalogs in the FoF folder. For this reason we keep both halo catalogs. These halo catalogs can be read in exactly the same way as above, but now you can also access the IDs of the particles in a given halo as

.. code-block:: python
		
    import readfof 

    # input files
    snapdir = '/home/fvillaescusa/Quijote/Halos/FoF_id/s8_p/145/' #folder hosting the catalogue
    snapnum = 4                                                   #redshift 0

    # determine the redshift of the catalogue
    z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
    redshift = z_dict[snapnum]

    # read the halo catalogue
    FoF = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
		              swap=False, SFR=False, read_IDs=True)
										
    # get the properties of the halos
    pos_h = FoF.GroupPos/1e3            #Halo positions in Mpc/h
    mass  = FoF.GroupMass*1e10          #Halo masses in Msun/h
    vel_h = FoF.GroupVel*(1.0+redshift) #Halo peculiar velocities in km/s
    Npart = FoF.GroupLen                #Number of CDM particles in the halo

    # get the IDs of the halos
    IDs_h = FoF.GroupIDs

    # To get the IDs of the particles belong to the first halo one would do
    IDs_0  = IDs_h[0:Npart[0]]
    pos_0  = pos_h[0]
    mass_0 = mass_h[0]

    # Similarly, to get the IDs of the particles in the second halo one would do
    IDs_1  = IDs_h[Npart[0]:Npart[0]+Npart[1]]
    pos_1  = pos_h[1]
    mass_1 = mass_h[1]


Rockstar
~~~~~~~~

Quijote also contain Rockstar halo catalogs. A typical Rockstar folder will contain the following files:

- ``out_X.list``. These are the Rockstar-generated halo+subhalo catalogs. X usually goes from 0 to 4, and it represents the snapshot number. E.g. the rockstar catalog corresponding to the snapdir_004 would be out_4.list. Those are ASCII files where the header describes the content of the file.
- ``out_X_pid.list``. These are the Rockstar-generated halo+subhalo catalogs. X usually goes from 0 to 4, and it represents the snapshot number. E.g. the rockstar catalog corresponding to the snapdir_004 would be out_4.list. Those are ASCII files where the header describes the content of the file. The main difference between these files and the ``out_X.list`` is that ``out_X_pid.list`` contains an additional column called PID that allow to distinguish between halos and halos. For halos :math:`{\rm PID}=-1` while for subhalos PID is the parent halo ID.
- ``rockstar_params.cfg``. This file contains the Rockstar parameter file.
- ``rockstar.slurm``. This file contains the slurm submission script used to run Rockstar.
- ``rockstar.slurm``. This file contains the output from the slurm script.
- ``rockstar.cfg``. The Rockstar-generated configuration file. This is generated by Rockstar when running it.
- ``output.dat``. The output generated by Rockstar when running it.

In general, we recommend using the ``out_X_pid.list`` files that can be read easily with something like this:

.. code-block:: python

   import numpy as np

   # catalog file
   f_catalog = '/home/fvillaescusa/Quijote/Halos/fiducial/0/out_4_pid.list'
   
   # read the halo catalog
   data = np.loadtxt('f_catalog')

   # we can now get the different properties of the halos
   Mvir = data[:,2]
   Vmax = data[:,3]
   PID  = data[:,41] 
   
.. important::

   In some cases, like in the BSQ simulations, there are some additional folders, like ``hlists`` and ``trees``. These folders contains the halo/subhalo catalogs and merger trees generated after running consistent trees. We note that consistent trees needs multiple snapshots to run, so only some Quijote simulations have these folders. In the case these folders exists, we recommend the user to use them. E.g. it is better to read the ``hlist/hlist_1.00000.list`` file than the ``out_4_pid.list`` as the former contains more information.

