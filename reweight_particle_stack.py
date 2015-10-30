#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
import linecache
import random
import shutil
import numpy as np

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --stareuler=<relion_star_file> --starparticle=<relion_star_file> [lims]")
        parser.add_option("--stareuler",dest="stareuler",type="string",metavar="FILE",
                help="Output Relion star from refinement/classification containing euler angles ")
        parser.add_option("--starparticle",dest="starparticle",type="string",metavar="FILE",
                help="Relion star file that will be reweighted based upon euler angles.")
        parser.add_option("--remove",dest="remove",type="int",metavar="INT",
                help="Number of particles to remove from preferential view, specified WITHIN the limits below")
        parser.add_option("--AngleRotLim1",dest="rotlim1",type="int",metavar="INT",default=-180,
                help="Lower limit for AngleRot.")
        parser.add_option("--AngleRotLim2",dest="rotlim2",type="int",metavar="INT",default=180,
                help="Upper limit for AngleRot.")
        parser.add_option("--AngleTiltLim1",dest="tiltlim1",type="int",metavar="INT",default=0,
                help="Lower limit for AngleTilt.")
        parser.add_option("--AngleTiltLim2",dest="tiltlim2",type="int",metavar="INT",default=180,
                help="Upper limit for AngleTilt.")
        parser.add_option("--AnglePsiLim1",dest="psilim1",type="int",metavar="INT",default=-180,
                help="Lower limit for AnglePsi.")
        parser.add_option("--AnglePsiLim2",dest="psilim2",type="int",metavar="INT",default=180,
                help="Upper limit for AnglePsi.")
        parser.add_option("--saveremoved", action="store_true",dest="savetemp",default=False,
                help="Flag to save list of particle numbers removed from original list.")
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

        if os.path.exists('%s_reweight.star' %(params['starparticle'][:-5])):
            print 'Error: File %s_reweight.star already exists. Exiting.' %(params['starparticle'][:-5])
            sys.exit()

        if not params['remove']:
            print 'Error: No variable specified for number of particles to remove. Exiting.'
            sys.exit()

        if params['savetemp'] is True:
            if os.path.exists('%s_particlesRemoved.star' %(params['stareuler'][:-5])):
                print 'Error: File %s_particlesRemoved.star already exists. Exiting.' %(params['stareuler'][:-5])
                sys.exit()

        if params['rotlim2'] < params['rotlim1']:
            print 'Error: AngleRotLim2 < AngleRotLim1. Exiting'
            sys.exit()

        if params['tiltlim2'] < params['tiltlim1']:
            print 'Error: AngleTiltLim2 < AngleTiltLim1. Exiting'
            sys.exit()

        if params['psilim2'] < params['psilim1']:
            print 'Error: AnglePsiLim2 < AnglePsiLim1. Exiting'
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
def getNumberofLinesRelionHeader(star):

    f1=open(star,'r')
    tot=0

    for line in f1:
        if len(line) < 50:
            tot=tot+1
    f1.close()

    return tot

#==============================
def getNumberParticlesRelion(star):

    f1=open(star,'r')
    tot=0

    for line in f1:
        if len(line) > 50:
            tot=tot+1

    f1.close()

    return tot

#==============================
def reweight_starfile(euler,particle,rotlim1,rotlim2,tiltlim1,tiltlim2,psilim1,psilim2,debug,tot,remove):

        #Get column numbers for euler angles
        colrot=getRelionColumnIndex(euler,'_rlnAngleRot')
        coltilt=getRelionColumnIndex(euler,'_rlnAngleTilt')
        colpsi=getRelionColumnIndex(euler,'_rlnAnglePsi')

        if not colrot:
            print 'Could not find _rlnAngleRot in header of %s. Exiting' %(euler)
            sys.exit()
        if not coltilt:
            print 'Could not find _rlnAngleTilt in header of %s. Exiting' %(euler)
            sys.exit()
        if not colpsi:
            print 'Could not find _rlnAnglePsi in header of %s. Exiting' %(euler)
            sys.exit()

        #Find number of particles that need to be removed & write into temp file
        #Create temporary file
        tmp='tmpfile122.txt'
        if os.path.exists(tmp):
            os.remove(tmp)


