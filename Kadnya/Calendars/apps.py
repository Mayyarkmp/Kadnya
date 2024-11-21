import os

from django.apps import AppConfig
from Kadenya import settings
from Kadenya.settings import BASE_DIR


class CalendarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Calendars'
    oAuthRedirectUrl = settings.OAUTH_REDIRECT_URI

