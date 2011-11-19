#def author(form): return '%(first_name)s %(last_name)s' % auth.user

"""set auth settings to allow basic auth"""
auth.settings.allow_basic_login = True

PROJ_PHASE = ('Approved - Not started', 'Design', 'Development', 'Testing', 'Deployement/Maintenance')
#PRIORITIES = ('Critical','Major','Minor','Trivial')
db.define_table(
    'project',
    Field('name',unique=True,notnull=True),
    #Field('author',compute=author,writable=False),
    Field('author'),
    Field('manager', 'reference auth_user'),
    Field('phase', requires=IS_IN_SET(PROJ_PHASE,zero=None)),
    #Field('priority', requires=IS_IN_SET(PRIORITIES,zero=None)),
    Field('description','text'),
    Field('super_project','reference project'),
    Field('license'),
    Field('repo'),
    Field('members_email','list:string'),
    auth.signature,
    format = '%(name)s'
    )
db.project.super_project.requires=IS_EMPTY_OR(IS_IN_DB(db,db.project,'project.name'))
    
db.define_table ('team',
    Field('team_name',unique=True,notnull=True),
    Field('team_lead', db.auth_user,required=False),
    Field('members', 'list:reference auth_user'),
    Field('assigned_projects', 'list:reference project'),
    format = '%(team_name)s'
    )
db.team.id.readable=db.team.id.writable=False


STATUSES = ('New','Accepted','Started',
            'Fixed','Verified','Invalid','Duplicate',
            'WontFix','Done')
DESCRIPTION = """
What steps will reproduce the problem?
What is the expected output and what do you see instead?
What version are you using and which platform?
Additional information
"""

db.define_table(
    'issue',
    Field('project','reference project',readable=False,writable=False),
    Field('uuid',readable=False,writable=False),
    Field('summary',requires=IS_NOT_EMPTY()),
    Field('description','text',default=''),
    Field('attachment','upload'),
    Field('status',requires=IS_IN_SET(STATUSES,zero=None)),
    Field('owner',requires=IS_IN_DB(db,db.auth_user.email)),
    Field('cc','list:string',writable=False, readable=False),
    Field('send_email','boolean',default=True),
    Field('labels','list:string'),
    #Field('author',compute=author,writable=False,readable=True),
    Field('author'),
    Field('is_last','boolean',default=True,readable=False,writable=False),
    auth.signature, format='%(summary)s')


db.project.is_active.writable=db.project.is_active.readable=False
db.issue.is_active.writable=db.issue.is_active.readable=False
db.project.created_on.readable=True
db.issue.created_on.readable=True

def do_mail(items):
    email_ok = []
    email_no = []
    email_ok.append(items[-1].project.created_by.email)
    for item in items:
        email = item.created_by.email
        cc = item.cc or []
        if item.send_email:
            email_ok.append(email)
            email_ok += [x.strip() for x in cc if x.strip()]
        else:
            email_no.append(email)
            email_no +=[x.strip() for x in ccitem.cc if x.strip()]
    email_ok = [e for e in set(email_ok) if not e in email_no]
    message = 'http://%s/%s' % (request.env.http_host,
                                URL('issue',items[-1].uuid)) + "\n\n" + \
                                items[-1].description

    auth.settings.mailer.send(to=email_ok,
                              subject='IssueTracker:'+items[-1].summary,
                              message=message)
                              
extra = {}
extra['code'] = lambda code: CODE(code,language=None).xml()
extra['code_python'] = lambda code: CODE(code,language='python').xml()
extra['code_c'] = lambda code: CODE(code,language='c').xml()
extra['code_cpp'] = lambda code: CODE(code,language='cpp').xml()
extra['code_java'] = lambda code: CODE(code,language='java').xml()
extra['code_html_plain'] = lambda code: CODE(code,language='html_plain').xml()
extra['code_html'] = lambda code: CODE(code,language='html').xml()
extra['code_web2py'] = lambda code: CODE(code,language='web2py').xml()
