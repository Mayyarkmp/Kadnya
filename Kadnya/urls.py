from django.contrib import admin
from django.urls import path, include
from Calendars.api import calendarApi
from GoogleAnalytics.api import AnalyticsApi

# from .api import api
from PaymentGateways.api import paymentGatewayApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("payment_gateways/", paymentGatewayApi.urls),
    path("calendar/", calendarApi.urls),
    path("google_analytics/", AnalyticsApi.urls),
    path("", include("ui_test.urls")),
]
