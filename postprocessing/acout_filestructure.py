#!/usr/bin/env python
import numpy as np

'''
Output file structure

Up to date with AquaCropV7.1

'''

def ac_columns(len):
    '''Contains name of AquaCrop variables. You can refer to the PlugIn reference manual V7.1 available on the
    FAO website. Note that when there are dublicate vairables (e.g. Rain) a suffix _a and _b were added.'''
    if len == 98:
        ACout_cols = ['Day', 'Month', 'Year', 'DAP', 'Stage', 'WC(x.xx)', 'Rain_a', 'Irri', 'Surf', 'Infilt',
                      'RO', 'Drain', 'CR',
                      'Zgwt_a', 'Ex', 'E', 'E/Ex', 'Trx', 'Tr', 'Tr/Trx', 'ETx', 'ET', 'ET/ETx', 'GD',
                      'Z_a', 'StExp', 'StSto',
                      'StSen', 'StSalt', 'StWeed', 'CC', 'CCw', 'StTr', 'Kc(Tr)', 'Trx', 'Tr', 'TrW',
                      'Tr/Trx', 'WP', 'Biomass',
                      'HI', 'Y(dry)', 'Y(fresh)', 'Brelative', 'WPet', 'Bin', 'Bout',
                      'WC(x.xx)', 'Wr(x.xx)', 'Z_b', 'Wr', 'Wr(SAT)',
                      'Wr(FC)', 'Wr(exp)', 'Wr(sto)', 'Wr(sen)', 'Wr(PWP)',
                      'SaltIn', 'SaltOut', 'SaltUp', 'Salt(x.xx)', 'SaltZ',
                      'Z_c', 'ECe', 'ECsw',
                      'StSalt', 'Zgwt_b', 'ECgw', 'WC01', 'WC02', 'WC03', 'WC04', 'WC05', 'WC06', 'WC07', 'WC08',
                      'WC09', 'WC10', 'WC11', 'WC12', 'ECe01', 'ECe02', 'ECe03', 'ECe04', 'ECe05', 'ECe06', 'ECe07',
                      'ECe08', 'ECe09', 'ECe10', 'Ece11', 'Ece12', 'Rain_b', 'ETo', 'Tmin', 'Tavg', 'Tmax', 'CO2']

    elif len == 93:
        ACout_cols = ['Day', 'Month', 'Year', 'DAP', 'Stage', 'WC(x.xx)', 'Rain_a', 'Irri', 'Surf', 'Infilt',
                      'RO', 'Drain', 'CR',
                      'Zgwt_a', 'Ex', 'E', 'E/Ex', 'Trx', 'Tr', 'Tr/Trx', 'ETx', 'ET', 'ET/ETx', 'GD',
                      'Z_a', 'StExp', 'StSto',
                      'StSen', 'StSalt', 'StWeed', 'CC', 'CCw', 'StTr', 'Kc(Tr)', 'Trx', 'Tr', 'TrW',
                      'Tr/Trx', 'WP', 'Biomass',
                      'HI', 'Y(dry)', 'Y(fresh)', 'Brelative', 'WPet', 'Bin', 'Bout',
                      'WC(x.xx)', 'Wr(x.xx)', 'Z_b', 'Wr', 'Wr(SAT)',
                      'Wr(FC)', 'Wr(exp)', 'Wr(sto)', 'Wr(sen)', 'Wr(PWP)',
                      'SaltIn', 'SaltOut', 'SaltUp', 'Salt(x.xx)', 'SaltZ',
                      'Z_c', 'ECe', 'ECsw',
                      'StSalt', 'Zgwt_b', 'ECgw', 'WC01', 'WC02', 'WC03', 'WC04', 'WC05', 'WC06', 'WC07', 'WC08',
                      'WC09', 'WC10', 'WC11', 'ECe01', 'ECe02', 'ECe03', 'ECe04', 'ECe05', 'ECe06', 'ECe07',
                      'ECe08', 'ECe09', 'ECe10', 'Ece11', 'Rain_b', 'ETo', 'Tmin', 'Tavg', 'Tmax', 'CO2']
    elif len == 91:
        ACout_cols = ['Day', 'Month', 'Year', 'DAP', 'Stage', 'WC(x.xx)', 'Rain_a', 'Irri', 'Surf', 'Infilt',
                      'RO', 'Drain', 'CR',
                      'Zgwt_a', 'Ex', 'E', 'E/Ex', 'Trx', 'Tr', 'Tr/Trx', 'ETx', 'ET', 'ET/ETx', 'GD',
                      'Z_a', 'StExp', 'StSto',
                      'StSen', 'StSalt', 'StWeed', 'CC', 'CCw', 'StTr', 'Kc(Tr)', 'Trx', 'Tr', 'TrW',
                      'Tr/Trx', 'WP', 'Biomass',
                      'HI', 'Y(dry)', 'Y(fresh)', 'Brelative', 'WPet', 'Bin', 'Bout',
                      'WC(x.xx)', 'Wr(x.xx)', 'Z_b', 'Wr', 'Wr(SAT)',
                      'Wr(FC)', 'Wr(exp)', 'Wr(sto)', 'Wr(sen)', 'Wr(PWP)',
                      'SaltIn', 'SaltOut', 'SaltUp', 'Salt(x.xx)', 'SaltZ',
                      'Z_c', 'ECe', 'ECsw',
                      'StSalt', 'Zgwt_b', 'ECgw', 'WC01', 'WC02', 'WC03', 'WC04', 'WC05', 'WC06', 'WC07', 'WC08',
                      'WC09', 'WC10', 'ECe01', 'ECe02', 'ECe03', 'ECe04', 'ECe05', 'ECe06', 'ECe07',
                      'ECe08', 'ECe09', 'ECe10', 'Rain_b', 'ETo', 'Tmin', 'Tavg', 'Tmax', 'CO2']
    else:
        ACout_cols = print('check number of columns AC output', len)
    return(ACout_cols)


def ac_skiprows(yearstart, yearend):
    '''Tool for leap years to skip the right rows when reading the daily output file'''
    years = np.arange(yearstart, yearend+1)
    year_n = yearend - yearstart + 1
    skiprows = [0, 1, 2, 3, 4]
    for i in np.arange(0, year_n):
        if (years[i] % 4) == 0:
            if (years[i] % 100) == 0:
                if (years[i] % 400) == 0:
                    skiprows.append(skiprows[-1] + 367)
                    skiprows.append(skiprows[-1] + 1)
                    skiprows.append(skiprows[-1] + 1)
                    skiprows.append(skiprows[-1] + 1)
                else:
                    skiprows.append(skiprows[-1] + 366)
                    skiprows.append(skiprows[-1] + 1)
                    skiprows.append(skiprows[-1] + 1)
                    skiprows.append(skiprows[-1] + 1)
            else:
                skiprows.append(skiprows[-1] + 367)
                skiprows.append(skiprows[-1] + 1)
                skiprows.append(skiprows[-1] + 1)
                skiprows.append(skiprows[-1] + 1)
        else:
            skiprows.append(skiprows[-1] + 366)
            skiprows.append(skiprows[-1] + 1)
            skiprows.append(skiprows[-1] + 1)
            skiprows.append(skiprows[-1] + 1)

    return(skiprows)
