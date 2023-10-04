# RegionalAC_Py
This repository stores the basis to run AquaCrop (version 7.0 and higher) spatially with a Python wrapper. Note that his code is not readily usable and needs to be adapeted to your domain, purpose, options.

## Functioning
The domain is gridded in rows and columns. For each pixel, there is a corresponding latitute and longitude that the user has to define. A useful example on how to set teh Georeference can be found under preprocessing/COORD.py, based on de Roos et al. (2021).

## Regional AquaCrop scripts
The regional AquaCrop is based on de Roos et al. (2021) and originally developed for AquaCropV6.1. The code has been updated to run for AquaCropV7.0 and higher. To spatially run AquaCrop with the python wrapper, two scripts are required:
1. AC_exec.py
   This script executes and contains the parallelization (via multiprocessing package) to distribute the simulations spatially through a defined number of processes and distributes the pixels (combinations of rows and columns) across the different processes. This scripts prepares the AquaCrop environement and calls the function run_ac_pro_yrs (from AC_PRM.py) to prepare the project file in order to run AquaCrop.
2. AC_PRM.py
   This script prepares the project file (.PRM) to run AquaCrop. Note that only the soil files and the climate files are spatially varying. The crop, irrigation, and management files can be used but will be applied for the whle domain. However, this can be readily upgraded.

## Preprocessing
In this folder, some example scripts are given to help the users preprocess their data to run the regional AquaCrop.
1. AC_SOL_253.py - Creation of soil siles for given grid based on the Harmonized Soil World DataBase
2. ERA5_CLI.py - Creation of climate files based on ERA5 climate data
3. MERRA2_CLI.py - Creation of climate files based on MERRA2

## Postprocessing
An example script is given to store the AquaCrop output (generated in different directories, one for each pixel) into a netcdf files with dimensions (time, lat, lon). 

## Citation

