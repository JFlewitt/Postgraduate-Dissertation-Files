import numpy as np
import xarray as xar

def merid_sf(dataset, a=3390.0e3, g=3.71, start_integration_from_top=True, trap_rule=True, surf_pressure=None, time_var='time', pressure_var='pfull', vcomp_var='vcomp'):
    
    vbar = dataset[vcomp_var].mean(('lon')).load()
    c = 2*np.pi*a*np.cos(vbar.lat*np.pi/180) / g
    if trap_rule:

        c_all_time = np.zeros((len(dataset[time_var]), len(dataset.lat)))

        for t_tick in range(len(dataset[time_var])):
            c_all_time[t_tick,:] = c

        merid_sf_trap_rule = np.zeros_like(vbar)

        if dataset[pressure_var].units=='hPa':
            p_values = dataset[pressure_var].values*100.
        else:
            p_values = dataset[pressure_var].values

        if start_integration_from_top:
            delta_p = (-0. + p_values[0])
            mid_value = (0.+vbar[:,0,:])/2.
            merid_sf_trap_rule[:,0,:] = mid_value * delta_p *c_all_time

            for p_idx in range(1, len(p_values)):
                delta_p = (-p_values[p_idx-1] + p_values[p_idx])
                mid_value = (vbar[:,p_idx-1,:]+vbar[:,p_idx,:])/2.
                merid_sf_trap_rule[:,p_idx,:] = merid_sf_trap_rule[:,p_idx-1,:]+(mid_value*delta_p*c_all_time)
        else:

            delta_p = (surf_pressure - p_values[-1])
            mid_value = (0.+vbar[:,-1,:])/2.
            merid_sf_trap_rule[:,-1,:] = mid_value * delta_p *c_all_time

            for p_idx in range(len(p_values)-1, 0):
                delta_p = -(-p_values[p_idx-1] + p_values[p_idx])
                mid_value = (vbar[:,p_idx-1,:]+vbar[:,p_idx,:])/2.
                merid_sf_trap_rule[:,p_idx,:] = merid_sf_trap_rule[:,p_idx-1,:]+(mid_value*delta_p*c_all_time)

        dataset['merid_sf_trap_rule'] = ((time_var,pressure_var, 'lat'), merid_sf_trap_rule)

        merid_sf_sign = merid_sf_trap_rule / np.abs(merid_sf_trap_rule)

        dataset['log_merid_sf_trap_rule'] = ((time_var,pressure_var, 'lat'), merid_sf_sign*np.log(np.abs(merid_sf_trap_rule)))
        

    else:
        dp=xar.DataArray(dataset.phalf.diff('phalf').values*100, coords=[(pressure_var, dataset.pfull)])
        if start_integration_from_top:
            product = vbar*dp
            product.load()
            merid_sf=c*np.cumsum(product, axis=product.dims.index(pressure_var))
            merid_sf = merid_sf.transpose(time_var,pressure_var,'lat')
            dataset['merid_sf']=(merid_sf.dims,merid_sf)        
        else:
            product = vbar[:,::-1,:]*dp[::-1]
            product.load()
            merid_sf=c*np.cumsum(product, axis=product.dims.index(pressure_var))
            merid_sf = -1.*merid_sf[:,:,::-1]           
            merid_sf = merid_sf.transpose(time_var,pressure_var,'lat')
            dataset['merid_sf_bot']=(merid_sf.dims,merid_sf) 
        
def regional_hadley_cell(dataset, a=3390.0e3, g=3.71, start_integration_from_top=True, trap_rule=True, time_var='time', pressure_var='pfull'):
    
    v_div = dataset['v_divergent']

    c =  2*np.pi*a*np.cos(dataset.lat*np.pi/180) / g

    if trap_rule:

        c_all_time = np.zeros((len(dataset[time_var]), len(dataset.lat), len(dataset.lon)))

        for t_tick in range(len(dataset[time_var])):
            for lon_tick in range(len(dataset['lon'])):
                c_all_time[t_tick,:, lon_tick] = c

        merid_sf_trap_rule = np.zeros_like(v_div)

        if dataset[pressure_var].units=='hPa':
            p_values = dataset[pressure_var].values*100.
        else:
            p_values = dataset[pressure_var].values

        if start_integration_from_top:
            delta_p = (-0. + p_values[0])
            mid_value = (0.+v_div[:,0,...])/2.
            merid_sf_trap_rule[:,0,...] = mid_value * delta_p *c_all_time

            for p_idx in range(1, len(p_values)):
                delta_p = (-p_values[p_idx-1] + p_values[p_idx])
                mid_value = (v_div[:,p_idx-1,...]+v_div[:,p_idx,...])/2.
                merid_sf_trap_rule[:,p_idx,...] = merid_sf_trap_rule[:,p_idx-1,...]+(mid_value*delta_p*c_all_time)    

    dataset['merid_sf_v_div'] = (v_div.dims, merid_sf_trap_rule)
