.. _png:

Primordial non-Gaussianities
============================

Quijote contains 4,000 N-body simulations with primordial non-Gaussianities: **Quijote-PNG**. All these simulations contain :math:`512^3` dark matter particles in a periodic volume of :math:`(1~h^{-1}{\rm Gpc})^3` and share the same cosmology as the fiducial model: :math:`\Omega_{\rm m}=0.3175`, :math:`\Omega_{\rm b}=0.049`, :math:`h=0.6711`, :math:`n_s=0.9624`, :math:`\sigma_8=0.834`, :math:`w=-1`, :math:`M_\nu=0.0` eV. These are standard N-body simulations run with initial conditions generated in a particular way. 

The simulations in Quijote-PNG can be classified into four different sets: 1) local, 2) equilateral, 3) orthogonal CMB, and 4) orthogonal LSS (see :ref:`shapes`). Each set contains 1,000 simulations: 500 with :math:`f_{\rm NL}=+100` and 500 with :math:`f_{\rm NL}=-100`. Quijote-PNG is thus organized into eight different folders, depending on the non-Gaussianity shape and the value of :math:`f_{\rm NL}`:

- **LC_p**: contains data from 500 simulations with local type and :math:`f_{\rm NL}=+100`
- **LC_m**: contains data from 500 simulations with local type and :math:`f_{\rm NL}=-100`
- **EQ_p**: contains data from 500 simulations with equilateral type and :math:`f_{\rm NL}=+100`
- **EQ_m**: contains data from 500 simulations with equilateral type and :math:`f_{\rm NL}=-100`
- **OR_CMB_p**: contains data from 500 simulations with orthogonal CMB type and :math:`f_{\rm NL}=+100`
- **OR_CMB_m**: contains data from 500 simulations with orthogonal CMB type and :math:`f_{\rm NL}=-100`
- **OR_LSS_p**: contains data from 500 simulations with orthogonal LSS type and :math:`f_{\rm NL}=+100`
- **OR_LSS_m**: contains data from 500 simulations with orthogonal LSS type and :math:`f_{\rm NL}=-100`
  
Each of the above folders contains 500 sub-folders, each of them hosting the result of a different simulation. For instance, the folder ``EQ_p/72/`` contains the results of the 72th simulation run with :math:`f_{\rm NL}=+100` for the equilateral shape. Depending on the location, these folder will contain the snapshots, halo catalogues, or other data products.


.. _shapes:

Bispectrum shapes
~~~~~~~~~~~~~~~~~

In Quijote-PNG we only consider models that have a primordial bispectrum, defined as

.. math::
   
    \langle \Phi(\mathbf{k}_1) \Phi(\mathbf{k}_2) \Phi(\mathbf{k}_3) \rangle =  (2\pi)^3 \delta^{(3)}(\mathbf{k}_1+\mathbf{k}_2+\mathbf{k}_3)B_{\Phi}(k_1,k_2,k_3)~,

where :math:`\Phi(\mathbf{k})` is the primordial potential. We consider four different shapes for the primordial bispectrum:
  

1) **Local**. The local shape can be characterized by

.. math::
   
   B^{\mathrm{local}}_{\Phi}(k_1,k_2,k_3) = 2 f_{\mathrm{NL}}^{\mathrm{local}} P_\Phi(k_1)P_\Phi(k_2)+  \text{ 2 perm.}
   
2) **Equilateral**. The equilaterial shape is described by

.. math::

   B^{\mathrm{equil.}}_{\Phi}(k_1,k_2,k_3) = 6 f_{\mathrm{NL}}^{\mathrm{equil.}}\Big[- P_\Phi(k_1)P_\Phi(k_2)+\text{ 2 perm.} \\ 
  -2 \left( P_\Phi(k_1)P_\Phi(k_2)P_\Phi(k_3) \right)^{\frac{2}{3}} +  P_\Phi(k_1)^{\frac{1}{3}}P_\Phi(k_2)^{\frac{2}{3}}P_\Phi(k_3)  + \text{5 perm.}\Big]

   