#####TO DO
#create random list without replacement containing the number of entries in tmpfile
#then, read each line of tmpfile, asking if it is in teh random array
#If in random array, write to new text file
#Now, loop over all particles, and check if given particle is in the 'bad list', if so, do not write to output file .

        out=open(tmp,'w')

        counter=1
        particlecounter=1

        while counter <= tot:
            line=linecache.getline(euler,counter)

            if len(line) < 50:
                counter=counter+1
                continue

            l=line.split()

            rot=float(l[int(colrot)-1])
            tilt=float(l[int(coltilt)-1])
            psi=float(l[int(colpsi)-1])

            flag=0
            if debug is True:
                print rot
                print tilt
                print psi

            if rotlim1 > -180:
                if rotlim2 < 180:
                    if rot>rotlim1 and rot<rotlim2:
                        flag=1
                        if debug is True:
                            print 'flagged b/c of rot'

            if tiltlim1 >0:
                if tiltlim2<180:
                    if tilt>tiltlim1 and tilt<tiltlim2:
                        flag=1
                        if debug is True:
                            print 'flagged b/c of tilt'

            if psilim1 > -180:
                if psilim2 < 180:
                    if psi>psilim1 and ps<psilim2:
                        flag=1
                        if debug is True:
                            print 'flagged b/c of psi'
            if flag == 1:
                out.write('%i\n'%(particlecounter))
            counter=counter+1
            particlecounter=particlecounter+1

        out.close()

        #Get number of lines in tmpfile
        numLinesTemptFile=len(open(tmp,'r').readlines())

        #Throw error if number to be removed is greater than number in group
        if remove>numLinesTemptFile:
            print 'Error: Number of particles to removed from euler angle range is greater than the number of particles in given group. Check tmpfile122.txt for number of particles that are in euler angle group.Exiting'
            sys.exit()

        #Create numpy list of random numbers withOUT replacement to be removed
        toberemoved=np.random.choice(numLinesTemptFile,remove,replace=False)

        #Create new text file from which actual bad particle numbers will be stored
        tmp2='tmpfile122_sel.txt'
        if os.path.exists(tmp2):
            os.remove(tmp2)
        tmpread=open(tmp,'r')
        tmp2out=open(tmp2,'w')
        counter=1

        for line in tmpread:

            if counter in toberemoved:
                tmp2out.write(line)

            counter=counter+1

        tmp2out.close()
        tmpread.close()

        badparticlelist=np.loadtxt(tmp2)

        #Write header lines from edited file into new file header
        particleopen=open(particle,'r')
        particlewrite=open('%s_reweight.star' %(particle[:-5]),'w')
        counter=1
        counter=1
        for line in particleopen:
            if counter<80:
                if len(line)<50:
                    particlewrite.write(line)
            counter=counter+1

        #Get number of lines in header for edited file
        header_particle=getNumberofLinesRelionHeader(particle)-1
        if debug is True:
            outtemp=open('tmpout_flaggedtoberemoved.txt','w')
            print 'Number of lines in header: %i' %(header_particle)

        #Go through each line, decide if it should/shouldn't be included and write into new file
        euler_open=open(euler,'r')
        counter=1

        #Particlesremoved
        outtmp=open('%s_linesRemoved.txt'%(tmp[:-4]),'w')

        for line in euler_open:

            if len(line) < 50:
                counter=counter+1
                continue

            #Debug print
            #if debug is True:
                #print 'Working on particle %i in euler file' %(counter)
                #print 'Euler line: %s' %(line)

            #Check if this particle is to be removed
            #remove_flag=checkInList('tmpfile122_222.txt',counter)
            remove_flag=0

            if (counter-header_particle) in badparticlelist:
                remove_flag=1

            if not (counter-header_particle) in badparticlelist:
                remove_flag=0

            #Determine corresponding line number in edited file for this particle
            particle_num=counter

            #Get line from file
            particle_line=linecache.getline(particle,particle_num)

            #if debug is True:
                #print 'Particle %i is on line %i in %s' %(counter,particle_num,particle)
                #print 'Particle line: %s' %(particle_line)

            if remove_flag == 0:
                particlewrite.write(particle_line)
                #if debug is True:
                    #'Writing particle %i to new file' %(counter)

                if debug is True:
                    outtemp.write('%s\n' %(str(remove_flag)))

            counter=counter+1
        return badparticlelist
#============================
def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    return file.readline()

#==============================
def checkInList(badlist,checknum):

    readingfile=open(badlist,'r')

    flag=0

    for line in readingfile:
        #print float(line.split()[0])
        #print float(checknum)
        if float(line.split()[0]) == float(checknum):
            flag=1

    readingfile.close()
    return flag

#==============================
if __name__ == "__main__":

        #Get input options
        params=setupParserOptions()

        #Check that files exists
        checkConflicts(params)

        #Number of particles of euler file
        tot=getNumberParticlesRelion(params['stareuler'])

        #Number of particles in file that will be edited (Should be same number of particles!)
        tot2=getNumberParticlesRelion(params['starparticle'])

        if tot != tot2:
            print 'Error: %s and %s do not have the same number of particles: %i in %s and %i in %s. Exiting.' %(params['stareuler'],params['starparticle'],tot,params['stareuler'],tot2,params['starparticle'])
            sys.exit()

        if params['debug'] is True:
            print params['rotlim1']
            print params['rotlim2']
            print params['tiltlim1']
            print params['tiltlim2']
            print params['psilim1']
            print params['psilim2']

        #Remove particles in over-represented views & write into new file {particle}_reweight.star
        npout=reweight_starfile(params['stareuler'],params['starparticle'],params['rotlim1'],params['rotlim2'],params['tiltlim1'],params['tiltlim2'],params['psilim1'],params['psilim2'],params['debug'],tot,params['remove'])

        #Save temporary list of particles that were excluded
        if params['savetemp'] is True:
            np.savetxt('%s_particlesRemoved.txt' %(params['stareuler'][:-5]),npout,fmt='%i')

        #Clean up
        if params['debug'] is False:
            os.remove('tmpfile122.txt')
            os.remove('tmpfile122_sel.txt')
            os.remove('tmpfile122_linesRemoved.txt')
