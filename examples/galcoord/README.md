## This directory contains an example for running the routine gal_project.py

The routine reads a parameter file containing informatio about the galaxy with the usual astronomical conventions

It then reads and astropy table, which must have the RA and Dec of objects in columns names RA and Dec

It produces a new version of the table with 3 additional columns, the x and y position of the galaxy in galactocentric coordinates and the galactocentric distance for the object.

The example is for M83
