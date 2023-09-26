print('INITIALISING')

import xarray as xar
import numpy as np
from plotting_function import plotting_function
print('Packages Installed')

### LOAD DATA

base_dir = '/home/links/jf731/'

control_file_list= [f'{base_dir}/isca_data/grey_mars_mk36_per_value70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(0,240)]
control_dataset = xar.open_mfdataset(control_file_list, decode_times=False)
control_dataset['mars_solar_long'] = control_dataset['mars_solar_long'].squeeze()
print('data loaded - control')

storm_name='mk19'
storm_file_list = [f'{base_dir}/isca_data/dust_storm_{storm_name}_70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(240,479)]
storm_dataset = xar.open_mfdataset(storm_file_list, decode_times=False)
storm_dataset['mars_solar_long'] = storm_dataset['mars_solar_long'].squeeze()
print('data loaded - storm')

reanalysis_type='back'
reanalysis_year='26'
reanalysis_ls='240-270'
not_bg=True
if not_bg: ground_suffix='_not_bg'
else: ground_suffix='_new_regrid'
reanalysis_file=f'{base_dir}/emars_data/emars_v1.0_{reanalysis_type}_mean_MY{reanalysis_year}_Ls{reanalysis_ls}_interp{ground_suffix}.nc'
reanalysis_dataset = xar.open_dataset(reanalysis_file)
print('data loaded - reanalysis')

topography_file=f'{base_dir}/emars_data/t42_mola_mars.nc'
topography_dataset = xar.open_dataset(topography_file)
print('data loaded - topography')

### PLOTTING

plotting_function(dataset=control_dataset, x='lat', y='pfull', variable='omega', experiment='control', average=True,
       streamfunction=True, season='summer',
       cbar_min=-0.004, cbar_max=0.004)
