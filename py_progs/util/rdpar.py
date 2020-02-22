#!/usr/bin/env python 

'''
                    Space Telescope Science Institute

Synopsis:  

	A very simple set of routines designed to read
	inputs from a parameter file or the command line.  If
	the parameter file does not exist, then one is 
	created for future use.


Description:  
Primary routines:

	get_input(question='what',answer='Massachusetts")  

	where answer is a suggested answer.  The routine 
	checks to see whether the answer is a number, and if
	so will convert the answer to a number 

	opar(filenae="whatever.pf") opens the parameter file,
	assuming it exists.  If it does not exist opar sets
	the program up to read inputs interactivwely from the
	command line.

	cpar()  closes the parameter file or the temporary file
	as appropriate.  If the parameter file did not exist
	then the tmp file is moved to the parameter file


Notes:
	IO routines intended to be able to read the .pf files that 
	ksl has used for a long time to provide inputs to programs

	These routines can read data both from the command line
	or from a file.
									   
History:

120602 ksl Coding begun

'''

import sys
import shutil

parameter_handle=0
parameter_file=''
tmp_handle=0
tmp_file=''



def opar(filename='test.pf'):
	'''
	open a parameter file if it exists,
	or a temporary file if the parmeter
	file does not exist

	If filename does not include
	an extension .pf one is added


	'''
	global parameter_handle
	global parameter_file
	global tmp_handle
	global tmp_file

	# Add a standard extension to the
	# name
	if filename.count('.pf')==0:
		filename=filename+'.pf'

	tmp_file='tmp.'+filename
	tmp_handle=open(tmp_file,'w')

	parameter_file=filename

	try: 
		parameter_handle=open(filename)
	except IOError:
		print('File does not exist, Using command line input')
		parameter_handle=0
	return

def cpar():
	'''
	Close either the parameter file or the temporary file
	as appropriate

	If the parameter file did not exist, copy the temporary
	parameter file to the parameter file

	'''
	global tmp_handle
	global parameter_handle
	global tmp_file
	global parameter_file

	if tmp_handle!=0:
		tmp_handle.close()
		tmp_handle=0
	if parameter_handle==0:
		shutil.move(tmp_file,parameter_file)
	if parameter_handle!=0:
		parameter_handle.close()
		parameter_handle=0
	return

def get_from_command_line(question='what',answer='?'):
	'''
	Put a question on the command line and return
	the answer

	This routine is not normally called directly
	'''
	if isinstance(answer,str) == False:
		answer='%g' % answer
	string=question+' ('+answer+'):  '
	ss=input(string)
	if ss=='':
		ss=answer
	return ss

def get_from_file(question='what',answer='?'):
	'''
	Read data from a parameter file, if possible.
	If the parameter file has not been opened
	raise an io error.  If we have simple
	reached the end of the file close it

	This routine is not normally called directly
	'''
	global parameter_handle
	if parameter_handle==0:
		raise IOError
		return ''
	z=parameter_handle.readline()
	while z!='':
		zz=z.strip()
		zz=zz.split()
		if len(zz)==0 or zz[0][0]=='#':
			z=parameter_handle.readline()
			continue
		elif zz[0]==question:
			if len(zz)>=2:
				answer=zz[1]
				print('file: Matched  %-30s %-30s' % (question,z.strip()))
				return answer
		print('file: Unmatched  %-30s %-30s' % (question,z.strip()))
		z=parameter_handle.readline()

	if parameter_handle!=0:
		parameter_handle.close()
		parameter_handle=0
	raise IOError
	return ''


def get_input(question='what',answer='?'):
	'''
	This is the main routine for this very
	simple version of rdpar.  

	normal usage: 
		answer=get_input(question,answer) 
	
	The routine attempts to convert the answer
	value to a number, before returning the answer,
	but if it is given something that is obviously
	a word it will return that word.
	'''
	global tmp_handle

	try:
		answer=get_from_file(question,answer)
	except IOError:
		answer=get_from_command_line(question,answer)
	if tmp_handle!=0:
		tmp_handle.write('%-30s %s\n' % (question,answer))
		tmp_handle.flush()
	try:
		answer=eval(answer)
	except NameError:
		return answer 
	except SyntaxError:
		return answer
	except AttributeError:
		return answer
	return answer

