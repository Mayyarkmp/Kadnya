from ninja import NinjaAPI
from . import schemas
from . import apiClient

cronofyApi = NinjaAPI(urls_namespace='Cronofy')
cronofy = apiClient.CronofyApiModel()


@cronofyApi.get('/calenders', response={200: schemas.GetUserCalendarsResponse, 401: schemas.ErrorResponse,
                                        400: schemas.ErrorResponse})
def Get_User_Calendar(request, uid):
    try:
        calendarData = cronofy.Get_User_Calenders(uid)
        if calendarData['success']:
            return 200, {'success': True, 'calendars_list': calendarData['calendars_list']}
        else:
            if calendarData['error_msg'] == 'invalid or expired token':
                return 401, {'error': 'invalid or expired token'}
            else:
                return 400, {'error': calendarData['error_msg']}
    except Exception as e:
        return 400, {"error": str(e)}


@cronofyApi.get('/available', response={200: schemas.GetUserAvailabilityResponse, 401: schemas.ErrorResponse,
                                        400: schemas.ErrorResponse})
def Get_User_Availability(request, uid):
    try:

        availablePeriods = cronofy.Get_User_Availability(uid)
        if availablePeriods['success']:
            # print(f'userBusyTime: {userBusyTime["user_busy_time"]}')
            return 200, {'success': True, 'available_periods': availablePeriods['available_periods']}
        else:
            if availablePeriods['error_msg'] == 'invalid or expired token':
                return 401, {'error': 'invalid or expired token'}
            else:
                return 400, {'error': availablePeriods['error_msg']}

    except Exception as e:
        return 400, {"error": str(e)}


@cronofyApi.get('/auth', response={200: schemas.AuthorizationCodeResponse, 401: schemas.ErrorResponse})
def Redirect_Authorization_Cronofy(request, code, uid=None):
    try:
        if code is None:
            return 403, {"error": "unauthorized"}

        userTokens = cronofy.Get_Access_Token(code, uid if uid is not None else None)
        if userTokens['success']:
            return 200, {"success": True}
        else:
            return 401, {"error": "Cannot exchange authorization code with user tokens."}

    except Exception as e:
        return 500, {"error": str(e)}


@cronofyApi.get('/token', response={200: schemas.CheckTokenResponse, 401: schemas.ErrorResponse})
def Check_Token(request, uid):
    try:
        if uid is not None:
            resopnse = cronofy.Generate_Access_Token(uid)
            if resopnse['success']:
                return 200, {"success": True}

            return 401, {"error": "Cannot refresh the token"}

    except Exception as e:
        return 500, {"error": str(e)}
