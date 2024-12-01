from unittest.mock import patch

from django.test import TestCase, Client


class CalendarTest(TestCase):
    fixtures = ['Calendars/TestData/calendarUserMock.json']

    def setUp(self):
        self.client = Client()
        self.base_url = '/calendar'

    @patch('Calendars.api.User_Scheduled_Events')
    def test_user_scheduled_events_success(self, mock_get_user_scheduled_events):
        mock_get_user_scheduled_events.return_value = {
            "success": True,
            "user_scheduled_events": [
                {
                    'name': 'test-1-',
                    'status': 'active',
                    'event_uuid': 'sadsad54as45d4asd544asd788as7d4as5d112asd',
                    'event_uri': 'askpasfasflkasflaksfj',
                    'start_time': '2020/64/1666/20:20:20',
                    'end_time': '2020/64/1666/20:20:30',
                    'invitees_counter': '30',
                    'location': {
                        'testLocation': 'zoom'
                    }
                },
                {
                    'name': 'test-2-',
                    'status': 'canceled',
                    'event_uuid': 'sadsad54as45d4asd54ss4asd788as7d4as5d112asd',
                    'event_uri': 'askpasfasflkasflaksfj',
                    'start_time': '2020/64/1666/20:20:20',
                    'end_time': '2020/64/1666/20:20:30',
                    'invitees_counter': '30',
                    'location': {
                        'testLocation': 'zoom'
                    }
                }
            ]
        }

        response = self.client.get(f"{self.base_url}/user_scheduled_events", query_params={"uid": 1, "sp": "calendly"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(len(response.json()["user_scheduled_events"]), len(response.json()["user_scheduled_events"]))

    @patch('Calendars.api.User_Scheduled_Events')
    def test_user_scheduled_events_failure(self, mock_get_user_scheduled_events):
        mock_get_user_scheduled_events.return_value = {
            "success": False,
            "error_msg": "User not found"
        }

        response = self.client.get(f"{self.base_url}/user_scheduled_events", {"uid": 3, "sp": "calendly"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "CalendarUser matching query does not exist.")

    @patch('Calendars.api.User_Busy_Time')
    def test_user_busy_time_success(self, mock_get_user_busy_time):
        mock_get_user_busy_time.return_value = {
            "success": True,
            "user_busy_time": [
                {
                    'type': 'external',
                    'start_time': '2020/64/1666/20:20:20',
                    'end_time': '2020/64/1666/20:20:30',
                    'event_uuid': 'asdasdjbhvbe',
                    'event_uri': 'http://event/uri'

                },
                {
                    'type': 'internal',
                    'start_time': '2020/6/1666/20:20:20',
                    'end_time': '2020/6/1666/20:20:30',
                    'event_uuid': 'asdasdjbhvb232e',
                    'event_uri': 'http://event/uri123'
                }
            ]
        }
        response = self.client.get(f"{self.base_url}/busy_time", query_params={"uid": 1, "sp": "calendly"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(len(response.json()["user_busy_time"]), len(response.json()["user_busy_time"]))

    @patch('Calendars.api.User_Busy_Time')
    def test_user_busy_time_failure(self, mock_get_user_busy_time):
        mock_get_user_busy_time.return_value = {
            "success": False,
            "error_msg": "User not found"
        }

        response = self.client.get(f"{self.base_url}/user_scheduled_events", {"uid": 3, "sp": "calendly"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "CalendarUser matching query does not exist.")

    @patch('Calendars.api.User_Scheduled_Events_Details')
    def test_user_scheduled_events_details_success(self, mock_get_user_scheduled_events_details):
        mock_get_user_scheduled_events_details.return_value = {
            "success": True,
            "event":
                {
                    'name': 'test-1-',
                    'status': 'active',
                    'event_uuid': 'sadsad54as45d4asd544asd788as7d4as5d112asd',
                    'event_uri': 'askpasfasflkasflaksfj',
                    'start_time': '2020/64/1666/20:20:20',
                    'end_time': '2020/64/1666/20:20:30',
                    'invitees_counter': '30',
                    'location': {
                        'testLocation': 'zoom'
                    }
                }
        }
        response = self.client.get(f"{self.base_url}/scheduled_event_details", query_params={"uid": 1, "sp": "calendly",
                                                                                             "event_uuid": "93090660-06d2-440f-9304-05593c37d1c3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(len(response.json()["event"]), len(response.json()["event"]))

    @patch('Calendars.api.User_Scheduled_Events_Details')
    def test_user_scheduled_events_details_failure(self, mock_get_user_scheduled_events_details):
        mock_get_user_scheduled_events_details.return_value = {
            "success": False,
            "error_msg": "User not found"
        }

        response = self.client.get(f"{self.base_url}/user_scheduled_events", {"uid": 3, "sp": "calendly",
                                                                              "event_uuid": "93090660-06d2-440f-9304-05593c37d1c3"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "CalendarUser matching query does not exist.")

    @patch('Calendars.api.User_Scheduled_Events_Invitees')
    def test_user_scheduled_events_invitees_success(self, mock_get_user_scheduled_events_invitees):
        mock_get_user_scheduled_events_invitees.return_value = {
            "success": True,
            "user_events_invitees":
                [
                    {
                        'name': 'majd ali',
                        'status': 'active',
                        'rescheduled': False,
                        'reschedule_url': 'url',
                        'cancel_url': 'url',
                        'timezone': 'utc',
                    }
                ]
        }
        response = self.client.get(f"{self.base_url}/user_scheduled_events_invitees", query_params={"uid": 1, "sp": "calendly",
                                                                                             "event_uuid": "93090660-06d2-440f-9304-05593c37d1c3"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], True)
        self.assertEqual(len(response.json()["user_events_invitees"]), len(response.json()["user_events_invitees"]))

    @patch('Calendars.api.User_Scheduled_Events_Invitees')
    def test_user_scheduled_events_invitees_failure(self, mock_get_user_scheduled_events_invitees):
        mock_get_user_scheduled_events_invitees.return_value = {
            "success": False,
            "error_msg": "User not found"
        }

        response = self.client.get(f"{self.base_url}/user_scheduled_events_invitees", {"uid": 3, "sp": "calendly",
                                                                              "event_uuid": "93090660-06d2-440f-9304-05593c37d1c3"})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "CalendarUser matching query does not exist.")
