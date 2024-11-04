# !/usr/bin/env python
import os
import shutil
import numpy as np
from multiprocessing import Pool
from AC_PRM import run_ac_pro_yrs

''' --------------------------------------------------------------------------------------------------------------------------
Executable for AquaCrop, the regional version. With multiprocessing it can be run on the max available cores on a single node.
@ Shannon de Roos 2020: original author, for AquaCropV6.1
@ Louise Busschaert 2023: simplified and adapted for AquaCropV7 and higher
Note 4 Nov 2024: for windows users, avoid using the multiprocessing/Pool package and replace the symbolic link to the AquaCrop
executable to an actual copy of the aquacrop.exe. LB will later add if statements to run with the apropriate configuration 
(Linux/Windows).
----------------------------------------------------------------------------------------------------------------------------'''


# ------------------------ parallel processing python ------------------------------------------------------------------------

def main():

    row_start = int(0)
    row_end = int(1)
    col_start = int(0)
    col_end = int(1)
    args = list()
    for row in np.arange(row_start, row_end + 1):
        for col in np.arange(col_start,col_end + 1):
            args.append((col, row))

    p = Pool(1)            # For paralelization: define number of cores.
                            # If not (1 process): p = Pool(1)
    p.map(wrapper, args)    #performs actual parallelization


def wrapper(coords):  # wraps all functions into one list of functions

    col, row = coords

    #filenames and directories
    input_dir =  '/my_dir/test_linux/INPUT/'
    dir_out = '/my_dir/text_linux/OUTPUT/'
    dir_soil = input_dir + 'soil/'
    dir_cli = input_dir + 'climate/'
    dir_crop = input_dir + 'crop/'
    dir_suppl = input_dir + 'suppl_input/'

    start_year = 2011
    end_year = 2016

    fname = str(row) + '_' + str(col)
    pa = dir_out  + fname + '/'
    PRM = pa + 'LIST/' + fname + '.PRM'


    if os.path.exists(dir_soil + fname+'.SOL'): # To run only for pixel
                                                # with available soil file
        print('=========', row, col, '=========')

        # Make new local directory for each gridcell
        os.mkdir(pa)
        os.chdir(pa)

        # Place Aquacrop directories SIMUL and LIST in local directory
        shutil.copytree(input_dir + 'SIMUL', pa + 'SIMUL')
        os.mkdir(pa + 'OUTP')
        os.mkdir(pa + 'LIST')
        with open(pa + 'LIST/ListProjects.txt', 'a') as file:
            file.write(fname + '.PRM\n')

        # Link Aquacrop model to current directory
        AC_loc =  '/my_executable_dir/aquacrop'
        os.symlink(AC_loc, pa + 'aquacrop')

        # Prepare PRM file
        run_ac_pro_yrs(row, col,
                       dir_out, dir_soil, dir_cli, dir_crop, dir_suppl,
                       start_year, end_year)
        # Run the executable
        os.system(pa + 'aquacrop')

        #remove extra files and directories: only save PRM and output file
        # Comment in case of debugging to look into the files
        shutil.copyfile(PRM, pa + fname + '.PRM')
        shutil.rmtree(pa + 'SIMUL')
        shutil.rmtree(pa + 'LIST')
        os.unlink(pa + 'aquacrop')
        os.remove(pa + 'OUTP/AllDone.OUT')
        os.remove(pa + 'OUTP/ListProjectsLoaded.OUT')

main()
