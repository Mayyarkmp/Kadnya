from . import baseCalendar


class InterfaceCalendar(baseCalendar.BaseCalendar):

    def Authorization(self, uid, sp):
        return self.authorization(uid, sp)

    def GetAccessToken(self, code, uid, sp, request):
        return self.getAccessToken(code, uid, sp, request)

    def RefreshAccessToken(self, uid, sp):
        return self.refreshAccessToken(uid, sp)

    def GetUserBusyTime(self, uid, sp):
        return self.getUserBusyTime(uid, sp)

    # def GetUserAvailableSchedule(self, uid, sp):
    #     self.getUserAvailableSchedule(uid, sp)

    # def GetUserEvents(self, uid, sp, active):
    #     self.getUserEvents(uid, sp, active)

    def GetUserScheduledEvents(self, uid, sp, status):
        return self.getUserScheduledEvents(uid, sp, status)

    def GetUserScheduledEventsInvitees(self, uid, sp, event_uuid, status):
        return self.getUserScheduledEventsInvitees(uid, sp, event_uuid, status)

    def GetScheduledEventDetails(self, uid, sp, event_uuid):
        return self.getScheduledEventsDetails(uid, sp, event_uuid)
