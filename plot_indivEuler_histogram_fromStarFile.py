#!/usr/bin/env python

from pylab import *
from matplotlib.colors import LogNorm
import numpy as np
import matplotlib.pyplot as plt
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
                help="Name of Relion euler angle designation: AngleRot,AngleTilt, AnglePsi. Provide two angle names (e.g. AngleRot,AngleTilt) for a 2D heat map of euler angles")
        parser.add_option("--binsize",dest="bin",type="int",metavar="INT",default=5,
                help="Optional: bin size for histogram of euler angles (Default=5)")
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

        if len(params['rlnEuler'].split(',')) == 1:

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
def plotEuler_single(star,colnum,debug,rln):

    #open star file
    f1=open(star,'r')

    #remove temporary file
    tmp='tmp_relion_star.star'
    if os.path.exists(tmp):
        os.remove(tmp)

    #open for writing into new tmp file without header
    o1=open(tmp,'w')

    for line in f1:
        if len(line)<50:
            continue
        o1.write(line)

    o1.close()
    f1.close()

    usecolumn=int(colnum-1)

    eulers=np.loadtxt(tmp,usecols=[usecolumn])

    #Get number of particles
    tot=len(open(tmp,'r').readlines())

    #Create bins:
    if rln == 'AngleTilt':
        bins=np.arange(0,180,params['bin'])
        random_thresh=tot/(180/params['bin'])

    if rln == 'AngleRot':
        bins=np.arange(-180,180,params['bin'])
        random_thresh=tot/(360/params['bin'])

    if rln == 'AnglePsi':
        bins=np.arange(-180,180,params['bin'])
        random_thresh=tot/(360/params['bin'])

    #Plot histogram
    plt.hist(eulers,bins=bins)
    plt.title("%s euler angle histogram\n (Random distribution = %s per bin)" %(rln,str(random_thresh)))
    plt.xlabel("%s" %(rln))
    plt.ylabel("Number of particles")
    plt.show()

#==============================
def plotEuler_double(star,colnum1,rln1,colnum2,rln2,debug):

    #open star file
    f1=open(star,'r')

    #remove temporary file
    tmp='tmp_relion_star.star'
    if os.path.exists(tmp):
        os.remove(tmp)

    #open for writing into new tmp file without header
    o1=open(tmp,'w')

    for line in f1:
        if len(line)<50:
            continue
        o1.write(line)

    o1.close()
    f1.close()

    usecolumn1=int(colnum1-1)
    usecolumn2=int(colnum2-1)

    eulers1=np.loadtxt(tmp,usecols=[usecolumn1])
    eulers2=np.loadtxt(tmp,usecols=[usecolumn2])

    #Get number of particles
    tot=len(open(tmp,'r').readlines())

    #Create bins:
    if rln1 == 'AngleTilt':
        bins1=np.arange(0,180,params['bin'])

    if rln1 == 'AngleRot':
        bins1=np.arange(-180,180,params['bin'])

    if rln1 == 'AnglePsi':
        bins1=np.arange(-180,180,params['bin'])

    if rln2 == 'AngleTilt':
        bins2=np.arange(0,180,params['bin'])

    if rln2 == 'AngleRot':
        bins2=np.arange(-180,180,params['bin'])

    if rln2 == 'AnglePsi':
        bins2=np.arange(-180,180,params['bin'])

    #Random threshold
    random_thresh=tot/(len(bins1)*len(bins2))

    #Plot histogram
    plt.hist2d(eulers1,eulers2,bins=[bins1,bins2])
    plt.colorbar()
    plt.title("%s vs. %s euler angle histogram\n (Random distribution = %s per bin)" %(rln1,rln2,str(random_thresh)))
    plt.xlabel("%s" %(rln1))
    plt.ylabel("%s" %(rln2))
    plt.show()

#==============================
if __name__ == "__main__":

        params=setupParserOptions()

        #Check that file exists & relion euler designation is real
        rln=checkConflicts(params)
        if len(params['rlnEuler'].split(',')) == 1:
            if rln == 'empty':
                print 'Error: Unrecognized Relion euler angle designation %s. Must be AngleRot, AngleTilt, AnglePsi' %(params['rlnEuler'])
                sys.exit()

        #Get column number for euler designation
        if len(params['rlnEuler'].split(',')) == 1:
            columnindex=getRelionColumnIndex(params['star'],rln)
            plotEuler_single(params['star'],int(columnindex),params['debug'],params['rlnEuler'])

        if len(params['rlnEuler'].split(',')) == 2:
            columnindex1=getRelionColumnIndex(params['star'],'_rln'+params['rlnEuler'].split(',')[0])
            columnindex2=getRelionColumnIndex(params['star'],'_rln'+params['rlnEuler'].split(',')[1])
            plotEuler_double(params['star'],int(columnindex1),params['rlnEuler'].split(',')[0],int(columnindex2),params['rlnEuler'].split(',')[1],params['debug'])

        if len(params['rlnEuler'].split(',')) > 2:
            print 'Error: too many angles specified at once. Exiting'
            sys.exit()
