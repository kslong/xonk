#!/usr/bin/env python 

'''
                    Space Telescope Science Institute

Synopsis:  

Read an Excel spread_sheet and print it to a txt file


Command line usage (if any):

    usage: excel2ascii.py filename [outroot]

Description:  

    This uses xlrd and astropy.io to write an 
    excel spread sheet to one or mor files

    The output file has the specific format
    fixed_width_two_line

Returns:

    Each sheet of the Excel spread sheet is written
    to a different file

Primary routines:

Notes:

    The routines assume that the first row in the
    excel spread sheet will be the names of the
    columns.
                                       
History:

141028 ksl Coding begun
150721 ksl Incorporated or reincorporated astropy
           tables as the output forma. The older
       version oft he code exists as doit2, but
       can only be exeucuted from within python

'''

import sys
import os
import numpy
from xlrd import open_workbook
from astropy.table import Table

    

def read_excel_sheet_cols(filename='simple.xls',sheet_number=0):
    '''
    Read and return the each column for a single sheet in
    an Excel workbook as a list.  

    Returns

    The name of the spread sheet, and a list of
    the cols in the spread sheet.

    Notes:

    The sheets are numbered from 0


    History

    150721 ksl Added as part of an effort to move to astropy
               table outputs


    '''
    try:
        wb = open_workbook(filename)
    except IOError:
        print ('Workbook %s not found ' % filename)
        return []
    records=[]

    # print 'Give me a break',sheet_number
    s=wb.sheets() # This returns a list of the sheets
    s=s[sheet_number]
    sheet_name=s.name
    print ('Sheet:',sheet_name)
    for col in range(s.ncols):
        values = []
        for row in range(s.nrows):
                values.append(s.cell(row,col).value)
        # print values
        records.append(values)
    return sheet_name,records


def read_excel_sheet(filename='simple.xls',sheet_number=0):
    '''
    Read and return the reocords for a single sheet in
    an Excel workbook.  

    Returns

    The name of the spread sheet, and a list of
    the rows in the spread sheet.

    Notes:

    The sheets are numbered from 0


    '''
    try:
        wb = open_workbook(filename)
    except IOError:
        print ('Workbook %s not found ' % filename)
        return []
    records=[]

    # print 'Give me a break',sheet_number
    s=wb.sheets() # This returns a list of the sheets
    s=s[sheet_number]
    sheet_name=s.name
    print ('Sheet:',sheet_name)
    for row in range(s.nrows):
        values = []
        for col in range(s.ncols):
                values.append(s.cell(row,col).value)
        # print values
        records.append(values)
    return sheet_name,records

def get_number_of_worksheets(filename='simple.xls'):
    '''
    Simple routine to determine the number of sheets in the
    spreadsheet
    '''

    try:
        wb = open_workbook(filename)
    except IOError:
        print ('Workbook %s not found ' % filename)
        return 0
    return len(wb.sheets())


def doit(filename='simple.xls',outroot=''):
    '''
    Read each of the sheets in an Excel spread sheet
    and  write the sheet to a file

    where 
        filename is the name of the input file (with its extension)
        outroot is the root name of the ouput file or files (in
            the case where there are multiple files)



    Description:

    

    Notes:

    Previously, there were problems in some cases when logic was
    inserted into an ascii file.  See doit_old.  This may reappear,
    in which case more logic might be required in the processing 
    of the cells.


    History: 

    141028: ksl Wrote using astropy.io.ascii
    141128    ksl Rewrite without astropy so that I would have more control on
            exaclty how the file is written out.
    150721  ksl Rewrite back into astopy, because I would like to be able to
                handle spaces, and I want to write fixed_width_two_line files


    '''

    nsheets=get_number_of_worksheets(filename)
    if nsheets==0:
        return

    print ('File %s has %d sheet or sheets ' % (filename,nsheets))

    if outroot=='':
        outroot=filename[0:filename.rindex('.')]


    i=0
    while i<nsheets:
        sheet_name,records=read_excel_sheet_cols(filename,i)
        # At this point we have retrieved the sheet as a list
        # with the first element being the column name
        if nsheets>1:
            outfile=outroot+'.%02d.txt'% i
        else:
            outfile=outroot+'.txt'
        if os.path.isfile(outfile)==True:
            outfile='new_'+outfile
            print ('This file already exists so writing to %s' % outfile)


        # now create a file for each sheet
        # We want to use astropy Tables package so that the 
        # data are formated in a sensible fashion, but astropy
        # Tables are Fundamentall column abased

        # Assume word 0 ate column names


        x=''
        for line in records:
            # print(line)
            col_name=line[0]
            data=[]
            j=1
            while j<len(line):
                one=line[j]
                # print('xxx',type(one))
                # Note that this was changned for Python3, which does not
                # have a unicode type.  This problem may come back because
                # it only occured in rare situations.
                if type(one) is str:
                    one=one.strip()
                elif type(one)==float:
                    if int(one)==one:
                        one=int(one)
                j=j+1
                data.append(one)
            if x=='':
                x=Table([data],names=[col_name])
            else:
                x[col_name]=data
        x.write(outfile,format='ascii.fixed_width_two_line')
        i=i+1





