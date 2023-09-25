import numpy as np
import xarray as xar

choose_lon=180
choose_pressure=4.45

storm_heating_rate={'mk12'  :22.5 ,
                    'mk5'   :18   ,
                    'mk10'  :13.5 ,
                    'mk6'   :9    ,
                    'mk7'   :4.5  ,
                    'mk13'  :2.25 ,
                    'mk17'  :22.5 ,
                    'mk11'  :18   ,
                    'mk16'  :13.5 ,
                    'mk15'  :9    ,
                    'mk9'   :4.5  ,
                    'mk14'  :2.25 
                    }

storm_lat={'mk12'  :38 ,
           'mk5'   :38 ,
           'mk10'  :38 ,
           'mk6'   :38 ,
           'mk7'   :38 ,
           'mk13'  :38 ,
           'mk17'  :0  ,
           'mk11'  :0  ,
           'mk16'  :0  ,
           'mk15'  :0  ,
           'mk9'   :0  ,
           'mk14'  :0
           }

base_dir = '/home/links/jf731/isca_data/'

# no dust data
no_dust_file_list = [f'{base_dir}grey_mars_mk36_per_value70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(0,240)]
no_dust_dataset = xar.open_mfdataset(no_dust_file_list, decode_times=False)
no_dust_dataset['mars_solar_long'] = no_dust_dataset['mars_solar_long'].squeeze()
print('data loaded - no dust')

storage={'mk12'  :0 ,
         'mk5'   :0 ,
         'mk10'  :0 ,
         'mk6'   :0 ,
         'mk7'   :0 ,
         'mk13'  :0 ,
         'mk17'  :0 ,
         'mk11'  :0 ,
         'mk16'  :0 ,
         'mk15'  :0 ,
         'mk9'   :0 ,
         'mk14'  :0
        }

# Size comparison
plt.figure()

for storm_name in storm_heating_rate.items():
    #Load data
    file_list = [f'{base_dir}dust_storm_{storm_name[0]}_70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(240,479)]
    dataset = xar.open_mfdataset(file_list, decode_times=False)
    dataset['mars_solar_long'] = dataset['mars_solar_long'].squeeze()
    print(f'data loaded - {storm_name[0]} dust')

    test=dataset.sel(lon=choose_lon, method='nearest')
    old_lon=choose_lon
    choose_lon=np.round(float((test.lon)),2)

    test=dataset.sel(pfull=choose_pressure, method='nearest')
    old_pressure=choose_pressure
    choose_pressure=np.round(float((test.pfull)),2)

 
    dust_av = dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lon=choose_lon, method='nearest')
    no_dust_av = no_dust_dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lon=choose_lon, method='nearest')
    av_difference = dust_av - no_dust_av

    storage[f'{storm_name[0]}']=np.min(av_difference)
    label=f'{storm_lat[storm_name[0]]}N storm, heating rate = {storm_heating_rate[storm_name[0]]} K/s'
    if storm_lat[storm_name[0]]==0: linestyle='dotted'
    if storm_lat[storm_name[0]]==38: linestyle='dashed'
    av_difference.plot(x='lat', label=label, linestyle=linestyle)
        
    plt.gca().invert_yaxis()
    plt.legend(fontsize='x-small')
    plt.title(f'Change in omega in response to 38N & 0N storm',fontsize=10)
    plt.xlabel('Latitude (Degrees N)')
    plt.ylabel('Vertical Wind (Pa/s)')
    plt.savefig(f'change_in_omega_38N_&_0N_storm_response_lon_{choose_lon}E_pressure_{choose_pressure}hPa.pdf')
    plt.close()
    print(f'change_in_omega_38N_&_0N_storm_response_lon_{choose_lon}E_pressure_{choose_pressure}hPa.pdf plotted')

# Shape comparison (normalisation)
#pressure-longitude
plt.figure()

