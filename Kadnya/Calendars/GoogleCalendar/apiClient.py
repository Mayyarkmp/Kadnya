import datetime
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import google_apis_oauth
from googleapiclient.discovery import build

from Calendars.apps import CalendarsConfig
from Calendars.baseCalendarClient import BaseCalendarClient
from . import config
from ..models import CalendarUser


class GoogleCalendar(BaseCalendarClient):
    def getUserScheduledEventInvitees(self, uid, sp, event_uuid):
        try:
            userCredential = None
            try:
                user = CalendarUser.objects.get(user_id=uid)
                userCredential = user.userData['credentials'][f'{sp}']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

            creds, refreshed = google_apis_oauth.load_credentials(userCredential)
            if refreshed:
                self.storeCredentials(creds=creds, uid=uid, sp=sp)

            service = build('calendar', 'v3', credentials=creds)
            response = service.events().get(calendarId='primary', eventId=f'{event_uuid}').execute()

            col = response
            eventInviteesList = []
            if 'attendees' in col:
                for att in response['attendees']:
                    newAtt = {
                        'name': att['displayName'],
                        'email': att['email'],
                        'responseStatus': col['responseStatus'],
                        # 'event_uri': col['htmlLink'],
                        # 'start_time': col['start'],
                        # 'end_time': col['end'],

                    }
                    eventInviteesList.append(newAtt)

            return {'success': True, 'user_events_invitees': eventInviteesList, 'error': True,
                    'error_msg': f''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserScheduledEventDetails(self, uid, sp, event_uuid):
        try:
            userCredential = None
            try:
                user = CalendarUser.objects.get(user_id=uid)
                userCredential = user.userData['credentials'][f'{sp}']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

            creds, refreshed = google_apis_oauth.load_credentials(userCredential)
            if refreshed:
                self.storeCredentials(creds=creds, uid=uid, sp=sp)

            service = build('calendar', 'v3', credentials=creds)
            response = service.events().get(calendarId='primary', eventId=f'{event_uuid}').execute()

            col = response

            newCol = {
                'name': col['summary'],
                'status': col['status'],
                'event_uuid': col['id'],
                'event_uri': col['htmlLink'],
                'start_time': col['start'],
                'end_time': col['end'],

            }
            if 'attendees' in col:
                newCol.update({
                    'invitees_counter': len(col['attendees']),
                })
            if 'location' in col:
                newCol.update({
                    'location': col['location']
                })

            return {'success': True, 'event': newCol, 'error': True,
                    'error_msg': f''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserScheduledEvents(self, uid, sp):
        try:
            userCredential = None
            try:
                user = CalendarUser.objects.get(user_id=uid)
                userCredential = user.userData['credentials'][f'{sp}']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

            creds, refreshed = google_apis_oauth.load_credentials(userCredential)
            if refreshed:
                self.storeCredentials(creds=creds, uid=uid, sp=sp)

            service = build('calendar', 'v3', credentials=creds)
            response = service.events().list(calendarId='primary', singleEvents=False).execute()
            # response = service.calendarList().list().execute()
            userScheduledEventList = []
            for col in response['items']:

                newCol = {
                    'name': col['summary'],
                    'status': col['status'],
                    'event_uuid': col['id'],
                    'event_uri': col['htmlLink'],
                    'start_time': col['start'],
                    'end_time': col['end'],

                }
                if 'attendees' in col:
                    newCol.update({
                        'invitees_counter': len(col['attendees']),
                    })
                if 'location' in col:
                    newCol.update({
                        'location': col['location']
                    })

                userScheduledEventList.append(newCol)
            print(response)
            return {'success': True, 'user_scheduled_events': userScheduledEventList, 'error': True,
                    'error_msg': f''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserBusyTime(self, uid, sp):
        try:
            userCredential = None
            try:
                user = CalendarUser.objects.get(user_id=uid)
                userCredential = user.userData['credentials'][f'{sp}']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

            creds, refreshed = google_apis_oauth.load_credentials(userCredential)
            if refreshed:
                self.storeCredentials(creds=creds, uid=uid, sp=sp)

            service = build('calendar', 'v3', credentials=creds)
            timePeriod = self.generateStartEndTimePeriod(date=datetime.datetime.now(datetime.UTC), period=7)
            body = {
                "timeMin": timePeriod['start'],
                "timeMax": timePeriod['end'],
                "items": [
                    {"id": "primary"},
                ]
            }
            response = service.freebusy().query(body=body).execute()
            print(f'response: {response}')
            return {'success': True, 'user_busy_time': response['calendars']['primary']['busy'], 'error': True,
                    'error_msg': f''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getAccessToken(self, request, uid, sp):
        try:
            #
            redirectUri = f'{CalendarsConfig.oAuthRedirectUrl}'
            print("here")
            credentials = google_apis_oauth.get_crendentials_from_callback(
                request,
                config.GOOGLE_CALENDAR_CLIENT_SECRETS_FILE,
                config.GOOGLE_CALENDAR_API_SCOPES,
                redirectUri
            )
            print("meow")

            # Stringify credentials for storing them in the DB
            data = google_apis_oauth.stringify_credentials(
                credentials)
            try:
                newUser, created = CalendarUser.objects.get_or_create(user_id=uid)
                if created:
                    newUser.userData = {
                        'credentials':
                            {f'{sp}': data}
                    }
                else:
                    newUser.userData['credentials'].update({
                        f'{sp}': data
                    })

                newUser.save()
                return {'success': True, 'error': False, 'error_msg': ''}
            except Exception as e:
                return {'success': False, 'error': True, 'error_msg': f'error in storing user data {str(e)}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def authorization(self, uid, sp):
        try:
            redirectUri = f'{CalendarsConfig.oAuthRedirectUrl}'
            # print(redirectUri) #uid={uid}-{sp}
            redirectAuthorizationUrl = google_apis_oauth.get_authorization_url(
                client_json_filepath=config.GOOGLE_CALENDAR_CLIENT_SECRETS_FILE,
                scopes=config.GOOGLE_CALENDAR_API_SCOPES,
                redirect_uri=redirectUri,

            )

            parsedUrl = urlparse(redirectAuthorizationUrl)
            queryParams = parse_qs(parsedUrl.query)
            currentState = queryParams.get("state", [""])[0]
            additionalData = {"uid": f"{uid}-{sp}"}
            newState = f"{currentState}&{urlencode(additionalData)}"
            queryParams["state"] = newState
            new_query = urlencode(queryParams, doseq=True)
            redirectAuthorizationUrl = urlunparse((
                parsedUrl.scheme,
                parsedUrl.netloc,
                parsedUrl.path,
                parsedUrl.params,
                new_query,
                parsedUrl.fragment,
            ))

            return {'success': True, 'url': redirectAuthorizationUrl, 'error': False, 'error_msg': ''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': str(e)}
