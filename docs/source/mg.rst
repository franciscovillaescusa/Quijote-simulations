.. _mg:

================
Modified Gravity
================

We are expanding Quijote to incorporate simulations with modified gravity using the `Hu & Sawicki f(R) model <https://arxiv.org/abs/0705.1158>`_. Currently, we have 2048 simulations, run with `MG-Gadget <https://arxiv.org/abs/1305.2418>`_, whose cosmological parameters are arranged in a Sobol sequence with boundaries:

.. math::

   0.1 & \leq \Omega_{\rm m} \leq & 0.5\\
   0.03 & \leq \Omega_{\rm b} \leq & 0.07\\
   0.5 & \leq h \leq & 0.9\\
   0.8 & \leq n_s \leq & 1.2\\
   0.6 & \leq \sigma_8 \leq & 1.0\\
   0.01 & \leq M_\nu[{\rm eV}] \leq & 1.0\\
   -3\times10^{-4} & \leq f_{R0} \leq & 0


Each of those 2048 simulations have a different initial random seed. The initial conditions have been generated using the Zel'dovich approximation at :math:`z=127` and the simulations have been run with the appropiate Hubble function :math:`H(z)`. We have saved 5 snapshots, at redshifts 0, 0.5, 1, 2, and 3. For each simulation we saved FoF and Rockstar halo catalogs. 
   

The movie below shows an example of these simulations and its comparison with :math:`\Lambda {\rm CDM}`:

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/D0NjEgSB3Is" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>


If you are interested in using these simulations, please contact us at marco.baldi5@unibo.it or villaescusa.francisco@gmail.com.
