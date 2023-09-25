from plevel_fn import plevel_call
import os
import xarray as xar
import numpy as np

def add_pk(nc_file_in_orig, nc_file_pk_sorted, reference_lon, reference_lat, reference_lonb, reference_latb ):
    print(f'sorting pk for {nc_file_in_orig}')
    dataset = xar.open_dataset(nc_file_in_orig, decode_times=False)
    dataset['pk'] = ('phalf', dataset['ak'].values)
    dataset['pk'].attrs = dataset['ak'].attrs

    try:
        lonb = dataset['lonb'].values
    except:
        if np.all(dataset['lon'].values == reference_lon):
            dataset.coords['lonb'] = ('lonb', reference_lonb)
        else:
            raise NotImplementedError('new lon and old lon do not match')
        if np.all(dataset['lat'].values == reference_lat):
            dataset.coords['latb'] = ('latb', reference_latb)            
        else:
            raise NotImplementedError('new lat and old lat do not match')            

    dataset.to_netcdf(nc_file_pk_sorted) 

base_dir='/home/links/jf731/emars_data'
exp_name_list = ['anal', 'back']
avg_or_daily_list=['mars']
# choose the input file to be interpolated
my_value = '31'
ls = '240-270'

level_set='standard' 
mask_below_surface_set='-x ' #if interpolation below ground is wanted, set to '-x'

plevs={}
var_names={}

if level_set=='standard':

    plevs['mars']  =' -p "1 3 6 12 19 30 45 68 99 140 191 250 317 386 454 519 576 625 665 696 721 739 752 761 767" '

    var_names['mars']='-a '

    if '-x' in mask_below_surface_set:
        file_suffix='_interp_new'
    else:
        file_suffix='_interp_not_bg_new'        

files_to_adjust = []
files_to_interpolate = []

reference_file =  xar.open_dataset(f'{base_dir}/emars_v1.0_back_mean_MY26_Ls240-270.nc', decode_times=False)
reference_lon, reference_lat, reference_lonb, reference_latb = reference_file['lon'].values, reference_file['lat'].values, reference_file['lonb'].values, reference_file['latb'].values

for exp_name in exp_name_list:
    print(f'running MY {my_val}')

    for avg_or_daily in avg_or_daily_list:

        nc_file_in_orig = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls}.nc'
        nc_file_pk_sorted = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls}_pk.nc'

        does_file_exist = os.path.isfile(nc_file_in_orig)    
        if does_file_exist:
            if not os.path.isfile(nc_file_pk_sorted):
                add_pk(nc_file_in_orig, nc_file_pk_sorted, reference_lon, reference_lat, reference_lonb, reference_latb )

            nc_file_in = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls}_pk.nc'
            nc_file_out = f'{base_dir}/emars_v1.0_{exp_name}_mean_MY{my_val}_Ls{ls}{file_suffix}.nc'

            if not os.path.isfile(nc_file_out):
                plevel_call(nc_file_in,nc_file_out, var_names = var_names[avg_or_daily], p_levels = plevs[avg_or_daily], mask_below_surface_option=mask_below_surface_set, add_back_scalar_axis_vars=True)
