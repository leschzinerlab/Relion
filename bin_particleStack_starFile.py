#!/usr/bin/env python

import shutil
import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system


#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i [file].star --bin=[factor] --oext=[output]")
        parser.add_option("-i",dest="star",type="string",metavar="FILE",
                help="Data file (.star) for RELION particle stack")
        parser.add_option("--bin",dest="bin",type="int", metavar="INTEGER",
                help="Binning factor for particle data set")
	parser.add_option("--apix",dest="apix",type="float", metavar="FLOAT",
                help="Pixel size for input particles")
	parser.add_option("--oext",dest="oext",type="string", metavar="STRING",                
		help="Output extension for particle stacks and star files")
        parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()
        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))
        if len(sys.argv) < 6:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#==============================
def checkConflicts(params):

	if not os.path.exists(params['star']):
		print 'File %s does not exist. Exiting' %(params['star'])
		sys.exit()

	if os.path.exists('%s_%s.star' %(params['star'][:-5],params['oext'])):
		print 'File %s_%s.star already exists. Exiting.' %(params['star'][:-5],params['oext'])
		sys.exit()

#==============================
def binStack(params):
	
	#Open star file and get particle stack, X & Y coordinates

	f1=open(params['star'],'r')
	o1=open('%s_%s.star' %(params['star'][:-5],params['oext']),'w')

	for line in f1:

		if len(line.split()) < 3:
                        o1.write(line)
			continue
		linesplit=line.split()	
		stack=(line.split()[3].split('@')[1])
		number=(line.split()[3].split('@')[0])
		xcoord=line.split()[1]
		ycoord=line.split()[2]
		pixelsize=line.split()[-2]
	
		if params['debug'] is True:
			print stack

		if os.path.exists('%s_%s.mrcs' %(stack[:-5],params['oext'])):
			if params['debug'] is True:
				print '%s_%s.mrcs already exists, skipping' %(stack[:-5],params['oext'])
			
		if not os.path.exists('%s_%s.mrcs' %(stack[:-5],params['oext'])):
			#relion image handler to bin stack
			cmd='relion_image_handler --i %s --o %s_%s.mrcs --angpix %f --rescale_angpix %f' %(stack,stack[:-5],params['oext'],params['apix'],float(params['bin'])*params['apix'])
			if params['debug'] is True:
				print cmd
			subprocess.Popen(cmd,shell=True).wait()							

		#Write new coordinates, stack name, and new detector size into new star file
		seq=("%s"%(number),"@","%s_%s.mrcs"%(stack[:-5],params['oext']))
		newstack=''.join(seq)
		linesplit[3]=newstack
		linesplit[1]=str(round(float(xcoord)/float(params['bin'])))
		linesplit[2]=str(round(float(ycoord)/float(params['bin'])))
		linesplit[-2]=str(float(pixelsize)*float(params['bin']))
		linesplit='\t'.join(linesplit)
	
		o1.write('%s\n' %(linesplit))

		if not os.path.exists('%s_%s.star' %(stack[:-5],params['oext'])):
			shutil.copy('%s.star' %(stack[:-5]),'%s_%s.star' %(stack[:-5],params['oext']))

	f1.close()

#==============================
if __name__ == "__main__":

        params=setupParserOptions()
	checkConflicts(params)
	binStack(params)
