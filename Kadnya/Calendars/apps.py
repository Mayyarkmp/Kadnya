from django.apps import AppConfig
from Kadenya import settings


class CalendarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Calendars'
    oAuthRedirectUrl = settings.OAUTH_REDIRECT_URI

