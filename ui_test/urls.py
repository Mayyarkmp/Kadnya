from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("calendar_options/", views.calendar_options, name="calendar_options"),
    path("get_user_busy_time/", views.get_user_busy_time, name="get_user_busy_time"),
    path("get_scheduled_events/", views.get_scheduled_events, name="get_scheduled_events"),
    path("scheduled_event_details/", views.get_scheduled_event_details, name="scheduled_event_details"),
    path("user_scheduled_events_invitees/", views.get_user_scheduled_events_invitees,
         name="user_scheduled_events_invitees"),
    path("schedule_event/", views.schedule_event, name="schedule_event"),

    path("payment_options/", views.payment_options, name="payment_options"),
    path("charge/", views.charge_operation, name="charge_operation"),
    path(
        "retrieve/", views.retrieve_charge_operation, name="retrieve_charge_operation"
    ),
    path("initiate-merchant/", views.initiate_merchant, name="initiate_merchant"),
    path("card-sdk/", views.card_demo, name="card_sdk"),
]