3) **Orthogonal CMB**. The orthogonal CMB template is given by

.. math::

   B^{\mathrm{ortho-CMB}}_\Phi(k_1,k_2,k_3) = 6 f_{\mathrm{NL}}^{\mathrm{ortho-CMB}}\Big[-3 P_\Phi(k_1)P_\Phi(k_2) \\ 
   +\text{ 2 perm.}  -8 \left( P_\Phi(k_1)P_\Phi(k_2)P_\Phi(k_3) \right)^{\frac{2}{3}} +  3P_\Phi(k_1)^{\frac{1}{3}}P_\Phi(k_2)^{\frac{2}{3}}P_\Phi(k_3)  + \text{5 perm.}\Big]
   
4) **Orthogonal LSS**. The orthogonal LSS template is given by

.. math::

   B^{\mathrm{ortho-LSS}}_\Phi(k_1,k_2,k_3) = \\ 6 f_{\mathrm{NL}}^{\mathrm{ortho-CMB}}
        \left(P_\Phi(k_1)P_\Phi(k_2)P_\Phi(k_3)\right)^{\frac{2}{3}}\Bigg[ \\  -\left(1+\frac{9p}{27}\right) \frac{k_3^2}{k_1k_2} + \textrm{2 perms} +\left(1+\frac{15p}{27}\right)  \frac{k_1}{k_3} \\   + \textrm{5 perms}  -\left(2+\frac{60p}{27}\right)  \\ +\frac{p}{27}\frac{k_1^4}{k_2^2k_3^2} + \textrm{2 perms}  -\frac{20p}{27}\frac{k_1k_2}{k_3^2}+ \textrm{2 perms}  \\ -\frac{6p}{27}\frac{k_1^3}{k_2k_3^2} + \textrm{5 perms}+\frac{15p}{27}\frac{k_1^2}{k_3^2} + \textrm{5 perms}\Big]


Initial conditions
~~~~~~~~~~~~~~~~~~

The initial conditions of the Quijote-PNG simulations have been generated using a modified version of the code described in `Scoccimarro et al. 2012 <https://arxiv.org/abs/1108.5512>`_. Our modified version of the code is publicly available `here <https://github.com/dsjamieson/2LPTPNG>`_.

The initial conditions of a given simulation can be found in a folder called ``ICs``, that contains:

- ``ics.X``. These are the initial conditions that contain the particle positions, velocities, and IDs. These are Gadget format-II snapshots and can be read as described in :ref:`snapshots`. ``X`` can go from 0 to 127.
- ``2LPT.params``. This is the parameter file used to generate the initial conditions.
- ``logIC``. The output of the initial conditions generator code.

The value of initial random seed for the simulation :math:`i` is :math:`10\times i+5` (this can be found in the ``2LPT.params`` file) independently of the shape and :math:`f_{\rm NL}` value. For instance, the value of the initial random seed for ``OR_CMB_p/100`` and ``OR_CMB_m/100`` is 1005. This choice enables the calculation of partial derivatives, needed for Fisher matrix calculations.

For the details about the linear matter power spectrum used for these simulations see :ref:`linear_Pk`.


Snapshots
~~~~~~~~~

We keep snapshots at redshifts 0, 0.5, 1, 2, and 3. The snapshots are saved as HDF5 files, and they can be read in the standard way (see :ref:`snapshots` for details on this).


Team
~~~~

Quijote-PNG was developed in 2022 by:

- William Coulton (CCA, USA)
- Gabriel Jung (Padova, Italy)
- Francisco Villaescusa-Navarro (CCA/Princeton, USA)
- Dionysios Karagiannis (Cape Town, South Africa)
- Drew Jamieson (MPA, Germany)
- Michele Liguori (Padova, Italy)
- Marco Baldi (Bologna, Italy)
- Licia Verde (Barcelona, Spain)
- Benjamin Wandelt (IAP, France)
