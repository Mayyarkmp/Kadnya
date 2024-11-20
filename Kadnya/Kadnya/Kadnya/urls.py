from django.contrib import admin
from django.urls import path, include

# from .api import api
from PaymentGateways.api import tapApi

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("api/", include("Kadnya.api")),
    path("api/", tapApi.urls),
    # path("api/", api.urls),
]
