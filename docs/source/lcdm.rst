.. _lcdm:

****
LCDM
****


Quijote contains standard N-body simulations varying the five vanilla :math:`\Lambda{\rm CDM}` parameters: :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_s`, :math:`\sigma_8`. In these simulations :math:`w=-1`, :math:`M_\nu=0~{\rm eV}`, :math:`\Omega_K=0` and the initial conditions are generated with 2LPT.

These simulations include ``Om_p``, ``Om_m``, ``Ob_p``, ``Ob_m``, ``h_p``, ``h_m``, ``ns_p``, ``ns_m``, ``s8_p``, ``s8_m``, ``Ob2_p``, ``Ob2_m``, ``fidcial``, ``fiducial_HR``, ``fiducial_LR``, ``fiducial_ZA``, and the three standard latin-hypercubes.

.. Note::

   The initial conditions of the ``fiducial_ZA`` simulations have been generated with the Zel'dovich approximation and not 2LPT. This is because these simulations are designed to be used with other Zel'dovich generated ICs simulation such as ``Mnu_p``, ``Mnu_pp``, and ``Mnu_ppp``.

These simulations are designed to explore and quantify the impact of vanilla cosmological parameters of the spatial distribution of matter, halos, and galaxies.
