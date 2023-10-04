#!/usr/bin/env python
import xarray as xr
import numpy as np
import pandas as pd
from pathlib import Path
from netCDF4 import Dataset
from datetime import datetime
import math
import os, glob
import matplotlib.pyplot as plt
from defParam import parameters
par = parameters()
from COORD_AC import MERRA2_GEOreference
crds = MERRA2_GEOreference()

np.warnings.filterwarnings('ignore')
#env_keep += "XDG_RUNTIME_DIR"

'''===================================================================================================================
Creates climates files
Note: the extraction of the meteorological forcings will depend on the source.
Here for 2011 through 2016
======================================================================================================================'''

def run_cli_ts(VAR_lat, VAR_lon,latini, lonini, st_lat,st_lon):
    #INPUT BY USER
    start_date = '2011-01-01'
    end_date = '2016-12-31'
    Freq = 1                            #1=daily, 2=10-daily, 3=monthly
    years =['Y2011', 'Y2012', 'Y2013','Y2014', 'Y2015','Y2016']
    months = ['M01', 'M02', 'M03','M04','M05','M06','M07','M08','M09','M10','M11','M12']

    #Convert variables to lat lon
    latpt = crds.M2AC_row_to_lat(VAR_lat)
    lonpt  =crds.M2AC_col_to_lon(VAR_lon)


    name_dir = '/my_dir/CLI_files/' + str(VAR_lat) + '_' + str(VAR_lon) + '_2011-2016'
    name = str(round(latpt,2)) + '_' + str(round(lonpt,3)) + '_'
    name_fil = str(VAR_lat) + '_' + str(VAR_lon)+ '_'
    os.mkdir(name_dir)

    #Define minimum distance function for coordinate matching
    def mindist(point, array):
        mindist = np.abs(array - point).argmin()
        return mindist

    # Only run for grid-cells on land  # Need cleaner method
    lat_id, lon_id = mindist(latpt, lats), mindist(lonpt, lons)

    # Create DataFrames for data ouput METEO
    date_s = datetime.strptime(start_date, '%Y-%m-%d').date()
    date_e = datetime.strptime(end_date, '%Y-%m-%d').date()
    TMP = pd.DataFrame(columns=['TSmin', 'TSmax'], index=pd.date_range(date_s, date_e))
    PLU = pd.DataFrame(columns=['PLU'], index=pd.date_range(date_s, date_e))
    ETo = pd.DataFrame(columns=['ETo'], index=pd.date_range(date_s, date_e))

    # Loop over files
    # EXTRACT METEO FORCING FROM SOURCE AND FILL TMP, PLU, ETo
    #....


    # write output files
    title = name + '- daily data:' + start_date + ' to ' + end_date
    head_date = '\n'.join([title,
                            '     ' + str(Freq) + '  : Daily records (1=daily, 2=10-daily and 3=monthly data)',
                            '     ' + str(
                            date_s.day) + '  : First day of record (1, 11 or 21 for 10-day or 1 for months)',
                            '     ' + str(date_s.month) + '  : First month of record',
                            '  ' + str(
                            date_s.year) + '  : First year of record (1901 if not linked to a specific year)'
                                                  '\n'])

    hd_tmp = '''Tmin (C)   Tmax (C)\n======================'''
    head_tmp = '\n'.join([head_date, hd_tmp])
    tmp_fn = name_fil + '.Tnx'

    hd_prec = ''' Total Rain (mm)\n======================='''
    head_prec = '\n'.join([head_date, hd_prec])
    prec_fn = name_fil + '.PLU'

    hd_ETo = '''  Average ETo (mm/day)\n======================='''
    head_ETo = '\n'.join([head_date, hd_ETo])
    eto_fn = name_fil + '.ETo'

    np.savetxt(name_dir + tmp_fn, TMP, fmt=('%3.1f', '%3.1f'), comments='', header=head_tmp, delimiter='\t')
    np.savetxt(name_dir + prec_fn, PLU, fmt='%3.1f', comments='', header=head_prec)
    np.savetxt(name_dir + eto_fn, ETo, fmt='%3.1f', comments='', header=head_ETo)
    climate = (open(name_dir + name_fil + '.CLI', 'w')).write('\n'.join([title,
                                                        ' 7.1   : AquaCrop Version (August 2023)',
                                                        tmp_fn,
                                                        eto_fn,
                                                        prec_fn,'MaunaLoa.CO2']))
