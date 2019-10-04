#!/usr/bin/env python 

'''
                    Space Telescope Science Institute

Synopsis:  

Write an Excell spread sheet from an ascii file

The file should be a simple txt file with column names
in the first row (No # or columns will be ignored


Command line usage (if any):

    usage: usage: ascii2excel.py filename [outputfile]

    where 
        filename is the input ascii file
        output file is the optional name of Excel
        spread sheet that will be produced.
    

Description:  

    This simply reads the file with astropy.io and
    writes out the excel spread sheet using  xlwt

Primary routines:

Notes:

    This routine does not set formats but a way
    to do this is described here

    https://github.com/python-excel/xlwt/blob/master/xlwt/examples/num_formats.py
                                       
History:

141028 ksl Coding begun

'''

import sys
import os
from astropy.io import ascii
import numpy
from xlwt import Workbook



def doit(filename='foo.txt',output_file='',style='fixed_width_two_line'):
    '''
    Read a text file and make an excel file

    Description:

    Notes:

    From the command line, one cannot modify the style.  This is partly
    deliberate since the most transportable astorpy tables seem to be
    fixed_width_two_line

    History:

    150721 ksl Added some error handling.


    '''
    try:
        data=ascii.read(filename,format=style)
    except IOError:
        print(('Error: file %s does not appear to exist' % filename))
        return
    except:
        print(('Error: Probably the input file did not correspond to a %s astropy table' % style))
        return

    # Create or modify the output file name if necessary
    if output_file=='':
        output_file=filename
        output_file=output_file.replace('.txt','')
        print(('test:',output_file))
        output_file=output_file.replace('.dat','')
        output_file=output_file+'.xls'
    if output_file.count('.xls')==0:
            output_file=output_file+'.xls'
    
    if os.path.isfile(output_file)==True:
        output_file='new_'+output_file
        print(('This file already exists so writing to %s' % output_file))




    # This section just verifies that the file has been in correctly

    print ('Here are the column names:')
    
    print((data.colnames))

    print('Here is the data:')

    print (data)


    # Now create a workbook and put in the data



    book=Workbook()
    sheet=book.add_sheet(filename,cell_overwrite_ok=True)

    # First write out the column names to row zero

    row=sheet.row(0)
    i=0
    while i<len(data.colnames):
        name=data.colnames[i]
        name = str (name)
        row.write(i,name)
        i=i+1

    i=0
    while i<len(data):
        row=sheet.row(i+1)
        j=0
        while j<len(data[i]):
            value=data[i][j]
            if isinstance(value,numpy.ma.core.MaskedConstant):
                value='--'
            if isinstance(value, (numpy.int64, numpy.int32)):
                value=int(value)
            row.write(j,value)
            j=j+1
        i=i+1


    book.save(output_file)

    print(('Completed: %s --> %s' % (filename,output_file)))

    

    





# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)==2:
        doit(sys.argv[1])
    elif len(sys.argv)==3:
        doit(sys.argv[1],sys.argv[2])
    else:
        print ('usage: ascii2excel.py filename [outputfile]')
