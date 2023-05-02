# Open issues:
# - Status messages
# - reduce number of openai requests!
# - store answers (emails, api responses, everything!)

import base64
import json
import os.path
import time
import logging

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

import aouth2_send

# TODO(Developer): move away from global variables
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CHECK_FREQ = 10
DEBUG_LVL = logging.INFO


# API docs:
# https://developers.google.com/gmail/api/reference/rest/v1/users.messages

def main():
    # Logs section
    logname = datetime.now().strftime('log_%m_%d_%Y.log')

    logging.basicConfig(filename='logs/' + logname, encoding='utf-8', level=DEBUG_LVL,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Checking email...')

    # Check & initialize configuration files
    if os.path.exists('config.json'):
        with open('config.json') as json_file:
            params = json.load(json_file)
            auth_users = params['users']
            from_email = params['sender_email']
            CHECK_FREQ = params['check_freq']  # TODO (Developer): non visible
    else:
        logging.error('Configuration file not found. Terminating.')
        exit()

    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('tokens/get_token.json'):
        creds = Credentials.from_authorized_user_file('tokens/get_token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # TODO (Developer): google.auth.exceptions.RefreshError: ('invalid_grant:...
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'tokens/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('tokens/get_token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        inbox_messages = service.users().messages().list(userId='me').execute()

        for message_id in inbox_messages['messages']:
            message = service.users().messages().get(userId='me', id=message_id['id'], format='full').execute()

            # Extract the sender of the message from the message payload            
            sender_address = next((item for item in message.get('payload').get('headers') if
                                   item['name'].lower() == 'from'), {}).get('value')
            # Extract the subject of the message from the message payload
            message_subject = next((item for item in message.get('payload').get('headers') if
                                    item['name'].lower() == 'subject'), {}).get('value')
            # Extract the body of the message from the message payload
            payload = message['payload']
            if 'parts' in payload:
                parts = payload['parts']
                data = ''
                for part in parts:
                    if part.get('body').get('attachmentId'):
                        attachment = service.users().messages().attachments().get(
                            userId='me', messageId=message_id, id=part['body']['attachmentId']).execute()
                        try:
                            data += base64.urlsafe_b64decode(attachment.get('data')).decode()
                        except (TypeError, ValueError):
                            logging.error(
                                'MessageID: ' + message_id['id'] + ' Invalid base64-encoded data at attachmentId.')
                            pass
                    else:
                        if part.get('body').get('data'):
                            try:
                                data += base64.urlsafe_b64decode(part.get('body').get('data')).decode()
                            except (TypeError, ValueError):
                                logging.error(
                                    'MessageID: ' + message_id['id'] + ' Invalid base64-encoded data at data.')
                                pass
                body_text = data
            else:
                body = payload.get('body').get('data')
                body_text = base64.urlsafe_b64decode(body).decode()

            message_body = body_text

            # Remove special symbols \/:*?"<>|
            sender_addr_f = sender_address.translate(str.maketrans('\/:*?"<>|', '_________'))

            # Check if user is registered
            if any(user in sender_addr_f for user in auth_users):

                # Check if the message was already replied to
                # Check if pid exists:
                if os.path.exists('pids/' + sender_addr_f + '.pid'):
                    with open('pids/' + sender_addr_f + '.pid', 'r') as pid:
                        # Check if message is already processed
                        if message_id['id'] in pid.read():
                            continue
                # Create pid file
                else:
                    with open('pids/' + sender_addr_f + '.pid', 'w'):
                        logging.info('Creating pid for user: ' + sender_addr_f)
                        pass

                logging.info('Processing message:' + message_id['id'])
                logging.info('Message from: ' + sender_address)
                logging.debug('Responding from: ' + from_email)
                logging.debug('Subject: ' + message_subject)
                logging.debug('Body: ' + message_body)

                sender = aouth2_send.send_email(e_to=sender_address,
                                                e_from=from_email,
                                                e_subject=message_subject,
                                                e_body=message_body)

                if sender != -1:
                    # Create pid for user and add processed msg ID
                    with open('pids/' + sender_addr_f + '.pid', 'a') as pid:
                        pid.write(message_id['id'] + ' ')
                        logging.info('Message processed:' + message_id['id'])
                else:
                    logging.error('Was not able to send response:', message_id['id'])
                    # TODO(Developer): Identify where the error was (g api, sending, openai api?).
                    # TODO(Developer): Pass error code? Work with logging directly?

    except HttpError as error:
        logging.error(f'Gmail API: An error occurred: {error}')


if __name__ == '__main__':
    while True:
        main()
        time.sleep(CHECK_FREQ)
