from abc import ABC, abstractmethod
import requests
import os
from PaymentGateways.models import Order
from Kadnya.settings import paymenyTechKey, testKey
from django.core.files.storage import default_storage


class PaymentGateway(ABC):
    @staticmethod  # to accomodate for the subclass having its methods static
    @abstractmethod  # has to be implemented in subclass
    def charge(self):
        pass

    @staticmethod
    @abstractmethod
    def refund(self):
        pass


# Main functionality:
# create_lead which should be converted to merchant later on
# charge
# refund
class Tap(PaymentGateway):
    @staticmethod
    def create_lead(payload):
        brand = {
            "name": {"en": payload.nameEn, "ar": payload.nameAr},
            "sector": ["Education"],
            "logo": payload.logo_id,
            "channelServices": [
                {"channel": "website", "address": "https://kadnya.com/"}
            ],
            "segment": {"type": {"code": "non_profit"}, "team": {"code": "small"}},
            "terms": [
                {"term": "general", "agree": True},
                {"term": "chargeback", "agree": True},
                {"term": "refund", "agree": True},
            ],
        }
        entity = {
            "country": payload.country,
            "is_licensed": payload.is_licensed,
            "license": {
                "number": payload.licenseNumber,
                "country": payload.licenseConutry,
                "type": payload.licenseType,
                "documents": [
                    {
                        "type": payload.licenseDocumentType,
                        "number": payload.licenseDocumentNumber,
                        "issuing_country": payload.licenseIssuingCountry,
                        "issuing_date": payload.issuingDate,
                        "expiry_date": payload.expiryDate,
                        "images": payload.licenseImages,
                    }
                ],
            },
        }
        wallet = {
            "bank": {
                "name": payload.bankName,
                "account": {
                    "name": payload.accountName,
                    "number": payload.accountNumber,
                    "swift": payload.accountSwift,
                    "iban": payload.accountIban,
                },
                "documents": [
                    {
                        "type": payload.documentType,
                        "number": payload.documentNumber,
                        "issuing_country": payload.documentIssuingCountry,
                        "issuing_date": payload.documentIssuingDate,
                        "images": payload.documentImages,
                    }
                ],
            }
        }
        user = {
            "name": {
                "lang": payload.userLang,
                "title": payload.userTitle,
                "first": payload.userFirstName,
                "middle": payload.userMiddleName,
                "last": payload.userLastname,
            },
            "email": [
                {
                    "type": payload.userEmailType,
                    "address": payload.userEmailAddress,
                    "primary": True,
                }
            ],
            "phone": [
                {
                    "type": payload.phoneNumberType,
                    "country_code": payload.phoneCountryCode,
                    "number": payload.phoneNumber,
                }
            ],
            "nationality": payload.nationality,
            "identification": {
                "number": payload.idNumber,
                "type": payload.idType,
                "issuer": payload.Isuuer,
                "images": payload.idImages,
            },
            "birth": {
                "country": payload.birthCountry,
                "city": payload.birthCity,
                "birth_date": payload.birthDate,
            },
            "primary": True,
        }
        post = {"url": "https://kadnya.com/pay"}
        payload_data = {
            "brand": brand,
            "entity": entity,
            "wallet": wallet,
            "user": user,
            "post": post,
            "metadata": payload.metadata,
            "payment_provider": {"id": paymenyTechKey},
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": testKey,
        }
        response = requests.post(
            "https://api.tap.company/v3/connect/lead/",
            json=payload_data,
            headers=headers,
        )

    @staticmethod
    def create_file(payload, file):
        temp_file_path = f"tmp/{file.name}"

        temp_file_name = default_storage.save(temp_file_path, file)
        headers = {
            "Authorization": testKey,
        }
        payload_data = payload.dict()
        with default_storage.open(temp_file_name, "rb") as temp_file:
            files = {"file": (file.name, temp_file)}
            response = requests.post(
                "https://api.tap.company/v2/files/",
                data=payload_data,
                files=files,
                headers=headers,
            )
        if default_storage.exists(temp_file_name):
            default_storage.delete(temp_file_name)
        return response

    @staticmethod
    def charge(payload):
        os.environ["SECRET_KEY"]
        order_id = Order.objects.get(user_id=payload.user_id).id
        reference = {"transaction": order_id, "order": order_id}
        receipt = {"email": payload.email, "sms": payload.sms}
        customer = {
            "first_name": payload.firstName,
            "middle_name": payload.middleName,
            "last_name": payload.lastName,
            "email": payload.emailAddress,
            "phone": {
                "country_code": payload.phoneCountryCode,
                "number": payload.phoneNumber,
            },
        }
        merchant = {"id": payload.merchant_id}
        source = {"id": payload.ID}
        post = {"url": payload.postUrl}
        redirect = {"url": payload.redirectUrl}
        payload_data = {
            "amount": payload.amount,
            "currency": payload.currency,
            "customer_initiated": True,
            "threeDSecure": True,
            "save_card": payload.saveCard,
            "description": payload.description,
            "metadata": payload.metadata,
            "reference": reference,
            "receipt": receipt,
            "customer": customer,
            "merchant": merchant,
            "source": source,
            "post": post,
            "redirect": redirect,
            "payment_provider": {"technology": {"id": paymenyTechKey}},
        }
        headers = {
            "Authorization": testKey,
        }
        response = requests.post(
            url="https://api.tap.company/v2/charges", json=payload_data, headers=headers
        )
        return response

    @staticmethod
    def retrieve_charge(charge_id):
        headers = {
            "Authorization": testKey,
        }

        response = requests.get(
            url=f"https://api.tap.company/v2/charges/{charge_id}",
            headers=headers,
        )
        return response

    @staticmethod
    def refund():
        pass
