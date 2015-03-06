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
                help="particle.star file containing per-particle entries that need their paths updated")
        parser.add_option("-o",dest="output",type="string",metavar="FILE",
                help="Output file name with updated particle info")
        parser.add_option("--path",dest="path",type="string",metavar="PATH",
                help="Path to include to each particle entry")
	parser.add_option("--mag",dest="mag",type="int",metavar="INT",
                help="New magnification")
	parser.add_option("--pix",dest="apix",type="float",metavar="FLOAT",
		help="New detector pixel size")
	parser.add_option("--removeParticleName",dest="removeParticleName",type="string",metavar="PATH",
		help="Name of particle that needs to be replaced")
	parser.add_option("--replaceParticleNameWith",dest="replaceParticleNameWith",type="string",metavar="PATH",
		help="Name that will be replaced")
	parser.add_option("--moreHelp", action="store_true",dest="morehelp",default=False,
                help="Flag for more running information")
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
def updatePaths(params):

	f1 = open(params['star'],'r')

	outfile = open(params['output'],'w')

	for line in f1:
		
		if line[:11] == 'Micrographs':

			l = line.split()

			first = params['path']+l[0]

			splitAgain = l[3].split('@')

			second = splitAgain[0]+'@'+params['path']+splitAgain[1]

			l[0] = first
			l[3] = second
			line = "   ".join(l)
			line = line+"\n"
		outfile.write(line)

#==============================
def updateMag(params):

        if os.path.exists(params['output']):
                print "\nOutput file %s already exists, updating information.\n" %(params['output'])
                shutil.move(params['output'],'tmpFile.txt')
                f1 = open('tmpFile.txt','r')

        if not os.path.exists(params['output']):

                f1 = open(params['star'],'r')

	outfile = open(params['output'],'w')

	for line in f1:

                if len(line) > 40:
                        
			l = line.split()

			l[10] = str(params['mag'])
                        line = "   ".join(l)
                        line = line+"\n"
                outfile.write(line)	
	f1.close()

	if os.path.exists('tmpFile.txt'):
		os.remove('tmpFile.txt')

#==============================
def updateApix(params):

	f1 = open(params['star'],'r')

	if os.path.exists(params['output']):
                print "\nOutput file %s already exists, updating information.\n" %(params['output'])
                shutil.move(params['output'],'tmpFile.txt')
		f1 = open('tmpFile.txt','r')

        outfile = open(params['output'],'w')

        for line in f1:
                if len(line) > 40:

                        l = line.split()

                        l[11] = str(params['apix'])
                        line = "   ".join(l)
                        line = line+"\n"
                outfile.write(line)

	f1.close()

	if os.path.exists('tmpFile.txt'):
                os.remove('tmpFile.txt')
	
#=============================
def updateParticleName(params):

	f1 = open(params['star'],'r')

        if os.path.exists(params['output']):
                print "\nOutput file %s already exists, updating information.\n" %(params['output'])
                shutil.move(params['output'],'tmpFile.txt')
                f1 = open('tmpFile.txt','r')

        outfile = open(params['output'],'w')

        for line in f1:

                if len(line) > 40:

                        l = line.split()

			#Need to change 4 & 14
			#print l[3]
			#print l[13]
			
			particle = l[13].replace(params['removeParticleName'],params['replaceParticleNameWith'])
			
			movie = l[3].replace(params['removeParticleName'],params['replaceParticleNameWith'])

			l[3]=str(movie)
			l[13]=str(particle)
	
                        line = "   ".join(l)
                        line = line+"\n"
                outfile.write(line)
        f1.close()

#==============================
if __name__ == "__main__":

        params=setupParserOptions()
        if params['morehelp'] is True:
		print '\n'
        	print 'A multi-functional command to change parameters in relion particles.star files.'
        	print '--> You can specify one or more changes to make to the file'
        	print '--> Assumes 13 columns:\n'
		print '_rlnMicrographName #1 '
		print '_rlnCoordinateX #2' 
		print '_rlnCoordinateY #3 '
		print '_rlnImageName #4 '
		print '_rlnDefocusU #5 '
		print '_rlnDefocusV #6 '
		print '_rlnDefocusAngle #7 '
		print '_rlnVoltage #8 '
		print '_rlnSphericalAberration #9 '
		print '_rlnAmplitudeContrast #10 '
		print '_rlnMagnification #11 '
		print '_rlnDetectorPixelSize #12 '
		print '_rlnCtfFigureOfMerit #13 '
        	print '\n'
		print 'Specify any the following inputs to make changes to the information for each particle:'
		print '--path=/Path/to/add/to/your/particle/paths'
		print '--mag=[new magnification, #11]'
		print '--pix=[new detector pixel size, #12]'
		print '\n'
		sys.exit()
	checkConflicts(params)
	if params['path']:
		updatePaths(params)

	if params['mag']:
		if params['debug'] is True:
			print 'Updating magnification'
		updateMag(params)

	if params['apix']:
		updateApix(params)

	if params['removeParticleName']:

		if params['replaceParticleNameWith']:

			updateParticleName(params)
