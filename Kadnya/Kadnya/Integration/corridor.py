from Base.service_providers import Tap


# the file parameter is dedicated to the case the rqeuest has a file, it's not always used in all requests
def corridor(payload, task, file=None):
    sp = payload.service_provider
    match sp:
        case "Tap":
            return getattr(Tap, task)(payload)  # equivalent to Tap.{task}
        case "EdfaPay":
            pass
