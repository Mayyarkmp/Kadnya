import random
from datetime import datetime, timedelta
from typing import List, Dict
from ninja import NinjaAPI, Schema

whatsAppApi = NinjaAPI(urls_namespace="whatsapp")

MOCK_TOKENS = {"valid_token": {"expires_at": datetime.now() + timedelta(hours=1)}}


class CreateTemplateSchema(Schema):
    name: str
    allow_category_change: bool
    category: str  # enum {UTILITY, MARKETING, AUTHENTICATION}
    language: str
    components: List[Dict]


class CreateTemplateResponseSchema(Schema):
    id: str
    status: str
    category: str


class WhatsAppMessagePayload(Schema):
    messaging_product: str
    recipient_type: str
    to: str  # Recipient's phone number in international format
    type: str
    template: Dict


def validate_access_token(token: str):
    """Simulates access token validation."""
    token_data = MOCK_TOKENS.get(token)
    if not token_data or datetime.now() > token_data["expires_at"]:
        return False
    return True


# Mock endpoint for creating a template
@whatsAppApi.post(
    "/create_template",
    response={200: CreateTemplateResponseSchema, 401: Dict[str, str]},
)
def create_template(request, payload: CreateTemplateSchema, Authorization: str = None):
    if not Authorization or not validate_access_token(Authorization.split()[-1]):
        return 401, {"error": "Invalid OAuth 2.0 Access Token"}

    template_id = f"tmpl_{random.randint(1000, 9999)}"
    return {
        "id": template_id,
        "status": "PENDING",
        "category": payload.category,
    }


@whatsAppApi.get("/retrieve_templates")
def retrieve_templates(request, category: str, Authorization: str = None):
    if not Authorization or not validate_access_token(Authorization.split()[-1]):
        return 401, {"error": "Invalid OAuth 2.0 Access Token"}

    mock_templates = [
        {
            "id": f"tmpl_{random.randint(1000, 9999)}",
            "name": "Sample Template",
            "category": category,
        },
    ]
    return {"data": mock_templates}


@whatsAppApi.post("/send_message")
def send_custom_whatsapp_message(
    request, payload: WhatsAppMessagePayload, Authorization: str = None
):
    if not Authorization or not validate_access_token(Authorization.split()[-1]):
        return 401, {"error": "Invalid OAuth 2.0 Access Token"}

    if not payload.template.get("name"):
        return 400, {"error": "Invalid template structure"}

    return {
        "messages": [
            {
                "id": f"msg_{random.randint(1000, 9999)}",
                "status": "SENT",
                "to": payload.to,
                "template": payload.template,
            }
        ]
    }


@whatsAppApi.post("/token")
def generate_token(request, client_id: str, client_secret: str):
    if client_id != "mock_client_id" or client_secret != "mock_client_secret":
        return 401, {"error": "Invalid client credentials"}

    token = f"mock_token_{random.randint(1000, 9999)}"
    MOCK_TOKENS[token] = {"expires_at": datetime.now() + timedelta(hours=1)}
    return {
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 3600,
    }
