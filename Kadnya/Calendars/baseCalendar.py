from Calendars.Calendly.apiClient import Calendly


class BaseCalendar:
    calendly = Calendly()

    def getAccessToken(self, code, uid, sp):
        try:

            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getAccessToken(code=code, uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def refreshAccessToken(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.refreshAccessToken(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserBusyTime(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getUserBusyTime(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserAvailableSchedule(self, uid, sp):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getUserAvailabilitySchedule(uid=uid, sp=sp)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserEvents(self, uid, sp, active=None):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getUserEvents(uid=uid, sp=sp, active=active)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserScheduledEvents(self, uid, sp, status=None):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getScheduledEvents(uid=uid, sp=sp, status=status)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}

    def getUserScheduledEventsInvitees(self, uid, sp, event_uuid=None, status=None):
        try:
            if uid is not None and sp is not None:
                if sp == 'calendly':
                    response = self.calendly.getScheduledEventsInvitees(uid=uid, sp=sp,event_uuid=event_uuid, status=status)
                    return response

            return {'success': False, 'error': True, 'error_msg': "Missing required Fields"}
        except Exception as e:
            return {'success': False, 'error': True, 'error_msg': f"{str(e)}"}
