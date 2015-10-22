#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
import linecache

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --stareuler=<relion_star_file> --starparticle=<relion_star_file> [lims]")
        parser.add_option("--stareuler",dest="stareuler",type="string",metavar="FILE",
                help="Output Relion star from refinement/classification containing euler angles ")
        parser.add_option("--starparticle",dest="starparticle",type="string",metavar="FILE",
                help="Relion star file that will be reweighted based upon euler angles.")
        parser.add_option("--AngleRotLim1",dest="rotlim1",type="int",metavar="INT",default=0,
                help="Lower limit for AngleRot. (Default=0)")
        parser.add_option("--AngleRotLim2",dest="rotlim2",type="int",metavar="INT",default=0,
                help="Upper limit for AngleRot. (Default=Total number of particles)")
        parser.add_option("--AngleTiltLim1",dest="tiltlim1",type="int",metavar="INT",default=0,
                help="Lower limit for AngleTilt. (Default=0)")
        parser.add_option("--AngleTiltLim2",dest="tiltlim2",type="int",metavar="INT",default=0,
                help="Upper limit for AngleTilt. (Default=Total number of particles)")
        parser.add_option("--AnglePsiLim1",dest="psilim1",type="int",metavar="INT",default=0,
                help="Lower limit for AnglePsi. (Default=0)")
        parser.add_option("--AnglePsiLim2",dest="psilim2",type="int",metavar="INT",default=0,
                help="Upper limit for AnglePsi. (Default=Total number of particles)")
        parser.add_option("-d", action="store_true",dest="debug",default=False,
                help="debug")
        options,args = parser.parse_args()

        if len(args) > 0:
                parser.error("Unknown commandline options: " +str(args))

        if len(sys.argv) < 3:
                parser.print_help()
                sys.exit()
        params={}
        for i in parser.option_list:
                if isinstance(i.dest,str):
                        params[i.dest] = getattr(options,i.dest)
        return params

#==============================
def checkConflicts(params):

        if not os.path.exists(params['stareuler']):
            print 'Error: File %s does not exist' %(params['stareuler'])
            sys.exit()

        if not os.path.exists(params['starparticle']):
            print 'Error: File %s does not exist' %(params['starparticle'])
            sys.exit()

        if os.path.exists('%s_reweight.star' %(params['starparticle'][:-4])):
            print 'Error: File %s already exists. Exiting.' %(params['starparticle'][:-4])
            sys.exit()

#===============================
def getRelionColumnIndex(star,rlnvariable):

    counter=50
    i=1

    while i<=50:

        line=linecache.getline(star,i)

        if len(line)>0:
            if len(line.split())>1:
                if line.split()[0] == rlnvariable:
                    return line.split()[1][1:]

        i=i+1

#==============================
def getNumberParticlesRelion(star):

    f1=open(star,'r')
    tot=0

    for line in f1:
        if len(line) > 50:
            tot=tot+1

    return tot

#==============================
def reweight_starfile(euler,particle,rotlim1,rotlim2,tiltlim1,tiltlim2,psilim1,psilim2,debug):

        #Get column numbers for euler angles
        colrot=getRelionColumnIndex(stareuler,'rln_AngleRot')
        coltilt=getRelionColumnIndex(stareuler,'rln_AngleTilt')
        colpsi=getRelionColumnIndex(stareuler,'rln_AnglePsi')

        #Open output file
        o1=open('%s_reweight.star' %(params['starparticle'][:-4]),'w')

        #Read relion header from original file (particle) and then write into new file
        f1=open(particle,'r')

        #Counter for number of header lines
        headercount=0

        for line in f1:
            if len(line)<50:
                headercount=headercount+1
                o1.write(line)
        f1.close()

        #Find number of particles that need to be removed

        #Randomly select from this particle list a set number to be included

        #Go through each line, decide if it should/shouldn't be included and write into new file

#==============================
if __name__ == "__main__":

        #Get input options
        params=setupParserOptions()

        #Check that files exists
        checkConflicts(params)

        #Number of particles
        tot=getNumberParticlesRelion(params['stareuler'])

        #Set max numbers if default was entered for limits
        if params['rotlim2'] == 0:
            params['rotlim2'] = tot
        if params['tiltlim2'] == 0:
            params['tiltlim2'] = tot
        if params['psilim2'] == 0:
            params['psilim2'] = tot

        if params['debug'] is True:
            print params['rotlim2']
            print params['tiltlim2']
            print params['psilim2']

        #Remove particles in over-represented views & write into new file {particle}_reweight.star 
        reweight_starfile(params['stareuler'],params['starparticle'],params['rotlim1'],params['rotlim2'],params['tiltlim1'],params['tiltlim2'],params['psilim1'],params['psilim2'],params['debug'])
