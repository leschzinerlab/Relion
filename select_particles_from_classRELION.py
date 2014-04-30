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
        parser.set_usage("%prog -i [file].star --class=[classNum]")
 	parser.add_option("-i",dest="star",type="string",metavar="FILE",
                help="Data file (.star) from RELION 3D classification")
        parser.add_option("--class",dest="classNumber",type="int", metavar="INT",
                help="Class number of particle data that you would like extracted")
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
def selectParts(params):

	#Check if input exists
	if os.path.exists(params['star']) is False:
		print '%s does not exist, exiting...' %(params['star'])
                sys.exit()

        #Check if output exists
        if os.path.exists('%s_class%02d.star' %(params['star'][:-5],params['classNumber'])) is True:
                print '%s_class%02d.star already exists, exiting...' %(params['star'][:-5],params['classNumber'])
                sys.exit()

	starfile = open(params['star'],'r')
	outfile = open('%s_class%02d.star' %(params['star'][:-5],params['classNumber']),'w')

	#File in header info
	outfile.write('\n')
	outfile.write('data_images\n')     
	outfile.write('\n')
	outfile.write('loop_\n')     
 	outfile.write('_rlnImageName\n')     
	outfile.write('_rlnClassNumber\n')         
 	outfile.write('_rlnMagnificationCorrection\n')     
 	outfile.write('_rlnLogLikeliContribution\n')     
 	outfile.write('_rlnMaxValueProbDistribution\n')     
 	outfile.write('_rlnNrOfSignificantSamples\n') 

	for line in starfile:
		lineparse = line.split()
		if len(lineparse) < 3:
			continue
		if params['debug'] is True:
			print lineparse[6]
		if float(lineparse[6]) == params['classNumber']:
			outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(lineparse[0],lineparse[6],lineparse[8],lineparse[9],lineparse[10],lineparse[11]))	

#==============================
if __name__ == "__main__":

	params=setupParserOptions()
	selectParts(params)	
