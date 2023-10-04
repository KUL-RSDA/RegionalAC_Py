# RegionalAC_Py
This repository stores the basis to run AquaCrop (version 7.0 and higher) spatially with a Python wrapper. Examples of preprocessing and postprocessing scripts are provided. Note that these scripts are only there to provide examples to the users, that can serve as basis for their regional simulations.

## Regional AquaCrop scripts
The regional AquaCrop is based on de Roos et al. (2021) and originally developed for AquaCropV6.1. The code has been updated to run for AquaCropV7.0 and higher. To spatially run AquaCrop with the python wrapper, two scripts are required:
1. AC_exec.py
   This script executes and contains the parallelization (using the multiprocessing Python package). This scripts prepares the AquaCrop environement and calls the function run_ac_pro_yrs (from AC_PRM.py) to prepare the project file in order to run AquaCrop.
2. AC_PRM.py
   This script prepares the project file (.PRM) to run AquaCrop. Note that only the soil files and the climate files are dynamic in space. The crop, irrigation, and management files can be used but will be applied for the whole domain. However, dynamic (in time and space) input can readily be implemented.

The RegionalAC can be tested by adapting the paths in AC_exec.py to the testace (test_linux or test_windows). Reference output, generated on Linux with AquaCropV7.1 is also provided under OUTPUT_REF.

## Preprocessing
In this folder, some example scripts are given to help the users preprocess their data to run the regional AquaCrop. Note that these scripts may not be readily usable and should be adapeted to your setup (domain, parameters, options, datasets,...).
1. AC_SOL_253.py - Creation of soil siles for given grid based on the HWSD (as in de Roos et al., 2021).
2. prep_CLI.py - Creation of climate files
3. COORD.py - Example on how to set the Georeference for AquaCrop and other input data of another resolution (e.g. climate).

## Postprocessing
An example script is given to store the AquaCrop output (generated in different directories, one for each pixel) into a netcdf files with dimensions (time, lat, lon). 

## Citation
- de Roos, S., De Lannoy, G.J.M., Raes, D. (2021). Performance analysis of regional AquaCrop (v6.1) biomass and surface soil moisture simulations using satellite and in situ observations. Geoscientific Model Development, 14(12), 7309-7328, 10.5194/gmd-14-7309-2021.
- Busschaert, L., de Roos, S., Thiery, W., Raes, D., De Lannoy, G.J.M. (2022). Net irrigation requirement under different climate scenarios using AquaCrop over Europe. Hydrology and Earth System Sciences, 26, 3731–3752, 10.5194/hess-26-3731-2022.
