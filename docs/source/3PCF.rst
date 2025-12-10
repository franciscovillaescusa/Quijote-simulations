.. _3PCF:


3-point correlation functions
=============================

This dataset was prepared for the analysis presented in Labate et al. (prep. for submission), which explores the imprint of massive neutrinos on the halo 3-point correlation function (3PCF). 
If you use this dataset, please cite the above publication.

3PCF multipoles
---------------

The measurements were performed with the code `MeasCorr <https://gitlab.com/veropalumbo.alfonso/meascorr>`_ (`Farina et al. 2024 <https://arxiv.org/abs/2408.03036>`_), which implements the algorithm for estimating the isotropic 3PCF presented in `Slepian and Eisenstein (2015) <https://arxiv.org/abs/1506.02040>`_.
The algorithm estimates the Legendre multipoles :math:`\zeta_\ell` of the 3PCF :math:`\zeta` rather than the 3PCF itself, which substantially reduces the computational cost.

In general, a triangle with vertices 1, 2, and 3 can be parameterized by the lengths of two sides, e.g. :math:`r_{12}` and :math:`r_{13}` (respectively joining vertices 1–2 and 1–3), and the angle :math:`\theta` between them.
The multipoles are functions of the two sides, i.e. :math:`\zeta_\ell = \zeta_\ell(r_{12}, r_{13})`.

If the multipoles are measured in the range :math:`0 \le \ell \le \ell_{\max}`, then the 3PCF at any angle :math:`\theta \in [0, \pi]` can be estimated by computing the sum

.. math::

    \zeta(r_{12}, r_{13}, \theta) = \sum_{\ell = 0}^{\ell_{\max}} \zeta_\ell(r_{12}, r_{13}) \, \mathcal{L}_\ell(\cos\theta),

where :math:`\mathcal{L}_\ell` is the Legendre polynomial of degree :math:`\ell`. 

Dataset
-------

The dataset includes measurements of the 3PCF multipoles for the simulations ``fiducial``, ``fiducial_ZA``, ``Mnu_ppp``, ``Mnu_pp``, ``Mnu_p``, ``s8_m``, and ``s8_p`` at :math:`z = 0, 1, 2` in real and redshift space. In the latter case, redshift-space distortions are applied along the :math:`\hat{z}` axis of the simulation box.

The details of the simulations and realizations for which the measurements are available are summarized in the table below (see :ref:`types` for the total number of realizations and the values of the cosmological parameters of each simulation set).

+-------------------+----------------+------------+-----------------------------------------------+
| Name              | simulations    | ICs        | realization numbers                           |
+===================+================+============+===============================================+
|          fiducial |       standard |       2LPT |                                        0-2000 |
+-------------------+----------------+------------+-----------------------------------------------+
|          fiducial |   paired fixed |       2LPT |       NCV_0_0-NCV_0_249 and NCV_1_0-NCV_1_249 |
+-------------------+----------------+------------+-----------------------------------------------+
|       fiducial_ZA |       standard |  Zeldovich |                                         0-499 |
+-------------------+----------------+------------+-----------------------------------------------+
|           Mnu_ppp |       standard |  Zeldovich |                                         0-499 |
+-------------------+----------------+------------+-----------------------------------------------+
|            Mnu_pp |       standard |  Zeldovich |                                         0-499 |
+-------------------+----------------+------------+-----------------------------------------------+
|             Mnu_p |       standard |  Zeldovich |                                         0-499 |
+-------------------+----------------+------------+-----------------------------------------------+
|              s8_p |   paired fixed |       2LPT |       NCV_0_0-NCV_0_249 and NCV_1_0-NCV_1_249 |
+-------------------+----------------+------------+-----------------------------------------------+
|              s8_m |   paired fixed |       2LPT |       NCV_0_0-NCV_0_249 and NCV_1_0-NCV_1_249 |
+-------------------+----------------+------------+-----------------------------------------------+

All the measurements are characterized by the following parameters:

- :math:`2.5 \le r_{12}, r_{13} \, [\mathrm{Mpc}/h] \le 147.5`, using bins of width :math:`\Delta r = 5 \, \mathrm{Mpc}/h`.  
  The centers of the bins are therefore :math:`5 + i \times \Delta r`, with :math:`i = 0,1,\ldots,28`.  
- :math:`\ell_{\max} = 10`.

Format
------

The format of the individual 3PCF files is:

- r12 [Mpc/h] | r13 [Mpc/h] | ell | zeta

where r12 and r13 are the values of the centers of the :math:`r_{12}` and :math:`r_{13}` bins, ell is the multipole index :math:`\ell`, and zeta is the corresponding multipole :math:`\zeta_\ell(r_{12}, r_{13})`.

The files for a given simulation ``simname`` and realization number ``num`` are stored in the folder ``3PCF/simname/num/``. 
Each file in this folder follows the naming convention ``Slepian15_zx.x_2.5_147.5_5_11_simname_num_space.csv``, where ``x.x`` specifies the redshift (``0.0``, ``1.0``, ``2.0``) and ``space`` can be either ``real`` or ``redshift``.

Example to read the files:

.. code-block:: python

    import numpy as np
    import pandas as pd

    # choose the simulation name, realization number, redshift and space 
    simname = 'fiducial' 
    num = '0'
    redshift = '0.0'
    space = 'real'

    # read the file containing the measurements and store them in a dataframe
    meas_folder = f'3PCF/{simname}/{num}'
    meas_file = f'{meas_folder}/Slepian15_z{redshift}_2.5_147.5_5_11_{simname}_{num}_{space}.csv'
    meas_df = pd.read_csv(meas_file, delimiter='\t')

The value of :math:`\zeta(r_{12}, r_{13}, \theta)` can then be obtained by running:

.. code-block:: python

    from scipy.special import eval_legendre 

    # estimate the 3PCF for a given triangle (r12, r13, theta)
    
    # choose r12 and r13 (among the available values of bin centers) and the angle theta (here we choose some example values)
    r12 = 50  # in Mpc/h
    r13 = 80  # in Mpc/h
    theta = np.pi/3
    
    # extract from the dataframe the multipoles corresponding to r12 and r13 and compute the Legendre polynomials at theta
    slice_condition = (meas_df["r12 [Mpc/h]"] == r12) & (meas_df["r13 [Mpc/h]"] == r13)
    ells = meas_df.loc[slice_condition, "ell"].to_numpy()
    zeta_vals = meas_df.loc[slice_condition, "zeta"].to_numpy()
    zeta_ells = (2 * ells + 1) * zeta_vals  # the prefactor must be included to ensure the correct normalization
    legendre_vals = np.array([eval_legendre(l, np.cos(theta)) for l in ells])
    
    # linearly combine the polynomials with coefficients given by the multipoles
    zeta = np.dot(zeta_ells, legendre_vals)

Acknowledgments
---------------

The measurements were carried out at the Open Physics Hub (OPH) cluster of the Department of Physics and Astronomy (DiFA) “Augusto Righi”, Alma Mater Studiorum – University of Bologna.

Team 
----

- Andrea Labate (University of Bologna, INAF OAS – Italian National Institute for Astrophysics - Astrophysics and Space Science Observatory of Bologna)
- Michele Moresco (University of Bologna, INAF OAS)
- Massimo Guidi (University of Bologna, INAF OAS)
- Alfonso Veropalumbo (University of Genoa, INAF, INFN - Italian National Institute for Nuclear Physics)
