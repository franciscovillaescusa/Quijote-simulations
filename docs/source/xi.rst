Correlation functions
=====================

The format of the correlation functions are:

- R | xi(R)  for correlation functions in real-space
- R | xi0(R) | xi2(R) | xi4(R) for correlation functions in redshift-space

where xi0(R), xi2(R) and xi4(R) are the monopole, quadrupole and hexadecapole, respectively. The units of R are Mpc/h, while the different xi are dimensionless.

In redshift-space there are three different files for each realization/redshift. These have been computed by placing the redshift-space distortions along the three different axes.

In python, the files can be read as 

.. code-block:: python
		
    import numpy as np

    R, xi = np.loadtxt('/home/fvillaescusa/Quijote/CF/matter/fiducial/0/CF_m_1024_z=0.txt', unpack=True)
    R, xi0, xi2, xi4 = np.loadtxt('/home/fvillaescusa/Quijote/CF/matter/fiducial/0/CF_m_RS0_1024_z=0.txt', unpack=True)

