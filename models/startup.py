# coding: utf8

def startupcode():
     db.auth_user.truncate()
     db.auth_group.truncate()
     db.auth_membership.truncate()
     
     userID = db.auth_user.insert(first_name='admin',\
                         last_name='tracker',\
                         email='admin@issuetracker.com',\
                         password='47584980359b916c9484f909259d851f')
     groupID = db.auth_group.insert(role='manager')
     db.auth_membership.insert(user_id=userID, group_id=groupID)
     db.commit()
     import os
     os.rename(os.path.join(request.folder,'models','startup.py'),
 
os.path.join(request.folder,'private','startup.py'))
startupcode()
