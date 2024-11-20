from Integration.models import Charge, Lead, License, Wallet
from django.test import TestCase
from unittest.mock import patch, MagicMock
from ninja.testing import TestClient
from Integration.api import tapApi
from Integration.models import File as File2
from io import BytesIO


class ChargeEndpointTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(tapApi)
        self.valid_payload = {
            "serviceProvider": "Tap",
            "user_id": "user123",
            "amount": 100,
            "currency": "USD",
            "metadata": {"udf1": "Test Metadata"},
            "description": "Test transaction",
            "transaction": "txn_123",
            "order": "ord_123",
            "email": True,
            "sms": True,
            "firstName": "John",
            "middleName": "-",
            "lastName": "Doe",
            "emailAddress": "john.doe@example.com",
            "phoneCountryCode": 1,
            "phoneNumber": 1234567890,
            "merchant_id": "merchant123",
            "ID": "src_all",
            "saveCard": False,
            "postUrl": "http://kadynia.com/post_url",
            "redirectUrl": "http://kadynia.com/redirect_url",
        }

    @patch("Integration.corridor")
    def test_charge_success(self, mock_corridor):
        mock_corridor.return_value.status_code = 200
        mock_corridor.return_value.json.return_value = {
            "id": "charge123",
            "amount": 100.0,
            "currency": "USD",
            "status": "success",
            "transaction": {"url": "http://paymentgateway.com/continue"},
            "activities": [{"created": 1634155200}],
        }

        response = self.client.post("/charge", json=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": "charge123",
                "amount": 100.0,
                "currency": "USD",
                "status": "success",
                "url": "http://paymentgateway.com/continue",
                "timestamp": 1634155200,
            },
        )

    @patch("Integration.corridor")
    def test_charge_failure(self, mock_corridor):
        mock_corridor.return_value.status_code = 400
        mock_corridor.return_value.json.return_value = {"errors": ["Invalid data"]}

        response = self.client.post("/charge", json=self.valid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"errors": ["Invalid data"]})

    @patch("Integration.corridor")
    def test_charge_server_error(self, mock_corridor):
        mock_corridor.return_value.status_code = 500
        mock_corridor.return_value.json.return_value = {
            "errors": ["Internal server error"]
        }

        response = self.client.post("/charge", json=self.valid_payload)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"errors": ["Internal server error"]})


class CreateLeadEndpointTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(tapApi)
        self.valid_payload = {
            "serviceProvider": "Tap",
            "nameEn": "Test Name",
            "nameAr": "اختبار",
            "logo_id": "logo123",
            "country": "SA",
            "is_licensed": True,
            "licenseNumber": "123456789",
            "licenseDocumentNumber": "987654321",
            "licenseConutry": "SA",
            "licenseIssuingCountry": "SA",
            "issuingDate": "2023-01-01",
            "expiryDate": "2025-01-01",
            "licenseImages": ["image1", "image2"],
            "bankName": "Test Bank",
            "accountName": "Test Account",
            "accountSwift": "SWIFT123",
            "accountIban": "IBAN123456789",
            "accountNumber": "123456789",
            "documentNumber": "DOC123",
            "documentIssuingCountry": "SA",
            "documentIssuingDate": "2023-01-01",
            "documentImages": ["doc1", "doc2"],
            "userLang": "en",
            "userFirstName": "John",
            "userLastname": "Doe",
            "userEmailType": "work",
            "userEmailAddress": "john.doe@example.com",
            "phoneCountryCode": "+966",
            "phoneNumber": "555123456",
            "nationality": "SA",
            "idNumber": "ID123456789",
            "idType": "National ID",
            "Isuuer": "Saudi Arabia",
            "idImages": ["id1", "id2"],
            "birthCountry": "SA",
            "birthCity": "Riyadh",
            "birthDate": "1990-01-01",
            "metadata": {"key": "value"},
            "postUrl": "https://kadnya.com/pay",
            "licenseDocumentType": "commercial_registration",
            "licenseType": "commercial_registration",
            "documentType": "Bank Statement",
            "userMiddleName": "-",
            "userTitle": "Mr",
            "phoneNumberType": "WORK",
        }

    @patch("Integration.corridor")
    def test_create_lead_success(self, mock_corridor):
        mock_corridor.return_value.status_code = 200
        mock_corridor.return_value.json.return_value = {"id": "lead123"}

        response = self.client.post("/create_lead", json=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "lead123"})

        self.assertEqual(Lead.objects.count(), 1)
        self.assertEqual(License.objects.count(), 1)
        self.assertEqual(Wallet.objects.count(), 1)

    @patch("Integration.corridor")
    def test_create_lead_failure(self, mock_corridor):
        mock_corridor.return_value.status_code = 400
        mock_corridor.return_value.json.return_value = {"errors": ["Invalid data"]}

        response = self.client.post("/create_lead", json=self.valid_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"errors": ["Invalid data"]})

        self.assertEqual(Lead.objects.count(), 0)
        self.assertEqual(License.objects.count(), 0)
        self.assertEqual(Wallet.objects.count(), 0)

    @patch("Integration.corridor")
    def test_create_lead_server_error(self, mock_corridor):
        mock_corridor.return_value.status_code = 500
        mock_corridor.return_value.json.return_value = {
            "error": "Internal Server Error"
        }

        response = self.client.post("/create_lead", json=self.valid_payload)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Internal Server Error"})

        self.assertEqual(Lead.objects.count(), 0)
        self.assertEqual(License.objects.count(), 0)
        self.assertEqual(Wallet.objects.count(), 0)


class CreateFileEndpointTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(tapApi)
        self.valid_payload = {
            "serviceProvider": "Tap",
            "purpose": "Verification",
            "title": "Test File",
            "expires_at": "1913743462",
            "file_link_create": True,
        }
        self.valid_file = BytesIO(b"dummy file content")
        self.valid_file.name = "test_file.txt"

    @patch("Integration.corridor")
    def test_create_file_success(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": "file123"}
        mock_corridor.return_value = mock_response

        response = self.client.post(
            "/create_file",
            data=self.valid_payload,
            files={"file": self.valid_file},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": "file123"})

        self.assertEqual(File2.objects.count(), 1)
        self.assertEqual(File2.objects.first().file_id, "file123")

    @patch("Integration.corridor")
    def test_create_file_not_found(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"errors": ["File not found"]}
        mock_corridor.return_value = mock_response

        response = self.client.post(
            "/create_file",
            data=self.valid_payload,
            files={"file": self.valid_file},
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"errors": ["File not found"]})

        self.assertEqual(File2.objects.count(), 0)

    @patch("Integration.corridor")
    def test_create_file_server_error(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_corridor.return_value = mock_response

        response = self.client.post(
            "/create_file",
            data=self.valid_payload,
            files={"file": self.valid_file},
        )
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Internal Server Error"})

        self.assertEqual(File2.objects.count(), 0)


class RetrieveChargeEndpointTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(tapApi)
        self.valid_charge_id = "charge123"
        self.payload_retrieve = {
            "amount": 1000,
            "currency": "USD",
            "status": "success",
            "url": "http://example.com/payment",
            "timestamp": 1637854800,
        }

    @patch("Integration.corridor")
    def test_retrieve_charge_success(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": self.valid_charge_id,
            "amount": self.payload_retrieve["amount"],
            "currency": self.payload_retrieve["currency"],
            "status": self.payload_retrieve["status"],
            "transaction": {"url": self.payload_retrieve["url"]},
            "activities": [{"created": self.payload_retrieve["timestamp"]}],
        }
        mock_corridor.return_value = mock_response

        response = self.client.get(f"/retrive_charge/{self.valid_charge_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.payload_retrieve)

        self.assertEqual(Charge.objects.count(), 1)
        charge = Charge.objects.first()
        self.assertEqual(charge.charge_id, self.valid_charge_id)
        self.assertEqual(charge.amount, self.payload_retrieve["amount"])
        self.assertEqual(charge.currency, self.payload_retrieve["currency"])
        self.assertEqual(charge.status, self.payload_retrieve["status"])
        self.assertEqual(charge.url, self.payload_retrieve["url"])
        self.assertEqual(charge.timestamp, self.payload_retrieve["timestamp"])

    @patch("Integration.corridor")
    def test_retrieve_charge_not_found(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"errors": ["Charge not found"]}
        mock_corridor.return_value = mock_response

        response = self.client.get(f"/retrive_charge/{self.valid_charge_id}")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"errors": ["Charge not found"]})

        self.assertEqual(Charge.objects.count(), 0)

    @patch("Integration.corridor")
    def test_retrieve_charge_server_error(self, mock_corridor):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_corridor.return_value = mock_response

        response = self.client.get(f"/retrive_charge/{self.valid_charge_id}")
        self.assertEqual(
            response.status_code, 404
        )  # Function handles all non-200 as 404
        self.assertEqual(response.json(), {"error": "Internal Server Error"})

        # Verify that no Charge objects are created in the database
        self.assertEqual(Charge.objects.count(), 0)
