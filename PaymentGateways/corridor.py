from PaymentGateways.Base.service_providers import EdfaPay, Tap


# the file parameter is dedicated to the case the rqeuest has a file, it's not always used in all requests
def corridor(payload, task, **kwargs):
    try:
        sp = payload["serviceProvider"]
    except Exception as e:
        return 400, {"error": "No service provider selected"}
    match sp:
        case "Tap":
            return getattr(Tap, task)(payload, **kwargs)  # equivalent to Tap.{task}
        case "EdfaPay":
            return getattr(EdfaPay, task)(payload, **kwargs)
