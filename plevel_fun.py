def plevel_call(nc_file_in,nc_file_out, var_names = '-a', p_levels='default', mask_below_surface_option=' ', add_back_scalar_axis_vars=True):

    check_gfdl_directories_set()

    interper = './plevel.sh'
    nc_file = ' -i '+nc_file_in
    out_file = ' -o '+nc_file_out
    if p_levels == 'model':
        plev = ' -p "2 9 18 38 71 125 206 319 471 665 904 1193 1532 1925 2375 2886 3464 4115 4850 5679 6615 7675 8877 10244 11801 13577 15607 17928 20585 23630 27119 31121 35711 40976 47016 53946 61898 71022 81491 93503" '
        command = interper + nc_file + out_file + plev + var_names
    elif p_levels=='default':
        command = interper + nc_file + out_file + ' ' + var_names
    else:
        plev=p_levels
        command = interper + nc_file + out_file + plev +' '+mask_below_surface_option+ var_names
    print(command)
    subprocess.call([command], shell=True)
    
    if add_back_scalar_axis_vars:
        add_back_scalar_axis_vars_fn(nc_file_in, nc_file_out)

def add_back_scalar_axis_vars_fn(file_in, file_out):

    ds_in = xar.open_dataset(file_in, decode_times=False)
    ds_out = xar.open_dataset(file_out, decode_times=False)    
    
    try:
        ds_in.dims['scalar_axis']
    except KeyError:
        return  

    list_of_vars_to_copy=[]

    for name in ds_in.var().keys():
        if 'scalar_axis' in ds_in[name].dims and name not in ds_out.var().keys():
            list_of_vars_to_copy.append(name)
    
    ds_out.coords['scalar_axis'] = ('scalar_axis', ds_in['scalar_axis'].values)
    
    for out_name in list_of_vars_to_copy:
        ds_out[out_name] = (ds_in[out_name].dims, ds_in[out_name].values)
    
    ds_out.to_netcdf(path=file_out)    
