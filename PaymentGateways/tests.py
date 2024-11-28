import json
from django.test import TestCase
from ninja.testing import TestClient
from PaymentGateways.api import paymentGatewayApi


class PaymentGatewayTests(TestCase):
    def setUp(self):
        self.client = TestClient(paymentGatewayApi)

    def test_charge_success(self):
        """
        Test the `/charge` endpoint with valid data and expect a 200 response.
        """
        valid_payload = {
            "user_id": "1234",
            "serviceProvider": "Tap",
            "amount": "2",
            "currency": "AED",
            "customer_initiated": True,
            "threeDSecure": True,
            "save_card": "false",
            "description": "test",
            "metadata": {"udf1": "Metadata 1"},
            "phoneCountryCode": 965,
            "phoneNumber": 51234567,
            "saveCard": "false",
            "email": "true",
            "sms": "true",
            "firstName": "test",
            "middleName": "test",
            "lastName": "test",
            "emailAddress": "test@test.com",
            "country_code": "965",
            "number": "51234567",
            "merchant_id": "merchant_4m4B5624940fGnu21mj9W912",
            "ID": "src_all",
            "postUrl": "http://kadynia.com/post_url",
            "redirectUrl": "http://kadynia.com/post_url",
        }

        response = self.client.post("/charge", json=valid_payload)

        self.assertEqual(response.status_code, 200)

        self.assertIn("url", response.json())
        self.assertIn("extraData", response.json())
        extra_data = response.json()["extraData"]
        self.assertIn("id", extra_data)
        self.assertIn("amount", extra_data)
        self.assertIn("currency", extra_data)
        self.assertIn("status", extra_data)
        self.assertIn("timestamp", extra_data)

    def test_charge_bad_request(self):
        invalid_payload = {
            "user_id": "1234",
            "serviceProvider": "Tap",
            "amount": "2",
            "currency": "AEDasd",
            "customer_initiated": True,
            "threeDSecure": True,
            "save_card": "false",
            "description": "test",
            "metadata": {"udf1": "Metadata 1"},
            "phoneCountryCode": 965,
            "phoneNumber": 51234567,
            "saveCard": "false",
            "email": "true",
            "sms": "true",
            "firstName": "test",
            "middleName": "test",
            "lastName": "test",
            "emailAddress": "test@test.com",
            "country_code": "965",
            "number": "51234567",
            "merchant_id": "merchant_4m4B5624940fGnu21mj9W912",
            "ID": "src_all",
            "postUrl": "http://kadynia.com/post_url",
            "redirectUrl": "http://kadynia.com/post_url",
        }

        response = self.client.post("/charge", json=invalid_payload)

        self.assertEqual(response.status_code, 400)

        self.assertIn("error", response.json())

    def test_create_lead_success(self):
        valid_payload = {
            "nameEn": "om kelthom",
            "nameAr": "أم كلثوم",
            "logo_id": "logo123",
            "sector": "Education",
            "channel": "website",
            "channel_address": "https://kadnya.com/",
            "segment_type_code": "non_profit",
            "segment_team_code": "small",
            "term_general_agree": "true",
            "term_chargeback_agree": "true",
            "term_refund_agree": "true",
            "country": "CountryName",
            "is_licensed": "true",
            "licenseNumber": "LIC12345",
            "licenseCountry": "LicenseCountry",
            "licenseType": "TypeA",
            "licenseDocumentType": "DocTypeA",
            "licenseDocumentNumber": "DocNum123",
            "licenseIssuingCountry": "IssuingCountry",
            "issuingDate": "2024-01-01",
            "expiryDate": "2025-01-01",
            "licenseImages": ["image1.png", "image2.png"],
            "bankName": "Bank ABC",
            "accountName": "Account Holder",
            "accountNumber": "123456789",
            "accountSwift": "SWIFT123",
            "accountIban": "IBAN123456",
            "documentType": "BankDoc",
            "documentNumber": "DocNum789",
            "documentIssuingCountry": "BankDocCountry",
            "documentIssuingDate": "2023-01-01",
            "documentImages": ["docImage1.png", "docImage2.png"],
            "userLang": "en",
            "userTitle": "Mr.",
            "userFirstName": "John",
            "userMiddleName": "M.",
            "userLastname": "Doe",
            "userEmailType": "work",
            "userEmailAddress": "john.doe@example.com",
            "phoneNumberType": "mobile",
            "phoneCountryCode": "+1",
            "phoneNumber": "1234567890",
            "nationality": "American",
            "idNumber": "ID123456",
            "idType": "Passport",
            "Isuuer": "Gov Authority",
            "idImages": ["idImage1.png"],
            "birthCountry": "USA",
            "birthCity": "New York",
            "birthDate": "1990-01-01",
            "metadata": "Additional Metadata",
        }

        response = self.client.post("/charge", json=valid_payload)

        self.assertEqual(response.status_code, 200)

        self.assertIn("id", response.json())

    def test_tap_retrieve_success(self):
        payload = {
            "serviceProvider": "Tap",
            "charge_id": "chg_TS07A1520241328i2M32511834",
        }
        response = self.client.post("/retireve_payment", json=payload)
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("amount", response_data)
        self.assertIsInstance(response_data["amount"], int)

        self.assertIn("currency", response_data)
        self.assertIsInstance(response_data["currency"], str)

        self.assertIn("status", response_data)
        self.assertIsInstance(response_data["status"], str)

        self.assertIn("timestamp", response_data)
        self.assertIsInstance(response_data["timestamp"], int)

        self.assertIn("extraData", response_data)
        self.assertIsInstance(response_data["extraData"], dict)

        extra_data = response_data["extraData"]
        self.assertIn("merchant_id", extra_data)
        self.assertIsInstance(extra_data["merchant_id"], str)

        self.assertIn("source", extra_data)
        self.assertIsInstance(extra_data["source"], str)

        self.assertIn("url", extra_data)
        self.assertIsInstance(extra_data["url"], str)

        self.assertIn("expiry", extra_data)
        self.assertIsInstance(extra_data["expiry"], int)

        self.assertIn("unit", extra_data)
        self.assertIsInstance(extra_data["unit"], str)
