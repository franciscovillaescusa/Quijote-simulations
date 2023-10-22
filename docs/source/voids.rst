Void catalogs
=============

Beside Gigantes, Quijote also contain catalogs of voids identified using a spherical-overdensity algorithm (check `this website <https://pylians3.readthedocs.io/en/master/voids.html>`_ for details). The catalogs are stored as hdf5 files and they contain the following blocks:

- pos:    the positions of the void centers in Mpc/h
- radius: the sizes of the voids in in Mpc/h
- VSF: the void size function
- VSF_Rbins: the radii bins of the void size function
- parameters: the values of the void finder parameters used to generate the void catalogue

In python, the files can be read as

.. code-block:: python
		
    import h5py

    f = h5py.File('/home/fvillaescusa/Quijote/Voids/fiducial/0/void_catalogue_m_z=0.hdf5', 'r')
    pos        = f['pos'][:]        #void center positions in Mpc/h
    radius     = f['radius'][:]     #void radii in Mpc/h
    VSF        = f['VSF'][:]        #VSF (#voids/dR/Volume)
    VSF_Rbins  = f['VSF_Rbins'][:]  #VSF radii in Mpc/h
    parameters = f['parameters'][:] #parameters used to run the void finder
    f.close()
