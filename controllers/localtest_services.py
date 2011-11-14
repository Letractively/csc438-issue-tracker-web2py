# -*- coding: utf-8 -*-

"""call the test webservice"""
def test():
    import xmlrpclib
    server=xmlrpclib.ServerProxy('http://127.0.0.1:8000/issue_tracker/services/call/xmlrpc')
    return str(server.test())


"""xmlrpc call to create new issue"""
def newissue_test():
    import xmlrpclib
    from gluon.utils import web2py_uuid 
    projectIn=1
    summaryIn='summary from services'
    descriptionIn='test description services'
    ownerIn='bmbarnard@gmail.com'
    
    """call service"""
    import xmlrpclib
    server=xmlrpclib.ServerProxy('http://127.0.0.1:8000/issue_tracker/services/call/xmlrpc')
    #return str(server.newissue(projectIn, summaryIn, descriptionIn, ownerIn))
    
    try:
        result = server.newissue()
    except xmlrpclib.Fault, err:
        result = 'an error occurred'
        result += str(err.faultCode)
        result += err.faultString
    return str(result)
