#!/usr/bin/env python

import optparse
from sys import *
import os,sys,re
import linecache
import random

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --stareuler=<relion_star_file> --starparticle=<relion_star_file> [lims]")
        parser.add_option("--stareuler",dest="stareuler",type="string",metavar="FILE",
                help="Output Relion star from refinement/classification containing euler angles ")
        parser.add_option("--starparticle",dest="starparticle",type="string",metavar="FILE",
                help="Relion star file that will be reweighted based upon euler angles.")
        parser.add_option("--remove",dest="remove",type="int",metavar="INT",
                help="Number of particles to remove from preferential view")
        parser.add_option("--AngleRotLim1",dest="rotlim1",type="int",metavar="INT",default=-180,
                help="Lower limit for AngleRot. (Default=-180)")
        parser.add_option("--AngleRotLim2",dest="rotlim2",type="int",metavar="INT",default=180,
                help="Upper limit for AngleRot. (Default=180)")
        parser.add_option("--AngleTiltLim1",dest="tiltlim1",type="int",metavar="INT",default=0,
                help="Lower limit for AngleTilt. (Default=0)")
        parser.add_option("--AngleTiltLim2",dest="tiltlim2",type="int",metavar="INT",default=180,
                help="Upper limit for AngleTilt. (Default=180)")
        parser.add_option("--AnglePsiLim1",dest="psilim1",type="int",metavar="INT",default=-180,
                help="Lower limit for AnglePsi. (Default=-180)")
        parser.add_option("--AnglePsiLim2",dest="psilim2",type="int",metavar="INT",default=180,
                help="Upper limit for AnglePsi. (Default=180")
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

        #Open output file
        o1=open('%s_reweight.star' %(params['starparticle'][:-5]),'w')

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
        #Create temporary file
        tmp='tmpfile122.txt'
        if os.path.exists(tmp):
            os.remove(tmp)

        out=open(tmp,'w')

        counter=1

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
            if rot<rotlim1 or rot>rotlim2:
                flag=1
            if tilt<tiltlim1 or tilt>tiltlim2:
                flag=1
            if psi<psilim1 or psi>psilim2:
                flag=1
            if flag == 1:
                out.write('%i\n'%(counter))
            counter=counter+1

        #Randomly select from this particle list a set number to be included
        if os.path.exists('%s_222.txt' %(tmp[:-4])):
            os.remove('%s_222.txt' %(tmp[:-4]))
        out2=open('%s_222.txt' %(tmp[:-4]),'w')
        counter=1
        while counter<=remove:
            line=get_random_line(tmp)
            out2.write(line)
            counter=counter+1

        #Go through each line, decide if it should/shouldn't be included and write into new file

#============================
def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline() # skip this line to clear the partial line
    return file.readline()

#==============================
if __name__ == "__main__":

        #Get input options
        params=setupParserOptions()

        #Check that files exists
        checkConflicts(params)

        #Number of particles
        tot=getNumberParticlesRelion(params['stareuler'])

        if params['debug'] is True:
            print params['rotlim2']
            print params['tiltlim2']
            print params['psilim2']

        #Remove particles in over-represented views & write into new file {particle}_reweight.star
        reweight_starfile(params['stareuler'],params['starparticle'],params['rotlim1'],params['rotlim2'],params['tiltlim1'],params['tiltlim2'],params['psilim1'],params['psilim2'],params['debug'],tot,params['remove'])
