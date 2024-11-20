from django.contrib import admin
from django.urls import path, include

# from .api import api
from Integration.api import tapApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Integration/tap/", tapApi.urls),
]
