from . import baseCalendar


class InterfaceCalendar(baseCalendar.BaseCalendar):

    def GetAccessToken(self, code, uid, sp):
        self.getAccessToken(code, uid, sp)

    def RefreshAccessToken(self, uid, sp):
        self.refreshAccessToken(uid, sp)

    def GetUserBusyTime(self, uid, sp):
        self.getUserBusyTime(uid, sp)

    def GetUserAvailableSchedule(self, uid, sp):
        self.getUserAvailableSchedule(uid, sp)

    def GetUserEvents(self, uid, sp, active):
        self.getUserEvents(uid, sp, active)

    def GetUserScheduledEvents(self, uid, sp, status):
        self.getUserScheduledEvents(uid, sp, status)

    def GetUserScheduledEventsInvitees(self, uid, sp, event_uuid, status):
        self.getUserScheduledEventsInvitees(uid, sp, event_uuid, status)
