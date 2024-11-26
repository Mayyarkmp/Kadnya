import base64
import datetime
from urllib.parse import urlencode

import requests

from Calendars.apps import CalendarsConfig
from Calendars.baseCalendarClient import BaseCalendarClient
from Calendars.models import CalendarUser
from . import config
from . import endPoints


class Calendly(BaseCalendarClient):

    def getScheduledEventsDetails(self, uid, sp, event_uuid):
        try:

            accessToken = None
            uuid = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            lastEndPoint = endPoints.scheduledEvents + f'/{event_uuid}'
            url = endPoints.baseUrl + lastEndPoint

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}"
            }

            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],

            )

            if response.status_code == 200:
                data = response.json()
                col = data['resource']
                eventUuid = col['uri']
                eventUuidList: list = eventUuid.split('/')
                eventUuid = eventUuidList[len(eventUuidList) - 1]
                newCol = {
                    'name': col['name'],
                    'status': col['status'],
                    'event_uuid': eventUuid,
                    'event_uri': col['uri'],
                    'calendar_event': col['calendar_event'],
                    'start_time': col['start_time'],
                    'end_time': col['end_time'],
                    'invitees_counter': col['invitees_counter'],
                    'location': col['location']
                }

                return {'success': True, 'event': newCol, 'error': True, 'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)

                    if response['success']:
                        return self.getScheduledEventsDetails(uid=uid, sp=sp, event_uuid=event_uuid)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                print(response.status_code)

                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getScheduledEventsInvitees(self, uid, sp, event_uuid, status):
        try:

            accessToken = None
            uuid = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            lastEndPoint = endPoints.scheduledEventInvitees.replace('*', event_uuid)
            url = endPoints.baseUrl + lastEndPoint

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}"
            }

            queryParameter = {
                'count': 100
            }
            if status == 'active' or status == 'canceled':
                queryParameter.update({
                    'status': status
                })
            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],
                params=queryParameter
            )

            if response.status_code == 200:
                data = response.json()
                userEventInviteesList = []
                for col in data['collection']:
                    eventUuid = col['event']
                    eventUuidList: list = eventUuid.split('/')
                    eventUuid = eventUuidList[len(eventUuidList) - 1]
                    newCol = {
                        'name': col['name'],
                        # 'first_name': col['first_name'],
                        # 'last_name': col['last_name'],
                        'status': col['status'],
                        # 'event_uuid': eventUuid,
                        # 'event_uri': col['event'],

                        'rescheduled': col['rescheduled'],
                        'reschedule_url': col['reschedule_url'],
                        'cancel_url': col['cancel_url'],
                        'timezone': col['timezone'],
                    }

                    userEventInviteesList.append(newCol)

                return {'success': True, 'user_events_invitees': userEventInviteesList, 'error': True, 'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)

                    if response['success']:
                        return self.getScheduledEventsInvitees(uid=uid, sp=sp, event_uuid=event_uuid, status=status)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                print(response.status_code)
                print(f'err: {data}')
                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getScheduledEvents(self, uid, sp, status):
        try:

            accessToken = None
            uuid = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            # lastEndPoint = endPoints.scheduledEvents.replace('*', event_uuid)

            url = endPoints.baseUrl + endPoints.scheduledEvents

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {str(accessToken)}"
            }

            queryParameter = {
                'user': str(config.userEndPointUuid + uuid),
                'count': 100
            }
            if status == 'active' or status == 'canceled':
                queryParameter.update({
                    'status': status
                })
            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],
                params=queryParameter
            )
            if response.status_code == 200:
                data = response.json()
                userScheduledEventList = []
                for col in data['collection']:
                    eventUuid = col['uri']
                    eventUuidList: list = eventUuid.split('/')
                    eventUuid = eventUuidList[len(eventUuidList) - 1]
                    newCol = {
                        'name': col['name'],
                        'status': col['status'],
                        'event_uuid': eventUuid,
                        'event_uri': col['uri'],
                        # 'calendar_event': col['calendar_event'],
                        'start_time': col['start_time'],
                        'end_time': col['end_time'],
                        'invitees_counter': col['invitees_counter']['active'],
                        'location': col['location']
                    }

                    userScheduledEventList.append(newCol)

                return {'success': True, 'user_scheduled_events': userScheduledEventList, 'error': True,
                        'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)
                    if response['success']:
                        return self.getScheduledEvents(uid=uid, sp=sp, status=status)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                print(f'err: {data}')
                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserEvents(self, uid, sp, active):
        try:
            uuid = None
            accessToken = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            # lastEndPoint = endPoints.userAvailableSchedules.replace('/*', '')
            url = endPoints.baseUrl + endPoints.userEventTypes

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {str(accessToken)}"
            }

            queryParameter = {
                'user': str(config.userEndPointUuid + uuid),
                'count': 100
            }
            if active == 'True' or active == 'False':
                queryParameter.update({
                    'active': active,
                })

            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],
                params=queryParameter
            )
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'user_events': data['collection'], 'error': True, 'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)
                    print('here')
                    if response['success']:
                        return self.getUserEvents(uid=uid, sp=sp, active=active)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                print(f'err: {data}')
                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserAvailabilitySchedule(self, uid, sp):
        try:
            uuid = None
            accessToken = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            # lastEndPoint = endPoints.userAvailableSchedules.replace('/*', '')
            url = endPoints.baseUrl + endPoints.userAvailableSchedules

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {str(accessToken)}"
            }

            queryParameter = {
                'user': str(config.userEndPointUuid + uuid)
            }

            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],
                params=queryParameter
            )
            if response.status_code == 200:
                data = response.json()
                return {'success': True, 'user_available_schedule': data['collection'], 'error': True, 'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)

                    if response['success']:
                        return self.getUserAvailabilitySchedule(uid=uid, sp=sp)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                print(f'err: {data}')
                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getUserBusyTime(self, uid, sp):
        try:
            url = endPoints.baseUrl + endPoints.userBusyTime
            uuid = None
            accessToken = None
            user = None

            try:
                user = CalendarUser.objects.get(user_id=uid)
                uuid = user.userData['credentials'][f'{sp}']['owner']
                accessToken = user.userData['credentials'][f'{sp}']['access_token']
            except CalendarUser.DoesNotExist as e:

                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {accessToken}"
            }
            timePeriod = self.generateStartEndTimePeriod(date=datetime.datetime.now(datetime.UTC), period=7)

            queryParameter = {
                'start_time': timePeriod['start'],
                'end_time': timePeriod['end'],
                'user': config.userEndPointUuid + uuid
            }
            request = self.generateRequest(headers=headers, body=None)

            response = requests.get(
                url=url,
                headers=request['headers'],
                params=queryParameter
            )


            if response.status_code == 200:
                data = response.json()
                userBusyTimeList = []

                for col in data['collection']:
                    newCol = {
                        'type': col['type'],
                        'start_time': col['start_time'],
                        'end_time': col['end_time'],
                    }
                    eventUuid = col['event']['uri']
                    eventUuidList: list = eventUuid.split('/')
                    eventUuid = eventUuidList[len(eventUuidList) - 1]
                    newCol.update({
                        'event_uuid': eventUuid,
                        'event_uri': col['event']['uri']
                    })
                    userBusyTimeList.append(newCol)

                return {'success': True, 'user_busy_time': userBusyTimeList, 'error': True, 'error_msg': f''}
            elif response.status_code == 401 or response.status_code == 403:
                data = response.json()
                if data['message'] == 'The access token expired' or \
                        data['message'] == 'The access token is invalid' or \
                        data['message'] == 'The access token was revoked':
                    response = self.refreshAccessToken(uid=uid, sp=sp)
                    if response['success']:
                        return self.getUserBusyTime(uid=uid, sp=sp)
                    else:
                        return {'success': False, 'error': True, 'error_msg': f'{response["error_msg"]}'}
                return {'success': False, 'error': True, 'error_msg': f'{data["message"]}'}
            else:
                data = response.json()
                return {'success': False, 'error': True, 'error_msg': f'{data["details"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def getAccessToken(self, code, uid, sp):
        try:

            url = endPoints.authUrl + endPoints.getAccessTokenUrl
            authorization = config.clientId + ":" + config.clientSecret

            authorization_bytes = authorization.encode("ascii")
            encodedAuthorization = base64.b64encode(authorization_bytes)
            encodedAuthorization_str = encodedAuthorization.decode("ascii")

            headers = \
                {
                    "Content-Type": "application/x-www-form-urlencoded",
                    'Authorization': f'Basic {encodedAuthorization_str}'
                }
            additionalData = {"uid": f"{uid}-{sp}"}
            stateValues = urlencode(additionalData)
            redirectUrl = CalendarsConfig.oAuthRedirectUrl + f'?state={stateValues}'
            body = \
                {
                    'code': f'{code}',
                    'redirect_uri': f'{redirectUrl}'
                }

            request = self.generateRequest(headers=headers, body=body)

            response = requests.post(
                url=url,
                headers=request['headers'],
                data=request['body']
            )
            if response.status_code == 200:
                data = response.json()
                owner: str = data['owner']
                uuid = owner.split('/')
                uuid = uuid[len(uuid) - 1]
                data['owner'] = uuid
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
            else:
                data = response.json()
                return {'success': False, 'error': True, 'error_msg': f'{data["error_description"]}'}

        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def refreshAccessToken(self, uid, sp):
        try:
            url = endPoints.authUrl + endPoints.getAccessTokenUrl
            authorization = config.clientId + ":" + config.clientSecret

            authorization_bytes = authorization.encode("ascii")
            encodedAuthorization = base64.b64encode(authorization_bytes)
            encodedAuthorization_str = encodedAuthorization.decode("ascii")

            headers = \
                {
                    "Content-Type": "application/x-www-form-urlencoded",
                    'Authorization': f'Basic {encodedAuthorization_str}'
                }
            refreshToken = None
            user = None
            try:
                user = CalendarUser.objects.get(user_id=uid)
                refreshToken = user.userData['credentials'][f'{sp}']['refresh_token']

            except CalendarUser.DoesNotExist as e:
                return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}
            body = \
                {
                    'grant_type': 'refresh_token',
                    'refresh_token': f'{refreshToken}'
                }
            request = self.generateRequest(
                headers=headers,
                body=body
            )

            response = requests.post(
                url=url,
                headers=request['headers'],
                data=request['body']
            )

            if response.status_code == 200:
                data = response.json()
                owner: str = data['owner']
                uuid = owner.split('/')
                uuid = uuid[len(uuid) - 1]
                data['owner'] = uuid
                user.userData['credentials'][f'{sp}'] = data
                user.save()
                return {'success': True, 'error': False, 'error_msg': ''}
            else:
                data = response.json()
                return {'success': False, 'error': True, 'error_msg': f'{data["error_description"]}'}
        except Exception as e:
            print(str(e))
            return {'success': False, 'error': True, 'error_msg': f'{str(e)}'}

    def authorization(self, uid, sp):
        try:
            additionalData = {"uid": f"{uid}-{sp}"}
            stateValues = urlencode(additionalData)
            redirectUrl = CalendarsConfig.oAuthRedirectUrl + f'?state={stateValues}'
            redirectAuthorizationUrl = endPoints.authorization + \
                                       f'?client_id={config.clientId}&' \
                                       f'response_type=code&redirect_uri={redirectUrl}'

            return {'success': True, 'url': redirectAuthorizationUrl, 'error': False, 'error_msg': ''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': str(e)}
