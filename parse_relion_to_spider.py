#!/usr/bin/env python

#To run:
#./parse_relion_to_spi.py [relion data file]

import sys

f = sys.argv[1]
out = '%s.spi' %(f[:-5])
out2 = '%s_selectFile.spi' %(f[:-5])

f1 = open(f,'r')
o1 = open(out,'w')
o2 = open(out2,'w')

i = 1

for line in f1:
	
	if line[0] == '0': 

		l = line.split()
		sel = float(line[:6])
		sx = l[4]
		sy = l[5]
		phi = l[6]
		theta = l[7]
		psi = l[8]

		o1.write('%s\t5\t%s\t%s\t%s\t%s\t%s\n'%(str(i),psi,theta,phi,sx,sy))
		o2.write('%s\t1\t%s\n' %(str(i),str(sel)))		
		i = i + 1
