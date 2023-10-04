#!/usr/bin/env python
import os
import numpy as np
from netCDF4 import Dataset
import pandas as pd
import xarray as xr
from COORD_AC import AC_GEOreference, mindist
crds = AC_GEOreference()

'''
Generates soil files (.SOL), based on de Roos et al. (2021).

de Roos, S., De Lannoy, G. J. M., and Raes, D.: Performance analysis of regional AquaCrop (v6.1) 
biomass and surface soil moisture simulations using satellite and in situ observations, 
Geosci. Model Dev., 14, 7309–7328, https://doi.org/10.5194/gmd-14-7309-2021, 2021.
'''

def run_SOL253(row,col, dirout):

    # coonvert to latidude and longitude
    lat = crds.row_to_lat(row)
    lon = crds.col_to_lon(col)

    # Destination file
    Dirnew=  dirout#par.dirNew
    Soilname = str(row) + '_'+ str(col)#par.soilname
    title_soil = 'Soil_'+str(round(lat,3)) + '_'+ str(round(lon,3))
    print(title_soil)

    #file locations soil classification
    slcl_top = '/my_dir/soilcls_top_30sec.nc' # doi:10.5281/zenodo.4770738
    slcl_sub = '/my_dir/soilcls_sub_30sec.nc' # doi:10.5281/zenodo.4770738
    ds_TOP = Dataset(slcl_top, 'r')
    ds_SUB = Dataset(slcl_sub, 'r')

    # From origin netCDF to origin new file
    lt, ln = mindist(lat,np.arange((-90 + (1/240)),90,(1/120))), mindist(lon,np.arange((-180 + (1/240)),180,(1/120)))
    n_r= lt
    n_c= ln
    print(n_r,n_c)


    #Define soil class
    soil_top = ds_TOP.variables['soilcls_top_30sec'][n_c,n_r]
    soil_sub = ds_SUB.variables['soilcls_sub_30sec'][n_c,n_r]
    #print(soil_top, soil_sub)

    if soil_top == 0 and soil_sub == 0:
        print('no data')
        pass
        
    elif os.path.isfile(Dirnew + Soilname + '.SOL'):
        print('file exists')
        pass

    else:
        #file locations hydraulic parameters
        TOP = '/my_dir/Soil_param_100_mineral_3_OC_026_046_112_Woesten_topsoil.txt'
        SUB = '/my_dir/Soil_param_100_mineral_3_OC_026_046_112_Woesten_subsoil.txt'

        hydParam_TOP = pd.read_csv(TOP, delim_whitespace=True)
        hydParam_SUB = pd.read_csv(SUB, delim_whitespace=True)

        HP_TOP = pd.DataFrame(hydParam_TOP).set_index('Number')
        HP_SUB = pd.DataFrame(hydParam_SUB).set_index('Number')


        # constant parameters
        pen = 100
        grav = 0

        thickness = [0.3, 0.7]
        layers = [soil_top, soil_sub]
        SHPs = [HP_TOP, HP_SUB]

        data = []
        head =[]

        for layer, thick, SHP in zip(layers, thickness, SHPs):
            # extract SHP from refined classification
            OC = SHP.loc[layer][4]
            wp = SHP.loc[layer][5] * 100
            sat = SHP.loc[layer][6] * 100
            fc = SHP.loc[layer][11] * 100
            Ksat = SHP.loc[layer][9] * 86400000
            sd = round(float(SHP.loc[layer][1]),4)
            cl = round(float(SHP.loc[layer][2]),4)
            si = round(float(SHP.loc[layer][3]),4)
            print('OC:',OC,'wp:',wp,'sat:', sat,'fc:',fc,'Ksat:', Ksat, 'sd:',sd,'cl:',cl,'si:',si)

            # define default CN
            if Ksat > 864: CN = 46
            elif Ksat >= 347: CN = 61
            elif Ksat >= 36: CN = 72
            else: CN = 77

            # define default REW (only top layer will be used)
            Z_surf = 0.04
            REW=int(10*(fc-(wp/2))*Z_surf)
            if REW <0: REW = 0
            if REW >15: REW = 15

            #  associate soil class with USDA soil type for soil description
            if (1.5 * cl + si) < 15:
                descr = 0
            elif ((1.5 * cl + si) >= 15) and ((2 * cl + si) <= 30):
                descr = 1
            elif cl >= 7 and cl < 20 and sd >= 52 and (2 * cl + si >= 30):
                descr = 2
            elif cl < 7 and si < 50 and (2 * cl + si >= 30):
                descr = 2
            elif cl >= 7 and cl < 27 and si >= 28 and si < 50 and sd < 52:
                descr = 3
            elif si >= 50 and cl >= 12 and cl < 27:
                descr = 4
            elif si >= 50 and si < 80 and cl < 12:
                descr = 4
            elif si >= 80 and cl < 12:
                descr = 5
            elif cl >= 20 and cl < 35 and si < 28 and sd > 45:
                descr = 6
            elif cl >= 27 and cl < 40 and sd >= 20 and sd < 45:
                descr = 7
            elif cl >= 27 and cl < 40 and sd < 20:
                descr = 8
            elif cl >= 35 and cl < 55 and sd >= 45 and sd < 65:
                descr = 9
            elif cl >= 40 and si >= 40:
                descr = 10
            elif cl >= 40 and sd < 45 and si < 40:
                descr = 11
            else:
                print('no soil texture found for ' + str(row) + '_' + str(col))
            soil_type = ['sand', 'loamy sand', 'sandy loam', 'loam', 'silt loam', 'silt', 'sandy clay loam',
                         'clay loam',
                         'silty clay loam', 'sandy clay', 'silty clay', 'clay']
            print(descr)

            # function to calculate capillary rise with Ksat (according to USDA soil type)

            if descr == 0 or descr == 1 or descr == 2:
                CRa = -0.3112-10**-5*Ksat
                CRb = -1.4936+0.2416*np.log(Ksat)
            elif descr == 3 or descr == 4 or descr == 5:
                CRa = -0.4986-9*10**-5*Ksat
                CRb = -2.1320+0.4778*np.log(Ksat)
            elif descr == 6 or descr == 7 or descr == 9:
                CRa = -0.5677-4*10**-5*Ksat
                CRb = -3.7189+0.5922*np.log(Ksat)
            elif descr == 8 or descr == 10 or descr == 11:
                CRa = -0.6366+8*10**-4*Ksat
                CRb = -1.9165+0.7063*np.log(Ksat)

            data.append([thick,sat,fc,wp,Ksat,pen,grav, CRa, CRb, soil_type[descr]])
            print(sat)
            head.append([CN, REW])

        soil = pd.DataFrame(data)
        header=pd.DataFrame(head)

        '''-----------------------------------write soil file-----------------------------------------------------------'''

        headerS = '\n'.join([ title_soil,
            '   %3.1f'%7.1 + '\t: AquaCrop Version (August 2023)',
            '   %d'%header.iloc[0][0] + '\t: CN (Curve Number)',
            '   %d'%header.iloc[0][1] + '\t: Readily evaporable water from top layer (mm)',
            '   %d'%2 + '\t: Number of soil horizons',
            '   %d'%-9.00 + '\t: Depth (m) of restrictive soil layer inhibiting root zone expansion',
            '  Thickness\tSat \t FC \t WP \t Ksat \t Penetrability \t Gravel\t CRa\t   CRb \t\tdescription',
            '  ---(m)- \t------(vol %)----- \t(mm/day)      (%)        (%)    -----------------------------------------'])

        np.savetxt(Dirnew + Soilname + '.SOL', soil, fmt=('    %4.2f','\t%3.1f','\t%3.1f','\t%3.1f','\t%4.1f','         %d       ',
                                                  '%d     ', '%7.6f','  %7.6f', '\t%s'), comments='', header= headerS)

    ''''------------------------------------------------------------------------------------------------------------'''
