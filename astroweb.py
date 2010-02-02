#!/usr/bin/env python
"""
the mod_python interface
"""

from mod_python import apache,util
from os.path import join,exists
import sys

sys.path.append('/home/tom/py')

from velcorr import velcorr,velcorr_web

from hst2sdss import hst2sdss

BASE=join('/','home','tom','sites','astroweb')

def filecontent(filename,base=BASE):
    f=open(join(base,filename))
    content=f.read()
    f.close()
    return content

def startpage():
    result='<p>'
    result+='This is where I will put up a few astronomy tools.<br/>'
    result+='Up to now, there is only '
    result+='<a href="/velcorr/">velocity correction</a>.'
    result+='<a href="/hst2sdss/">get SDSS matches from a HST proposal ID</a>.'
    result+='</p>'
    return result

def handler(req):
    req.content_type = "text/html"
    form=util.FieldStorage(req)

    req.write(filecontent('head'))

    if req.uri == '/velcorr/': result=velcorr_web(form)
    elif req.uri == '/src/velcorr/': result='<pre>%s</pre>'%filecontent('velcorr.py').replace('<','&lt;').replace('>','&gt;')
    elif req.uri == '/hst2sdss/': result=hst2sdss(form)
    
    else: result= startpage()

    req.write(result.encode('ascii','xmlcharrefreplace'))

    req.write(filecontent('foot'))
    return apache.OK

