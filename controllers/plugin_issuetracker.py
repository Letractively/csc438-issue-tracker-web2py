# -*- coding: utf-8 -*-
"""
samlple variables
plugin_issuetracker_host='test'
plugin_issuetracker_user='bmbarnard'
plugin_issuetracker_pwd=''
plugin_issuetracker_projectid=1
"""

def ping():
    import xmlrpclib
    server=xmlrpclib.ServerProxy(plugin_issuetracker_host)
    
    try:
        result=server.ping()
    except xmlrpclib.Fault, err:
        result = 'an error occurred '
        result += str(err.faultCode)
        result += err.faultString
    return dict(result=result) 

"""default index function for testing"""
def index():    
    return dict(message='plugin_issuetracker config variables',
    issuetracker_host=plugin_issuetracker_host,
    issuetracker_user=plugin_issuetracker_user,
    issuetracker_pwd=plugin_issuetracker_pwd,
    issuetracker_projectid=plugin_issuetracker_projectid)

"""submit new issue to remote issue_tracker"""
def postnewissue():
    result=''    
    form = SQLFORM.factory(
        Field('summary', requires=IS_NOT_EMPTY()),
        Field('description', requires=IS_NOT_EMPTY()),
        Field('owner', requires=IS_NOT_EMPTY()))
    
    #handle submission
    if form.process().accepted:
        
        import xmlrpclib
        server=xmlrpclib.ServerProxy(plugin_issuetracker_host)
        projectid=issuetracker_projectid=plugin_issuetracker_projectid
        
        #summary='test from plugin'
        summary=form.vars.summary
        
        #description='test description from plugin'
        description=form.vars.description
        
        #owner='bmbarnard@gmail.com'
        owner=form.vars.owner

        """attempt to submit new issue to remote tracker"""
        try:
            result=server.newissue(projectid, summary, description, owner)
            result=str(result)
            result='New Issue Submitted. Issue Number: ' + result
        except xmlrpclib.Fault, err:
            result = 'an error occurred '
            result += str(err.faultCode)
            result += err.faultString
            session.flash='Error submitting issue to remote issue tracker'
    elif form.errors:
        session.flash='form has errors'
    else:
        session.flash='form cannot be blank'
    return dict(form=form,result=result)
