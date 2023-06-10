from redminelib import Redmine
from io import BytesIO


def crm_create_new_ticket(write_data):


    # should be moved to the config file
    crm_url = 'http://192.168.230.129/'
    crm_usr = 'api'
    crm_pwd = 'password'

    # check if data contains lead
    if write_data.get('LEAD') == 'Yes':
        redmine = Redmine(crm_url, username=crm_usr, password=crm_pwd)
        projects = redmine.project.all()

        issue = redmine.issue.new()
        issue.project_id = 'compnay1-property-rent' # HARDCODE WARNING
        issue.subject = 'Lead: ' + write_data.get('DEAL_TYPE') + write_data.get('PROPERTY_TYPE')
        #issue.tracker_id = 8
        issue.description = 'Here will be detailed description'
        #issue.status_id = 3
        #issue.priority_id = 7
        #issue.assigned_to_id = 123
        #issue.watcher_user_ids = [123]
        #issue.parent_issue_id = 345
        #issue.start_date = datetime.date(2014, 1, 1)
        #issue.due_date = datetime.date(2014, 2, 1)
        #issue.estimated_hours = 4
        #issue.done_ratio = 40
        #issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
        #issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
        issue.save()