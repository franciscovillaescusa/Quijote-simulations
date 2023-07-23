.. _Mnu:

*****************
Massive neutrinos
*****************

Quijote include N-body simulations that model massive neutrinos. In these simulations, neutrinos as modelled as a separate cold and pressureless fluid represented by neutrino particles. The main difference between these particles and those of dark matter is that neutrino particles have thermal velocities that are draw in the initial conditions from the underlying Fermi-Dirac distribution.

The initial conditions of these simulations are generated using the Zel'dovich approximation taking into account the scale-dependent growth factor and growth rate induced by neutrinos. For details on this we refer the reader `1605.05283 <https://arxiv.org/abs/1605.05283>`_.

Currently, the simulations including massive neutrinos are ``Mnu_p``, ``Mnu_pp``, ``Mnu_ppp`` (designed to compute derivatives for Fisher matrix calculations), and the ``nwLH`` latin-hypercube (designed for machine learning applications). See :ref:`types` for further details.

These simulations are designed to explore and quantify the impact of massive neutrinos on the different elements of the cosmic web.
