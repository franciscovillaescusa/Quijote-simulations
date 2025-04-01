.. _interloper_contaminated_catalogues:

###########
Interlopers
###########

We provide contaminated halo catalogs and associated summary statistics. We contaminated the snapshots at :math:`z=1`. Therefore, we provide the catalogs and the statistics corresponding to that redshift alone. The fractions are always produced in the range :math:`[0.01, 0.11]`.

We produced two types of interlopers:

1. **Inbox interlopers**: the halos are shifted within the box at :math:`z=1` by :math:`\bigtriangleup d = 90 \, {\rm Mpc}/h`.
2. **Outbox interlopers**: the interloper halos are shifted inside the box at :math:`z=1` from the box at :math:`z=2`.

There are three directories:

- ``inbox``
- ``outbox``
- ``Pk_contaminated``


Contaminated FoF Catalogs
===========================

The contaminated halo catalogs have the same characteristics as the original Quijote FoF catalogs (columns, naming, redshift, etc.).

The two directories (``inbox`` and ``outbox``) have the same internal structure:

- ``fiducial``: 2000 contaminated FoF catalogs at :math:`z=1` (``groups_002``) produced from 1000 FoF original Quijote catalogs and 100 fractions extracted from a Latin hypercube, stored in the file ``fiducial/fractions-2000.txt``.

  .. list-table::
     :header-rows: 1

     * - Original number
       - Contaminated number
     * - ``0-499``
       - ``0-499``
     * - ``0-499``
       - ``500-999``
     * - ``500-999``
       - ``1000-1499``
     * - ``500-999``
       - ``1500-1999``

- ``latin_hypercube``: 10000 catalogs at :math:`z=1` (``groups_002``) produced from the 2000 Quijote original Latin hypercube cosmologies and 2000 fractions sampled from a Latin hypercube. Each cosmology has 5 fraction realizations. The folders are ordered as in the original Quijote hypercube, and each contains 5 subdirectories (from ``0`` to ``4``) for the different fraction realizations. The fraction values for the cosmologies are stored in each cosmology folder in the file ``fractions.txt``.

- ``BSQ``: :math:`2^{15}` catalogs at :math:`z=1` (``groups_006``) from the original Quijote big Sobol sequence (BSQ) with :math:`2^{15}` different fractions sampled from a Sobol sequence. The directory structure is the same as the Latin hypercube, but for each cosmology, there is only one fraction realization (``0``), whose fraction value is stored in ``fractions.txt`` in each cosmology directory.

Example to read the contaminated catalogs:

.. code-block:: python

   import readfof

   snapdir = '/home/cagliari/Quijote/FoF_contaminated/inbox/fiducial/0' # folder hosting the catalogue
   snapnum = 2  # redshift 1

   # Determine the redshift of the catalogue
   z_dict = {4: 0.0, 3: 0.5, 2: 1.0, 1: 2.0, 0: 3.0}
   redshift = z_dict[snapnum]

   # Read the halo catalogue
   FoF_c_r = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
                     swap=False, SFR=False, read_IDs=False, read_type=True)

   pos_h = FoF_c_r.GroupPos / 1e3  # Halo positions in Mpc/h
   mass  = FoF_c_r.GroupMass * 1e10  # Halo masses in Msun/h
   vel_h = FoF_c_r.GroupVel * (1.0 + redshift)  # Halo peculiar velocities in km/s
   Npart = FoF_c_r.GroupLen  # Number of CDM particles in the halo
   Type  = FoF_c_r.GroupType  # 0 if target, 1 if interloper

   # Check interloper fraction
   N_t = len(pos_h[Type == 0, :])
   N_i = len(pos_h[Type == 1, :])

   print('Targets    :', N_t)
   print('Interlopers:', N_i)
   print('Total      :', N_t + N_i)
   print('Interloper fraction:', N_i / (N_t + N_i))

Contaminated Statistics
=========================

The statistics that we provide are:

1. The non-contaminated power spectrum saved in ``Pk_pylians_no-dz.dat``.
2. The contaminated power spectrum saved in ``Pk_pylians_dz.dat``.
3. The contaminated bispectrums saved in ``Bk_6k_pyspectrum_dz.dat``.

The power spectrum files have the following 5 columns: ``k [h/Mpc] Pk0 Pk2 Pk4 Nmodes``. The bispectrum files have the following 9 columns: ``k1 k2 k3 P(k1) P(k2) P(k3) B(k1,k2,k3) SN_B number_of_triangles_in_bin``. The bin centers are in units of :math:`k_f=6.2832 \times 10^{-3}`.

The statistics are stored in the folder ``Pk_contaminated`` and its subdirectories ``inbox`` and ``outbox``. The structure within these folders is the same as the catalogs folder, with the difference that the fraction values are only stored in the corresponding FoF folders.

1. ``inbox``: has the three subdirectories ``fiducial``, ``latin_hypercube``, ``BSQ``. Here each folder contains:
   - Non-contaminated power spectrum
   - Contaminated power spectrum
   - Contaminated bispectrum

2. ``outbox``: has the three subdirectories:
   
   - ``fiducial``: each folder contains:
     
     - Non-contaminated power spectrum
     - Contaminated power spectrum
     - Contaminated bispectrum
       
   - ``latin_hypercube`` and ``BSQ``: each cosmology folder contains:
     
     - Non-contaminated power spectrum
     - Different fraction folders containing:
       
       - Contaminated power spectrum
       - Contaminated bispectrum

Acknowledgements
==================

This work has been done thanks to the facilities offered by the Univ. Savoie Mont Blanc - CNRS/IN2P3 MUST computing center.

Team
=====

- Marina Silvia Cagliari (LAPTh, France)
- Azadeh Moradinezhad (LAPTh, France)
- Francisco Villaescusa-Navarro (Simons/Princeton, USA)

