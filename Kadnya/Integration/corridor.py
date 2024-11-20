from Integration.Base.service_providers import EdfaPay, Tap


# the file parameter is dedicated to the case the rqeuest has a file, it's not always used in all requests
def corridor(payload, task, **kwargs):
    sp = payload.serviceProvider
    match sp:
        case "Tap":
            return getattr(Tap, task)(payload, **kwargs)  # equivalent to Tap.{task}
        case "EdfaPay":
            return getattr(EdfaPay, task)(payload, **kwargs)
