# Quijote simulations
The Quijote simulations are a set of 25000 N-body simulations. They were initially designed for two main tasks
- Quantify the information content on cosmological observables
- Provide enough statistics to train machine learning algorithms

But they can be used for a large variety of problems.

### Features
- 15000 simulations for a fiducial Planck cosmology
- 500 simulations/cosmology for 15 different cosmologies
- 2000 simulations in a latin hypercube expanding 5 cosmological parameters
- 512^3 cold dark matter particles (+512^3 neutrino particles) per simulation
- 3.6 trillions of particles at a single redshift
- Boxes of 1 Gpc/h, with spatial resolution of 50 kpc/h
- Outputs at redshifts 0, 0.5, 1, 2, 3 and 127 (initial conditions)
- 500 Tb of data
- 15 Million cpu hours
- Snapshots and data products (halo and voids catalogues, power spectra, bispectra, pdfs...) publicly available

## Data
The data is stored in the Gordon cluster of the San Diego Supercomputer Center. It can be access through [globus](https://www.globus.org/). 

- Log in into [globus](https://www.globus.org/) (create an account if you dont have one)
- In collection type Quijote_simulations

The folders fiducial, h_p, Om_m..etc contain the data products for the different cosmologies.

![](https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/Sims.jpg)
