.. _density_fields:


Density fields
==============

3D fields
---------

The 3D density fields are located in the New York cluster (see :ref:`data_access`) under the ``3D_cubes`` folder.

There are different folders for the different cosmologies. Inside each cosmology folder there are the folder containing the data for the different realizations. Inside each of those folders the 3D density fields can be found with names as ``df_m_X_Y_z=Z.npy``, where X can be 64, 128, 256, or 512, and it represents the grid size of the cube. Y represents the mass assignment scheme used to construct the density field, and can be something like CIC (cloud-in-cell) or PCS (piece-wise spline). Z represents the redshift of the density field. For instance, ``df_m_256_CIC_z=0.npy`` contains the 3D density field on a grid with :math:`256^3` voxels constructed using the CIC mass-assignment scheme at :math:`z=0`.

.. note::

   These fields are constructed in real-space. Please reach us if you need them in redshift-space.

The files can be read simply as

.. code-block:: python

   import numpy as np

   df = np.load('/home/fvillaescusa/Quijote/3D_cubes/Om_p/df_m_128_PCS_z=0.npy')

.. warning::

   Density fields with a large number of voxels occupy a significant amount of disk space, so they may not be available. However, constructing these fields is straightforward and it can be done directly on binder; thus, there is no need to download and process the data. We have examples of how to create these density fields directly on binder in :ref:`tutorials`.
   
   

2D fields
---------

2D fields (say images) can be constructed from the above 3D fields by taking a slice and projected it into 2D. For instance:

.. code-block::  python

   import numpy as np

   # read the 3D density field
   df_3D = np.load('/home/fvillaescusa/Quijote/3D_cubes/Om_p/df_m_128_PCS_z=0.npy')

   # take a slice of 4 voxels width, i.e. 1000/128*4 = 31.25 Mpc/h
   # along z-direction and project into 2D by computing the mean value
   df_2D = np.mean(df_3D[:,:,0:4], axis=2)
   
   
   
