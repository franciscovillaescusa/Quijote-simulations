.. _bsq:

******************
Big Sobol Sequence
******************

The Big Sobol Sequence (BSQ) is a collection of 32,768 N-body simulations designed for machine learning applications. Each simulation follows the evolution of :math:`512^3` dark matter particles in a periodic comoving volume of :math:`(1000~h^{-1}{\rm Mpc})^3`. Each of these simulations have a different initial random seed and a value of the cosmological parameters :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_s`, :math:`\sigma_8` that are arranged in a Sobol sequence with boundaries (the value of the cosmological parameters for each BSQ simulation can be found `here <https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/BSQ/BSQ_params.txt>`_):

.. math::
   \Omega_{\rm m} \in [0.10 ; 0.50]\\
   \Omega_{\rm b} \in [0.02 ; 0.08]\\
   h \in [0.50 ; 0.90]\\
   n_s \in [0.80 ; 1.20]\\
   \sigma_8 \in [0.60 ; 1.00]

The value of the other cosmological parameters is the same in all simulations: :math:`M_\nu=0.0` eV, :math:`w=-1`, :math:`\Omega_{\rm K}=0`. The initial conditions were generated at :math:`z=127` using 2LPT, and the simulations have been run using Gadget-III with a slightly more stringent force accuracy parameters than the other Quijote simulations. 

.. Warning::

   As of January 7th 2024, 16,384 simulations have been run and are publicly available in both globus and binder (see :ref:`data_access`). The remaining simulations are being run and they are made publicly available inmediatly. The expected time to have the full set run is summer 2024.


For each simulation we dump 11 snapshots at redshifts 6, 5, 4, 3, 2, 1.5, 1, 0.7, 0.5, 0.2, and 0. We then post-process that data and saved halo catalogs, power spectra, bispectra, and density fields. We now describe the different data we store:


Snapshots
~~~~~~~~~

We have saved full snapshots for the initial conditions (ICs) and at redshifts 1 (``snap_006.hdf5``) and 0 (``snap_010.hdf5``). Note that that snapshots at redshifts 0 and 1 only contain a single file, in contrast with standard Quijote ones that have 8. This data can be read in the standard way (see :ref:`snapshots`).


Halo catalogs
~~~~~~~~~~~~~

For each of the 11 snapshots per simulation we have generated both FoF and Rockstar halo catalogs. We have also run consistent trees on the Rockstar catalogs and we have saved the generated merger tree. For FoF, the convention is this:

- 000: redshift 6
- 001: redshift 5
- 002: redshift 4
- 003: redshift 3
- 004: redshift 2
- 005: redshift 1.5
- 006: redshift 1
- 007: redshift 0.7
- 008: redshift 0.5
- 009: redshift 0.2
- 010: redshift 0

We refer the reader to :ref:`halo_catalogues` for details on how to read these files.


Power spectra
~~~~~~~~~~~~~

For each snapshot of each simulation we have computed the matter power spectrum in real- and redshift-space and saved the results.


Bispectra
~~~~~~~~~

For each snapshot of each simulation we have computed the matter bispectrum in real- and redshift-space and saved the results. The bispectrum is computed on grids with :math:`256^3` voxels and it contains ~2000 triangles down to :math:`k\sim0.5~h{\rm Mpc}^{-1}`.


Density fields
~~~~~~~~~~~~~~

We have generated density fields with the matter field with :math:`256^3` voxels in real- and redshift-space for all 11 available redshifts. The density fields have been generated using the Cloud-in-Cell (CIC) mass assignments scheme. The files are stored as hdf5 files, and can be read as this

.. code:: python

   import numpy as np
   import h5py

   f = h5py.File('df_m_CIC_z=0.00.hdf5', 'r')
   df = f['df'][:]  #df contains the number of particles in each voxel
   f.close()


   
