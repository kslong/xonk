#!/usr/bin/env python 

'''
                    Space Telescope Science Institute


Synopsis:  
    This is a simple program to project from RA and DEC
    to galactiocentric coordinates for target list

    Usage:
        gal_projct.py  whatever.pf
    
    Inputs may be read in from the command line or from 
    a separate parameter file

Description:  

    This program converts from RA, Dec to galactocentric coordinates.

    Just answer the questions using the same formats as the defaults, 
        or return to use the defaults, whch  are set up for M33.  
    
    You will need an input file that can be read by astropy.io.ascii.read.
    The columns of the table that are used are the ones labelled
    Source_name RA DEC

    Lines beginning with # will be treated as comments and ignored.
    RA, DEC can be expressed in degrees or hh:mm:ss deg:mm:ss

    You will be queried regarding the center of the galaxy, the 
    inclination angle and position angle (measured in the conventional
    way E of north).  If you want to accept the default values, just
    hit return.

    An output file will created that will have the extension .gal
    It will contain the parameters used to describe the galaxy, e.g
    the ra and dec of the center, the inclination angle, the PA, and
    the distance to ghe galaxy

    It will then provide

    name   the one word label used to describe the source
    RA    
    DEC  
    x      distance in kpc along the major axis of the galaxy
    y      distance in kpc along the minor axis of the galaxy
    R      galactocentric radius in kpc

    Send comments and complaints to Knox  (long@stsci.edu) 

Arguments:  

    None

Returns:
    A new output file 

Notes:
                                       
    This program should work with any vanilla version
    of python

History:
08aug    ksl    Coded
101229    ksl    Added additional comments
120601    ksl    Modified to accept inputs through ksl's rdpar.py
        routines.  Format of input file changed to match
        masterfile format.  Program structure modified
        to be similar to most of ksl's other python programs.
        output file format modified to print name first
141110  ksl    Modified so uses astropy.io on input. Output is still
        homegrown 
15aug    ksl    Finish adaption to use astropy


'''



import sys
import math
from rdpar import *
from astropy.io import ascii
from astropy.table import Table


RADIAN=57.29578
INFINITY=1.e32


def read_table(filename='foo.txt'):
    '''
    Read a file using astropy.io.ascii and 
    return this 

    Description:

    Notes:

    History:


    '''
    try:
        data=ascii.read(filename)
    except IOError:
        print(('Error: file %s does not appear to exist' % filename))
        return

    print ('Here are the column names:')
    
    print((data.colnames))

    return data

def radec2deg(ra,dec):
    ''' Convert an ra dec string to degrees.  The string can already
    be in degrees in which case all that happens is a conversion to
    a float'''

    if isinstance(ra,str) == True:
        r=ra.split(':')
        d=dec.split(':')

        try:
            rr=float(r[0])
        except ValueError:
            print(('Could not convert ',r))
        if len(r)>1:
            rr=rr+float(r[1])/60.
        if len(r)>2:
            rr=rr+float(r[2])/3600.
        if len(r)>1:
            rr=15.*rr  # Since we assume ra was in hms
    else:
        rr=ra
    
    if isinstance(ra,str) == True:
        dd=float(d[0])
        x=0
        if len(d)>1:
            x=x+float(d[1])/60.
        if len(d)>2:
            x=x+float(d[2])/3600.
    
        if dd > 0:
            dd=dd+x
        else:
            dd=dd-x
    else: 
        dd=dec
    
    return rr,dd  

def read_file(filename='foo.txt'):
        '''
        Read a file using astropy.io.ascii and 
        return this 

        Description:

        Notes:

        History:
    '''
        try:
                data=ascii.read(filename)
                test=data[0][0]
                if test.count('-')==len(test):
                        ata=data[1:]
        except IOError:
                print(('Error: file %s does not appear to exist' % filename))
                return

        print ('Here are the column names:')
        print((data.colnames))

        return data



def get_radec_list(filename='centers.dat',deg='yes',col_name='Source_name',col_ra='RA',col_dec='Dec'):
    '''
    read a file in which the first column is a name
    and the second and third columns are the ra and
    dec. 
    if deg='yes' then convert the ra and dec to degrees

    The routine returns a list in which each record
    has the following fomrat

    Name RA(deg)  Deg(deg)   RA(orig)  Dec(orig) 

    141110 - Modify to use astropy
    '''

    data=read_file(filename)

    sources=[]

    for one in data:
        # print 'test',one[0],one[1],one[2]
        sources.append([one[col_name],one[col_ra],one[col_dec]])
        
    # print sources
    return sources   

def distance(r1,d1,r2,d2):
    '''
    Return the angular offset between two ra,dec positions

    All units are in degrees
    '''
#    print 'distance',r1,d1,r2,d2
    r1=r1/RADIAN
    d1=d1/RADIAN
    # print (r1,d1, r2,d2)
    r2=r2/RADIAN
    d2=d2/RADIAN
    xlambda=math.sin(d1)*math.sin(d2)+math.cos(d1)*math.cos(d2)*math.cos(r1-r2)
