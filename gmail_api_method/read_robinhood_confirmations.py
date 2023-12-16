# https://developers.google.com/gmail/api/quickstart/python
# https://developers.google.com/resources/api-libraries/documentation/gmail/v1/python/latest/index.html
# https://developers.google.com/gmail/api/guides

from __future__ import print_function

import os.path
from nlp_regex_extract import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file: token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


import base64

def get_message(service, user_id, msg_id):
    message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    return message

def decode_message(raw_message):
    msg_raw = base64.urlsafe_b64decode(raw_message['raw'].encode('ASCII'))
    return msg_raw

def main():
    """basic usage of the Gmail API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # TODO: remove token.json after it expires so a fresh one can be generated
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        RBH_emails = service.users().messages().list(userId='me', q='from:noreply@robinhood.com',).execute()

        # ex. other Gmail API uses
        # results = service.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])
        # RBH_emails = service.users().messages().list(userId='me', labelIds=['RBH']).execute()

        # print(type(RBH_emails))
        print(f"\n>>> Estimated # of Robinhood Emails: {RBH_emails['resultSizeEstimate']}\n")
        

        # Extract the email messages from the responses
        RBH_messages = RBH_emails['messages']

        print('Indexing emails...')

        # testthing = service.users().messages().get(userId='me', id=RBH_messages[0]['id']).execute()
        # # print(json.dumps(testthing, indent=4))
        # print()
        # print(list(testthing.keys()))
        # print()

        # Print the SNIPPETS of each message
        snippets = []
        for message in RBH_messages:
            message_data = service.users().messages().get(userId='me', id=message['id']).execute()
            snippet = message_data['snippet']
            # snippet_words = set(list(str(snippet).split(' ')))
            # print(f'{snippet_words}\n')
            # print(f'{snippet}\n')
            snippets.append(snippet)

        # print(f'\n{snippets}\n')

        # To get the full HtML context of messages:
        # message_htmls = []
        # for message in RBH_messages:
        #     message_data = service.users().messages().get(userId='me', id=message['id']).execute()
        #     message = get_message(service=service, user_id='me', msg_id=message['id'])
        #     decoded_message = decode_message(message)
        #     print(decoded_message)
        #     message_htmls.append(decoded_message)

        # message0 = get_message(service=service, user_id='me', msg_id=RBH_messages_2[0]['id'])
        # print(decode_message(message0))

        # test_msg_data = service.users().messages().get(userId='me', id=RBH_messages_2[0]['id']).execute()
        # email_data = test_msg_data['payload']['body']
        # print(email_data)

        # data = email_data.decode("UTF-8")
        # print(data)
        # print(json.dumps(test_msg_data, indent=4))
        
        # for message in RBH_messages_2:
        #     message_data = service.users().messages().get(userId='me', id=message['id']).execute()
        #     subject = [header['value'] for header in message_data['payload']['headers'] if header['name'] == 'Subject'][0]
        #     print()
        #     # print("Subject:", subject)
        #     print("Message: ", message_data['snippet'])
        #     # print(message_data)
        #     print()
        #     # print(json.dumps(message_data, indent=4))
        #     # print(message_data)
        
        print("finished!")
        return snippets
    
    except Exception as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')
        return []


if __name__ == '__main__':
    snippets = main()
    # print(snippets)

    print(f'\n# snippets: {len(snippets)}\n')

    my_symbols, failed_idxs = spacy_extract(snippets)
    print(f'Emails where no tickers found: \n{failed_idxs}')
    print()
    print(f'Found ticker symbols: \n{str(my_symbols)}')
    print()