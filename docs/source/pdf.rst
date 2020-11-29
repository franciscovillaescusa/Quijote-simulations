*******
PDFs
*******

The format of the PDF files is:

- delta | pdf
  
where delta is the density contrast (rho/< rho > - 1).

In python, the files can be read as

.. code-block:: python

    import numpy as np
    
    delta, pdf = np.loadtxt('/home/fvillaescusa/Quijote/PDF/matter/latin_hypercube/0/PDF_m_5.0_z=0.txt', unpack=True)

