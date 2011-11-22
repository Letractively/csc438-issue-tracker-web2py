# -*- coding: utf-8 -*-

def index():
    return dict(message=T('Hello World'))


def projects():
    FIELDS=(db.project.id,db.project.name,db.project.created_by,db.project.manager,db.project.phase,db.project.repo)
    LINKS=[lambda row: A('Subprojects',_href=URL('projects',args=row.id)),
           lambda row: A('Issues',_href=URL('issues',args=row.id)),
           lambda row: A('Team',_href=URL('teams',args=row.id)) ]
    def check(row): return ((row.created_by == auth.user_id)|(row.manager == auth.user_id))
    if (request.args(0)):
        query = (db.project.super_project==request.args(0))
        #name = 'The subprojects of: '+ str(db(db.project.id==request.args(0)).select(db.project.name)).lstrip('project.name ')
    else:
        query = db.project
        #name = 'Project directory'
    grid = SQLFORM.grid(query,editable=check,deletable=check,
                        fields = FIELDS,links=LINKS)
    return dict(grid=grid)#name=name)
    
def teams():
    def check(row): 
        return (row.team_lead == auth.user_id)
    if (request.args(0)):
        query = (db.team.assigned_projects==request.args(0))
    else:
        query = db.team
    grid=SQLFORM.grid(query,editable=check,deletable=check)
    return dict(grid=grid)
    
    
@auth.requires_membership('managers')
def roles():
    manager_id = db(db.auth_group.role == 'managers').select().first().id
    query = (db.auth_membership.group_id == manager_id)
    grid = SQLFORM.grid(query,editable=False)
    return dict(grid=grid)
    

def issues():
    project = db.project(request.args(0)) or redirect(URL('projects'))
    status = request.args(1)
    query = (db.issue.project == project.id)&(db.issue.is_last==True)
    if not status or status=='Open':
        query = query&(db.issue.status.belongs(['New','Assigned','Accepted','Started']))
    elif status=='Closed':
        query = query&(db.issue.status.belongs(
                ['Fixed','Verified','Invalid','Duplicate','WontFix','Done']))
    elif status!='All':
        query = query&(db.issue.status==status)
    """comment"""
    from gluon.utils import web2py_uuid
    db.issue.project.default = project.id
    db.issue.uuid.default = web2py_uuid()
    db.issue.is_last.default = True
    db.issue.owner.default = project.created_by.email
    db.issue.description.default = DESCRIPTION
    db.issue.labels.represent = lambda v,r: ', '.join(v or [])
    if not auth.user or not (
        auth.user.id == project.created_by or \
            auth.user.email in (project.members_email or [])):
        db.issue.owner.writable = False
        db.issue.status.writable = False
    #COLUMNS=('issue.status','issue.summary','issue.created_on',
    #         'issue.author','issue.labels')
    FIELDS=(db.issue.id,db.issue.uuid,db.issue.status,db.issue.summary,db.issue.created_on,db.issue.author,db.issue.labels,)
    LINKS=[lambda row: A('issue',_href=URL('issue',args=row.uuid)),lambda row2:A('assign',_href=URL('assign',args=row2.uuid)),
           lambda row3: A('dependencies',_href=URL('dependencies',args=row3.id))]
    grid = SQLFORM.grid(query, fields = FIELDS,links=LINKS,
                        details=False,editable=False,
                        deletable=project.created_on==auth.user_id,
                        create=auth.user_id,args=[project.id],
                        oncreate=lambda form:do_mail([db.issue(form.vars.id)]))
    return dict(grid=grid, project=project)

def issue():
    last = db(db.issue.uuid==request.args(0))\
        (db.issue.is_last==True).select().first()
    project = db.project(last.project) or redirect(URL('projects'))
    if auth.user:
        db.issue.status.default = last.status
        db.issue.summary.default = last.summary
        db.issue.project.default = last.project
        db.issue.uuid.default = last.uuid
        db.issue.is_last.default = True
        db.issue.owner.default = last.owner
        db.issue.labels.default = last.labels
        if not (auth.user.id == project.created_by or \
                    auth.user.email == last.owner or \
                    auth.user.email in (project.members_email or [])):
            db.issue.owner.default = project.created_by
            db.issue.owner.writable = False
            db.issue.status.writable = False
        form = SQLFORM(db.issue)
        if form.process().accepted:
            last.update_record(is_last=False)
    else:
        form = DIV('login to comment')
    items = db(db.issue.uuid==request.args(0)).select(
        orderby=db.issue.created_on)
    if isinstance(form,FORM) and form.accepted: do_mail(items)
    return dict(project=project,form=form,items=items,last=last)

@auth.requires_login()
def assign():
    issue = request.args(0)
    issue = db(db.issue.uuid==issue).select().first()
    project = db.project(issue.project) or redirect(URL('projects'))
    if auth.user:
        db.issue.status.default = issue.status
        db.issue.summary.default = issue.summary
        db.issue.project.default = issue.project
        db.issue.uuid.default = issue.uuid
        db.issue.is_last.default = True
        db.issue.owner.default = issue.owner
        db.issue.labels.default = issue.labels
        if not (auth.user.id == project.created_by or \
                    auth.user.email == issue.owner or \
                    auth.user.email in (project.members_email or [])):
            db.issue.owner.default = project.created_by
            db.issue.owner.writable = False
            db.issue.status.writable = False
        else:
            db.issue_assignment.assigned_by.default=auth.user.email
            db.issue_assignment.assigned_by.writable=False
            
        form = SQLFORM.factory(db.issue, db.issue_assignment)
        if form.process().accepted:
            db.issue.is_last.default=False
            #issue.update_record(is_last=False)
            issue.update_record(**db.issue._filter_fields(form.vars))
            form.vars.issue=issue.id
            id = db.issue_assignment.insert(**db.issue_assignment._filter_fields(form.vars))
            redirect(URL('projects'))
    else:
        form = DIV('login to assign')
    
    return dict(form=form)

def dependencies():
    id= request.args(0)
    issue = db(db.issue.id==id).select().first()
    query = (db.issue_dependencies.issue==issue.id)
    db.issue_dependencies.issue.default=issue.id
    db.issue_dependencies.issue.writable=False
    #COLUMNS=('issue_dependencies.dependent',)
    FIELDS=(db.issue_dependencies.dependent,)
    LINKS=[lambda row: A('detail',_href=URL('issue',args=row.dependent.id))]
    grid = SQLFORM.grid(query,editable=False,deletable=True, fields=FIELDS,links=LINKS,
                        details=False,create=auth.user_id,args=[id])        
    return dict(grid=grid)
    
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs bust be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
