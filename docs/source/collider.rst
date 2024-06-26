.. _collider:

Collider simulations
====================

These simulations include primordial non-Gaussianity (PNG) described by the following squeezed bispectrum,

.. math::
   \lim\limits_{k_1\ll k_2\approx k_3} B_\Phi({k}_1, {k}_2, {k}_3)=4f_{\rm NL}^\Delta \left(\frac{k_1}{k_2} \right)^\Delta P_\Phi(k_1)P_\Phi(k_2),


where :math:`\Phi(\mathbf{k})` is the primordial potential. This squeezed bispectrum arises in the "Cosmological Collider" scenario from intermediate-mass scalar (:math:`0\leq m/H<3/2`) exchange during inflation (`Arkani-Hamed and Maldacena 2015 <https://arxiv.org/abs/1503.08043>`_). 
These simulations are described in detail in `Goldstein et al. 2024 <ADD_REF>`_. 




Initial conditions
~~~~~~~~~~~~~~~~~~

Primordial non-Gaussianity
--------------------------
We generate initial conditions with PNG using a modified version of the code described in `Scoccimarro et al. 2012 <https://arxiv.org/abs/1108.5512>`_. 
Our modified code outputs initial conditions with the Cosmological Collider bispectrum in the squeezed limit. These simulations should not be used to study statistics that are sensitive to non-squeezed bispectrum configurations.


Separate universe
-----------------
In addition to the simulations with PNG, we run separate universe simulations with Gaussian initial conditions, but a modified initial power spectrum that mimics the primordial mode coupling induced by the squeezed Cosmological Collider bispectrum. Specifically, we run simulations with the following scale-dependent modification to the initial power spectrum,

.. math::
    P_{m}^{\rm lin.}(k|\epsilon,\Delta)\equiv \left(1+2\epsilon k^{-\Delta} \right)P_{m}^{\rm lin.}(k),

for small values of :math:`\pm\epsilon`. These simulations can be used to study the impact of intermediate-mass scalars on non-linear structure formation. For example, they can be used to estimate non-Gaussian bias parameters.

IC files
--------
The initial conditions of a given simulation can be found in a folder called ``ICs``, that contains:

- ``ics.X``. These are the initial conditions that contain the particle positions, velocities, and IDs. These are Gadget format-II snapshots and can be read as described in :ref:`snapshots`. ``X`` can go from 0 to 7.
- ``2LPT.params``. This is the parameter file used to generate the initial conditions.
- ``logfile_ICs``. The output of the initial conditions generator code.
- ``inputspec_ics.txt``. The input power spectrum used to generate the initial conditions.


Aside from having modified initial conditions, all simulations are run using the fiducial settings from the Quijote simulations. Specifically, these simulations contain :math:`512^3` dark matter particles in a periodic volume of :math:`(1~h^{-1}{\rm Gpc})^3` and share the same cosmology as the fiducial model: :math:`\Omega_{\rm m}=0.3175`, :math:`\Omega_{\rm b}=0.049`, :math:`h=0.6711`, :math:`n_s=0.9624`, :math:`\sigma_8=0.834`, :math:`w=-1`, :math:`M_\nu=0.0` eV. The value of initial random seed for simulation :math:`i` is :math:`10\times i+5`. Thus, our simulation :math:`i` has the same seed as the fiducial Quijote simulation :math:`i`.

Simulation products
~~~~~~~~~~~~~~~~~~~
The data release includes the following simulations:

- **Delta_0p5**: contains data from 50 simulations with :math:`\Delta=0.5` and :math:`f_{\rm NL}=+300`. Also includes five realizations of separate universe simulations with modified linear power spectrum (:math:`\epsilon=\pm0.01`).
- **Delta_1**: contains data from 50 simulations :math:`\Delta=1` and :math:`f_{\rm NL}^\Delta=+1000`. Also includes five realizations of separate universe simulations with modified linear power spectrum (:math:`\epsilon=\pm0.001`).

The separate universe simulations can be accessed from the ``Delta_{}/separate_universe/`` sub-directory. For example, the first realization of the :math:`\Delta=0.5` separate universe simulation with :math:`\epsilon=+0.01` is located in ``Delta_0p5/separate_universe/alpha_p0p01/0/``.

Snapshots
~~~~~~~~~
We save the snapshot output at redshifts 0, 0.5, 1 as HDF5 files. 

Halo catalogues
~~~~~~~~~~~~~~~
We store Friends-of-Friends (FoF) halo catalogues for each snapshot of each simulation. We refer the user to :ref:`halo_catalogues` for details on how to read these files.


Team
~~~~
- Sam Goldstein (Columbia University)
- Oliver Philcox (Columbia University/Simons Foundation)
- J\. Colin Hill (Columbia University)
- Lam Hui (Columbia University)
