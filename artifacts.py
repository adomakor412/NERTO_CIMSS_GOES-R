#!/usr/bin/env python3
'!/usr/bin/python3'

import sys
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
from pathlib import Path
from subprocess import Popen
import itertools
from pyproj import Proj
import pyproj
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from pyresample import image, geometry
import metpy
import seaborn as sns
sns.set(style="darkgrid")
import os
import os.path as op
import glob
from convertdate import gregorian, ordinal
from multiprocessing import Pool
import warnings
import logging

#logger = logging.getLogger()

# store = '../artifacts/'
# sharkfins_FD_NC = '/scratch/gops/amqpfind/adomako_data/l1b_imagery_sharkfin/'
# caterpillar_FD_NC = '/scratch/gops/amqpfind/adomako_data/l1b_imagery_caterpillar_track/'

def Rad2BT(rad, planck_fk1, planck_fk2, planck_bc1, planck_bc2):
    """Radiances to Brightness Temprature (using black body equation)"""
    planck_fk1 = abs(planck_fk1)
    planck_fk2 = abs(planck_fk2)
    planck_bc1 = abs(planck_bc1)
    planck_bc2 = abs(planck_bc2)
    invRad = np.array(abs(rad))**(-1)
    arg = (invRad*planck_fk1) + 1.0
    T = (- planck_bc1+(planck_fk2 * (np.log(arg)**(-1))) )*(1/planck_bc2)
    return T

# def download(url,toPath, saveName):
#     cmd = [ 'wget ' + url +' -P ' + toPath +' -O '+ saveName]#if re.search('C07',url)
#     #print(cmd)
#     pid = Popen(cmd, shell=True)
#     pid.communicate()
#     return



# Sat = [16,17]
# year = [2021]
# month = list(range(1,3))
# day = list(range(1,32))
# hour = list(range(1,24))

# search = list(itertools.product(Sat, year, month, day, hour))

def main(argv):
    file = argv[0]
    
    #filelog = open('log_artifact.txt','w')
    try:
        #netcdf = glob.glob(op.join(artifact,'*.nc'))
        #print(netcdf, file=filelog)
        
        my_dpi = 192
        resolution = 5424
        GOES_R = xr.open_dataset(file)
        GOES_image = GOES_R['Rad']
        planck_fk1 = float(GOES_R['planck_fk1'].data)
        planck_fk2 = float(GOES_R['planck_fk2'].data) 
        planck_bc1 = float(GOES_R['planck_bc1'].data)                       
        planck_bc2 = float(GOES_R['planck_bc2'].data)
        Kelvin_GOES_image = Rad2BT(GOES_image, planck_fk1, planck_fk2, planck_bc1, planck_bc2)
        plt.figure(figsize=(resolution/my_dpi, resolution/my_dpi), dpi=my_dpi)
        fig1 = plt.imshow(Kelvin_GOES_image, interpolation='none', vmin=180, vmax=300, cmap='plasma')
        plt.grid(None)
        plt.axis('off')
        naming = str(os.path.basename(os.path.normpath(str(file)[:-3])))+'_UTC_5424x5424.png'           
        savePath = argv[1]#op.join(store,storage)       
        if not os.path.isfile(op.join(savePath,naming)):
            fig1.figure.savefig( op.join(savePath,naming) )
        #cbar = plt.colorbar()
        #cbar.ax.set_ylabel('Kelvin')
        naming = str(os.path.basename(os.path.normpath(file[:-3])))+'_UTC_5424x5424_BW.png'
        fig1=plt.imshow(Kelvin_GOES_image, cmap ='Greys', vmin=180, vmax=300)    
        if not os.path.isfile(op.join(savePath,naming)):
            fig1.figure.savefig(op.join(savePath,naming))
        plt.close('all')
        GOES_R.close()

    except ValueError as e:
        print('THERE IS AN ERROR')
        print(file)
#         print('\n', file = filelog)
#         print(file, file = filelog)
#         print(e, file = filelog)
#         print('\n', file = filelog)

    #filelog.close()
    return

if __name__ == "__main__":
   main(sys.argv[1:])

# artifactList = [sharkfins_FD_NC, caterpillar_FD_NC]

# for artifact in artifactList:
#     if artifact == sharkfins_FD_NC:
#         storage = 'sharkfin'
#     else:
#         storage = 'caterpillar'
#     execute(artifact,storage)