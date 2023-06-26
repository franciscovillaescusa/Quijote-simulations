.. _odd:

Parity-violation
================

Quijote contains N-body simulations whose intial conditions were generated with parity-violation properties: Quijote-ODD. All these simulations contain :math:`512^3` dark matter particles in a periodic volume of :math:`(1~h^{-1}{\rm Gpc})^3` and share the same cosmology as the fiducial model: :math:`\Omega_{\rm m}=0.3175`, :math:`\Omega_{\rm b}=0.049`, :math:`h=0.6711`, :math:`n_s=0.9624`, :math:`\sigma_8=0.834`, :math:`w=-1`, :math:`M_\nu=0.0` eV. As the Quijote-PNG simulations (see :ref:`png`), these are standard N-body simulations run with initial conditions generated in a particular way.

The video below show an example of two N-body simulations with Gaussian initial conditions (top-left) and parity-violating initial conditions (bottom-left). The parity-violating simulation has been flipped along the x-axis to mimick the effect of a mirror in the center. The panels on the right show the differences between both.

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/4bnKGFYoLpA" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

   
Currently, the simulations in Quijote-ODD can be classified into two sets depending on the sign of :math:`p_{\rm NL}`:

- **ODD_p**: 500 simulations with :math:`p_{\rm NL}=+10^6`.
- **ODD_m**: 500 simulations with :math:`p_{\rm NL}=-10^6`.

The simulations in the above sets can be directly compared (the share the same underlying Gaussian density field) with the first 500 simulations of the fiducial model.



Initial conditions
~~~~~~~~~~~~~~~~~~

The initial conditions of the Quijote-ODD simulations have been generated using a modified version of the code described in `Scoccimarro et al. 2012 <https://arxiv.org/abs/1108.5512>`_. Our modified version of the code is publicly available `here <https://github.com/wcoulton/2LPTPNG-ODD>`_.

The initial conditions of a given simulation can be found in a folder called ``ICs``, that contains:

- ``ics.X``. These are the initial conditions that contain the particle positions, velocities, and IDs. These are Gadget format-II snapshots and can be read as described in :ref:`snapshots`. ``X`` can go from 0 to 127.
- ``2LPT.params``. This is the parameter file used to generate the initial conditions.
- ``logIC``. The output of the initial conditions generator code.

The value of initial random seed for the simulation :math:`i` is :math:`10\times i+5` (this can be found in the ``2LPT.params`` file) independently of the shape and :math:`f_{\rm NL}` value. For instance, the value of the initial random seed for ``ODD_p/100`` and ``ODD_m/100`` is 1005. This choice enables the calculation of partial derivatives, needed for Fisher matrix calculations.



Snapshots
~~~~~~~~~

We keep snapshots at redshifts 0, and 1. The snapshots are saved as compressed HDF5 files, and they can be read in the standard way (see :ref:`snapshots` for details on this).

Halo catalogs
~~~~~~~~~~~~~~~

We store both Friends-of-Friends (FoF) and Rockstar halo catalogs for each snapshot of each simulation in Quijote-ODD. We refer the user to :ref:`halo_catalogues` for details on how to read the FoF files. The Rockstar catalogs are ASCII files and the header contains information about the structure of the data.

Density fields
~~~~~~~~~~~~~~

To facilitate the post-processing of the data we also provide 3D grids containing the overdensity, :math:`\delta(x)=\rho(x)/\bar{\rho}-1`, for each redshift of all PNG simulations. We refer the user to :ref:`density_fields` for details on how to read these files.


Team
~~~~

Quijote-ODD was developed in 2023 by:

- William Coulton (CCA, USA)
- Oliver Philcox (Columbia/Simons, USA)
- Francisco Villaescusa-Navarro (Simons/Princeton, USA)

