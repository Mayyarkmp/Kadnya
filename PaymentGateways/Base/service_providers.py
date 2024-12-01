from abc import ABC
import requests
import os
from PaymentGateways.models import Transaction
from Kadnya.settings import paymenyTechKey, testKey, SECRET_KEY
from django.core.files.storage import default_storage

from PaymentGateways.utils.Dateformats import dateToMilliseconds
from PaymentGateways.utils.generateHash import Hash


class PaymentGateway(ABC):
    @staticmethod  # to accomodate for the subclass having its methods static
    def charge():
        pass

    @staticmethod
    def retrieve_payment():
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
            "name": {"en": payload["brandNameEn"], "ar": payload["brandNameAr"]},
            "sector": ["Education"],
            "logo": payload["brandLogo_id"],
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
            "country": payload["entityCountry"],
            "is_licensed": payload["entity_is_licensed"],
            "license": {
                "number": payload["entityLicenseNumber"],
                "country": payload["entityLicenseCountry"],
                "type": payload["entityLicenseType"],
                "documents": [
                    {
                        "type": payload["entityLicenseDocumentType"],
                        "number": payload["entityLicenseDocumentNumber"],
                        "issuing_country": payload[
                            "entityLicenseDocumentIssuingCountry"
                        ],
                        "issuing_date": payload["entityLicenseDocumentIssuingDate"],
                        "expiry_date": payload["entityLicenseDocumentExpiryDate"],
                        "images": payload["entityLicenseDocumentImages"],
                    }
                ],
            },
        }
        wallet = {
            "bank": {
                "name": payload["walletBankName"],
                "account": {
                    "name": payload["walletAccountName"],
                    "number": payload["walletAccountNumber"],
                    "swift": payload["walletAccountSwift"],
                    "iban": payload["walletAccountIban"],
                },
                "documents": [
                    {
                        "type": payload["WalletBankDocumentType"],
                        "number": payload["WalletBankDocumentNumber"],
                        "issuing_country": payload["WalletBankDocumentIssuingCountry"],
                        "issuing_date": payload["WalletBankDocumentIssuingDate"],
                        "images": payload["WalletBankDocumentImages"],
                    }
                ],
            }
        }
        user = {
            "name": {
                "lang": payload["userLang"],
                "title": payload["userTitle"],
                "first": payload["userFirstName"],
                "middle": payload["userMiddleName"],
                "last": payload["userLastName"],
            },
            "email": [
                {
                    "type": payload["userEmailType"],
                    "address": payload["userEmailAddress"],
                    "primary": True,
                }
            ],
            "phone": [
                {
                    "type": payload["userPhoneType"],
                    "country_code": payload["userPhoneCountryCode"],
                    "number": payload["userPhoneNumber"],
                }
            ],
            "nationality": payload["userNationality"],
            "identification": {
                "number": payload["userIdentificationNumber"],
                "type": payload["userIdentificationType"],
                "issuer": payload["userIdentificationIssuer"],
                "images": payload["userIdentificationImages"],
            },
            "birth": {
                "country": payload["userBirthCountry"],
                "city": payload["userBirthCity"],
                "birth_date": payload["userBirthDate"],
            },
            "primary": True,
        }
        post = {"url": payload["postUrl"]}
        payload_data = {
            "brand": brand,
            "entity": entity,
            "wallet": wallet,
            "user": user,
            "post": post,
            "metadata": {"mtd": "metadata"},
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
        status_code = response.status_code
        response = response.json()
        return status_code, response

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
        # try:
        #     print("#1-------------------------------------------")
        #     order_id = Transaction.objects.filter(user_id=payload["user_id"])[0].id
        # except Exception as e:
        #     print("#2++++++++++++++++++++++++++++++++++++++++++++   +")
        #     return {"status_code": 500, "error": f"{e}"}
        reference = {"transaction": "2", "order": "2"}
        print(payload)
        receipt = {
            "email": payload["email_notification"],
            "sms": payload["sms_notification"],
        }
        customer = {
            "first_name": payload["firstName"],
            "middle_name": payload["middleName"],
            "last_name": payload["lastName"],
            "email": payload["emailAddress"],
            "phone": {
                "country_code": payload["phoneCountryCode"],
                "number": payload["phoneNumber"],
            },
        }
        merchant = {"id": payload["merchant_id"]}
        source = {"id": payload["source_id"]}
        post = {"url": payload["postUrl"]}
        redirect = {"url": payload["redirectUrl"]}
        payload_data = {
            "amount": payload["amount"],
            "currency": payload["currency"],
            "customer_initiated": True,
            "threeDSecure": True,
            "save_card": payload["saveCard"],
            "description": payload["description"],
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
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            extraData = {
                "id": response["id"],
                "amount": response["amount"],
                "currency": response["currency"],
                "status": response["status"],
                "timestamp": response["activities"][0]["created"],
            }
            data = {"url": response["transaction"]["url"], "extraData": extraData}
            return 200, data
        return 400, {"error": "Invalid Request", "extra": response}

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
    def retrieve_payment(payload, **kwargs):  # setup correct unified response
        headers = {
            "Authorization": testKey,
        }

        response = requests.get(
            url=f"https://api.tap.company/v2/charges/{payload['charge_id']}",
            headers=headers,
        )
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            extraData = {
                "merchant_id": response["merchant"]["id"],
                "source": response["source"]["id"],
                "url": response["transaction"]["url"],
                "expiry": response["transaction"]["expiry"]["period"],
                "unit": response["transaction"]["expiry"]["type"],
            }
            data = {
                "status": response["status"],
                "amount": response["amount"],
                "currency": response["currency"],
                "timestamp": response["transaction"]["created"],
                "extraData": extraData,
            }
            return 200, data
        return 400, {"error": "Invalid Request", "extra": response}

    @staticmethod
    def refund():
        pass


class EdfaPay(PaymentGateway):
    @staticmethod
    def charge(
        payload, **kwargs
    ):  # corresponds to the initiate operation in the documentatin, **kwargs
        try:
            hash = Hash.hash_initiate_edfa(
                order_number="ORD001",
                order_amount=payload["amount"],
                order_currency=payload["currency"],
                order_description=payload["description"],
                merchant_pass=payload["pass"],
            )
        except Exception as e:
            return 400, {
                "error": "Validation error, one of [odrer_id order_amount order_currency order_description] is invalid"
            }
        payload_data = {
            "action": "SALE",  # Currently it's always SALE
            "edfa_merchant_id": payload["merchant_id"],
            "order_id": "ORD001",  # to be audited, maybe we need an order table to register transactions before validation
            "order_amount": payload["amount"],
            "order_currency": payload["currency"],
            "order_description": payload["description"],
            "req_token": payload["req_token"],  # OPTIONAL: in case of card payment
            "payer_first_name": payload["firstName"],
            "payer_last_name": payload["lastName"],
            "payer_address": payload["address"],  # Maybe not Required
            "payer_country": payload["country"],
            "payer_city": payload["city"],
            "payer_zip": payload["zip"],
            "payer_email": payload["email"],
            "payer_phone": payload["phone"],
            "payer_ip": payload["ip"],
            "term_url_3ds": payload["redirectUrl"],  # redirect url
            "auth": "N",  # Indicates that transaction must be only authenticated, but not captured
            "recurring_init": "N",  # OPTIONAL: Initialization of the transaction with possible following recurring
            "hash": hash,
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", data=payload_data
        )
        status_code = response.status_code
        response = response.json()
        print(response)
        if status_code == 200:
            data = {"url": response["redirect_url"]}
            return 200, data
        return 400, {"error": "Invalid Request", "extra": response}

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
    def retrieve_payment(
        payload, **kwargs
    ):  # Can't test untill webhook is setup so I can get gway_Payment_Id from callback
        hash = Hash.hash_status_edfa(
            amount=payload["amount"],
            payment_id=payload["payment_id"],
            merchnat_pass=payload["merchant_pass"],
        )
        payload_data = {
            "merchant_id": payload[
                "merchant_id"
            ],  # String , Public transaction id of Payment Gateway
            "gway_Payment_Id": payload["gway_Payment_Id"],
            "order_id": payload["order_id"],
            "hash": hash,  # Special signature to validate your request to payment platform
        }
        response = requests.post(
            "https://api.edfapay.com/payment/initiate", data=payload_data
        )
        status_code = response.status_code
        response = response.json()
        if status_code == 200:
            date = response["responseBody"]["date"]
            timestamp = dateToMilliseconds(date)
            clientName = response["customer"]["name"]
            clientEmail = response["customer"]["email"]
            data = {
                "amount": response["order"]["amount"],
                "currency": response["order"]["currency"],
                "status": response["responseBody"]["status"],
                "timestamp": timestamp,
                "extraData": {
                    "clientName": clientName,
                    "clientEmail": clientEmail,
                    "payment_id": response["payment_id"],
                    "order_number": response["order"]["number"],
                },
            }
            return 200, data
        return 400, {"error": "Invalid Request", "extra": response}

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
