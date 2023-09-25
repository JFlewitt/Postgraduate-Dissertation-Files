import xarray as xar
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp
import pdb
import windspharm.xarray as windsp
from streamfunction_vars import merid_sf, regional_hadley_cell

### LOAD DATA
base_dir = '/home/links/jf731/'

control_file_list= [f'{base_dir}/isca_data/grey_mars_mk36_per_value70.85_none_mld_2.0/run{runval+1:04d}/atmos_daily.nc' for runval in range(0,240)]
control_dataset = xar.open_mfdataset(control_file_list, decode_times=False)
control_dataset['mars_solar_long'] = control_dataset['mars_solar_long'].squeeze()

topography_file=f'{base_dir}/emars_data/t42_mola_mars.nc'
topography_dataset = xar.open_dataset(topography_file)

### DICTIONARIES

units={'ucomp'  : 'm/s'       ,
       'vcomp'  : 'm/s'       ,
       'temp'   : 'K'         ,
       'omega'  : 'Pa/s'      ,
       'height' : 'm'         ,
       'U'      : 'm/s'       ,
       'V'      : 'm/s'       ,
       'T'      : 'K'         ,
       'ps'     : 'Pa'        ,
       'u'      : 'm/s'       ,
       'v'      : 'm/s'       ,
       't'      : 'K'         ,
       'omega'  : 'Pa/s'      ,
       'dod'    : 'Unitless'  ,
       'tod'    : 'Unitless'  ,
       'hrad'   : 'K/s'       ,
       'o1'     : 'kg/kg'     ,
       'o2'     : 'kg/kg'     ,
       'o3'     : 'kg/kg'     ,
       'lat'    : 'Degrees N' ,
       'lon'    : 'Degrees E' ,
       'pfull'  : 'hPa'
       }

long_name={'ucomp'  : 'Zonal Wind'                  ,
           'vcomp'  : 'Meridional Wind'             ,
           'temp'   : 'Temperature'                 ,
           'omega'  : 'Vertical Wind'               ,
           'height' : 'Geopotential Height'         ,
           'U'      : 'Zonal Wind'                  ,
           'V'      : 'Meridional Wind'             ,
           'T'      : 'Temperature'                 ,
           'ps'     : 'Surface Pressure'            ,
           'u'      : 'Zonal Wind'                  ,
           'v'      : 'Merisional Wind'             ,
           't'      : 'Temperature'                 ,
           'omega'  : 'Vertical Wind'               ,
           'dod'    : 'Column Dust Visible Opacity' ,
           'tod'    : 'Target Dust Visible Opacity' ,
           'hrad'   : 'Radiative Heating Rate'      ,
           'o1'     : '0.3 micro m Dust Mass Mixing Ratio',
           'o2'     : '1.2 micro m Dust Mass Mixing Ratio',
           'o3'     : '2.5 micro m Dust Mass Mixing Ratio',
           'lat'    : 'Latitude'                    ,
           'lon'    : 'Longitude'                   ,
           'pfull'  : 'Pressure'
           }

long_storm_name={'mk5':'18K/hr Midlatitude Storm',
                 'mk6':'9K/hr Midlatitude Storm',
                 'mk7':'4.5K/hr Midlatitude Storm',
                 'mk9':'4.5K/hr Equatorial Storm',
                 'mk10':'13.5K/hr Midlatitude Storm',
                 'mk11':'18K/hr Equatorial Storm',
                 'mk12':'22.5K/hr Midlatitude Storm',
                 'mk13':'2.25K/hr Midlatitude Storm',
                 'mk14':'2.25K/hr Equatorial Storm',
                 'mk15':'9K/hr Equatorial Storm',
                 'mk16':'13.5K/hr Equatorial Storm',
                 'mk17':'22.5K/hr Equatorial Storm',
                 'mk18':'1K/hr Regional Storm',
                 'mk19':'18K/hr Regional Storm'
                 }


season_longitudes={'spring_min':315.0,
                   'spring_max':45.0,
                   'summer_min':45.0,
                   'summer_max':135.0,
                   'autumn_min':135.0,
                   'autumn_max':225.0,
                   'winter_min':225.0,
                   'winter_max':315.0,
                   'year_max'  :360.0,
                   'year_min'  :0.0
                   }

