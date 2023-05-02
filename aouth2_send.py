import base64
import os.path
import json
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import openai_API, module_out_csv

# If modifying these scopes, delete the file token.json.
SCOPESOUT = ['https://www.googleapis.com/auth/gmail.send']


def send_email(e_to, e_from, e_subject, e_body):
    # Trim signature and etc
    e_body_t = e_body

    # Process message body
    openai_response_raw = openai_API.openai_request(e_body_t) # TODO (Developer) bad API output
    openai_response = json.loads(openai_response_raw) # TODO (Developer) issues with string decoding

    processed_body = openai_response.get('EMAIL_DRAFT')

    # Trigger write to local csv module
    module_out_csv.write_local_csv("client_base.csv", openai_response) # TODO (Developer) move filename to config

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens/send_token.json'):
        creds = Credentials.from_authorized_user_file('tokens/send_token.json', SCOPESOUT)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'tokens/credentials.json', SCOPESOUT)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('tokens/send_token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        message = MIMEText(str(processed_body))
        message['to'] = e_to
        message['from'] = e_from
        message['subject'] = e_subject
        message_body = {
            'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()
        }
        message = service.users().messages().send(userId='me', body=message_body).execute()
        return message['id']

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        return -1
