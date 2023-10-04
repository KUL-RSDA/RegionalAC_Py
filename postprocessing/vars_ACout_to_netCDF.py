#!/usr/bin/env python
import numpy as np
from datetime import date, timedelta
from matplotlib import dates
import pandas as pd
import os
from acout_filestructure import ac_columns, ac_skiprows
from netCDF4 import Dataset
from preprocessing.COORD import AC_GEOreference, mindist
crds = AC_GEOreference() # GEO_reference example

'''

Generates netcdf file from AquaCrop output.
@Louise Busschaert

'''

years = [2011, 2016]
run_name = 'test' # name of the netcdf file, e.g. AC_testrun
vars = ['WC01', 'Biomass'] #the variables you want to extract
newfile = run_name + '_' + str(years[0]) + '-' + str(years[1])

row_start = 0
row_end = 1
rows = np.arange(row_start, row_end+1)
col_start = 0
col_end = 1
cols = np.arange(col_start, col_end+1)
dir_out = '/RegionalAC_Py/test_linux/OUTPUT_REF/' #AC output dir
dir_nc = dir_out # the directory where you want your netcdf file

# Long names and units of variables to add information to the netcdf file
# More can be added, check the Standalone reference manual of the relevant
# AquaCrop version
long_names = {'WC01': 'water content layer 1',
              'Biomass': 'daily biomass production',
              }
units = {'WC01': '%',
         'Biomass': 'ton/ha',
         }


#Define dimensions (time, lat, lon) as arrays
lats = np.arange(crds.row_to_lat(row_start), crds.row_to_lat(row_end)+crds.step/2, crds.step)
lons = np.arange(crds.col_to_lon(col_start), crds.col_to_lon(col_end)+crds.step/2, crds.step)
Dates = np.arange(date(years[0], 1, 1), date(years[1]+1, 1, 1), timedelta(days=1))
index = pd.DatetimeIndex(Dates)
times = dates.date2num(index.to_pydatetime()).astype('int32')
timeunit ='days since ' + str(years[0]) + '-01-01 00:00'
times = times - times[0]

dims = (len(vars), len(times), len(lats), len(lons))

#Create an empty dataframe
ts_data = np.full(dims, np.nan)

#Fill it in a loop:
for row in rows:
    for col in cols:
        # Convert row/col to lat/lon
        lat, lon = crds.row_to_lat(row), crds.col_to_lon(col)
        # Use mindist to find the row/col index (lat_id/lon_id) number
        lat_id, lon_id = mindist(lat, lats), mindist(lon, lons)
        # Extract soil moisture data from AquaCrop for your entire 
        # time series at one pixel, read as a DataFrame
        file_id = str(row) + '_' + str(col)
        path = dir_out + file_id + '/OUTP/' + file_id + 'PRMday.OUT'

        if not os.path.exists(path): # no AC output simulated
            pass
        else:
            df = pd.read_csv(path, encoding='cp1252',
                              delim_whitespace=True, skiprows=ac_skiprows(years[0], years[1]), header=None,
                              index_col=False). \
                replace({-9.9: 0, -9.00: 0., -9.000: 0, -900.0: 0})
            df_len_cols = df.shape[1]
            df.columns = ac_columns(df_len_cols)
            # add data at the right location for each variable
            for v, var in enumerate(vars):
                ts_data[v, :, lat_id, lon_id] = df[var]
            print(str(row) + '_' + str(col))


# --create netcdf with dimensions and variables---------------
with Dataset(dir_nc + newfile + '.nc', 'w', format="NETCDF4") as ds:

    ds.createDimension('lat', len(lats))
    print('lat created')
    ds.createDimension('lon', len(lons))
    print('lon created')
    ds.createDimension('time', len(times))
    print('time created')

    ds.createVariable('time', 'float', dimensions='time', zlib=True)
    ds.createVariable('lat', 'float', dimensions='lat', zlib=True)
    ds.createVariable('lon', 'float', dimensions='lon', zlib=True)
    for v, var in enumerate(vars):
        ds.createVariable(var, 'float', dimensions=('time', 'lat', 'lon'), zlib=True)
        ds.variables[var][:] = ts_data[v,:,:,:]
        ds.variables[var].setncatts({'long_name': long_names[var], 'unit': units[var]})

    ds.variables['lat'][:] = lats
    ds.variables['lon'][:] = lons

    ds.variables['time'][:] = times
    ds.variables['time'].setncatts({'long_name': 'time', 'units': timeunit})
print('Done')
