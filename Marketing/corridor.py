from Marketing.Base.Sendgrid.ClientAPI import SendGridClient
from PaymentGateways.Base.service_providers import Whatsapp


# the file parameter is dedicated to the case the rqeuest has a file, it's not always used in all requests
def corridor(payload, task, **kwargs):
    try:
        sp = payload["serviceProvider"]
    except Exception as e:
        return 400, {"error": "No service provider selected"}
    match sp:
        case "Whatsapp":
            return getattr(Whatsapp, task)(
                payload, **kwargs
            )  # equivalent to Whatsapp.{task}
        case "SendGrid":
            return getattr(SendGridClient, task)(payload, **kwargs)
