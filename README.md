# Quijote simulations
The Quijote simulations are a set of 25000 N-body simulations. They are designed for two main tasks
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
The data are stored in the Gordon cluster of the San Diego Supercomputer Center. It can be access through [globus](https://www.globus.org/). 

- Log in into [globus](https://www.globus.org/) (create an account if you dont have one)
- In collection type Quijote_simulations

There are different folders: 
- __Snapshots__. This folder contains the snapshots of the simulations
- __Halos__. This folder contains the halo catalogues
- __Voids__. This folder contains the void catalogues
- __Pk__. This folder contains the power spectra
- __Bk__. This folder contains the bispectra 
- __PDF__. This folder contains the pdfs

Inside each of the above folders there is the data for the different cosmologies, e.g. h_p, fiducial, Om_m. A brief description of the different cosmologies is provided in the below table. Further details can be found in the Quijote paper.

![](https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/Sims.jpg)

### Halo catalogues
The halo catalogues can be read through the [readfof.py](https://github.com/franciscovillaescusa/Pylians/blob/master/library/readfof.py) script. If you have [Pylians](https://github.com/franciscovillaescusa/Pylians) installed you already have it. An example on how to read a halo catalogue is this:

```
import readfof 

# input files
snapdir = '/home/fvillaescusa/Quijote/Halos/s8_p/145/' #folder hosting the catalogue
snapnum = 4                                                                 #redshift 0

# determine the redshift of the catalogue
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# read the halo catalogue
FoF = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
                                        swap=False, SFR=False, read_IDs=False)
										
# get the properties of the halos
pos_h = FoF.GroupPos/1e3             #Halo positions in Mpc/h                                                                                                                                                                       
mass  = FoF.GroupMass*1e10         #Halo masses in Msun/h                                                                                                                                                                      
vel_h = FoF.GroupVel*(1.0+redshift) #Halo peculiar velocities in km/s                                                                                                                                                                        
Npart = FoF.GroupLen                     #Number of CDM particles in the halo
```
The number in the name of the halo catalogue represents its redshift: 
- 000 ------> z=3
- 001 ------> z=2
- 002 ------> z=1
- 003 ------> z=0.5
- 004 ------> z=0