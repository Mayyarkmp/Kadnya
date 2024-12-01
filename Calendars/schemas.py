from ninja import Schema

class GetScheduledEventsDetailsResponse(Schema, ):
    success: bool
    event: object
class GetUserScheduledEventsInviteesResponse(Schema, ):
    success: bool
    user_events_invitees: list

class GetUserScheduledEventsResponse(Schema, ):
    success: bool
    user_scheduled_events: list


class GetUserEventsResponse(Schema, ):
    success: bool
    user_events: list


class GetUserAvailableResponse(Schema, ):
    success: bool
    user_available_schedule: list


class GetUserBusyTimeResponse(Schema, ):
    success: bool
    user_busy_time: list


class GetUserCalendarsResponse(Schema, ):
    success: bool
    calendars_list: list


class GetUserAvailabilityResponse(Schema, ):
    success: bool
    available_periods: list


class AuthorizationCodeResponse(Schema):
    success: bool


class CheckTokenResponse(Schema):
    success: bool


class ErrorResponse(Schema):
    error: str
