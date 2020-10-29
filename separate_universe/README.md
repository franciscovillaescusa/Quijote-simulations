Edit the paths to executables in
* run\_camb.sh
* temp\_sbatch.txt

In these files, you may also need to edit the modules,
if you built the code with different versions of the libraries.

Note that the sigma8 parameter in parameter\_file\_generator.py
should not do anything, for this I have a custom version of 2LPT that
does not perform the rescaling of the power spectrum to a desired sigma8.
Conversely, you need to edit the scalar amplitude in temp\_camb.txt so
that it gives the desired value of sigma8.

The code is written for a custom version of Gadget-4, which takes the additional
parameter SUGlobalScaleFile in its input parameter file.
This is only important if you want to run the Gadget FoF halo finder, since we
need to rescale the linking length in the separate universes as a function of time.

Running
```shell
python parameter_file_generator.py
```
will produce the file structure

    root/
      CAMB/
        CAMB_params.ini
        ...
      seed{seeds}/
        {abs(delta_bs)}[p,m]/
          2LPT/
            2LPT.param
            CAMB_matterpow_0_headerremoved_rescaled.dat
            seed.txt
          G4/
            G4.param
            times.txt
            SU_scale_file.dat
          slurm/
            in.sh

The python script will automatically run CAMB. It needs to be run only once
since we rescale the matter power spectrum for the different values of the DC mode.
The rescaled power spectra are then placed in the respective 2LPT directories.

The root directory as well as the seeds and the values of delta\_b
can be set in parameter\_file\_generator.py.

A file submit.sh will also be produced in the working directory, which you can use
to automatically submit all the in.sh scripts to slurm:
```shell
sh submit.sh
```
