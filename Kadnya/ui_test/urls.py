from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_options, name="payment_options"),
    path("charge/", views.charge_operation, name="charge_operation"),
    path(
        "retrieve/", views.retrieve_charge_operation, name="retrieve_charge_operation"
    ),
    path("initiate-merchant/", views.initiate_merchant, name="initiate_merchant"),
]