cmaps={'ucomp' : 'RdBu_r',
       'vcomp' : 'RdBu_r',
       'temp'  : 'Reds',
       'omega' : 'RdBu',
       'height': 'Reds',
       'ucomp_diff' : 'PuOr_r' ,
       'vcomp_diff' : 'PuOr_r' ,
       'temp_diff'  : 'PuOr_r' ,
       'omega_diff' : 'PuOr'   ,
       'height_diff': 'PuOr_r' ,
       'temp_alt'  : 'PiYG_r' ,
       'omega_alt' : 'PiYG'   ,
       'U'     : 'RdBu_r'  ,
       'V'     : 'RdBu_r'  ,
       'T'     : 'Reds'    ,
       'ps'    : 'terrain_r' ,
       'u'     : 'RdBu_r'  ,
       'v'     : 'RdBu_r'  ,
       't'     : 'Reds'    ,
       'omega' : 'RdBu'    ,
       'dod'   : 'Reds'    ,
       'tod'   : 'Reds'    ,
       'hrad'  : 'RdBu_r'  ,
       'o1'    : 'Reds'    ,
       'o2'    : 'Reds'    ,
       'o3'    : 'Reds'    ,
       'U_diff'     : 'PuOr_r'  ,
       'V_diff'     : 'PuOr_r'  ,
       'T_diff'     : 'PuOr_r'  ,
       'ps_diff'    : 'PuOr_r'  ,
       'u_diff'     : 'PuOr_r'  ,
       'v_diff'     : 'PuOr_r'  ,
       't_diff'     : 'PuOr_r'  ,
       'omega_diff' : 'PuOr'    ,
       'dod_diff'   : 'PuOr_r'  ,
       'tod_diff'   : 'PuOr_r'  ,
       'hrad_diff'  : 'PuOr_r'  ,
       'o1_diff'    : 'PuOr_r'  ,  
       'o2_diff'    : 'PuOr_r'  ,  
       'o3_diff'    : 'PuOr_r'  ,  
       }

no_pressure_list=['dod','tod','ps']

### DEFINE FUNCTION 

