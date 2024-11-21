from Calendars.models import CalendarUser


class BaseCalendarClient:
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    getAccessTokenBody = \
        {
            'grant_type': 'authorization_code',
            'code': f'',
            'redirect_uri': f''
        }

    def generateRequest(self, headers, body):

        try:
            requestHeader = None
            requestBody = None

            requestHeader = self.headers
            if headers is not None:
                requestHeader.update(headers)
            if body is not None:
                requestBody = self.getAccessTokenBody
                requestBody.update(body)

            return {'headers': requestHeader, 'body': requestBody}
        except Exception as e:
            print(f'error in Base calendar client: {e}')

    def generateStartEndTimePeriod(self, date, period):
        startTime = date.strftime('%Y-%m-%dT%H:%M:%SZ')
        currentDay = date.day
        endTimeDay = currentDay + period
        endTime = date.strftime(f'%Y-%m-{endTimeDay}T%H:%M:%SZ')
        return {'start': startTime, 'end': endTime}

    def storeCredentials(self, creds, uid, sp):
        try:
            newUser, created = CalendarUser.objects.get_or_create(user_id=uid)
            if created:
                newUser.userData = {
                    'credentials':
                        {f'{sp}': creds}
                }
            else:
                newUser.userData['credentials'].update({
                    f'{sp}': creds
                })

            newUser.save()
            return {'success': True, 'error': False, 'error_msg': ''}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f'error in storing user data {str(e)}'}

    def generateOutput(self, keysList, response):
        res = {}

        for key in keysList:

            res.update({
                f"{key}": response[f"{key}"]
            })

        return res
