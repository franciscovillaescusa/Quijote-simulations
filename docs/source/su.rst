.. _su:

*****************
Separate Universe
*****************

In standard N-body simulations, the mean matter matter density in the box is :math:`\Omega_{\rm m}\rho_{\rm crit}(1+z)^3`, where :math:`\rho_{\rm crit}(z)` is the critical density at redshift 0. In other words, the mean matter overdensity (with respect to the global one), :math:`\delta_b`, is zero. However, in the real Universe, regions of finite volume will exhibit fluctuations around :math:`\delta_b=0` due to perturbation on scales larger than the considered regions. Separate Universe simulations will follow the evolution of dark matter particles under the influence of an overdensity different to zero; or equivalently under the impact of a fluctuation that is larger than the size of the box. These simulations will thus have one extra parameter, :math:`\delta_b` that represents the mean overdensity over the entire box.

The way to incorporate the global overdensity is to change the cosmology of it, introducing curvature. Thus, in these simulations :math:`\Omega_K \neq 1`. Currently, the only Quijote simulations with :math:`\delta_b\neq 0` are ``DC_p`` and ``DC_m`` that are designed to compute partial derivatives to quantify supersample covariance effects. See section 2.3 of the `Quijote paper <https://arxiv.org/abs/1909.05273>`_.

These simulation are designed to explore and quatify the impact of super-sample covariance on cosmological ohservables. Many thanks to Yin Li for setting up the initial conditions and cosmology of these simulations.

 
