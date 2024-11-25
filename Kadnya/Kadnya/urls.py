from django.contrib import admin
from django.urls import path, include
from Calendars.api import calendarApi

# from .api import api
from PaymentGateways.api import paymentGatewayApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("payment_gateways/", paymentGatewayApi.urls),
    path("calendar/", calendarApi.urls),
    path("", include("ui_test.urls")),
]