#    print 'xlambda ',xlambda
    if xlambda>=1.0:
        xlambda=0.0
    else:
        xlambda=math.acos(xlambda)

    xlambda=xlambda*RADIAN
#    print 'angle ',xlambda
    return xlambda


def radec2gal(ra,dec,gra,gdec,ginc,gpa,gdist):
    '''
    This converts an ra and dec to galactocentric coordinates
    given the parameters that describe the galaxy

    where gra and gdec are the ra,dec of the center of the 
    galaxy and

    ginc,gpa are the inclination and position angle

    Inputs, except the distance gdist,  are all in degrees

    The routine returns of tuple containing the postion 
    of the object in galactocentric coordinates in the
    same units as gdist
    '''
#    print '\n Start ',ra,dec,gra,gdec,ginc,gpa,gdist

    

    # First calculate the position angle of the source
    # measured E of North

    length=distance(gra,gdec,ra,dec)
    if length==0:  # Then we have chosen the center
#        print 'Point at center'
        return 0.,0.


    delta=dec-gdec # distance along +y axis

#    print 'length',length, ' delta ',delta

    theta=RADIAN*math.acos(delta/length)  # angle with respect to y axis

    if gra > ra:
        theta=-theta

    # Now calculate the difference btween the position angle of the source
    # and the major axis of the galaxy 

    dtheta=theta-gpa
#    print 'theta,dtheta ',theta,dtheta

    # Now project the length from the center along the major and minor axes
    # on the sky

    x=length*math.cos(dtheta/RADIAN) # length along major axis
    y=length*math.sin(dtheta/RADIAN) # length along minor axis

#    print 'x,y before ',x,y

    # Then correct for the inclination angle 

    y=y/math.cos(ginc/RADIAN)

#    print 'x,y after ',x,y, math.sqrt(x*x+y*y)

    # Now convert to a distance

    x=math.tan(x/RADIAN)*gdist
    y=math.tan(y/RADIAN)*gdist

    # print 'Finish ',x,y, math.sqrt(x*x+y*y)

    return x,y  # The distance in kpc along the major and minor axes

def doit(parameterfile='gal_project.pf'):
    '''
    Main routine for converting from ra, dec to galactocentric coordinates.

    Note:
        The inputs are also read in in this routine
    '''

    opar(parameterfile)

    # M33 inputs.  Note these must all be strings

    gal_ra="1:33:50.89"
    gal_dec="30:39:36.8"
    gal_pa="22."     #Position angle measured E of North
    gal_inc="56."    #Inclination in eg
    gal_dist="817"   # Distance in kpc
    input_file="snr_fixed.dat"


    # Get inputs
    xgal_ra=get_input("Galaxy.RA",gal_ra)
    xgal_dec=get_input("Galaxy.Dec",gal_dec)
    gal_ra,gal_dec=radec2deg(xgal_ra,xgal_dec)

    gal_pa=float(get_input("Galaxy.Position.Angle(deg)",gal_pa))
    gal_inc=float(get_input("Galaxy.Inclination(deg)",gal_inc))
    gal_dist=float(get_input("Galaxy.Distance(kpc):",gal_dist))

    input_file=get_input("Input_file",input_file)
    output_file=input_file+'.gal'
    output_file=get_input("Output_file",output_file)

    # At this point all of the galaxies parameters are in degrees (and are floats)

    # Read the input file
    # objects=get_radec_list(input_file)

    objects=read_table(input_file)


    if len(objects)==0:
        return



    xx=[]
    yy=[]
    rho=[]
    for row in objects:
        ra,dec=radec2deg(row['RA'],row['Dec'])
        # print (ra,dec)
        x,y=radec2gal(ra,dec,gal_ra,gal_dec,gal_inc,gal_pa,gal_dist)
        xx.append(x)
        yy.append(y)
        rho.append(math.sqrt(x*x+y*y))
    
    objects['x(kpc)']=xx
    objects['y(kpc)']=yy
    objects['R(kpc)']=rho

    objects['x(kpc)'].format='5.2f'
    objects['y(kpc)'].format='5.2f'
    objects['R(kpc)'].format='5.2f'

    


    # Create a table instead

    meta={}
    meta['Galaxy center']='%12s %12s' % (xgal_ra,xgal_dec)
    meta['Galaxy Position Angle (deg)']='%8.1f' % (gal_pa)
    meta['Galaxy Inclination    (deg)']='%8.1f' % (gal_inc)
    meta['Galaxy Distance       (kpc)']='%8.1f' % (gal_dist)

    objects.meta=meta

    objects['RA'].format='.6f'
    objects['Dec'].format='.6f'
    

    objects.write(output_file,format='ascii.fixed_width_two_line',overwrite=True)

    return objects['R(kpc)']



    # You are now done

# End of subroutines:

# Next lines permit one to run the routine from the command line
if __name__ == "__main__":


    argc=len(sys.argv)


    if argc>1:
        if sys.argv[1]=='-h':
            print (__doc__)
        else:
            doit(sys.argv[1])
    else:
        print ('for help enter gal_coords.py -h')
        doit('gal_coords.pf')
