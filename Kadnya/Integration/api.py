import requests
from ninja import NinjaAPI, Schema, UploadedFile, Form, File
from django.core.files.storage import default_storage
import os
from Kadnya.settings import testKey, paymenyTechKey
from .models import Lead, License, Wallet, Charge
from .models import File as File2


tapApi = NinjaAPI(urls_namespace="tap")


# User info should be absolutely accurate in case of Saudia Arabia
# licenseImages is the license image(s) (type is fileID)
# bankImages is file type too
# same goes for idImages
class CreateLeadSchema(Schema):
    nameEn: str
    nameAr: str
    logo_id: str
    country: str
    is_licensed: bool
    licenseNumber: str
    licenseDocumentNumber: str
    licenseConutry: str
    licenseIssuingCountry: str
    issuingDate: str
    expiryDate: str
    licenseImages: list[str]
    bankName: str
    accountName: str
    accountSwift: str
    accountIban: str
    accountNumber: str
    documentNumber: str
    documentIssuingCountry: str
    documentIssuingDate: str
    documentImages: list[str]
    userLang: str
    userFirstName: str
    userLastname: str
    userEmailType: str
    userEmailAddress: str
    phoneCountryCode: str
    phoneNumber: str
    nationality: str
    idNumber: str
    idType: str
    Isuuer: str
    idImages: list[str]
    birthCountry: str
    birthCity: str
    birthDate: str
    metadata: dict
    postUrl: str = "https://kadnya.com/pay"
    licenseDocumentType: str = "commercial_registration"
    licenseType: str = "commercial_registration"
    documentType: str = "Bank Statement"
    userMiddleName: str = "-"
    userTitle: str = "Mr"
    phoneNumberType: str = "WORK"


class LeadErrorSchema(Schema):
    errors: list


class LeadResponseSchema(Schema):
    id: str


