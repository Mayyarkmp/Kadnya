from Calendars.Calendly.apiClient import Calendly
from Calendars.Calendly.config import sp as CalendlySp
from Calendars.GoogleCalendar.apiClient import GoogleCalendar
from Calendars.GoogleCalendar.config import sp as GoogleCalendarSp


class BaseCalendar:
    calendly = Calendly()
    googleCalendar = GoogleCalendar()

    def authorization(self, uid, sp):
        try:

            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.authorization(uid=uid, sp=sp)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.authorization(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getAccessToken(self, code, uid, sp, request=None):
        try:

            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.getAccessToken(code=code, uid=uid, sp=sp)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.getAccessToken(request=request, uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def refreshAccessToken(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.refreshAccessToken(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserBusyTime(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.getUserBusyTime(uid=uid, sp=sp)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.getUserBusyTime(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserAvailableSchedule(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.getUserAvailabilitySchedule(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserEvents(self, uid, sp, active=None):
        try:
            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.getUserEvents(uid=uid, sp=sp, active=active)
                    return response


            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserScheduledEvents(self, uid, sp, status=None):
        try:
            if uid is not None and sp is not None:
                if sp == CalendlySp:
                    response = self.calendly.getScheduledEvents(uid=uid, sp=sp, status=status)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.getUserScheduledEvents(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserScheduledEventsInvitees(self, uid, sp, event_uuid=None, status=None):
        try:
            if uid is not None and sp is not None and event_uuid is not None:
                if sp == CalendlySp:
                    response = self.calendly.getScheduledEventsInvitees(uid=uid, sp=sp, event_uuid=event_uuid,
                                                                        status=status)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.getUserScheduledEventInvitees(uid=uid, sp=sp, event_uuid=event_uuid)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getScheduledEventsDetails(self, uid, sp, event_uuid):
        try:
            if uid is not None and sp is not None and event_uuid is not None:
                if sp == CalendlySp:
                    response = self.calendly.getScheduledEventsDetails(uid=uid, sp=sp, event_uuid=event_uuid)
                    return response
                elif sp == GoogleCalendarSp:
                    response = self.googleCalendar.getUserScheduledEventDetails(uid=uid, sp=sp, event_uuid=event_uuid)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}
