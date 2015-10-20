#!/usr/bin/env python

import numpy as np
import pylab as P
import optparse
from sys import *
import os,sys,re
import linecache

#=========================
def setupParserOptions():
        parser = optparse.OptionParser()
        parser.set_usage("%prog --starfile=<relion_star_file>")
        parser.add_option("--starfile",dest="star",type="string",metavar="FILE",
                help="Relion star file (data.star)")
        parser.add_option("--rlnEuler",dest="rlnEuler",type="string",metavar="STRING",
                help="Name of Relion euler angle designation: AngleRot,AngleTilt, AnglePsi")
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

        if not os.path.exists(params['star']):
            print 'Error: File %s does not exist' %(params['star'])
            sys.exit()

        if params['rlnEuler'] == 'AngleRot':
            return '_rlnAngleRot'

        if params['rlnEuler'] == 'AngleTilt':
            return '_rlnAngleTilt'

        if params['rlnEuler'] == 'AnglePsi':
            return '_rlnAnglePsi'

        return 'empty'

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

#===============================
def plotEuler(star,colnum,debug):

    #open star file
    f1=open(star,'r')

    #remove temporary file
    tmp='tmp_relion_star.star'
    if os.path.exists(tmp):
        os.remove(tmp)

    #open for writing
    o1=open(tmp,'w')

    for line in f1:
        if len(line)<50:
            continue
        o1.write(line)

    o1.close()
    f1.close()


#==============================
if __name__ == "__main__":

        params=setupParserOptions()

        #Check that file exists & relion euler designation is real
        rln=checkConflicts(params)
        if rln == 'empty':
            print 'Error: Unrecognized Relion euler angle designation %s' %(params['rlnEuler'])
            sys.exit()

        #Get column number for euler designation
        columnindex=getRelionColumnIndex(params['star'],rln)

        if params['debug'] is True:
            print 'rln variable=%s' %(rln)
            print 'index number=%s' %(columnindex)

        plotEuler(params['star'],int(columnindex),params['debug'])