def doit_old(filename='simple.xls',outroot=''):
    '''
    Read each of the sheets in an Excel spread sheet
    and  write the sheet to a file

    where 
        filename is the name of the input file (with its extension)
        outroot is the root name of the ouput file or files (in
            the case where there are multiple files)



    Description:

    

    Notes:

    The code does not seem to work with Excel " or ' in the code, the error
    produced is a unicode one.  So all unicode characters that are outside the
    ascii range are convered to *, These are flagged
    

    History: 

    141028: ksl Wrote using astropy.io.ascii
    141128    ksl Rewrite without astropy so that I would have more control on
            exactly ohow the file is written out.
    150721    ksl Deprecated this version of conversion routines because I would
                like to use astropy if at all possilble.  This version avoids
            astropy but does not quite produce the format of a fixed_format_two_line
            file.  


    '''

    nsheets=get_number_of_worksheets(filename)
    if nsheets==0:
        return

    print ('File %s has %d sheet or sheets ' % (filename,nsheets))

    if outroot=='':
        outroot=filename[0:filename.rindex('.')]


    i=0
    while i<nsheets:
        sheet_name,records=read_excel_sheet(filename,i)
        if nsheets>1:
            outfile=outroot+'.%02d.txt'% i
        else:
            outfile=outroot+'.txt'
        if os.path.isfile(outfile)==True:
            outfile='new_'+outfile
            print ('This file already exists so writing to %s' % outfile)

        f=open(outfile,'w')

        # now create a file for each sheet
        # We want to use astropy Tables package so that the 
        # data are formated in a sensible fashion, but astropy
        # Tables are Fundamentall column abased

        # Assume row 0 ate column names

        # Create a list with 0 in all records to get the columns widths

        width=[0]*len(records[0])

        for line in records:
            # print line
            string=''
            j=0
            while j<len(line):
                one=line[j]
                if type(one) is unicode:
                    one=one.strip()
                    if one.count(' '):
                        # print 'gotcha',one
                        one=one.replace(' ','~')
                        # print 'fixed',one
                        # one='"'+one+'"'
                word='%s' % one
                if len(word)>width[j]:
                    width[j]=len(word)
                        
                j=j+1
             

        # Finished establishing the column widths
        print (width)



        for line in records:
            string=''
            j=0
            while j<len(line):
                one=line[j]
                if type(one) is unicode:
                    one=one.strip()
                    if one.count(' '):
                        one=one.replace(' ','~')

                word='%s' % one
                if word=='':
                    word='~'
                    print ('HOTCHA')
                my_format=' %'+'%d' % width[j]+'s '
                # print my_format
                string=string+my_format % word 
                j=j+1
             
            try:
                f.write('%s\n' % string)
            except UnicodeEncodeError:
                # print 'gotcha'
                xstring=''
                for ii in string:
                    if ord(ii)<128:
                        xstring=xstring+ii
                    else:
                        xstring=xstring+'*'
                # xstring=''.join(ii for ii in string if ord(ii)<128) 
                print ('Unicode Error',len(string),len(xstring), xstring)
                f.write('%s\n' % xstring)




        i=i+1





# Next lines permit one to run the routine from the command line
if __name__ == "__main__":
    import sys
    if len(sys.argv)==2:
        # doit(int(sys.argv[1]))
        doit(sys.argv[1])
    elif len(sys.argv)==3:
        doit(sys.argv[1],sys.argv[2])
    else:
        print ('usage: excel2ascii.py filename [outroot]')
