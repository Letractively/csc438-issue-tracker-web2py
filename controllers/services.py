# -*- coding: utf-8 -*-

def index():
    return dict(message='test')

"""xmlrpc call"""
def newissue():
    from gluon.utils import web2py_uuid 
    projectIn=1
    summaryIn='summary from services'
    descriptionIn='test description services'
    statusIn='New'
    ownerIn='bmbarnard@gmail.com'
    uuidIn=web2py_uuid()
    result=db.issue.insert(project=projectIn,
            summary=summaryIn,
            description=descriptionIn,
            status=statusIn,
            owner=ownerIn,
            uuid=uuidIn)
    return dict(result=result)
