import requests
from ninja import NinjaAPI, Schema, UploadedFile, Form, File
from .models import Lead, License, Wallet, Charge, Transaction
from .models import File as File2
from PaymentGateways.corridor import corridor

tapApi = NinjaAPI(urls_namespace="tap")

ACCESS_TOKEN = "<ACCESS_TOKEN_HERE>"


# User info should be absolutely accurate in case of Saudia Arabia
# licenseImages is the license image(s) (type is fileID)
# bankImages is file type too
# same goes for idImages
class CreateLeadSchema(Schema):
    serviceProvider: str = "Tap"
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
    response = corridor(payload, task="create_lead")
    jsonResponse = response.json()
    status_code = response.status_code
    if "errors" in jsonResponse.keys():
        status_code = 400

    if status_code == 200:
        Lead.objects.create(
            lead_id=jsonResponse["id"],
            en_name=payload.nameEn,
            ar_name=payload.nameAr,
            country=payload.country,
            is_licensed=payload.is_licensed,
        )
        License.objects.create(
            number=payload.licenseNumber,
            country=payload.licenseConutry,
            type=payload.licenseType,
        )
        Wallet.objects.create(
            bankName=payload.bankName,
            accountName=payload.accountName,
            accountNumber=payload.accountNumber,
            accountSwift=payload.accountSwift,
            accountIban=payload.accountIban,
        )
        return (200, {"id": jsonResponse["id"]})
    elif status_code == 400:
        return (400, jsonResponse)
    elif status_code == 500:
        return (500, jsonResponse)
    else:
        return (status_code, "Unknown error occured")


class CreateFileSchema(Schema):
    serviceProvider: str = "Tap"
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
    response = corridor(payload, task="create_file", file=file)
    jsonResponse = response.json()
    print(response)
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


# Remember to set up the webhook
class ChargeSchema(Schema):
    serviceProvider: str  # eg: Tap EdfaPay Paypal etc..
    user_id: str
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
    middleName: str = "-"
    lastName: str = ""
    emailAddress: str
    # Under customer -> phone
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
    url: str  # the url to go to to continue the payment process (I think)
    timestamp: int


class ChargeErrorSchema(Schema):
    errors: list


class Charge500Schema(Schema):
    status_code: int
    response: dict


# Need update charge in the case where OTP is required such as STCpay
@tapApi.post(
    "/charge",
    response={200: ChargeResponseSchema, 400: ChargeErrorSchema, 500: Charge500Schema},
)
def charge(request, payload: ChargeSchema):
    status_code, response = corridor(payload, task="charge")
    if status_code == 200:
        Transaction.objects.create(
            amount=payload.amount,
            currency=payload.currency,
            serviceProvider=payload.serviceProvider,
            user_id=payload.user_id,
            merchant_id=payload.merchant_id,
        )
        Charge.objects.create(
            charge_id=response["id"],
            amount=response["amount"],
            currency=response["currency"],
            status=response["status"],
            url=response["transaction"]["url"],
            timestamp=response["activities"][0]["created"],
        )
        return 200, {
            "id": response["id"],
            "amount": response["amount"],
            "currency": response["currency"],
            "status": response["status"],
            "url": response["transaction"]["url"],
            "timestamp": response["activities"][0]["created"],
        }
    elif status_code == 400:
        return 400, response
    else:
        print(response)
        return 500, response


class UpdateChargeSchema(Schema):
    name: str = "STC_PAY"
    response: dict  # resposne: {reference: {otp: 123123123}}


# Used to send OTP
@tapApi.put("/update_charge/{charge_id}")
def update_charge(request, charge_id: str, payload: UpdateChargeSchema):
    response = corridor(payload, task="update_charge", charge_id=charge_id)
    status_code = response.status_code
    if status_code == 200:
        return 200, "success: true"
    else:  # To be checked when we can actually test this
        return 400, "success: false"


class RetrieveChargeErrorSchema(Schema):
    errors: list


class RetrieveChargeSchema(Schema):
    amount: int
    currency: str
    status: str
    url: str
    timestamp: int


class payloadRetrieve:
    charge_id = None
    serviceProvider = None


@tapApi.get(
    "/retrive_charge/{charge_id}",
    response={200: RetrieveChargeSchema, 404: RetrieveChargeErrorSchema},
)
def retrieve_charge(request, charge_id):
    # special case because the retrieve function needs only charge id, so we need to match the syntax expected in the corridor by sending an object
    payload = payloadRetrieve()
    payload.charge_id = charge_id
    payload.serviceProvider = "Tap"
    response = corridor(payload, task="retrieve_charge", charge_id=charge_id)
    jsonResponse = response.json()
    if response.status_code == 200:
        # Creating a new object in the data base is optional here, mayebe needs further investigation
        Charge.objects.create(
            charge_id=jsonResponse["id"],
            amount=jsonResponse["amount"],
            currency=jsonResponse["currency"],
            status=jsonResponse["status"],
            url=jsonResponse["transaction"]["url"],
            timestamp=jsonResponse["activities"][0]["created"],
        )
        return (
            200,
            {
                "amount": jsonResponse["amount"],
                "currency": jsonResponse["currency"],
                "status": jsonResponse["status"],
                "url": jsonResponse["transaction"]["url"],
                "timestamp": jsonResponse["activities"][0]["created"],
            },
        )  # Might need to return specific values from the response body - to be discussed later
    else:
        return 404, jsonResponse


# Todo - Add refund