#!/usr/bin/env python
"""

Documentation:


"""

from xml.dom.minidom import parseString
import urllib
from sys import argv
from os.path import exists
from string import join

URLBASE='http://www.stsci.edu/observing/phase2-public/'
TMP='/tmp/'
SEARCH_RADIUS= 1 /60.  # in arcmin

def sdss_url(name,ra,dec):
   return  'http://cas.sdss.org/DR6/en/tools/search/x_radial.asp?ra=%.4f&dec=%.4f&radius=%.4f&format=html&entries=all'%(ra,dec,SEARCH_RADIUS)
    
def download_or_read(id):
    fname=TMP+'phas2_%s.xml'%id
    if not exists(fname):
        url='%s%s.apt'%(URLBASE,id)
        raw_xml = urllib.urlopen(url).read()
        f=open(fname,'w')
        f.write(raw_xml)
        f.close()
    else:
        raw_xml = open(fname).read()

    return parseString(raw_xml)

def myparse(dom):
    namepos=[]
    for target in dom.getElementsByTagName('FixedTarget'):
        tname=target.attributes['Name'].value
        pos=target.getElementsByTagName('EquatorialPosition')[0]
        h=pos.getElementsByTagName('RA')[0].attributes['Hrs'].value
        m=pos.getElementsByTagName('RA')[0].attributes['Mins'].value
        s=pos.getElementsByTagName('RA')[0].attributes['Secs'].value
        h,m,s=map(float,(h,m,s))
        ra=(h + (m/60.) + (s/3600.))*15
        d=pos.getElementsByTagName('DEC')[0].attributes['Degrees'].value
        m=pos.getElementsByTagName('DEC')[0].attributes['Arcmin'].value
        s=pos.getElementsByTagName('DEC')[0].attributes['Arcsec'].value
        d,m,s=map(float,(d,m,s))
        dec=d + (m/60.) + (s/3600.)
        namepos.append((tname, ra, dec))
    return namepos

def prep_data(data):
    if not data: return None
    out=''
    for c in data:
	if c in '0123456789': out+=c
    return out

def handle_rid(rid):
    if rid==0: return ''
    dom=download_or_read(rid)
    namepos=myparse(dom)
    result=''
    for po in namepos:
       result+='<h3>%s</h3>'%po[0]
       url=sdss_url(*po)
       result+='<iframe src="%s" width="100%" height="300" />'%(url,)
    return result


def hst2sdss(form):
    rid=prep_data(form.getfirst('data'))
    result='<p></p>'
    result+='<p><FORM ACTION="/hst2sdss/" METHOD="POST">'
    result+='<input type="text" maxlength="15" size="15" value="%s" name="data" />&nbsp;'%0
    result+='<INPUT TYPE="submit" VALUE="SEND" NAME="send"></p>'
    if not rid: result+=handle_rid(0)
    else: result+=handle_rid(rid)
    result+='<p><pre>%s</pre></p>'%__doc__
    
    return result


def main():
   for id in argv[1:]:
        dom=download_or_read(id)
        namepos=myparse(dom)

        for po in namepos:
            url=sdss_url(*po)
            #urllib.urlopen(url).read()
            print url
        


if __name__=='__main__':
    main()