for storm_name in storm_heating_rate.items():
    #Load data
    file_list = [f'{base_dir}dust_storm_{storm_name[0]}_70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(240,479)]
    dataset = xar.open_mfdataset(file_list, decode_times=False)
    dataset['mars_solar_long'] = dataset['mars_solar_long'].squeeze()
    print(f'data loaded - {storm_name[0]} dust')

    choose_lat=storm_lat[storm_name[0]]
    test=dataset.sel(lat=choose_lat, method='nearest')
    old_lat=choose_lat
    choose_lat=np.round(float((test.lat)),2)

    test=dataset.sel(lon=choose_lon, method='nearest')
    old_lon=choose_lon
    choose_lon=np.round(float((test.lon)),2)

    test=dataset.sel(pfull=choose_pressure, method='nearest')
    old_pressure=choose_pressure
    choose_pressure=np.round(float((test.pfull)),2)
  
    dust_av = dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lat=choose_lat, method='nearest')
    no_dust_av = no_dust_dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lat=choose_lat, method='nearest')
    av_difference = dust_av - no_dust_av

    storage[f'{storm_name[0]}']=np.min(av_difference)
    av_difference=av_difference/np.min(av_difference)
    label=f'{storm_lat[storm_name[0]]}N storm, heating rate = {storm_heating_rate[storm_name[0]]} K/s'
    if storm_lat[storm_name[0]]==0: linestyle='dotted'
    if storm_lat[storm_name[0]]==38: linestyle='dashed'
    av_difference.plot(x='lon', label=label, linestyle=linestyle)
  
    plt.legend(fontsize='x-small')
    plt.title(f'Normalised change in omega in response to 38N & 0N storm',fontsize=10)
    plt.xlabel('Longitude (Degrees E)')
    plt.ylabel('Vertical Wind (Pa/s)')
    plt.savefig(f'normalised_change_in_omega_38N_&_0N_storm_response_storm_lat_pressure_{choose_pressure}hPa.pdf')
    print(f'normalised_change_in_omega_38N_&_0N_storm_response_storm_lat_pressure_{choose_pressure}hPa.pdf plotted')
    plt.close()

#pressure-latitude
plt.figure()

for storm_name in storm_heating_rate.items():
    #Load data
    file_list = [f'{base_dir}dust_storm_{storm_name[0]}_70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(240,479)]
    dataset = xar.open_mfdataset(file_list, decode_times=False)
    dataset['mars_solar_long'] = dataset['mars_solar_long'].squeeze()
    print(f'data loaded - {storm_name[0]} dust')

    test=dataset.sel(lon=choose_lon, method='nearest')
    old_lon=choose_lon
    choose_lon=np.round(float((test.lon)),2)

    test=dataset.sel(pfull=choose_pressure, method='nearest')
    old_pressure=choose_pressure
    choose_pressure=np.round(float((test.pfull)),2)
 
    dust_av = dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lon=choose_lon, method='nearest')
    no_dust_av = no_dust_dataset['omega'].mean('time').sel(pfull=choose_pressure, method='nearest').sel(lon=choose_lon, method='nearest')
    av_difference = dust_av - no_dust_av

    storage[f'{storm_name[0]}']=np.min(av_difference)
    av_difference=av_difference/np.min(av_difference)
    label=f'{storm_lat[storm_name[0]]}N storm, heating rate = {storm_heating_rate[storm_name[0]]} K/s'
    if storm_lat[storm_name[0]]==0: linestyle='dotted'
    if storm_lat[storm_name[0]]==38: linestyle='dashed'
    av_difference.plot(x='lat', label=label, linestyle=linestyle)

    plt.legend(fontsize='x-small')
    plt.title(f'Normalised change in omega in response to 38N & 0N storm',fontsize=10)
    plt.xlabel('Latitude (Degrees N)')
    plt.ylabel('Vertical Wind (Pa/s)')
    plt.savefig(f'normalised_change_in_omega_38N_&_0N_storm_response_lon_{choose_lon}E_pressure_{choose_pressure}hPa.pdf')
    print(f'normalised_change_in_omega_38N_&_0N_storm_response_lon_{choose_lon}E_pressure_{choose_pressure}hPa.pdf plotted')
    plt.close()

# Maximum trend
heating_rate_0N=[]
heating_rate_38N=[]
values_0N=[]
values_38N=[]

for storm_name in storm_heating_rate.items(): 
    if storm_lat[storm_name[0]]==0:
        heating_rate_0N.append(storm_heating_rate[f'{storm_name[0]}'])
        values_0N.append(storage[f'{storm_name[0]}'])
    if storm_lat[storm_name[0]]==38:    
        heating_rate_38N.append(storm_heating_rate[f'{storm_name[0]}'])
        values_38N.append(storage[f'{storm_name[0]}'])

    plt.figure()
    plt.plot(heating_rate_0N,values_0N,linestyle='dotted',marker='o',label='0N storm')
    plt.plot(heating_rate_38N,values_38N,linestyle='dashed',marker='o',label='38N storm')
    plt.legend()
    plt.xlabel('Heating Rate K/s')
    plt.ylabel(f'Maximum change in omega Pa/s')
    plt.gca().invert_yaxis()
    plt.minorticks_on()
    plt.grid()
    plt.title(f'Maximum change in omega in response to varying strength storms at 38N & 0N',fontsize=10)
    plt.savefig(f'maximum_omega_change_with_38N_&_0N_storm_strength.pdf')
    print(f'maximum_omega_change_with_38N_&_0N_storm_strength.pdf plotted')
    plt.close()         
            
