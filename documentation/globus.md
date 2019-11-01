# Transfering data with Globus

The simplest way to transfer data is to use the graphical environment of [globus.org](https://www.globus.org).
The data of the Quijote simulations can be accessed by typing Quijote_simulations in Collection.

For instance, if you want to transfer all halo catalogues to your local machine, select the Halos folder, log in into the machine where you want to transfer the data, and click on the start buttom.

<img src="https://raw.githubusercontent.com/franciscovillaescusa/Quijote-simulations/master/documentation/Globus.png" alt="Globus" width="900"/>

In some cases, the above option may not be desirable. For instance, imagine that you want to download all linear matter power spectra of the high-resolution latin-hypercube simulations. Those files are located in, e.g. for realization 45,

/Snapshots/latin_hypercube_HR/45/ICs/Pk_mm_z=0.000.txt

Thus, to download all those files, without involving downloading the full snapshots, will require that you access each simulation folder, then the ICs folder and then transfer the file individually. For 2000 files this is unpractical. For these situations, we recommend the usage of [Command Line Interface (CLI)](https://docs.globus.org/cli/). The first step is to install the CLI package, if you don't have it. Then, the following command allow you to determine the associated endpoint of the Quijote simulations:

```bash
globus endpoint search "Quijote_simulations"
```

ID                                   | Owner                     | Display Name       
------------------------------------ | ------------------------- | -------------------
c42757fe-d570-11e9-98e2-0a63aa6b37da | fvillaescusa@globusid.org | Quijote_simulations

You should do the same to know the endpoint of the machine where you are transfering the data to. You can then explore the filesystem of the Quijote simulations as:

```bash
ep1=c42757fe-d570-11e9-98e2-0a63aa6b37da
globus ls $ep1:/Snapshots/latin_hypercube_HR/45/ICs/
```

The above command will list the content of the /Snapshots/latin_hypercube_HR/45/ICs/ directory.

A single file can be transfered as:

```bash
ep1=c42757fe-d570-11e9-98e2-0a63aa6b37da
ep2=ddb59af0-6d04-11e5-ba46-22000b92c6ec
globus transfer $ep1:/Snapshots/latin_hypercube_HR/45/ICs/Pk_mm_z=0.000.txt $ep2:/Quijote_simulations/linear_Pk/45/Pk_mm_z=0.000.txt --label "single file transfer"
```

Where ep2 should be the endpoint of the machine where you are transfering the data. Entire folders can be moved as follows:

```bash
ep1=c42757fe-d570-11e9-98e2-0a63aa6b37da
ep2=ddb59af0-6d04-11e5-ba46-22000b92c6ec
globus transfer $ep1:/Snapshots/latin_hypercube_HR/45/ICs $ep2:/Quijote_simulations/45/ICs  --recursive --label "single folder transfer"
```

For more options and details see [Command Line Interface (CLI)](https://docs.globus.org/cli/).
