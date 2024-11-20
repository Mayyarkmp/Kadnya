from django.contrib import admin
from django.urls import path, include
from Calendars.api import calendarApi

# from .api import api
from Integration.api import tapApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("payment_gateways/", tapApi.urls),
    path("calendar/", calendarApi.urls),
]
