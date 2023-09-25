# Postgraduate-Dissertation-Files

## Introduction
The files contained here were written for my postgraduate dissertation, analysing the effects local heating phenomena have on wind profiles using an atmospheric model bult using ISCA. Files running the atmospheric model not included in this repository and belong to the University of Exeter.

## Versions
Python files here were witten in Python 3.11.

## Running
These files are not inted to be ran in isolation, most require netcdf data files created using the ISCA model or downloaded from the EMARS data repository https://www.datacommons.psu.edu/download/meteorology/greybush/emars-1p0/data/. EMARS data must be interpolated onto pressure levels, done using plevel_interpolation.py and plevel_fun.py. Zonally-symmetric and zonally-dependedent streamfunctions are calculated using streamfunction_vars.py, and can be applied to netcdf data files. 
