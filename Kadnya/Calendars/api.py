from urllib.parse import parse_qs

from django.http import HttpResponseRedirect
from ninja import NinjaAPI

from Calendars.interfaceCalendar import InterfaceCalendar
from . import schemas

calendarApi = NinjaAPI(urls_namespace='Calendars')
calendar = InterfaceCalendar()


@calendarApi.get('/authorization', response={400: schemas.ErrorResponse,})
def Calendar_Authorization(request, uid=None, sp=None):
    try:
        response = calendar.authorization(uid=uid, sp=sp)
        if response['success']:
            return HttpResponseRedirect(response['url'])
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get('/auth', response=
{
    200: schemas.AuthorizationCodeResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def Redirect_Authorization(request, code, state=None):
    try:
        if code is None:
            return 401, {"error": "unauthorized"}

        decodeState = parse_qs(state)

        decodeStateString: str = decodeState.get("uid", [None])[0]

        decodeStateList = decodeStateString.split('-')
        uid = decodeStateList[0]
        sp = decodeStateList[1]

        response = calendar.GetAccessToken(code, uid, sp, request)
        if response['success']:
            return 200, {"success": True}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get('/token', response=
{
    200: schemas.AuthorizationCodeResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def Refresh_Token(request, uid=None, sp=None):
    try:
        response = calendar.RefreshAccessToken(uid, sp)
        if response['success']:
            return 200, {"success": True}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get('/busy_time', response=
{
    200: schemas.GetUserBusyTimeResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def User_Busy_Time(request, uid=None, sp=None):
    try:
        response = calendar.GetUserBusyTime(uid, sp)
        if response['success']:
            return 200, {"success": True, 'user_busy_time': response['user_busy_time']}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


# @calendarApi.get('/user_available', response=
# {
#     200: schemas.GetUserAvailableResponse,
#     500: schemas.ErrorResponse,
#     400: schemas.ErrorResponse,
#     401: schemas.ErrorResponse
# }
#                  )
# def User_Available_Schedule(request, uid=None, sp=None):
#     try:
#         response = calendar.getUserAvailableSchedule(uid, sp)
#         if response['success']:
#             return 200, {"success": True, 'user_available_schedule': response['user_available_schedule']}
#         else:
#             return 400, {"error": response['error_msg']}
#
#     except Exception as e:
#         return 500, {"error": str(e)}
#
#
# @calendarApi.get('/user_events', response=
# {
#     200: schemas.GetUserEventsResponse,
#     500: schemas.ErrorResponse,
#     400: schemas.ErrorResponse,
#     401: schemas.ErrorResponse
# }
#                  )
# def User_Events(request, uid=None, sp=None, active=None):
#     try:
#         response = calendar.getUserEvents(uid, sp, active)
#         if response['success']:
#             return 200, {"success": True, 'user_events': response['user_events']}
#         else:
#             return 400, {"error": response['error_msg']}
#
#     except Exception as e:
#         return 500, {"error": str(e)}


@calendarApi.get('/user_scheduled_events', response=
{
    200: schemas.GetUserScheduledEventsResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def User_Scheduled_Events(request, uid=None, sp=None, status=None):
    try:
        response = calendar.GetUserScheduledEvents(uid, sp, status)
        if response['success']:
            return 200, {"success": True, 'user_scheduled_events': response['user_scheduled_events']}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get('/user_scheduled_events_invitees', response=
{
    200: schemas.GetUserScheduledEventsInviteesResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def User_Scheduled_Events_Invitees(request, uid=None, sp=None, event_uuid=None, status=None):
    try:
        response = calendar.GetUserScheduledEventsInvitees(uid, sp, event_uuid, status)
        if response['success']:
            return 200, {"success": True, 'user_events_invitees': response['user_events_invitees']}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get('/scheduled_event_details', response=
{
    200: schemas.GetScheduledEventsDetailsResponse,
    500: schemas.ErrorResponse,
    400: schemas.ErrorResponse,
    401: schemas.ErrorResponse
}
                 )
def User_Scheduled_Events_Details(request, uid=None, sp=None, event_uuid=None):
    try:
        response = calendar.GetScheduledEventDetails(uid, sp, event_uuid)

        if response['success']:
            return 200, {"success": True, 'event': response['event']}
        else:
            return 400, {"error": response['error_msg']}

    except Exception as e:
        return 500, {"error": str(e)}
