import requests
from ninja import NinjaAPI, Schema, UploadedFile, Form, File

from Marketing.Base.Sendgrid.ClientAPI import SendGridClient
from .models import Lead, License, Wallet, Charge, Transaction
from .models import File as File2
from PaymentGateways.corridor import corridor

whatsAppApi = NinjaAPI(urls_namespace="whatsapp")

# WHATSAPP_BUSINESS_ACCOUNT_ID = "your_business_account_id"
ACCESS_TOKEN = "your_access_token"
# Signup for Meta Business Manager
# Create a Whatsapp Platform Account


# https://graph.facebook.com/v21.0/{{WHATSAPP_BUSINESS_ACCOUNT_ID}}/message_templates
class CreateTemplateSchema(Schema):
    name: str = "TemplateExample"
    allow_category_change: bool = True
    category: str = "MARKETING"  # enum {UTILITY, MARKETING, AUTHENTICATION}
    language: str = "en"
    components: list  # list of objects, see https://developers.facebook.com/docs/whatsapp/business-management-api/message-templates/components


class CreateTemplate200Schema(Schema):
    id: str
    status: str  # pending or whatever
    category: str


class CreateTemplate100Schema(Schema):
    error: str = "Invalid parameter"


class CreateTemplate192Schema(Schema):
    error: str = "Invalid Phone Number"


class CreateTemplate368Schema(Schema):
    error: str = (
        "The action attempted has been deemed abusive or is otherwise disallowed"
    )


class CreateTemplate80008Schema(Schema):
    error: str = "There have been too many calls to this WhatsApp Business account. Wait a bit and try again. For more info, please refer to https://developers.facebook.com/docs/graph-api/overview/rate-limiting."


class CreateTemplate190Schema(Schema):
    error: str = "Invalid OAuth 2.0 Access Token"


@whatsAppApi.post(
    "/create_template",
    response={
        100: CreateTemplate100Schema,
        190: CreateTemplate190Schema,
        192: CreateTemplate192Schema,
        200: CreateTemplate200Schema,
        368: CreateTemplate368Schema,
    },
)
def create_template(request, payload):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    response = requests.post(url="", headers=headers, json=payload.dict())

    # Check response
    if response.status_code == 200:
        return 200, "success: true"
    else:
        return 200, f"error: {response}"


"""
    
    
    {
  "name": "seasonal_promotion",
  "language": "en",
  "category": "MARKETING",
  "components": [
    {
      "type": "HEADER",
      "format": "TEXT",
      "text": "Our {{1}} is on!",
      "example": {
        "header_text": [
          "Summer Sale"
        ]
      }
    },
    {
      "type": "BODY",
      "text": "Shop now through {{1}} and use code {{2}} to get {{3}} off of all merchandise.",
      "example": {
        "body_text": [
          [
            "the end of August","25OFF","25%"
          ]
        ]
      }
    },
    {
      "type": "FOOTER",
      "text": "Use the buttons below to manage your marketing subscriptions"
    },
    {
      "type":"BUTTONS",
      "buttons": [
        {
          "type": "QUICK_REPLY",
          "text": "Unsubcribe from Promos"
        },
        {
          "type":"QUICK_REPLY",
          "text": "Unsubscribe from All"
        }
      ]
    }
  ]
}'
    
"""


# https://graph.facebook.com/v16.0/102290129340398/message_templates?category=utility
class RetrieveTemplateSchema(Schema):
    data: list


@whatsAppApi("/retrieve_templates")
def retrieve_templates(request, category: str = "marketing"):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    # url = f"https://graph.facebook.com/v16.0/102290129340398/message_templates"
    url = ""
    params = {"category": category}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


class WhatsAppMessagePayload(Schema):
    messaging_product: str = "whatsapp"
    recipient_type: str = "individual"
    to: str  # Recipient's phone number in international format
    type: str = "template"
    template: dict


@whatsAppApi.post("/whatsapp_send_message")
def send_custom_whatsapp_message(request, payload: WhatsAppMessagePayload):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(url="", headers=headers, json=payload.dict())
        response.raise_for_status()  # raise HTTP error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, 400


@whatsAppApi.post("/send_email")
def send_email(request):
    payload = request.body
    status_code, response = corridor(payload, task="send_email")
    if status_code == 200:
        return 200, {"response": response}
    else:
        return 400, {"error": response}


@whatsAppApi.post("/get_statistics")
def get_statistics(request):
    payload = request.body
    status_code, response = corridor(payload, task="get_statistics")
    if status_code == 200:
        return 200, {"response": response}
    else:
        return 400, {"error": response}
