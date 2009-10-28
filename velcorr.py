#!/usr/bin/env python
"""
README:

The values given above are corrections to measured velocites that stem
from the the observers motion with respect to different reference
frames.

 * Earth rotation wrt earth center motion. (not implemented)
 * Earth center motion wrt to the sun.
 * Suns motion inside the Milky Way. (not implemented)
 * Milky Way motion wrt to the CMBR. (not implemented)

The values are the corrections to the next frame, i.e. they have to be
added togethether. Positive and negative numbers mean that the
measurment as redshifted and blueshifted respectively, i.e. the values
need to be SUBTRACTED from the measured velocities.

No guarantee for correctness. Feedback, bug reports and
implementations of the missing corrections are welcome to thomas AT
marquart DOT se.

"""

import coords as C
from datetime import datetime
from sys import argv
from math import pi,sin,cos,radians

au=1.4959787e8 # in km
yr=31556926.0    # in seconds
dy=86400.0       # in sec
circ=2*pi*au   # earth orbit circumference
vmax=circ/yr   # earths real velocity: 29.78 km/s
rashift=50/3600. # sping point shifts 50" / year
peryear=360+rashift # the earth moves this much per year

# equinox in 2000 (leap year) was on march 20, 7:35
equinox2000 = 2000.2157863715865

galrad=0
sunvel=0


class velcorr(object):
    def __init__(self,ra=0,dec=0,year=2000,month=3,day=20,hour=7,min=35,sec=0):
        self.pos=C.Position((ra,dec))
        self.datime=C.AstroDate(datetime(*map(int,(year,month,day,hour,min,sec))))
        self.fracyr=self.datime.year - equinox2000
        
        self.heliocorr()
        self.galacorr()
        self.earthcorr()
        self.cmbcorr()

    def heliocorr(self):
        ra_ecl,dec_ecl=self.pos.ecliptic(timetag='j2000')
        earth_ra_ecl=(self.fracyr * peryear) %360
        self.heliovel= vmax *\
            sin(radians(ra_ecl - earth_ra_ecl)) * \
            cos(radians(dec_ecl))
        self.heliovel *= -1
        return self.heliovel

    def galacorr(self):
        self.galavel=0.0
        return self.galavel

    def cmbcorr(self):
        self.cmbvel=0.0
        return self.cmbvel

    def earthcorr(self):
        self.earthvel=0.0
        return self.earthvel
    
    def __repr__(self):
        d=self.datime.datespec
        return '%.3f %.3f %04d %02d %02d %02d'%(self.pos.j2000()[0],self.pos.j2000()[1],d.year,d.month,d.day,d.hour)

def velcorr_web(velcorr):
    result='<p></p>'
    result+='<p><FORM ACTION="/velcorr" METHOD="POST">'
    result+='RA.xxx DEC.xxx YYYY MM DD HH [MM SS]: <input type="text" maxlength="30" size="30" value="%s" name="data" /><br/>'%velcorr
    result+='<INPUT TYPE="submit" VALUE="SKICKA" NAME="send"></p>'
    
    return result


if __name__ == '__main__':
    vc=velcorr(*map(float,argv[1:]))
    print vc.heliovel
    print vc
    #print __doc__
