#!/usr/bin/env python
import numpy as np


'''
Based on de Roos et al. (2021)
de Roos, S., De Lannoy, G. J. M., and Raes, D.: Performance analysis of regional AquaCrop (v6.1)
biomass and surface soil moisture simulations using satellite and in situ observations, 
Geosci. Model Dev., 14, 7309–7328, https://doi.org/10.5194/gmd-14-7309-2021, 2021.
'''

def mindist(point, array):
    '''Formula to find the minimum distance of an element in an array.'''
    mindist = np.abs(array - point).argmin()
    return mindist

class AC_GEOreference():
    '''Defines the coordinate range that is used in the spatial Aquacrop model and is equal to the coordinates of the HWSDv1.2.
    The resolution is 30 arc sec == 1/120 degrees lat/lon.'''
    def __init__(self,):
        # HWSD
        rows_hwsd = np.arange(0, 21600)
        cols_hwsd = np.arange(0, 43200)
        self.step = (1/120)
        hwsd_latini, hwsd_lonini = (-90 + 1/240),(-180 + 1/240)
        self.lat_ini = 14400 * self.step + hwsd_latini      # ini = 14400: initial point is -90 + (1/240) --> + 120deg is +/- 30deg
        self.lon_ini = 20340 * self.step + hwsd_lonini      # ini = 20340: initial point is -180 + (1/240) -->  + +/- 170 deg is -10deg

    # general formulas
    def lat_to_row(self,lat):
        row = round((lat - self.lat_ini) / (self.step))
        return row
    def lon_to_col(self, lon):
        col = round((lon - self.lon_ini) / (self.step))
        return col
    def row_to_lat(self, row):
        lat = row * self.step + self.lat_ini
        return lat
    def col_to_lon(self, col):
        lon = col * self.step + self.lon_ini
        return lon

    def AC_mindist(self,row, col, ds_lats, ds_lons):
        '''Formula to find closest AC row/col pixel in a dataset of lats/lons'''
        lat = row * self.step + self.lat_ini
        lon = col * self.step + self.lon_ini
        lat_id, lon_id = mindist(lat, ds_lats), mindist(lon, ds_lons)
        return(lat_id, lon_id)

class MERRA2_GEOreference():
    def __init__(self, ):
        self.M2AC_ini_lat = 60
        self.M2AC_ini_lon = -10.625
        self.M2AC_step_lat = 0.5
        self.M2AC_step_lon = 0.625
        self.CLI_latrange=np.arange(self.M2AC_ini_lat, 30, -self.M2AC_step_lat)
        self.CLI_lonrange=np.arange(self.M2AC_ini_lon, 45.625, self.M2AC_step_lon)
    def M2AC_row_to_lat(self, row):
        lat = self.M2AC_ini_lat - (row * self.M2AC_step_lat)
        return lat
    def M2AC_lat_to_row(self, lat):
        row = round((self.M2AC_ini_lat - lat) / self.M2AC_step_lat)
        return row
    def M2AC_col_to_lon(self, col):
        lon = self.M2AC_ini_lon + (col*self.M2AC_step_lon)
        return lon
    def M2AC_lon_to_col(self, lon):
        col = round((lon-self.M2AC_ini_lon)/self.M2AC_step_lon)
        return col


