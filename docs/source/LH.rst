.. _LH:

Latin-hypercubes
================

Quijote provides several latin-hypercubes that can be classified into several main categories depending on what parameters are varied:

LH
---

The simulations in this category only consider massless neutrinos. There are three latin-hypercubes in this category, each containing 2,000 simulations that vary the value of :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_s`, :math:`\sigma_8`. The limits of the latin-hypercubes are set by:

.. math::
   \Omega_{\rm m} \in [0.1 ; 0.5]\\
   \Omega_{\rm b} \in [0.03 ; 0.07]\\
   h \in [0.5 ; 0.9]\\
   n_s \in [0.8 ; 1.2]\\
   \sigma_8 \in [0.6 ; 1.0]

The value of the cosmological parameters for each simulation of a latin-hypercube of this category can be found `here <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube/latin_hypercube_params.txt>`__. Alternatively, inside each snapshot folder, there is a file called ``Cosmo_params.dat`` that contains the value of the cosmological parameters of that simulation. Each simulation of the latin-hypercube has a different value of the initial random seed. The value of the initial random seed of each simulation is written in the file ``ICs/2LPT.param`` inside each simulation folder.

The differences between the three latin-hypercubes are these:

- **standard**: This latin-hypercube contains 2,000 standard simulations with :math:`512^3` particles each. The snapshots, halo catalogues...etc of this latin-hypercube are located in a folder called ``latin_hypercube``. The folder names are ``X``, where ``X`` goes from 0 to 1999.
- **fixed**: This latin-hypercube contains 2,000 fixed simulations with :math:`512^3` particles each. The snapshots, halo catalogues...etc of this latin-hypercube are located in a folder called ``latin_hypercube``. The folder names are ``NCV_X`` where ``X`` goes from 0 to 1999.
- **high-resolution**. This latin-hypercube contains 2,000 standard simulations with :math:`1024^3` particles each. The snapshots, halo catalogues...etc of this latin-hypercube are located in a folder called ``latin_hypercube_HR``. The folder names are ``X``, where ``X`` goes from 0 to 1999.

.. note::
   The simulations in the standard and high-resolution latin-hypercubes share the same initial random seed. E.g. the simulation 723 of the standard latin-hypercube has the same initial random seed as the simulation 723 of the high-resolution latin-hypercube. The only difference is the maximum :math:`k` sampled in each.


nwLH
----

The simulations in this category include massive neutrinos. There is one single latin-hypercube in this category, and it contains 2,000 simulations that vary the value of :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_s`, :math:`\sigma_8`, :math:`M_\nu`, and :math:`w`. The limits of this latin-hypercube are set by

.. math::
   \Omega_{\rm m} \in [0.1 ; 0.5]\\
   \Omega_{\rm b} \in [0.03 ; 0.07]\\
   h \in [0.5 ; 0.9]\\
   n_s \in [0.8 ; 1.2]\\
   \sigma_8 \in [0.6 ; 1.0]\\
   M_\nu \in [0.01 ; 1.0]~{\rm eV}\\
   w \in [-1.3 ; -0.7]

The value of the cosmological parameters of each simulation of the latin-hypercube can be found `here <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube_nwLH/latin_hypercube_params.txt>`__. Alternatively, inside each snapshot folder, there is a file called ``Cosmo_params.dat`` that contains the value of the cosmological parameters of that simulation. Each simulation of the latin-hypercube has a different value of the initial random seed. The value of the initial random seed of each simulation is written in the file ``ICs/NGenIC.param`` inside each simulation folder.

.. note::
   Note that the initial conditions of these simulations have been generated using the Zel'dovich approximation, while the initial conditions of latin-hypercubes that do not include neutrinos were generated using 2LPT.
   

The snapshots, halo catalogues...etc of this latin-hypercube are located in a folder called ``latin_hypercube_nwLH``. The folder names are ``X``, where ``X`` goes from 0 to 1999.

fNL_LH
------

The simulations in this category are designed to explore the impact of primordial non-Gaussianities on the Universe's large-scale structure. This category contains two different latin-hypercubes, each of them with 1,000 N-body simulations. We noe describe each of them in detail:

- ``latin_hypercube_LC``. This latin-hypercube contains 1,000 simulations. All of them follows the evolution of :math:`512^3` dark matter particles in a periodic volume of :math:`(1000~h^{-1}{\rm Mpc})^3` down to :math:`z=0`. Each simulation has a different value of the initial random seed, that can be found in the ``ICs/2LPT.param`` file inside the simulation folder. All the simulations share the value of these cosmological parameters :math:`\Omega_{\rm m}=0.3175`, :math:`\Omega_{\rm b}=0.049`, :math:`h=0.6711`, :math:`n_s=0.9624`, :math:`\sigma_8=0.834`, :math:`M_\nu=0` eV, :math:`w_0`. The parameter that is varied is :math:`f_{\rm NL}` local that is varied within :math:`-300 \leq f_{\rm NL}^{\rm local} \leq +300`. The value of the :math:`f_{\rm NL}^{\rm local}` parameter for each simulation can be found in `here <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube_LC/latin_hypercube_params.txt>`__. Note that we run these simulations generating 46 snapshots. Thus, the names of the snapshots and catalogs are different. In `this file <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube_LC/times.txt>`__ you can find the value of the scale factor associated to each snapshot/catalog. For insteance, ``snapdir_045`` corresponds to :math:`a=1` or :math:`z=0`. 

- ``latin_hypercube_EQ``. This latin-hypercube contains 1,000 simulations. All of them follows the evolution of :math:`512^3` dark matter particles in a periodic volume of :math:`(1000~h^{-1}{\rm Mpc})^3` down to :math:`z=0`. Each simulation has a different value of the initial random seed, that can be found in the ``ICs/2LPT.param`` file inside the simulation folder. All the simulations share the value of these cosmological parameters :math:`\Omega_{\rm b}=0.049`, :math:`M_\nu=0` eV, :math:`w=-1`. The value of the other cosmological parameters are varied in the range:

.. math::
   \Omega_{\rm m} \in [0.1 ; 0.5]\\
   h \in [0.5 ; 0.9]\\
   n_s \in [0.8 ; 1.2]\\
   \sigma_8 \in [0.6 ; 1.0]\\
   f_{\rm NL}^{\rm equilateral} \in [-600 ; 600]

The value of the :math:`f_{\rm NL}^{\rm local}` parameter for each simulation can be found in `here <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube_EQ/latin_hypercube_params.txt>`__. Note that we run these simulations generating 46 snapshots. Thus, the names of the snapshots and catalogs are different. In `this file <https://github.com/franciscovillaescusa/Quijote-simulations/blob/master/latin_hypercube_EQ/times.txt>`__ you can find the value of the scale factor associated to each snapshot/catalog. For insteance, ``snapdir_045`` corresponds to :math:`a=1` or :math:`z=0`. 


