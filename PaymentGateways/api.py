import requests
from ninja import NinjaAPI, Schema, UploadedFile, Form, File
from .models import Lead, License, Wallet, Transaction
from .models import File as File2
from PaymentGateways.corridor import corridor
import json

paymentGatewayApi = NinjaAPI(urls_namespace="tap")

ACCESS_TOKEN = "<ACCESS_TOKEN_HERE>"


# User info should be absolutely accurate in case of Saudia Arabia
# licenseImages is the license image(s) (type is fileID)
# bankImages is file type too
# same goes for idImages
class CreateLeadSchema(Schema):
    serviceProvider: str = "Tap"
    brandNameEn: str
    brandNameAr: str
    brandLogo_id: str
    entityCountry: str
    entity_is_licensed: bool
    entityLicenseNumber: str
    entityLicenseCountry: str
    entityLicenseType: str
    entityLicenseDocumentType: str
    entityLicenseDocumentNumber: str
    entityLicenseDocumentIssuingCountry: str
    entityLicenseDocumentIssuingDate: str
    entityLicenseDocumentExpiryDate: str
    entityLicenseDocumentImages: list[str]
    walletBankName: str
    walletAccountName: str
    walletAccountNumber: str
    walletAccountSwift: str
    walletAccountIban: str
    WalletBankDocumentType: str
    WalletBankDocumentNumber: str
    WalletBankDocumentIssuingCountry: str
    WalletBankDocumentIssuingDate: str
    WalletBankDocumentImages: list[str]
    userFirstName: str
    userMiddleName: str
    userLastName: str
    userLang: str
    userTitle: str = "Mr"
    userEmailType: str
    userEmailAddress: str
    userEmailPrimary: bool
    userPhoneType: str = "WORK"
    userPhoneCountryCode: str
    userPhoneNumber: str
    userNationality: str
    userIdentificationNumber: str
    userIdentificationType: str
    userIdentificationIssuer: str
    userIdentificationImages: list[str]
    userBirthCountry: str
    userBirthCity: str
    userBirthDate: str
    postUrl: str


class LeadErrorSchema(Schema):
    errors: list


class LeadResponseSchema(Schema):
    id: str


@paymentGatewayApi.post(
    "/create_lead", response={200: LeadResponseSchema, 400: LeadErrorSchema}
)
def create_lead(request, payload: CreateLeadSchema):
    payload = payload.dict()
    status_code, response = corridor(payload, task="create_lead")

    if "errors" in response.keys():
        status_code = 400

    if status_code == 200:
        lead = Lead.objects.get(brandNameEn=payload["brandNameEn"])
        lead.lead_id = response["id"]
        # License.objects.create(
        #     number=payload.licenseNumber,
        #     country=payload.licenseConutry,
        #     type=payload.licenseType,
        # )
        # Wallet.objects.create(
        #     bankName=payload.bankName,
        #     accountName=payload.accountName,
        #     accountNumber=payload.accountNumber,
        #     accountSwift=payload.accountSwift,
        #     accountIban=payload.accountIban,
        # )
        return (200, {"id": response["id"]})
    elif status_code == 400:
        return (400, response)


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


@paymentGatewayApi.post(
    "/create_file", response={200: FileResponseSchema, 404: FileErrorSchema}
)
def create_file(request, payload: Form[CreateFileSchema], file: File[UploadedFile]):
    response = corridor(payload, task="create_file", file=file)
    jsonResponse = response.json()
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
    # user_id: str
    # amount: int
    # currency: str
    # metadata: dict = {"udf1": "Metadata 1"}
    # description: str
    # # Under reference object
    # transaction: str = "txn_123"
    # order: str = "ord_123"
    # # Under receipt object, used to send the receipt through email/sms to the user
    # email: bool = True
    # sms: bool = True
    # # Under customer object
    # firstName: str = ""
    # middleName: str = "-"
    # lastName: str = ""
    # emailAddress: str
    # # Under customer -> phone
    # phoneCountryCode: int
    # phoneNumber: int
    # merchant_id: str
    # # Under source, specifies the paymeny method
    # ID: str = "src_all"
    # saveCard: bool
    # postUrl: str = "http://kadynia.com/post_url"  # Webhook
    # redirectUrl: str = "http://kadynia.com/redirect_url"


class ChargeResponseSchema(Schema):
    # id: str
    # amount: float
    # currency: str
    # status: str
    # timestamp: int
    url: str  # the url to go to to continue the payment process (I think)
    extraData: dict = {}


class ChargeErrorSchema(Schema):
    error: str
    extra: dict


class Charge500Schema(Schema):
    status_code: int
    response: dict


# Need update charge in the case where OTP is required such as STCpay
@paymentGatewayApi.post(
    "/charge",
    response={200: ChargeResponseSchema, 400: ChargeErrorSchema, 500: Charge500Schema},
)
def charge(request):
    payload = json.loads(request.body)
    status_code, response = corridor(payload, task="charge")
    try:
        Transaction.objects.create(
            amount=payload["amount"],
            currency=payload["currency"],
            serviceProvider="Tap",
            user_id=payload["user_id"],
            merchant_id=payload["merchant_id"],
            status="Initiated",
        )
        print("Successfully created")
    except Exception as e:
        print("Transaction was not added to database", e)
    if status_code == 200:
        # Transaction.objects.create(
        #     amount=payload["amount"],
        #     currency=payload["currency"],
        #     serviceProvider=payload["serviceProvider"],
        #     user_id=payload["user_id"],
        #     merchant_id=payload["merchant_id"],
        # )
        return 200, response
    elif status_code == 400:
        return 400, response
    else:
        print(response)
        return 500, response


class UpdateChargeSchema(Schema):
    name: str = "STC_PAY"
    response: dict  # resposne: {reference: {otp: 123123123}}


# Used to send OTP
@paymentGatewayApi.put("/update_charge/{charge_id}")
def update_charge(request, charge_id: str, payload: UpdateChargeSchema):
    response = corridor(payload, task="update_charge", charge_id=charge_id)
    status_code = response.status_code
    if status_code == 200:
        return 200, "success: true"
    else:  # To be checked when we can actually test this
        return 400, "success: false"


class RetrieveChargeErrorSchema(Schema):
    error: str
    extra: dict = {}


class RetrievePaymentSchema(Schema):
    amount: int
    currency: str
    status: str
    timestamp: int
    extraData: dict = {}


@paymentGatewayApi.post(
    "/retrieve_payment",
    response={200: RetrievePaymentSchema, 400: RetrieveChargeErrorSchema},
)
def retrieve_payment(request):
    # special case because the retrieve function needs only charge id, so we need to match the syntax expected in the corridor by sending an object
    payload = json.loads(request.body)
    status_code, response = corridor(payload, task="retrieve_payment")
    if status_code == 200:
        # Creating a new object in the data base is optional here, mayebe needs further investigation
        # Charge.objects.create(
        #     charge_id=jsonResponse["id"],
        #     amount=jsonResponse["amount"],
        #     currency=jsonResponse["currency"],
        #     status=jsonResponse["status"],
        #     url=jsonResponse["transaction"]["url"],
        #     timestamp=jsonResponse["activities"][0]["created"],
        # )
        return (
            200,
            response,
        )  # Might need to return specific values from the response body - to be discussed later
    else:
        return 400, response


# Todo - Add refund
