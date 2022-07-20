#!/usr/bin/python3

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from storebox_rgb_led import *


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token, encoding="bytes")
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/usr/local/lib/storebox-rgb-led/certificates/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today = datetime.datetime.utcnow().date()
    start = datetime.datetime(today.year, today.month, today.day)
    end = start + datetime.timedelta(1)
    #.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #end_date = now + datetime.timedelta(days=1)
    startIso = start.isoformat() + 'Z'
    endIso = end.isoformat() + 'Z'
    #print("begin today", startIso)
    #print("end today", endIso)
    #print('Getting the upcoming 5 events')
    events_result = service.events().list(calendarId='yourstorebox.com_osemd4ar1ua9405gfqbtetg4bk@group.calendar.google.com', timeMin=startIso,
                                        timeMax=endIso,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No birthday today.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        if "FP " in event['summary']:
            # skip franchise partners
            print("Skip", start, event['summary'])
        else:
            print("Birthday for", start, event['summary'])
            startAnimation(StoreboxAnimation.Birthday)

    # Check rapid vienna games
    events_result = service.events().list(calendarId='guc1jitr84o9tsrn68lqqetfgkka04k2@import.calendar.google.com', timeMin=startIso,
                                        timeMax=endIso,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No rapid vienna game today.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print("Rapid Vienna game", start, event['summary'])
        startAnimation(StoreboxAnimation.Rapid)


if __name__ == '__main__':
    main()