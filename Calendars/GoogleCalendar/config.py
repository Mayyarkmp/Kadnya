import os

from Kadnya.settings import BASE_DIR


sp = 'gCalendar'
GOOGLE_CALENDAR_CLIENT_SECRETS_FILE = os.path.join(BASE_DIR,
                                                   'Calendars/GoogleCalendar/Credentials/client_secret_775340653192'
                                                   '-dkeq7ma1f8vjudhhfkk1v44r48amk4rf.apps.googleusercontent.com.json')
GOOGLE_CALENDAR_API_SCOPES = ['https://www.googleapis.com/auth/calendar']

