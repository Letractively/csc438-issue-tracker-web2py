# -*- coding: utf-8 -*-

def index():
        return dict(message='services controller index')

"""create new issue service """


@service.xmlrpc
def newissue(pid, smy, des, own):
    from gluon.utils import web2py_uuid 
    
    """set variables"""
    projectIn=pid
    #projectIn = 1
    
    summaryIn=smy
    #summaryIn = 'test test 123'
    
    descriptionIn=des
    #descriptionIn = 'test test 123'
    
    ownerIn=own
    #ownerIn = 'bmbarnard@gmail.com'
    
    statusIn='New'
    uuidIn=web2py_uuid()
    
    """insert to db"""
    result=db.issue.insert(project=projectIn, summary=summaryIn, description=descriptionIn, status=statusIn, owner=ownerIn, uuid=uuidIn)
    
    """return result"""
    return str(result)

@service.xmlrpc
def ping():
    from socket import gethostname
    return 'successful response from issue_tracker service at: ' + gethostname()

"""service call handler"""
"""@auth.requires_login"""
def call():
    session.forget()
    return service()
