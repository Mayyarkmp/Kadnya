from ninja import Schema

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
