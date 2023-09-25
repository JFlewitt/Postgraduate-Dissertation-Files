import numpy as np
import xarray as xar
import create_timeseries as cts
import pdb
from matplotlib import pyplot as plt

# Import the control dataset to act as a reference for latitude and longitude values
base_dir = '/home/links/jf731/isca_data/'
file_list = [f'{base_dir}grey_mars_mk36_per_value70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(0,240)]
resolution_file = xar.open_dataset(file_list[239], decode_times=False)

# Calculate grid values
lons = resolution_file['lon']
lats = resolution_file['lat']

latb_temp=np.zeros(lats.shape[0]+1)

for tick in np.arange(1,lats.shape[0]):
    latb_temp[tick]=(lats[tick-1]+lats[tick])/2.

lonb_temp=np.zeros(lons.shape[0]+1)

for tick in np.arange(1,lons.shape[0]):
    lonb_temp[tick]=(lons[tick-1]+lons[tick])/2.

latb_temp[0]=-90.
latb_temp[-1]=90.

lonb_temp[0]=0.
lonb_temp[-1]=360.

latbs=latb_temp
lonbs=lonb_temp

nlon=lons.shape[0]
nlat=lats.shape[0]

nlonb=len(lonbs)
nlatb=latbs.shape[0]

p_full = resolution_file['pfull']

p_half = resolution_file['phalf']

time_arr = resolution_file['time'].values

nphalf = p_half.shape[0] 

heating_rate = np.zeros((nphalf, nlat, nlon))

# Define the heating rate
# mu and sigma values are the mean and standard deviation for the regional storm. Change these to model a local storm.
for z in range(nphalf):
    for y in range(nlat):
        for x in range(nlon):

            #longitude center of storm
            mu=180
            #half longitude grid spaces of storm
            sigma=5*360/128
            dist=1/(sigma*np.sqrt(2*np.pi))*np.exp(-(lons.values-mu)**2/(2*sigma**2))
            heating_rate[z][y][x]=dist[x]
  
        #latitude center of storm  
        mu=19
        #half latitude grid spaces of storm
        sigma=5*360/128
        dist=1/(sigma*np.sqrt(2*np.pi))*np.exp(-(lats.values-mu)**2/(2*sigma**2))
        heating_rate[z][y]=dist[y]*heating_rate[z][y]
    
    #altitude of maximum of storm
    mu=6
    #half pressure grid spaces of storm
    sigma=1*6.1/26
    dist=1/(sigma*np.sqrt(2*np.pi))*np.exp(-(p_half.values-mu)**2/(2*sigma**2))
    heating_rate[z]=dist[z]*heating_rate[z]
    
multiplication_factor=18/60/60  # maximum heating rate per second
heating_rate=(heating_rate/np.max(heating_rate))*multiplication_factor

# no time variation
time_arr=None

npfull=p_full.shape[0]
nphalf=p_half.shape[0]

#Output to a netcdf file. 
file_name='heating_rate_no_time.nc'
variable_name='heating_rate'

number_dict={}
number_dict['nlat']=nlat
number_dict['nlon']=nlon
number_dict['nlatb']=nlatb
number_dict['nlonb']=nlonb
number_dict['npfull']=npfull
number_dict['nphalf']=nphalf

time_units = None

cts.output_to_file(heating_rate[...],lats,lons,latbs,lonbs,p_full,p_half,time_arr,time_units,file_name,variable_name,number_dict, on_half_levels=True)