@tapApi.post("/create_lead", response={200: LeadResponseSchema, 400: LeadErrorSchema})
def create_lead(request, payload: CreateLeadSchema):
    data = payload.dict()
    brand = {
        "name": {"en": data["nameEn"], "ar": data["nameAr"]},
        "sector": ["Education"],
        "logo": data["logo_id"],
        "channelServices": [{"channel": "website", "address": "https://kadnya.com/"}],
        "segment": {"type": {"code": "non_profit"}, "team": {"code": "small"}},
        "terms": [
            {"term": "general", "agree": True},
            {"term": "chargeback", "agree": True},
            {"term": "refund", "agree": True},
        ],
    }
    entity = {
        "country": data["country"],
        "is_licensed": data["is_licensed"],
        "license": {
            "number": data["licenseNumber"],
            "country": data["licenseConutry"],
            "type": data["licenseType"],
            "documents": [
                {
                    "type": data["licenseDocumentType"],
                    "number": data["licenseDocumentNumber"],
                    "issuing_country": data["licenseIssuingCountry"],
                    "issuing_date": data["issuingDate"],
                    "expiry_date": data["expiryDate"],
                    "images": data["licenseImages"],
                }
            ],
        },
    }
    wallet = {
        "bank": {
            "name": data["bankName"],
            "account": {
                "name": data["accountName"],
                "number": data["accountNumber"],
                "swift": data["accountSwift"],
                "iban": data["accountIban"],
            },
            "documents": [
                {
                    "type": data["documentType"],
                    "number": data["documentNumber"],
                    "issuing_country": data["documentIssuingCountry"],
                    "issuing_date": data["documentIssuingDate"],
                    "images": data["documentImages"],
                }
            ],
        }
    }
    user = {
        "name": {
            "lang": data["userLang"],
            "title": data["userTitle"],
            "first": data["userFirstName"],
            "middle": data["userMiddleName"],
            "last": data["userLastname"],
        },
        "email": [
            {
                "type": data["userEmailType"],
                "address": data["userEmailAddress"],
                "primary": True,
            }
        ],
        "phone": [
            {
                "type": data["phoneNumberType"],
                "country_code": data["phoneCountryCode"],
                "number": data["phoneNumber"],
            }
        ],
        "nationality": data["nationality"],
        "identification": {
            "number": data["idNumber"],
            "type": data["idType"],
            "issuer": data["Isuuer"],
            "images": data["idImages"],
        },
        "birth": {
            "country": data["birthCountry"],
            "city": data["birthCity"],
            "birth_date": data["birthDate"],
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
        "metadata": data["metadata"],
        "payment_provider": {"id": paymenyTechKey},
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": testKey,
    }
    response = requests.post(
        "https://api.tap.company/v3/connect/lead/", json=payload_data, headers=headers
    )
    jsonResponse = response.json()
    status_code = response.status_code
    print(response)
    if "errors" in jsonResponse.keys():
        status_code = 400

    if status_code == 200:
        Lead.objects.create(
            lead_id=jsonResponse["id"],
            en_name=data["nameEn"],
            ar_name=data["nameAr"],
            country=data["country"],
            is_licensed=data["is_licensed"],
        )
        License.objects.create(
            number=data["licenseNumber"],
            country=data["licenseConutry"],
            type=data["licenseType"],
        )
        Wallet.objects.create(
            bankName=data["bankName"],
            accountName=data["accountName"],
            accountNumber=data["accountNumber"],
            accountSwift=data["accountSwift"],
            accountIban=data["accountIban"],
        )
        return (200, {"id": jsonResponse["id"]})
    elif status_code == 400:
        return (400, jsonResponse)
    elif status_code == 500:
        return (500, jsonResponse)
    else:
        return (status_code, "Unknown error occured")


class CreateFileSchema(Schema):
    purpose: str
    title: str
    expires_at: str = "1913743462"
    file_link_create: bool


class FileResponseSchema(Schema):
    id: str


class FileErrorSchema(Schema):
    errors: list
    timestamp: int


# https://api.tap.company/v2/files/


@tapApi.post("/create_file", response={200: FileResponseSchema, 404: FileErrorSchema})
def create_file(request, payload: Form[CreateFileSchema], file: File[UploadedFile]):
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

    jsonResponse = response.json()
    if default_storage.exists(temp_file_name):
        default_storage.delete(temp_file_name)
    status_code = response.status_code
    if status_code == 200:
        File2.objects.create(file_id=jsonResponse["id"])
        return 200, {"id": jsonResponse["id"]}
    elif status_code == 404:
        return 404, jsonResponse
    elif status_code == 500:
        return 500, jsonResponse
    else:
        return status_code, "Unknown error occured"


class ChargeSchema(Schema):
    amount: int
    currency: str
    metadata: dict = {"udf1": "Metadata 1"}
    description: str
    # Under reference object
    transaction: str = "txn_123"
    order: str = "ord_123"
    # Under receipt object, used to send the receipt through email/sms to the user
    email: bool = True
    sms: bool = True
    # Under customer object
    firstName: str = ""
    middleName: str = ""
    lastName: str = ""
    emailAddress: str
    # Under customer -> phonen
    phoneCountryCode: int
    phoneNumber: int
    merchant_id: str
    # Under source, specifies the paymeny method
    ID: str = "src_all"
    saveCard: bool
    postUrl: str = "http://kadynia.com/post_url"  # Webhook
    redirectUrl: str = "http://kadynia.com/redirect_url"


class ChargeResponseSchema(Schema):
    id: str
    amount: float
    currency: str
    status: str
    url: str


class ChargeErrorSchema(Schema):
    errors: list


@tapApi.post(
    "/charge",
    response={200: ChargeResponseSchema, 400: ChargeErrorSchema},
)
def charge(request, payload: ChargeSchema):
    # print(os.getenv('SECRET_KEY'))
    os.environ["SECRET_KEY"]
    # data = payload.dict()
    metapayload = {"udf1": "Metapayload 1"}
    reference = {"transaction": payload.transaction, "order": payload.order}
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
    jsonResponse = response.json()
    print(response)
    print(jsonResponse)
    status_code = response.status_code
    if status_code == 200:
        Charge.objects.create(
            charge_id=jsonResponse["id"],
            amount=jsonResponse["amount"],
            currency=jsonResponse["currency"],
            status=jsonResponse["status"],
            url=jsonResponse["transaction"]["url"],
        )
        return 200, {
            "id": jsonResponse["id"],
            "amount": jsonResponse["amount"],
            "currency": jsonResponse["currency"],
            "status": jsonResponse["status"],
            "url": jsonResponse["transaction"]["url"],
        }
    elif status_code == 400:
        return 400, jsonResponse
    else:
        return 500, jsonResponse
