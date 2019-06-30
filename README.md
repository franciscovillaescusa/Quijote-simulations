<center>
<img src="https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/images/DL.png" alt="DL" width="250"/> <img src="https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/images/logo.gif" alt="DL" width="250"/> <img src="https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/images/LSS.png" alt="LSS" width="250"/>
<\center>

# Quijote simulations
The Quijote simulations are a set of 34500 N-body simulations. They are designed for two main tasks
- Quantify the information content on cosmological observables
- Provide enough statistics to train machine learning algorithms

But they can be used for a large variety of problems.

### Features
- 15500 simulations for a fiducial Planck cosmology
- 1000 (500) simulations/cosmology for 13 (2) different cosmologies
- 4000 simulations in a latin hypercube expanding 5 cosmological parameters
- 512^3 cold dark matter particles (+512^3 neutrino particles) per simulation
- 5 trillions of particles at a single redshift
- Boxes of 1 Gpc/h, with spatial resolution of 50 kpc/h
- Outputs at redshifts 0, 0.5, 1, 2, 3 and 127 (initial conditions)
- 172500 halo catalogues
- 172500 void catalogues
- more than 1 million power spectra
- more than 1 million bispectra
- 750 Tb of data
- 18 Million cpu hours
- Simulations run with the TreePM code Gadget-III
- Snapshots and data products (halo & void catalogues, power spectra, bispectra, pdfs...) publicly available

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

![](https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/images/Sims.jpg)

### Snapshots
The snapshots are stored in either Gadget-II format or HDF5. They can be read using the [readgadget.py](https://github.com/franciscovillaescusa/Pylians/blob/master/library/readgadget.py) and [readsnap.py](https://github.com/franciscovillaescusa/Pylians/blob/master/library/readsnap.py) scripts. If you have [Pylians](https://github.com/franciscovillaescusa/Pylians) installed you already have them.

The snapshots only contain 4 blocks:
- Header: This block contains general information about the snapshot such as redshift, number of particles, box size, particle masses...etc.
- Positions: This block contains the positions of all particles. Stored as 32-floats
- Velocities: This block contains the velocities of all particles. Stored as 32-floats
- IDs: This block contains the IDs of all particles. Stored as 32-integers. (This block may be removed in the future to reduce the size of the snapshots)

An example on how to read a snapshot is this:

```python
import readgadget

# input files
snapshot = '/home/fvillaescusa/Quijote/Snapshots/h_p/snapdir_002/snap_002'
ptype    = [1] #[1](CDM), [2](neutrinos) or [1,2](CDM+neutrinos)

# read header
header   = readgadget.header(snapshot)
BoxSize  = header.boxsize/1e3  #Mpc/h
Nall     = header.nall         #Total number of particles
Masses   = header.massarr*1e10 #Masses of the particles in Msun/h
Omega_m  = header.omega_m      #value of Omega_m
Omega_l  = header.omega_l      #value of Omega_l
h        = header.hubble       #value of h
redshift = header.redshift     #redshift of the snapshot
Hubble   = 100.0*np.sqrt(Omega_m*(1.0+redshift)**3+Omega_l)#Value of H(z) in km/s/(Mpc/h)

# read positions, velocities and IDs of the particles
pos = readgadget.read_block(snapshot, "POS ", ptype)/1e3 #positions in Mpc/h
vel = readgadget.read_block(snapshot, "VEL ", ptype)     #peculiar velocities in km/s
ids = readgadget.read_block(snapshot, "ID  ", ptype)-1   #IDs starting from 0
```
In the simulations with massive neutrinos it is possible to read the positions, velocities and IDs of the neutrino particles. Notice that the field should contain exactly 4 characters, that can be blank: ```"POS ", "VEL ", "ID  "```. The number in the name of the snapshot represents its redshift: 
- 000 ------> z=3
- 001 ------> z=2
- 002 ------> z=1
- 003 ------> z=0.5
- 004 ------> z=0

### Halo catalogues
The halo catalogues can be read through the [readfof.py](https://github.com/franciscovillaescusa/Pylians/blob/master/library/readfof.py) script. If you have [Pylians](https://github.com/franciscovillaescusa/Pylians) installed you already have it. An example on how to read a halo catalogue is this:

```python
import readfof 

# input files
snapdir = '/home/fvillaescusa/Quijote/Halos/s8_p/145/' #folder hosting the catalogue
snapnum = 4                                            #redshift 0

# determine the redshift of the catalogue
z_dict = {4:0.0, 3:0.5, 2:1.0, 1:2.0, 0:3.0}
redshift = z_dict[snapnum]

# read the halo catalogue
FoF = readfof.FoF_catalog(snapdir, snapnum, long_ids=False,
                          swap=False, SFR=False, read_IDs=False)
										
# get the properties of the halos
pos_h = FoF.GroupPos/1e3            #Halo positions in Mpc/h                                                                                                                                                                       
mass  = FoF.GroupMass*1e10          #Halo masses in Msun/h                                                                                                                                                                      
vel_h = FoF.GroupVel*(1.0+redshift) #Halo peculiar velocities in km/s                                                                                                                                                                        
Npart = FoF.GroupLen                #Number of CDM particles in the halo
```
The number in the name of the halo catalogue represents its redshift: 
- 000 ------> z=3
- 001 ------> z=2
- 002 ------> z=1
- 003 ------> z=0.5
- 004 ------> z=0

### Void catalogues

### Power spectra

### Bispectra

### PDFs

## Team
- Francisco Villaescusa-Navarro (CCA)
- ChangHoon Hahn (Berkeley)
- Emanuele Castorina (Berkeley)
- Arka Banerjee (Stanford)
- Elena Massara (CCA)
- Elena Giusarma (CCA)
- Chi-Ting Chiang (BNL)
- Andrej Obuljen (Waterloo)
- David Spergel (CCA/Princeton)
- Ben Wandelt (IAP Paris)
- Shirley Ho (CCA/Princeton)
- Licia Verde (Barcelona)
- Matteo Viel (SISSA)
- Roman Scoccimarro (NYU)
