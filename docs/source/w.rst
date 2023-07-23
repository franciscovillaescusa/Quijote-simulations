.. _w:

***********
Dark energy
***********

Quijote contains simulations where the dark energy equation of state is :math:`w=\neq -1`. These are standard N-body simulations run with a different Hubble function, :math:`H(z)`, that contains the changes introduced in the evolution of the background by the dark energy equation of state. 

The initial conditions of these simulations are generated using the Zel'dovich approximation and the inital matter power spectrum and :math:`H(z)` function is computed using `reps <https://github.com/matteozennaro/reps>`_. The simulations ``w_p`` and ``w_m`` (designed to compute partial derivatives for Fisher matrix calculations) together with the ``nwLH`` latin-hypercube are examples of simulations where :math:`w \neq -1`.

These simulations are designed to explore and quantify the impact of the dark energy equation of state on the large-scale structure of the Universe.
