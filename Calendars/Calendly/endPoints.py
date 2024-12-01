authUrl = 'https://auth.calendly.com'
baseUrl = 'https://api.calendly.com'

# auth end points
authorization = 'https://auth.calendly.com/oauth/authorize'
getAuthorizationCodeUrl = '/oauth/authorize'
getAccessTokenUrl = '/oauth/token'

# availability
userBusyTime = '/user_busy_times'
userBusyTimeOutputDataShape = ['type', 'start_time', 'end_time', 'event_uuid']

userAvailableSchedules = '/user_availability_schedules'

# events
userEventTypes = '/event_types'

# scheduled events
scheduledEventInvitees = '/scheduled_events/*/invitees'
scheduledEvents = '/scheduled_events'
