.. _faq:

===
FAQ
===

I am having problems reading the snapshots. What should I do?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note that the snapshots have been compressed to reduce the storage needs. To read them, you need to install the hdf5plugin with, e.g. ``python -m pip install hdf5plugin``.

If you are using python, you need to load that library as:

.. code-block:: python

   import h5py
   import hdf5plugin

Note that if you are reading the snapshots with `Pylians <https://github.com/franciscovillaescusa/Pylians3>`_ you dont need to do anything else. However, keep in mind that you may need to update Pylians to the latest version with ``python -m pip install --upgrade Pylians``.

If you are using a non-python software (e.g. using running Rockstar in a snapshot or running a simulation from the initial conditions using Gadget) you need to set ``HDF5_PLUGIN_PATH`` environment variable to make use of the HDF5 compression filters. The path can be obtained as:

.. code-block:: bash

   python -c "import hdf5plugin; print(hdf5plugin.PLUGIN_PATH)"

and therefore, one should set in a terminal:

.. code-block:: bash

   export HDF5_PLUGIN_PATH=$(python -c "import hdf5plugin; print(hdf5plugin.PLUGIN_PATH)")

After doing this, the code can be run as normal. For further details check `this <http://www.silx.org/doc/hdf5plugin/latest/usage.html#use-hdf5-filters-in-other-applications>`_. If you experience problems with this please reach out to us at villaescusa.francisco@gmail.com or lgarrison@flatironinstitute.org.

The documentation says that there are 15,000 realizations for the fiducial cosmology, but I can only find 8,000. Where is the rest?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The 15,000 realizations of the fiducial model are split among the New York and San Diego Cluster. The New York cluster contains the first 8,000 while the rest is in the San Diego cluster. Check :ref:`data_access` for details.

How many latin-hypercubes are there?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, there are 4 latin-hypercubes, each of them having 2,000 simulations:

- Three of them only vary :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_{\rm s}`, :math:`\sigma_8`.
- One of them vary :math:`\Omega_{\rm m}`, :math:`\Omega_{\rm b}`, :math:`h`, :math:`n_{\rm s}`, :math:`\sigma_8`, :math:`M_\nu`, :math:`w`.

