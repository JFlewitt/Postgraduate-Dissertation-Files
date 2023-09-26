# Postgraduate-Dissertation-Files

## Introduction
The files contained here were written for my postgraduate dissertation, analysing the effects local heating phenomena have on wind profiles using an atmospheric model bult using ISCA. Files running the atmospheric model not included in this repository and belong to the University of Exeter.

## Versions
Python files here were witten in Python 3.11.

## Running
These files are not inted to be ran in isolation, most require netcdf data files created using the ISCA model or downloaded from the EMARS data repository https://www.datacommons.psu.edu/download/meteorology/greybush/emars-1p0/data/. EMARS data must be interpolated onto pressure levels, done using plevel_interpolation.py and plevel_fun.py. Zonally-symmetric and zonally-dependedent streamfunctions are calculated using streamfunction_vars.py, and can be applied to netcdf data files. 

## File List
create_local_heating_input_file.py - Creates an input file which mimics a martian dust storm. Utilises a reference dataset to set the resolution of the atmospheric grid, then a normally distributed heating rate input is defined at a given location. 
<br/>
plevel_interpolation.py - Converts EMARS data files to a pressure coordinate system, with the option of having no data for below surface level, or for masking below surface data to create a file with no missing values (this is essential for calculating the Helmholtz decomposition for zonally-dependent streamfunctions). This uses plevel_fun.py.
<br/>
plotting_function.py - An all-encompassing function to create a map of EMARS reanalysis data, or data created via the ISCA model. Part of the function can calculate significant changes from a control model, and can plot the difference in any variable compared to a control or reference dataset. A zonally-symmetric meridional overturning streamfunction can be calculated using zonally-averaged data (utilising the merid_sf() function from the streamfunction_vars.py file), and a longitudinally depended Hadley cell can be calculated using global data from some variable (using the regional_hadley_cell() function from the streamfunction_vars.py file).
<br/>
plotting1.py - A file importing data needed for my dissertation and using the plotting function.
<br/>
plotting2.py - A file manipulating large netcdf data files to create spefific plots used for my dissertation.
