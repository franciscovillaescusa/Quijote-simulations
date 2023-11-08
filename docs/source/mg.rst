.. _mg:

================
Modified Gravity
================

Quijote contains N-body simulations with modified gravity: Quijote-MG. The movie below shows one of these simulations together wits :math:`\Lambda {\rm CDM}` counterpart:

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/D0NjEgSB3Is" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

   
If you are interested in using these simulations, please contact us at marco.baldi5@unibo.it or villaescusa.francisco@gmail.com.

General description
-------------------

Quijote-MG contains 2,048 N-body simulations run with `MG-Gadget <https://arxiv.org/abs/1305.2418>`_ and using the `Hu & Sawicki f(R) model <https://arxiv.org/abs/0705.1158>`_ as the modified gravity model. Each simulation follows the evolution of :math:`512^3` dark matter plus :math:`512^3` neutrinos in a periodic cosmological volume of :math:`(1000~{\rm Mpc}/h)^3`. The initial conditions have been generated using the Zel'dovich approximation at :math:`z=127` and the simulations have been run with the appropiate Hubble function :math:`H(z)`. 

Each simulation has a different value of the initial random seed and of the parameters :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_s`, :math:`\sigma_8`, :math:`M_\nu`, :math:`f_{R0}`. The value of those parameters in the simulations are organized in a Sobol sequence with boundaries:

.. math::

   0.1 & \leq \Omega_{\rm m} \leq & 0.5\\
   0.03 & \leq \Omega_{\rm b} \leq & 0.07\\
   0.5 & \leq h \leq & 0.9\\
   0.8 & \leq n_s \leq & 1.2\\
   0.6 & \leq \sigma_8 \leq & 1.0\\
   0.01 & \leq M_\nu[{\rm eV}] \leq & 1.0\\
   -3\times10^{-4} & \leq f_{R0} \leq & 0

.. Note::

   The actual value of these parameters for the different simulations can be found `here <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/modified_gravity/Cosmological_parameters.txt>`__. 
   
We have saved 5 snapshots, at redshifts 0, 0.5, 1, 2, and 3. For each simulation we have saved FoF catalogs, Rockstar catalogs, and different power spectra (see below).

Organization
------------

The data is split into different folders:

- ``Snapshots``. This folder contains 2,048 subfolders, one for each simulation. Inside these subfolders, the user can find the initial conditions, snapshots, simulation parameters, and additional files produced by MG-Gadget.
- ``Halos``. This folder contains 2 folders: ``FoF`` and ``Rockstar``. Each of those folders contains 2,048 folders, inside which the halo catalogs at different redshifts are located.
- ``Pk``. This folder contains 2,048 subfolders, one for each simulation. Inside these subfolders, the user can find the different power spectra.

Snapshots
---------

Every simulation contains 5 snapshots. Each snapshot is stored in a folder called ``snapdir_00X``, where ``X=0`` is :math:`z=3`, ``X=1`` is :math:`z=2`, ``X=2`` is :math:`z=1`, ``X=3`` is :math:`z=0.5`, ``X=4`` is :math:`z=0`. The snapshots are stored in hdf5 format, and can be read using Pylians (see details in :ref:`snapshots`). Note that the snapshots have been compressed to save space, so please take a look at :ref:`faq` if you encounter problems reading them.

.. Note::

   The initial conditions are located inside a folder called ``ICs``. The initial conditions are also stored as hdf5 files, and can be read in the same way as the simulation snapshots.

The MG-Gadget snapshots contains more blocks than traditional Gadget N-body simulations. The fields stored in the snapshots are:

::
   
   /CompressionInfo     	
   /Header              	
   /PartType1           	
   /PartType1/Acceleration  
   /PartType1/Coordinates   
   /PartType1/ModifiedGravityAcceleration Dataset 
   /PartType1/ModifiedGravityGradPhi Dataset 
   /PartType1/ModifiedGravityPhi Dataset 
   /PartType1/ParticleIDs   
   /PartType1/Velocities	
   /PartType2           	
   /PartType2/Acceleration  
   /PartType2/Coordinates   
   /PartType2/ModifiedGravityAcceleration Dataset 
   /PartType2/ModifiedGravityGradPhi Dataset 
   /PartType2/ModifiedGravityPhi Dataset 
   /PartType2/ParticleIDs   
   /PartType2/Velocities	

where ``PartType1`` represent cold dark matter and ``PartType2`` correspond to neutrinos.
   


Halo catalogs
-------------

Quijote-MG contains both FoF and Rockstar halo catalogs for every snapshot of each simulation. You can find details about how to read these files in :ref:`halo_catalogues`.

Power spectra
-------------

For every snapshot of each Quijote-MG simulation we have computed the following power spectra:

- cold dark matter auto-Pk in real-space: ``Pk_CDM_z=X.XXX.dat``
- cold dark matter auto-Pk in redshift-space: ``Pk_CDM_RS_axis=Y_z=X.XXX.dat``
- neutrino auto-Pk in real-space: ``Pk_NU_z=X.XXX.dat``
- neutrino auto-Pk in redshift-space: ``Pk_NU_RS_axis=Y_z=X.XXX.dat``
- total matter auto-Pk in real-space: ``Pk_CDM+NU_z=X.XXX.dat``
- total matter auto-Pk in redshift-space: ``Pk_CDM+NU_RS_axis=Y_z=X.XXX.dat``
- CDM-neutrino cross-Pk in real-space: ``Pk_CDMNU_z=X.XXX.dat``
- CDM-neutrino cross-Pk in redshift-space: ``Pk_CDMNU_RS_axis=Y_z=X.XXX.dat``

Where ``X.XXX`` is the redshift and ``Y`` (0, 1, or 2) is the axis along which the redshift-space distortions have been placed.
