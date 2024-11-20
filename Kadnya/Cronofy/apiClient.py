import requests
from django.conf import settings
import datetime
from Cronofy.models import CronofyUser
import base64
import json


class CronofyApiModel:
    baseUrl = "https://api.cronofy.com"
    authBaseUrl = "https://app.cronofy.com"
    cronofyGetAuthorizationCodeURI = f'{authBaseUrl}/oauth/authorize'
    cronofyGetAccessTokenURI = f'{authBaseUrl}/oauth/token'
    cronofyGetAvailability = f'{baseUrl}/v1/availability'
    cronofyGetCalenders = f'{baseUrl}/v1/calendars'
    cronofyGetEvents = f'{baseUrl}/v1/events'
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self):
        self.redirectUri = settings.CRONOFY_REDIRECT_URI
        self.clientId = settings.CRONOFY_CLIENT_ID
        self.clientSecret = settings.CRONOFY_CLIENT_SECRET


    def Get_User_Events(self, uid, start, end, timeZone ):
        try:
            if (uid, start, end, timeZone) is not None:
                try:
                    cronofyUser = CronofyUser.objects.get(user_id=uid)

                except Exception as e:
                    return {"success": False, "error": True, "error_msg": 'No such user'}
        except Exception as e:
            print('asasa')
    def Get_User_Calenders(self, uid=None):
        try:
            if uid is not None:
                try:
                    cronofyUser = CronofyUser.objects.get(user_id=uid)

                except Exception as e:
                    return {"success": False, "error": True, "error_msg": 'No such user'}
            headers = self.headers
            headers.update(
                {
                    "Authorization": "Bearer " + str(cronofyUser.accessToken)
                }
            )
            response = requests.get(url=f'{self.cronofyGetCalenders}',
                                    headers=headers
                                    )
            if response.status_code == 401:
                return {"success": False, "error": True, "error_msg": "invalid or expired token"}
            if response.status_code == 200:
                data = response.json()
                calendarList = []
                for calendar in data['calendars']:
                    newCalendar = {
                        "provider_name": calendar["provider_name"],
                        "profile_id": calendar["profile_id"],
                        "profile_name": calendar["profile_name"],
                        "calendar_id": calendar["calendar_id"],
                        "calendar_name": calendar["calendar_name"],
                        "calendar_readonly": calendar["calendar_readonly"],
                        "calendar_deleted": calendar["calendar_deleted"],
                        "calendar_primary": calendar["calendar_primary"],
                        "calendar_integrated_conferencing_available": calendar[
                            "calendar_integrated_conferencing_available"],
                        "calendar_attachments_available": calendar["calendar_attachments_available"],
                        "permission_level": calendar["permission_level"]
                    }
                    calendarList.append(newCalendar)
                return {"success": True, 'calendars_list': calendarList, "error": False, "error_msg": None}

        except Exception as e:
            print(str(e))
            return {"success": False, "error": True, "error_msg": str(e)}

    def Get_User_Availability(self, uid=None):
        try:
            if uid is not None:
                try:
                    cronofyUser = CronofyUser.objects.get(user_id=uid)

                except Exception as e:
                    return {"success": False, "error": True, "error_msg": 'No such user'}
                headers = self.headers
                headers.update({
                    'Content-Type': 'application/json',
                    'Authorization': f"Bearer {self.clientSecret}"
                })
                startTime = datetime.datetime.now(datetime.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
                currentDay = datetime.datetime.now().day
                endTimeDay = currentDay + 7
                endTime = datetime.datetime.now(datetime.UTC).strftime(f'%Y-%m-{endTimeDay}T00:00:00.000Z')

                availabilityParams = {
                    "participants": [{
                        "members": [{
                            "sub": cronofyUser.sub
                        }],
                        "required": "all"
                    }],
                    "required_duration": {"minutes": 60},
                    "query_periods": [{
                        "start": f'{startTime}',
                        "end": f'{endTime}'
                    }],
                    "response_format": "periods"
                }
                # data query for availability must be jesonized
                availabilityParamsJson = json.dumps(availabilityParams, indent=2)

                response = requests.post(
                    url=f'{self.cronofyGetAvailability}',
                    headers=headers,
                    data=availabilityParamsJson,
                )

                print(f'response: {str(response.json())}')
                if response.status_code == 401:
                    return {"success": False, "error": True, "error_msg": "invalid or expired token"}
                elif response.status_code == 200:
                    data = response.json()
                    availabilitiesList = []
                    for availablePeroid in data['available_periods']:
                        newavailablePeroid = {

                            'start': availablePeroid['start'],  # start time of the event
                            'end': availablePeroid['end'],  # end time of the event

                            # 'buffered_start_time': UserBusyTime['buffered_start_time'] if UserBusyTime[
                            #     'buffered_start_time'] else None,
                            # 'buffered_end_time': UserBusyTime['buffered_end_time'] if UserBusyTime[
                            #     'buffered_end_time'] else None,
                        }
                        availabilitiesList.append(newavailablePeroid)
                    return {"success": True, 'available_periods': availabilitiesList, "error": False, "error_msg": None}

        except Exception as e:
            return {"success": False, "error": True, "error_msg": str(e)}

    def Get_Access_Token(self, authorizationCode, uid=None):
        try:

            headers = self.headers

            body = {
                "client_id": f'{self.clientId}',
                "client_secret": f'{self.clientSecret}',
                'grant_type': 'authorization_code',
                'code': f'{str(authorizationCode)}',
                'redirect_uri': f'{str(self.redirectUri)}' if uid is None else f'{str(self.redirectUri)}?uid={uid}'
            }

            response = requests.post(url=self.cronofyGetAccessTokenURI,
                                     headers=headers,
                                     data=body)
            print(f'response: {str(response.json())}')
            if response.status_code == 200:
                data = response.json()

                try:
                    cronofyUser, created = CronofyUser.objects.get_or_create(user_id=uid)
                    cronofyUser.accessToken = data["access_token"]
                    cronofyUser.refreshToken = data["refresh_token"]
                    cronofyUser.sub = data["sub"]
                    cronofyUser.save()

                    return {'success': True, 'accessToken': data["access_token"]}
                except Exception as e:
                    # print(f"error in creating  {str(e)}")
                    return {"success": False, "error": True, "error_msg": str(e)}

            return {"success": False, "error": False, "error_msg": None}

        except Exception as e:
            print(f'error is {str(e)}')
            return {"success": False, "error": True, "error_msg": str(e)}

    # TODO: in Development pass the token to check it, in production pass the user or user id and token type
    def Generate_Access_Token(self, uid=None):
        try:
            try:
                cronofyUser = CronofyUser.objects.get(user_id=uid)

            except Exception as e:
                return {"success": False, "error": True, "error_msg": 'No such user'}

            headers = self.headers

            print(f'refresh token: {str(cronofyUser.refreshToken)}')
            body = {
                "client_id": f'{self.clientId}',
                "client_secret": f'{self.clientSecret}',
                'grant_type': 'refresh_token',
                'refresh_token': f'{str(cronofyUser.refreshToken)}',
            }
            response = requests.post(url=self.cronofyGetAccessTokenURI,
                                     headers=headers,
                                     data=body)
            print(f'response: {str(response.json())}')
            if response.status_code == 200:
                data = response.json()
                cronofyUser.accessToken = data["access_token"]
                cronofyUser.refreshToken = data["refresh_token"]
                cronofyUser.save()
                return {'success': True}

            return {"success": False, "error": False, "error_msg": None}
        except Exception as e:
            print(f'error is {str(e)}')
            return {"success": False, "error": True, "error_msg": str(e)}

    # def Check_Token(self, Token):
    #     try:
    #
    #         body = {
    #             'client_id': self.clientId,
    #             'client_secret': self.clientSecret,
    #             'token': Token
    #         }
    #         response = requests.post(
    #             url=self.calendlyIntrospectToken,
    #             headers=self.headers,
    #             data=body
    #         )
    #         if response.status_code == 200:
    #             data = response.json()
    #             return {"success": True, "active": data["active"]}
    #
    #         return {"success": False, "error": False, "error_msg": None}
    #
    #     except Exception as e:
    #         return {"success": False, "error": True, "error_msg": str(e)}

    # def Get_User(self, uid=None, currentUser=False):
    #     try:
    #         if currentUser is False:
    #
    #             try:
    #                 calendlyUser = CronofyUser.objects.get(user_id=uid)
    #
    #                 headers = self.headers
    #                 headers.update({
    #                     'Authorization': f"Basic {calendlyUser.accessToken}"
    #                 })
    #                 response = requests.get(
    #                     url=f'{self.calendlyGetUser}/{calendlyUser.uuid}',
    #
    #                 )
    #                 if response.status_code == 401:
    #                     return {"success": False, "error": True, "error_msg": "invalid or expired token"}
    #                 elif response.status_code == 200:
    #                     data = response.json()
    #                     calendlyUser.scheduling_link = data["scheduling_url"]
    #                     calendlyUser.save()
    #                     return {'success': True, 'scheduling_url': data["scheduling_url"]}
    #                 return {"success": False, "error": False, "error_msg": None}
    #
    #             except Exception as e:
    #                 return {"success": False, "error": True, "error_msg": str(e)}
    #
    #         else:
    #             try:
    #                 calendlyUser = CronofyUser.objects.get(user_id=uid)
    #                 headers = self.headers
    #                 headers.update({
    #                     'Authorization': f"Basic {calendlyUser.accessToken}"
    #                 })
    #                 response = requests.get(
    #                     url=f'{self.calendlyGetUser}/me',
    #
    #                 )
    #                 if response.status_code == 401:
    #                     print("invalid token")
    #                     return {"success": False, "error": True, "error_msg": "invalid or expired token"}
    #                 elif response.status_code == 200:
    #                     data = response.json()
    #                     calendlyUser.scheduling_link = data["scheduling_url"]
    #                     calendlyUser.save()
    #                     return {'success': True, 'scheduling_url': data["scheduling_url"]}
    #                 return {"success": False, "error": False, "error_msg": None}
    #
    #             except Exception as e:
    #                 return {"success": False, "error": True, "error_msg": str(e)}
    #
    #     except Exception as e:
    #         return {"success": False, "error": True, "error_msg": str(e)}
