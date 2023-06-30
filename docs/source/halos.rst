.. _halo_catalogues:

Halo catalogues
===============

The FoF halo catalogs can be read through the `readfof.py <https://github.com/franciscovillaescusa/Pylians3/blob/master/library/readfof.py>`_ script. If you have `Pylians <https://github.com/franciscovillaescusa/Pylians3>`_ installed you already have it. An example on how to read a halo catalog is this (we provide further details on how to read and manipulate these catalogs in :ref:`tutorials`):

.. code-block:: python
		
    import readfof 

    # input files
    snapdir = '/home/fvillaescusa/Quijote/Halos/s8_p/145/' #folder hosting the catalogue
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
