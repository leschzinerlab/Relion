#!/usr/bin/env python

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
	parser.add_option("--oext",dest="oext",type="string", metavar="STRING",                
		help="Output extension for particle stacks and star files")
        parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()
        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))
        if len(sys.argv) < 5:
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

#==============================
def binStack(params):
	
	#Open star file and get particle stack, X & Y coordinates

	f1=open(params['star'],'r')

	for line in f1:

		if len(line.split()) < 3:
                        continue

		stack=(line.split()[3].split('@')[1])
		xcoord=line.split()[1]
		ycoord=line.split()[2]
		pixelsize=line.split()[-2]
	
		if params['debug'] is True:
			print stack

		if os.path.exists('%s_%s.mrcs' %(stack[:-4],params['oext'])):
			if params['debug'] is True:
				print '%s_%s.mrcs already exists, skipping' %(stack[:-4],params['oext'])
			
		if not os.path.exists('%s_%s.mrcs' %(stack[:-4],params['oext'])):
			#relion image handler to bin stack
						

		#Write new coordinates, stack name, and new detector size into new star file

	f1.close()

#==============================
if __name__ == "__main__":

        params=setupParserOptions()
	checkConflicts(params)
	binStack(params)
