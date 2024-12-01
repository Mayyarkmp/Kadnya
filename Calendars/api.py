from ninja import NinjaAPI
from Calendars.interfaceCalendar import InterfaceCalendar
from . import schemas

calendarApi = NinjaAPI(urls_namespace="Calendars")
calendar = InterfaceCalendar()


@calendarApi.get(
    "/auth",
    response={
        200: schemas.AuthorizationCodeResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def Redirect_Authorization(request, code, uid=None):
    try:
        if code is None:
            return 401, {"error": "unauthorized"}

        uidArray = uid.split("-")
        uid = uidArray[0]
        sp = uidArray[1]

        response = calendar.getAccessToken(code, uid, sp)
        if response["success"]:
            return 200, {"success": True}
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/token",
    response={
        200: schemas.AuthorizationCodeResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def Refresh_Token(request, uid=None, sp=None):
    try:
        response = calendar.refreshAccessToken(uid, sp)
        if response["success"]:
            return 200, {"success": True}
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/busy_time",
    response={
        200: schemas.GetUserBusyTimeResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def User_Busy_Time(request, uid=None, sp=None):
    try:
        response = calendar.getUserBusyTime(uid, sp)
        if response["success"]:
            return 200, {"success": True, "user_busy_time": response["user_busy_time"]}
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/user_available",
    response={
        200: schemas.GetUserAvailableResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def User_Available_Schedule(request, uid=None, sp=None):
    try:
        response = calendar.getUserAvailableSchedule(uid, sp)
        if response["success"]:
            return 200, {
                "success": True,
                "user_available_schedule": response["user_available_schedule"],
            }
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/user_events",
    response={
        200: schemas.GetUserEventsResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def User_Events(request, uid=None, sp=None, active=None):
    try:
        response = calendar.getUserEvents(uid, sp, active)
        if response["success"]:
            return 200, {"success": True, "user_events": response["user_events"]}
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/user_scheduled_events",
    response={
        200: schemas.GetUserScheduledEventsResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def User_Scheduled_Events(request, uid=None, sp=None, status=None):
    try:
        response = calendar.getUserScheduledEvents(uid, sp, status)
        if response["success"]:
            return 200, {
                "success": True,
                "user_scheduled_events": response["user_scheduled_events"],
            }
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}


@calendarApi.get(
    "/user_scheduled_events_invitees",
    response={
        200: schemas.GetUserScheduledEventsInviteesResponse,
        500: schemas.ErrorResponse,
        400: schemas.ErrorResponse,
        401: schemas.ErrorResponse,
    },
)
def User_Scheduled_Events_Invitees(
    request, uid=None, sp=None, event_uuid=None, status=None
):
    try:
        response = calendar.getUserScheduledEventsInvitees(uid, sp, event_uuid, status)
        if response["success"]:
            return 200, {
                "success": True,
                "user_events_invitees": response["user_events_invitees"],
            }
        else:
            return 400, {"error": response["error_msg"]}

    except Exception as e:
        return 500, {"error": str(e)}
