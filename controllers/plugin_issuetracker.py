# -*- coding: utf-8 -*-

"""
samlple variables as they would be defined in config file (models/plugin_issuetracker.py)
plugin_issuetracker_host='test'
plugin_issuetracker_user='bmbarnard'
plugin_issuetracker_pwd=''
plugin_issuetracker_projectid=1
"""

"""
ping calls the ping function of the remote issue tracker application to test connectivity
"""
def ping():

    """import the xmlrpcib library to be able to make rpc calls""" 
    import xmlrpclib
    
    server=xmlrpclib.ServerProxy(plugin_issuetracker_host)
    
    try:
        result=server.ping()
    except xmlrpclib.Fault, err:
        result = 'an error occurred '
        result += str(err.faultCode)
        result += err.faultString
    return dict(result=result) 


"""
index function for debuging the variables that are defined in the config file for plugin_issuetracker
these are set at models/plugin_issuetracker.py
"""
def index():    
    return dict(message='plugin_issuetracker config variables',
    issuetracker_host=plugin_issuetracker_host,
    issuetracker_user=plugin_issuetracker_user,
    issuetracker_pwd=plugin_issuetracker_pwd,
    issuetracker_projectid=plugin_issuetracker_projectid)


"""
submit new issue to remote issue_tracker
"""
def postnewissue():
    
    """import the xmlrpcib library to be able to make rpc calls""" 
    import xmlrpclib 
    
    result=''    
   
   """define form for accepting variables for issue""" 
   form = SQLFORM.factory(
        Field('summary', requires=IS_NOT_EMPTY()),
        Field('description', requires=IS_NOT_EMPTY()),
        Field('owner', requires=IS_NOT_EMPTY()))
    
    #handle submission
    if form.process().accepted:
       
        """get variables from config file (models/plugin_issuetracker.py)"""
        server=xmlrpclib.ServerProxy(plugin_issuetracker_host)
        projectid=issuetracker_projectid=plugin_issuetracker_projectid
       
        """get variables from the form"""
        summary=form.vars.summary
        description=form.vars.description
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
