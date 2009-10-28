#!/usr/bin/env python
"""
the mod_python interface
"""

from mod_python import apache,util
from os.path import join,exists

from velcorr import velcorr,velcorr_web

BASE=join('/','home','tom','sites','astroweb')

def filecontent(filename,base=BASE):
    f=open(join(base,filename))
    content=f.read()
    f.close()
    return content

def handler(req):
    req.content_type = "text/html"
    form=util.FieldStorage(req)

    req.write(filecontent('head'))

    vc=velcorr()
    wanted=req.uri[1:]
    if wanted == 'velcorr': result=velcorr_web(form,vc)
    else:                   result='Don\'t know what to do with %s'%req.u
ri

    conn.commit()
    conn.close()

    req.write(result.encode('ascii','xmlcharrefreplace'))

    req.write(filecontent('foot'))
    return apache.OK

