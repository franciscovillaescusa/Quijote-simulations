Halo Statistics
===============

Statistics extracted from Friend-of-Friends halo catalogues for ``fiducial``, ``Om_m``, ``Om_p``, ``s8_m``, ``s8_p`` , ``DC_m``, ``DC_p`` and redshifts z=0,0.5,1. All statistics are extracted using the Ntot most massive halos for each realisation. Ntot is chosen to be close to the maximum number of halos and is tuned for each cosmology to leave the halo bias constant across cosmology with the following values

.. csv-table:: 
   :header: "z", "``fiducial``", "``Om_m``", "``Om_p``", "``s8_m``", "``s8_p``", "``DC_m``", "``DC_p``"

	"0.0", "358364", "390000", "329930", "361020", "355876", "348644", "366627"
    "0.5", "275253", "300000", "252965", "269741", "276134", "265038", "283874"
    "1.0", "165107", "180000", "151694", "162795", "167293", "157266", "171767"

Including:

- Halo PDFs of densities smoothed on scales of R=20,25,30Mpc/h for all 15,000 realisations of ``fiducial`` and 500 realisations for all other cosmologies. PDFs are also included for 500 realisations extracted using the Ntot least massive halos for ``fiducial``. Files contain PDFs in terms of number halo number count N_h and are formatted as N_h | P(N_h)

- Halo power spectra for all 15,000 realisations of ``fiducial`` and 500 realisations for all other cosmologies. Power spectra are also included for 500 realisations extracted using the Ntot least massive halos for ``fiducial``. Files are formatted as k | P(k) with k in units of h/Mpc.

- Conditional moments for halos and matter densities smoothed on scales of R=20,25,30Mpc/h. For ``fiducial`` there are 500 realisations for both the most massive and least massive halos and 42 for ``Om_m``, ``Om_p``, ``s8_m``, ``s8_p``. The files are formatted as delta_m+1 | <delta_h+1|delta_m+1> | <(delta_h)^2|delta_m+1>.



