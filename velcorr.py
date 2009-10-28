#!/usr/bin/env python
"""
README:

Input format: RA.xxx DEC.xxx YYYY MM DD HH MM SS
(omitting one or several numbers at the end of the list is allowed)

RA and DEC must be J2000. Date and time in UTC.
If you get thrown back to the standard values instead of your input
then you probably had erroneous input.

The calculated values are corrections to measured velocites that stem
from the the observers motion with respect to different reference
frames:

 * Earth rotation wrt center of earth. (not implemented)
 * Earth orbit around the sun. 
   (calculated relative to spring equinox 2000 by conversion to
    ecliptic coordinates, taking the 50"/year shift of the spring
    point into account)
 * Solar system orbit in the Milky Way. (not implemented)
 * Milky Way motion wrt to the CMBR. (not implemented)

The values are the corrections to the next frame, i.e. they have to be
added togethether. Positive/negative numbers mean that the
measurement was redshifted/blueshifted respectively, i.e. the values
need to be SUBTRACTED from the measured velocities.

No guarantee for correctness. Feedback, bug reports and implementations 
of the missing corrections are welcome to thomas AT marquart DOT se.

View the source code here: http://astroweb.tmy.se/src/velcorr

"""

import coords as C              # this is from astrolib
from datetime import datetime
from math import pi,sin,cos,radians

au = 1.4959787e8   # in km
yr = 31556926.0    # in seconds
dy = 86400.0       # in sec
circ = 2*pi*au     # earth orbit circumference
vmax = circ/yr     # earths real velocity: 29.78 km/s
rashift = 50/3600. # sping point shifts 50" / year
peryear = 360+rashift # the earth moves this much per year

# equinox in 2000 (leap year) was on march 20, 7:35
equinox2000 = 2000.2157863715865

class velcorr(object):
    def __init__(self,ra=0,dec=0,year=2000,month=12,day=15,hour=12,min=0,sec=0):
        self.pos=C.Position((ra,dec))
        self.datime=C.AstroDate(datetime(*map(int,(year,month,day,hour,min,sec))))
        self.fracyr=self.datime.year - equinox2000
        
        self.earthcorr()
        self.heliocorr()
        self.galacorr()
        self.cmbcorr()

    def earthcorr(self):
        self.earthvel=0.0
        return self.earthvel
    
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

    def __repr__(self):
        d=self.datime.datespec
        return '%.3f %.3f %04d %02d %02d %02d %02d %02d'%\
            (self.pos.j2000()[0],self.pos.j2000()[1],d.year,d.month,d.day,d.hour,d.minute,d.second)

    def html_result(self):
        result='<p>Velocity correction from...<ul>'
        result+='<li> earth rotation: %.2f km/s</li>'%self.earthvel
        result+='<li> earth orbit: %.2f km/s</li>'%self.heliovel
        result+='<li> solar system orbit: %.2f km/s</li>'%self.galavel
        result+='<li> galaxy to cmbr: %.2f km/s</li>'%self.cmbvel
	result+='</ul></p>'
	return result

def check_data(data):
    if not data: return None
    out=''
    for c in data:
	if c in '0123456789.- ': out+=c
    out=out.split()[:8]
    if len(out)<4: return None
    for i,o in enumerate(out):
        try: out[i]=float(o)
        except: out[i]=0.0
        if i >1: out[i]=int(o)
    if (out[0]<0.0) or (out[0]>360.0): return None
    if (out[1]<-90.0) or (out[1]>90.0): return None
    if (out[2]<1000) or (out[2]>3000): return None
    if (out[3]<1) or (out[3]>12): return None
    try: 
	if (out[4]<1) or (out[4]>31): return None
        if (out[5]<0) or (out[5]>23): return None
        if (out[6]<0) or (out[6]>59): return None
        if (out[7]<0) or (out[7]>59): return None
    except: pass
    return out

def velcorr_web(form):
    data=form.getfirst('data')
    data=check_data(data)
    if not data: vc=velcorr()
    else: vc=velcorr(*data)
    result='<p></p>'
    result+='<p><FORM ACTION="/velcorr/" METHOD="POST">'
    result+='<input type="text" maxlength="35" size="35" value="%s" name="data" />&nbsp;'%vc
    result+='<INPUT TYPE="submit" VALUE="CALCULATE" NAME="send"></p>'
    result+=vc.html_result()
    result+='<p><pre>%s</pre></p>'%__doc__
    
    return result


#if __name__ == '__main__':
#    from sys import argv
#    vc=velcorr(*map(float,argv[1:]))
#    print vc.heliovel
#    print vc
