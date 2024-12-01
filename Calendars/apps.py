import os

from django.apps import AppConfig
from Kadnya import settings
from Kadnya.settings import BASE_DIR


class CalendarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Calendars'
    oAuthRedirectUrl = settings.OAUTH_REDIRECT_URI

