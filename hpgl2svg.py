#!/usr/bin/env python

import sys

pens    = {}
curpen  = None

hpgl_pts_in = 955.0

at          = (float(sys.argv[3]),float(sys.argv[4]))

with open(sys.argv[2], 'w') as svg:
    print >> svg, '''<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg version="1.0" xmlns="http://www.w3.org/2000/svg"  xmlns:xlink="http://www.w3.org/1999/xlink" width="5in" height="5in" viewBox="-2.5 -2.5 5 5">
<defs>
<g id="hpgl2svg">
    <path d="'''

    with open(sys.argv[1]) as hpgl:
        for line in [x.strip() for x in hpgl.readlines()]:
            if len(line.strip()) == 0: continue
            cmd     = line[0:2]
            rem     = line[2:]
            if cmd == 'CO':
                pass # comment
            elif cmd == 'IN':
                pass # initialize
            elif cmd == 'IP':
                pass # set origin
            elif cmd == 'SC':
                pass # set scale
            elif cmd == 'SP':
                curpen  = int(rem.strip(';'))
                if curpen not in pens.keys():
                    pens[curpen]    = (0,0)
            elif cmd == 'PU':
                pens[curpen]        = tuple([int(x.strip().strip(';'))/hpgl_pts_in for x in rem.split(',')])
                print >> svg, "M %f,%f "%(pens[curpen][0]+at[0],pens[curpen][1]+at[1])
            elif cmd == 'PD':
                parts   = [int(x.strip().strip(';'))/hpgl_pts_in for x in rem.split(',')]
                pts     = [(parts[2*i],parts[2*i+1]) for i in xrange(len(parts)/2)]
                print >> svg, "l",
                for pt in pts:
                    oldpen          = pens[curpen]
                    pens[curpen]    = (pt[0],pt[1])
                    print >> svg, "%f,%f "%(pens[curpen][0]-oldpen[0],pens[curpen][1]-oldpen[1])
            elif cmd == 'CI':
                radius  = int(rem)
                pass # circle with radius
            elif cmd == 'SS':
                pass # select standard font
            elif cmd == 'DT':
                pass # select text delimiter
            elif cmd == 'LB':
                pass # draw label
            elif cmd == 'LT':
                pass # set linetype
            elif cmd == 'CS':
                pass # set caracter set
            elif cmd == 'DI':
                pass # set catheti
            elif cmd == 'SI':
                pass # set character width & height
            else:
                raise Exception('Unknown HPGL code "%s".'%line)


    print >> svg, '''" stroke="red" stroke-width="0.01" fill="none"/>
</g>
</defs>
<line x1="-.126" y1="0" x2=".126" y2="0" stroke-width="0.02" fill="black" stroke="blue" />
<line y1="-.126" x1="0" y2=".126" x2="0" stroke-width="0.02" fill="black" stroke="blue" />
<use xlink:href="#hpgl2svg" x="0" y="0"/>
</svg>'''
