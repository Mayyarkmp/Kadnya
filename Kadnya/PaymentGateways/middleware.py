import json
from django.utils.deprecation import MiddlewareMixin
from .models import RequestLog


class LogRequestResponseMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Attach request body and headers to the request object
        request.log_data = {
            "method": request.method,
            "path": request.path,
            "request_headers": dict(request.headers),
            "request_body": self.get_request_body(request),
        }

    def process_response(self, request, response):
        # Retrieve data from the request
        print("----------------------------Here----------------------------")
        log_data = getattr(request, "log_data", {})
        # print("/////////////wtf\\\\\\\\\\\\\\\\\\")
        # Capture response data
        log_data["response_status"] = response.status_code
        log_data["response_headers"] = dict(response.items())
        log_data["response_body"] = self.get_response_body(response)

        # Save log data to database
        print(log_data)
        RequestLog.objects.create(**log_data)

        return response

    def get_request_body(self, request):
        # Parse JSON body if it exists
        try:
            return json.loads(request.body.decode("utf-8")) if request.body else None
        except json.JSONDecodeError:
            return None

    def get_response_body(self, response):
        # Attempt to parse response JSON if it exists
        try:
            return json.loads(response.content.decode("utf-8"))
        except json.JSONDecodeError:
            return response.content.decode("utf-8") if response.content else None
