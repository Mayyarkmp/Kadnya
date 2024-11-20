from abc import ABC
import requests
import os
from Integration.models import Transaction
from Kadnya.settings import paymenyTechKey, testKey
from django.core.files.storage import default_storage


class PaymentGateway(ABC):
    @staticmethod  # to accomodate for the subclass having its methods static
    def charge():
        pass

    @staticmethod
    def refund():
        pass


# Main functionality:
# create_lead which should be converted to merchant later on
# charge
# refund
class Tap(PaymentGateway):
    @staticmethod
    def create_lead(payload, **kwargs):
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
        return response

    @staticmethod
    def create_file(payload, **kwargs):
        file = kwargs["file"]
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
    def charge(payload, **kwargs):
        os.environ["SECRET_KEY"]
        try:
            print("#1-------------------------------------------")
            order_id = Transaction.objects.filter(user_id=payload.user_id)[0].id
        except Exception as e:
            print("#2++++++++++++++++++++++++++++++++++++++++++++   +")
            return {"status_code": 500, "error": f"{e}"}
        print("//////////////////////////////////////////////////")
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
        return response.status_code, response.json()

    @staticmethod
    def update_charge(payload, **kwargs):
        headers = {
            "Authorization": "Bearer sk_test_XKokBfNWv6FIYuTMg5sLPjhJ",
        }
        response = requests.put(
            url=f"https://api.tap.company/v2/charges/{kwargs['charge_id']}",
            headers=headers,
            json=payload.dict(),
        )
        return response

    @staticmethod
    def retrieve_charge(payload, **kwargs):
        headers = {
            "Authorization": testKey,
        }

        response = requests.get(
            url=f"https://api.tap.company/v2/charges/{kwargs['charge_id']}",
            headers=headers,
        )
        return response

    @staticmethod
    def refund():
        pass


class EdfaPay(PaymentGateway):
    @staticmethod
    def charge(
        payload,
    ):  # corresponds to the initiate operation in the documentati, **kwargson
        payload_data = {
            "action": payload.action,
            "edfa_merchant_id": payload.merchant_id,
            "order_id": "ORD001",  # to be audited
            "order_amount": payload.amount,
            "order_currency": payload.currency,
            "order_description": payload.description,
            "req_token": "N",  # OPTIONAL: depends whether we want card payment option or not, is so the response will contain a token
            "payer_first_name": payload.firstName,
            "payer_last_name": payload.lastName,
            "payer_address": payload.address,  # email
            "payer_country": payload.country,
            "payer_city": payload.city,
            "payer_zip": payload.zip,
            "payer_email": payload.email,
            "payer_phone": payload.phone,
            "payer_ip": payload.ip,
            "term_url_3ds": payload.redirectUrl,  # redirect url
            "auth": "N",  # Indicates that transaction must be only authenticated, but not captured
            "recurring_init": "N",  # OPTIONAL: Initialization of the transaction with possible following recurring
            "hash": "xxxxxxx-xxxx-xxxxxx",
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", files=payload_data
        )
        return response

    @staticmethod
    def recur(payload, **kwargs):
        payload_data = {
            "gwayId": payload.gwayId,  # String , Public transaction id of Payment Gateway
            "order_id": payload.order_id,
            "edfapay_merchant_id": payload.user_id,
            "amount": payload.amount,
            "hash": "xxxxxxx-xxxx-xxxxxx",  # Special signature to validate your request to payment platform
            "payer_ip": payload.ip,
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", data=payload_data
        )
        return response

    @staticmethod
    def get_status(payload, **kwargs):
        payload_data = {
            "merchant_id": payload.merchant_id,  # String , Public transaction id of Payment Gateway
            "gway_Payment_Id": payload.gway_Payment_Id,
            "order_id": payload.order_id,
            "hash": "xxxxxxx-xxxx-xxxxxx",  # Special signature to validate your request to payment platform
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", data=payload_data
        )
        return response

    @staticmethod
    def refund(payload, **kwargs):
        payload_data = {
            "edfapay_merchant_id": payload.edfapay_merchant_id,  # String , Public transaction id of Payment Gateway
            "gwayId": payload.gwayId,
            "amount": payload.amount,
            "trans_id": payload.trans_id,
            "order_id": payload.order_id,
            "hash": "xxxxxxx-xxxx-xxxxxx",  # Special signature to validate your request to payment platform
            "payer_ip": payload.ip,
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", data=payload_data
        )
        return response
