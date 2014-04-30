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
        parser.set_usage("%prog -i [file].star --class=[classNum1],[classNum2],..")
 	parser.add_option("-i",dest="star",type="string",metavar="FILE",
                help="Data file (.star) from RELION 3D classification")
        parser.add_option("--class",dest="classNumber",type="string", metavar="STRING",
                help="Class number(s) of particle data that you would like extracted. (Comma separated if > 1 class)")
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
def selectPartsOneClass(params):

	#Check if input exists
	if os.path.exists(params['star']) is False:
		print '%s does not exist, exiting...' %(params['star'])
                sys.exit()

        #Check if output exists
        if os.path.exists('%s_class%02d.star' %(params['star'][:-5],int(params['classNumber']))) is True:
                print '%s_class%02d.star already exists, exiting...' %(params['star'][:-5],int(params['classNumber']))
                sys.exit()

	starfile = open(params['star'],'r')
	outfile = open('%s_class%02d.star' %(params['star'][:-5],int(params['classNumber'])),'w')

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
		if float(lineparse[6]) == int(params['classNumber']):
			outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(lineparse[0],lineparse[6],lineparse[8],lineparse[9],lineparse[10],lineparse[11]))	
#=============================
def selectPartsMoreThanOne(params):

        #Check if input exists
        if os.path.exists(params['star']) is False:
                print '%s does not exist, exiting...' %(params['star'])
                sys.exit()

        #Check if output exists
        if os.path.exists('%s_selClasses.star' %(params['star'][:-5])) is True:
                print '%s_selClasses.star already exists, exiting...' %(params['star'][:-5])
                sys.exit()

        starfile = open(params['star'],'r')
        outfile = open('%s_selClasses.star' %(params['star'][:-5]),'w')

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
			print params['classNumber'].split(',')
                if lineparse[6] in  params['classNumber'].split(','):
                        outfile.write('%s\t%s\t%s\t%s\t%s\t%s\n'%(lineparse[0],lineparse[6],lineparse[8],lineparse[9],lineparse[10],lineparse[11])) 	

#==============================
if __name__ == "__main__":

	params=setupParserOptions()
	if len(params['classNumber'].split(',')) == 1: 
		selectPartsOneClass(params)	
	if len(params['classNumber'].split(',')) > 1: 
                selectPartsMoreThanOne(params)
