Plugin_IssueTracker Installation and use instructions:

Plugin_IssueTracker Manifest

Views
- views/issue_tracker/postnewissue.html - view to format the postnewissue function of plugin_issuetracker controller.
- views/issue_tracker/index.html - view to handle the display from index function of plugin_issuetracker controller.     
- views/issue_tracker/ping.html - view to handle the display from ping function of plugin_issuetracker controller. 

Controllers
- controllers/plugin_issuetracker.py
-- Functions
--- ping :  connects to the issue tracker service via the variables specified in models/plugin_issuetracker.py, calling the service and returning a simple response if the connection is successful.
--- index:  displays the variables as defined in models/plugin_issuetracker.py for debugging purposes.
--- postnewissue: provides a form via which a user can input variables to be stored for a new issue in the issue tracker, utilizes the variables set in models/plugin_issuetracker.py, to make an xmlrpc call to the issue tracker and submit a new issue.

Models
models/plugin_issuetracker.py - used as a config file to define variables necessary to connect to the remote issue tracker.
- Variables
-- 'plugin_issuetracker_host' - the uri of the the controller hosting the service method for the issue tracker (ie. 'http://127.0.0.1:8000/issue_tracker/services/call/xmlrpc).
-- 'plugin_issuetracker_user' - username of the user account that should be used to connect to the remote host using basic authentication
-- 'plugin_issuetracker_pwd' - password for the user account that will be used to connect to the remote host using basic authentication
-- 'plugin_issuetracker_projectid' - project id of the remote project for which issues should be submitted, this is necessary to associate the issue with a project (i.e.. 1)

Static
- static/plugin_issuetracker/license.html - licensing info for the plugin
- static/plugin_issuetracker/about.html - general info about the use of the plugin

Issue Tracker Project
 
Controllers
- controllers/services.py
-- Functions
--- ping: simple response to send hostname and text in response to ping request, indicating the connection was made and it is responding
--- call: endpoint that routes xmlrpc calls to service functions (ping and new issue)
--- newissue: receives input for issue specific variables, including project id, summary, description, and owner and inserts a new record into the issue tracker db.

 
Files modified specifically to allow the submission of issues from the admin/errors controller
Controllers
- admin/controllers/default.py  - addition of new function 'newissue' - this allows for the submission of issues from tickets via xmlrpc calls.
       - addtition of 'assign' function: controller action that allows user to assign issues to other members of project team
       - addition of 'dependencies' function: controller action that allows user to view an issues dependencies and add new dependencies

Views
- admin/views/default/newissue.html - view to handle new function, newissue
- admin/views/default/errors.html - modify to add submit issue to the list of errors listed for any application
- admin/views/default/assign.html - view to handle assign controller action
- admin/views/default/dependencies.html - view to handle dependencies controller action

Models
- admin/models/issuetracker.py - settings for issuetracker
- admin/models/db_tracker.py - defines tables for issue tracker app

Plugin adds functionality to any app to be able to submit issues to a linked issue tracker, using xmlrpc services and ajax
-- update license and about pages
-- update to use ajax
-- repack