def plotting_function(dataset, x, y, variable, experiment, average=False, 
                      choose_lat=0, choose_lon=180, choose_pressure=4.45, choose_day=None, choose_ls=None, choose_sol=None,
                      storm_name=None, reanalysis_type='back', reanalysis_year=None, reanalysis_ls=None,
                      topography=False, streamfunction=False, significance=False, season='winter', difference=False,
                      cbar_min=None, cbar_max=None, r_time_av=False, not_bg=True, 
                      ymin=None, ymax=None, xmin=None, xmax=None, alt_colours=False):
    
    test=dataset.sel(lat=choose_lat, method='nearest')
    old_lat=choose_lat
    choose_lat=np.round(float((test.lat)),2)
    print(f'Longitude adjusted by {np.round(choose_lat-old_lat,2)}N')

    test=dataset.sel(lon=choose_lon, method='nearest')
    old_lon=choose_lon
    choose_lon=np.round(float((test.lon)),2)
    print(f'Latitude adjusted by {np.round(choose_lon-old_lon,2)}E')

    test=dataset.sel(pfull=choose_pressure, method='nearest')
    old_pressure=choose_pressure
    choose_pressure=np.round(float((test.pfull)),2)
    print(f'Pressure adjusted by {np.round(choose_pressure-old_pressure,2)}hPa')

    if experiment=='control':
        dataset=dataset.where(dataset.time>1*670,drop=True)
        print('Spin-up time removed')

    if experiment=='control' or experiment=='dust':
        dataset=dataset.where((dataset.mars_solar_long>season_longitudes[f'{season}_min']) & (dataset.mars_solar_long<season_longitudes[f'{season}_max']), drop=True)
        print('Season isolated')

    if experiment=='dust':
        if significance:        
            stats_data_exp = dataset[variable]

    if experiment=='reanalysis':
        if significance:
            stats_data_ctrl = dataset[variable]
        #if not_bg:
        reference_reanalysis_file=f'{base_dir}/emars_data/emars_v1.0_{reanalysis_type}_mean_MY{reanalysis_year}_Ls{reanalysis_ls}.nc'
        reference_reanalysis_dataset = xar.open_dataset(reference_reanalysis_file)
        dataset['time'] = ('time', reference_reanalysis_dataset['time'].values)
        if difference==False and r_time_av==False:
            dataset=dataset.where(reference_reanalysis_dataset.Ls<choose_ls+1, drop=True).where(reference_reanalysis_dataset.Ls>choose_ls-1, drop=True)
        
    title=''
    fig_title=''

    plt.figure()
    
    if variable not in no_pressure_list:
        if y=='pfull':
            if average:
                if x=='lat': 
                    var_data     = dataset[variable].mean('time').mean('lon')
                    location     = ', longitudinal mean'
                    fig_location = '_long_mean'
                if x=='lon': 
                    var_data     = dataset[variable].mean('time').mean('lat')
                    location     = ', latitudinal mean'
                    fig_location = '_lat_mean'
            else:
                if x=='lat': 
                    var_data     = dataset[variable].mean('time').sel(lon=choose_lon, method='nearest')
                    location     = f', longitude = {choose_lon}E'
                    fig_location = f'_long_slice_{choose_lon}E'
                if x=='lon': 
                    var_data     = dataset[variable].mean('time').sel(lat=choose_lat, method='nearest')
                    location     = f', latitude = {choose_lat}N'
                    fig_location = f'_lat_slice_{choose_lat}N'

        if y=='lat':
            var_data     = dataset[variable].mean('time').sel(pfull=choose_pressure, method='nearest')  
            location     = f', pressure = {choose_pressure}hPa'
            fig_location = f'_pressure_slice_{choose_pressure}hPa'

    if variable in no_pressure_list:
        if y=='lat':
            var_data     = dataset[variable].mean('time')
            location     = f', pressure average'
            fig_location = f'_pressure_average'
    print('Variable data selected')


    if experiment=='reanalysis':
        
        #diff_dataset=dataset.where(reference_reanalysis_dataset.Ls<choose_ls+1).where(reference_reanalysis_dataset.Ls>choose_ls-1)
        #diff_dataset=dataset.where(dataset.mars_soy<=choose_sol+1).where(dataset.mars_soy>=choose_sol-1)
        if significance:
            stats_data_exp=diff_dataset[variable]

        if difference:
            if variable not in no_pressure_list:
                if y=='pfull':
                    if average:
                        if x=='lat':
                            storm_data   = diff_dataset[variable].mean('time').mean('lon')
                        if x=='lon': 
                            storm_data   = diff_dataset[variable].mean('time').mean('lat')
                    else:
                        if x=='lat':
                            storm_data   = diff_dataset[variable].mean('time').sel(lon=choose_lon, method='nearest')
                        if x=='lon': 
                            storm_data   = diff_dataset[variable].mean('time').sel(lat=choose_lat, method='nearest')
                
                if y=='lat':
                    storm_data   = diff_dataset[variable].mean('time').mean('lon').sel(pfull=choose_pressure, method='nearest')

            if variable in no_pressure_list:
                storm_data   = diff_dataset[variable].mean('time')

            var_difference   = storm_data - var_data
            print('Difference data calculated')

            title=title+f'EMARS data : Change in {variable}, MY = {reanalysis_year}, Ls = {reanalysis_ls}'
            fig_title=fig_title+f'EMARS_data_difference_{variable}_MY{reanalysis_year}_Ls{reanalysis_ls}'
        
        elif r_time_av:
            title=title+f'EMARS data : {variable}, MY = {reanalysis_year}, Ls = {reanalysis_ls}'
            fig_title=fig_title+f'EMARS_data_{variable}_MY{reanalysis_year}_Ls{reanalysis_ls}'
        else:
            title=title+f'EMARS data : {variable}, MY = {reanalysis_year}, Ls = {choose_ls}'
            fig_title=fig_title+f'EMARS_data_{variable}_MY{reanalysis_year}_Ls{choose_ls}'

    if experiment=='control':
        title=title+f'no dust storm : {variable}, {season} average'
        fig_title=fig_title+f'no_dust_{variable}_{season}'
    
    if experiment=='dust':
        diff_dataset=control_dataset.where(control_dataset.time>1*670,drop=True)
        diff_dataset=diff_dataset.where((diff_dataset.mars_solar_long>season_longitudes[f'{season}_min']) & (diff_dataset.mars_solar_long<season_longitudes[f'{season}_max']), drop=True)
        
        if significance:
            stats_data_ctrl = diff_dataset[variable]

        if difference:
            if y=='pfull':
                if average:
                    if x=='lat':
                        control_data   = diff_dataset[variable].mean('time').mean('lon')
                    if x=='lon': 
                        control_data   = diff_dataset[variable].mean('time').mean('lat')
                else:
                    if x=='lat':
                        control_data   = diff_dataset[variable].mean('time').sel(lon=choose_lon, method='nearest')
                    if x=='lon': 
                        control_data   = diff_dataset[variable].mean('time').sel(lat=choose_lat, method='nearest')
            
            if y=='lat':
                control_data   = diff_dataset[variable].mean('time').mean('lon').sel(pfull=choose_pressure, method='nearest')

            var_difference   =  var_data - control_data
            print('Difference data calculated')

            title=title+f'{long_storm_name[storm_name]} : Change in {variable}, {season} average'
            fig_title=fig_title+f'{storm_name}_difference_{variable}_{season}'
        else:
            title=title+f'{long_storm_name[storm_name]} : {variable}, {season} average'
            fig_title=fig_title+f'{storm_name}_dust_{variable}_{season}'
        
    if difference:
        xar.plot.contourf(var_difference,add_colorbar=True,levels=30,cmap=cmaps[f'{variable}_diff'],cbar_kwargs={'label': f'{long_name[variable]} ({units[variable]})'},vmin=cbar_min,vmax=cbar_max)
    elif alt_colours: 
        xar.plot.contourf(var_data,add_colorbar=True,levels=30,cmap=cmaps[f'{variable}_alt'],cbar_kwargs={'label': f'{long_name[variable]} ({units[variable]})'},vmin=cbar_min,vmax=cbar_max)
    else:
        xar.plot.contourf(var_data,add_colorbar=True,levels=30,cmap=cmaps[f'{variable}'],cbar_kwargs={'label': f'{long_name[variable]} ({units[variable]})'},vmin=cbar_min,vmax=cbar_max)


    print('Data plotted')

    if y=='lat':
        if topography:
            xar.plot.contour(topography_dataset['zsurf'],colors='black',levels=3)

    title=title+location
    fig_title=fig_title+fig_location

    if significance:
        tvals,pvals=sp.stats.ttest_ind(stats_data_exp,stats_data_ctrl,equal_var=False)

        if variable in no_pressure_list:
            dataset['pvals']=(['lat','lon'],pvals)
        else:
            dataset['pvals']=(['pfull','lat','lon'],pvals)

        pvals=dataset['pvals']

        if y=='lat':
            if variable not in no_pressure_list:
                pvals = pvals.sel(pfull=choose_pressure, method='nearest')
        if y=='pfull':
            if x=='lat':
                pvals = pvals.sel(lon=choose_lon, method='nearest')
            if x=='lon':
                pvals = pvals.sel(lat=choose_lat, method='nearest')

        xar.plot.contourf(pvals,add_colorbar=False,levels=np.array([0.0,0.05]),hatches=['//',''],colors='none')
        xar.plot.contour(pvals,add_colorbar=False,levels=np.array([0.05]),colors='grey')
        fig_title=fig_title+'_&_sig'

        print('Significance hatches added')

    if streamfunction:

        if (dataset.lat.values)[0] < 0: 
            dataset = dataset.reindex(lat=dataset.lat[::-1])

        if experiment=='control' or experiment=='dust':
            vec_wind = windsp.VectorWind(dataset['ucomp'], dataset['vcomp'])
        if experiment=='reanalysis':
            if reanalysis_type=='back':
                vec_wind = windsp.VectorWind(dataset['u'], dataset['v'])
            if reanalysis_type=='anal':
                vec_wind = windsp.VectorWind(dataset['U'], dataset['V'])

        uchi, vchi, upsi, vpsi = vec_wind.helmholtz()

        dataset['u_divergent'] = (uchi.dims, uchi.values)
        dataset['v_divergent'] = (vchi.dims, vchi.values)

        dataset['u_rot'] = (upsi.dims, upsi.values)
        dataset['v_rot'] = (vpsi.dims, vpsi.values)

        print('helmholtz data calculated')

        if experiment=='reanalysis':
            if reanalysis_type=='back':
                merid_sf(dataset,vcomp_var='v')
                regional_hadley_cell(dataset)
            if reanalysis_type=='mean':
                merid_sf(dataset,vcomp_var='V')
                regional_hadley_cell(dataset)
        else:
            merid_sf(dataset)
            regional_hadley_cell(dataset)

        print('hadley cells calculated')

        if y=='pfull':
            if average:
                sf_data = dataset['merid_sf_trap_rule'].mean('time')
            elif x=='lat':
                sf_data = dataset['merid_sf_v_div'].mean('time').sel(lon=choose_lon, method='nearest')
            elif x=='lon':
                sf_data = dataset['merid_sf_v_div'].mean('time').sel(lat=choose_lat, method='nearest')

        if y=='lat':
            sf_data = dataset['merid_sf_v_div'].mean('time').sel(pfull=choose_pressure, method='nearest')

        if difference:

            if (diff_dataset.lat.values)[0] < 0: 
                diff_dataset = diff_dataset.reindex(lat=diff_dataset.lat[::-1])

            if experiment=='control' or experiment=='dust':
                vec_wind = windsp.VectorWind(diff_dataset['ucomp'], diff_dataset['vcomp'])
            if experiment=='reanalysis':
                if reanalysis_type=='back':
                    vec_wind = windsp.VectorWind(diff_dataset['u'], diff_dataset['v'])
                if reanalysis_type=='anal':
                    vec_wind = windsp.VectorWind(diff_dataset['U'], diff_dataset['V'])

            uchi, vchi, upsi, vpsi = vec_wind.helmholtz()

            diff_dataset['u_divergent'] = (uchi.dims, uchi.values)
            diff_dataset['v_divergent'] = (vchi.dims, vchi.values)

            diff_dataset['u_rot'] = (upsi.dims, upsi.values)
            diff_dataset['v_rot'] = (vpsi.dims, vpsi.values)

            print('helmholtz data calculated - difference')

            if experiment=='reanalysis':
                if reanalysis_type=='back':
                    merid_sf(diff_dataset,vcomp_var='v')
                    regional_hadley_cell(diff_dataset)
                if reanalysis_type=='mean':
                    merid_sf(diff_dataset,vcomp_var='V')
                    regional_hadley_cell(diff_dataset)
            else:
                merid_sf(diff_dataset)
                regional_hadley_cell(diff_dataset)

            print('hadley cells calculated - difference')

            if y=='pfull':
                if average:
                    sf_data_storm = diff_dataset['merid_sf_trap_rule'].mean('time')
                elif x=='lat':
                    sf_data_storm = diff_dataset['merid_sf_v_div'].mean('time').sel(lon=choose_lon, method='nearest')
                elif x=='lon':
                    sf_data_storm = diff_dataset['merid_sf_v_div'].mean('time').sel(lat=choose_lat, method='nearest')

            if y=='lat':
                sf_data_storm = diff_dataset['merid_sf_v_div'].mean('time').sel(pfull=choose_pressure, method='nearest')

            if experiment=='reanalysis':
                sf_difference = sf_data_storm - sf_data
            if experiment=='dust':
                sf_difference = sf_data - sf_data_storm
            sf_difference = sf_difference/1000000000

            sf_plot=xar.plot.contour(sf_difference,levels=15,colors='brown')
            plt.clabel(sf_plot, inline=1, fontsize=6)

        else:
            sf_data = sf_data/1000000000
            sf_plot=xar.plot.contour(sf_data,levels=15,colors='black')
            plt.clabel(sf_plot, inline=1, fontsize=6)

        print('Streamfunction plotted')
        fig_title=fig_title+'_&_sf'

    if experiment=='dust' or experiment=='reanalysis':
        if y=='lat':
            plt.axvline(x=old_lon,color='grey',linestyle='--')
            plt.axhline(y=old_lat,color='grey',linestyle='--')
            plt.plot(old_lon,old_lat,color='lime',marker='*')

        if y=='pfull':
            if x=='lat':
                plt.axvline(x=old_lat,color='grey',linestyle='--')
            if x=='lon':
                plt.axvline(x=old_lon,color='grey',linestyle='--')

    if experiment=='reanalysis':
        if not_bg:
            fig_title=fig_title+'_no_bg'

    if alt_colours:
        fig_title=fig_title+'_alt_colours'

    if y=='pfull':
        plt.gca().invert_yaxis()

    plt.ylim(ymin,ymax)
    plt.xlim(xmin,xmax)
    plt.xlabel(f'{long_name[x]} ({units[x]})')
    plt.ylabel(f'{long_name[y]} ({units[y]})')
    plt.title(title,fontsize=8)
    plt.savefig(fig_title+f'.pdf')
    plt.close()
    print(fig_title+f'.pdf plotted')
