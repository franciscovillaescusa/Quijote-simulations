Power spectra
=============

Linear power spectra
--------------------

The different folders contain both the CAMB parameter files and the matter power spectrum at z=0. In some cases transfer functions and power spectra for neutrinos, CDM, baryons, and CDM+baryons are also present. The format of the power spectrum files is

- k | P(k) 

where the units of k and P(k) are comoving h/Mpc and (Mpc/h)^3, respectively. For the fiducial, Om_p, Om_m, Ob_p, Ob_m, Ob2_p, Ob2_m, h_p, h_m, ns_p, ns_m, s8_p, s8_m the name of the matter power spectrum files at z=0 is 'CAMB_matterpow_0.dat'. For Mnu_p, Mnu_pp and Mnu_ppp the files are called instead 'XeV_Pm_rescaled_z0.0000.txt', where X = 0.1(Mnu_p), 0.2(Mnu_pp) and 0.4(Mnu_ppp). For the latin_hypercube simulations, the files are named 'Pk_mm_z=0.000.txt' 

Notice that the matter power spectra at z=0 are not normalized (this is because the normalization is performed in the code that generates the initial conditions). The normalization factor is stored in the file Normfac.txt. One example on how to obtain the correct normalized matter power spectrum for a given cosmology is this:

.. code-block:: python
		
    import numpy as np

    f_Pk   = '/home/fvillaescusa/Quijote/Linear_Pk/ns_p/CAMB_TABLES/CAMB_matterpow_0.dat'
    f_norm = '/home/fvillaescusa/Quijote/Linear_Pk/ns_p/Normfac.txt'

    k, Pk   = np.loadtxt(f_Pk, unpack=True)
    Normfac = np.loadtxt(f_norm)

    Pk_norm = Pk*Normfac


Non-linear power spectra
------------------------

The format of the power spectra are:

- k | P(k) for power spectra in real-space
- k | P0(k) | P2(k) | P4(k) for power spectra in redshift-space

where P0(k), P2(k) and P4(k) are the monopole, quadrupole and hexadecapole, respectively. The units of k are h/Mpc, while for the power spectra are (Mpc/h)^3.

In redshift-space there are three different files for each realization/redshift. These have been computed by placing the redshift-space distortions along the three different axes.

In python, the files can be read as 

.. code-block:: python
		
    import numpy as np

    k, Pk = np.loadtxt('/home/fvillaescusa/Quijote/Pk/matter/fiducial/3/Pk_m_z=0.txt', unpack=True)
    k, Pk0, Pk2, Pk4 = np.loadtxt('/home/fvillaescusa/Quijote/Pk/matter/fiducial/3/Pk_m_RS1_z=0.txt', unpack=True)


Marked power spectra
--------------------

The files whose name starts with

- Mk\_ contain marked power spectra M(k) evaluated at wavenumber k
- Xk\_ contain the cross spectra between marked and standard density field X(k) evaluated at wavenumber k

The unit of k is h/Mpc, while the one of M(k) and X(k) is (Mpc/h)^3.

Files with measurements performed in the fiducial cosmology have name

- Mk_fiducial0-4999\_....hdf5
- Xk_fiducial0-4999\_....hdf5

where the first numbers (in the above case 0-4999) indicate the realizations saved in the file, and the dots specify the marked model considered. 

The remaining files contain measurements performed in the other cosmologies and from 500 realization per cosmology. Their name is

- Mk_fTH\_....hdf5
- Xk_fTH\_....hdf5

Also in this case the dots specify the marked model considered. 

In python, the files can be read as 

.. code-block:: python
		
    import numpy as np

    f = h5py.File(FILENAME, 'r')
    k = f['k'][:]
    # Fiducial cosmology 
    Mk = f['i'][:]  
    # Massive neutrino cosmologies
    Mk = f['cosmo/i_suffix'][:]  
    # Other cosmologies
    Mk = f['cosmo/i'][:]  

where i is the number of the realization, cosmo is the wanted cosmology and suffix can be

- 'm' for the total matter field
- 'cb' for the cold dar matter plus baryons 

In order to see the name of each cosmology type

.. code-block:: python
		
    print(list(f.keys()))
