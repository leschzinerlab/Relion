#!/usr/bin/env python 

import optparse
from sys import *
import os,sys,re
from optparse import OptionParser
import glob
import subprocess
from os import system
import linecache
import time
import shutil

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog -i <particles.star file> -o <output name>")
        parser.add_option("-i",dest="star",type="string",metavar="FILE",
                help="_data.star file containing per-particle entries from auto-refine")
        parser.add_option("-o",dest="output",type="string",metavar="FILE",
                help="Output file name with updated particle info")
	parser.add_option("--newparticlename",dest="particlepath",type="string",metavar="STRING",
                help="Suffix for new pixel size data")
	parser.add_option("--oldpix",dest="oldpix",type="float",metavar="FLOAT",
		help="Old pixel size")
	parser.add_option("--newpix",dest="newpix",type="float",metavar="FLOAT",
                help="New pixel size")
	parser.add_option("--newdetectorpix",dest="newdetector",type="float",metavar="FLOAT",
                help="New detector pixel size. Must match up with mag & pixel size.")
	parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 2:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#=============================
def checkConflicts(params):
        if not params['star']:
                print "\nWarning: no .star file specified\n"
        elif not os.path.exists(params['star']):
                print "\nError: star file '%s' does not exist\n" % params['star']
                sys.exit()

        if os.path.exists(params['output']):
                print "\nError: output file %s already exists, exiting.\n" %(params['output'])
                sys.exit()

#==============================
def updateshifts(params):

	f1 = open(params['star'],'r')

	if os.path.exists(params['output']):
                print "\nOutput file %s already exists, updating information.\n" %(params['output'])
                shutil.move(params['output'],'tmpFile.txt')
		f1 = open('tmpFile.txt','r')

        outfile = open(params['output'],'w')

        for line in f1:
                if len(line) > 40:

                        l = line.split()

			l[5] = str(params['newdetector'])
                        l[15] = str((float(l[15])*params['oldpix'])/params['newpix'])
			l[16] = str((float(l[16])*params['oldpix'])/params['newpix'])
			l[9] = l[9][:-5]+"%s"%(params['particlepath']) 
                        line = "   ".join(l)
                        line = line+"\n"
                outfile.write(line)

	f1.close()

	if os.path.exists('tmpFile.txt'):
                os.remove('tmpFile.txt')
	
#==============================
if __name__ == "__main__":

        params=setupParserOptions()
	checkConflicts(params)
	if params['oldpix'] and params['newpix']:
		updateshifts(params)
