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


#==============================
def selectEveOdd(params):

	f1 = open(params['star'],'r')

	outfileeve = '%s_eve.star' %(params['star'][:-5])
	outfileodd = '%s_odd.star' %(params['star'][:-5])

	if os.path.exists(outfileeve):
                print "\nOutput file %s already exists, exiting.\n" %(outfileeve)
		sys.exit()

	if os.path.exists(outfileodd):
                print "\nOutput file %s already exists, exiting.\n" %(outfileodd)
                sys.exit()

	eve = open(outfileeve,'w')
        odd = open(outfileodd,'w')

	linecounter=1

        for line in f1:
                
		if len(line) < 40:

			eve.write(line)
			odd.write(line)

		if len(line) > 40:

			if linecounter % 2 == 0:

				eve.write(line)

			if linecounter % 2 != 0: 

				odd.write(line)
	
			linecounter = linecounter + 1
	f1.close()
	odd.close()
	eve.close()
	
#==============================
if __name__ == "__main__":

        params=setupParserOptions()
	checkConflicts(params)
	selectEveOdd(params)
