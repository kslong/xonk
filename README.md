# xonk

This repository contains tools, which are being used by ksl, wpb, and others 
in their attempts to better understand supernova remnants.

To set up everything, one should retrieve the repository:

git clone https://github.com/kslong/xonk.git

Some modifications to paths are required to be able to use the
routines.  

For testing purposes, one may simple source the comand file start_xork

e.g

source start_xonk

If one is planning to use the programs generally, then similar commands 
should be added to one of the login files, e.g .bash_profile.

Note that these commands are somewhat different in the csh and it's affiliates

### Packages needed

Generally, xonk is intended to result in a conda enviroment, usually astroconda, 
in which astropy, numpy, and matpltlib have already been installed.  
but there are a few packages that may be missing

xlwt is a routine used in translations between astropy tables and excel spreadsheets.
It is installed with

conda install xlwt
