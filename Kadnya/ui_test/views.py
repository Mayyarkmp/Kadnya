from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .forms import ChargeForm, RetrieveChargeForm


def payment_options(request):
    return render(request, "ui_test/payment_options.html")


def charge_operation(request):
    if request.method == "POST":
        print("------------------------Here------------------------")
        serviceProvider = request.POST.get("serviceProvider")

        if serviceProvider == "Tap":
            payload = {
                field: request.POST.get(field)
                for field in [
                    "serviceProvider",
                    "user_id",
                    "amount",
                    "currency",
                    "customer_initiated",
                    "threeDSecure",
                    "saveCard",
                    "description",
                    "phoneCountryCode",
                    "phoneNumber",
                    "email_notification",
                    "sms_notification",
                    "firstName",
                    "middleName",
                    "lastName",
                    "emailAddress",
                    "country_code",
                    "number",
                    "merchant_id",
                    "source_id",
                    "postUrl",
                    "redirectUrl",
                ]
            }

            # Make a POST request to the backend endpoint
            response = requests.post(
                "http://localhost:8000/payment_gateways/charge", json=payload
            )

            if response.status_code == 200:
                return render(
                    request, "ui_test/success.html", {"message": "Charge successful!"}
                )
            else:
                return render(
                    request, "ui_test/failure.html", {"message": "Charge failed!"}
                )
        elif serviceProvider == "EdfaPay":
            # Process EdfaPay data
            payload = {
                "serviceProvider": "EdfaPay",
                "amount": request.POST.get("amount"),
                "order_id": request.POST.get("order_id"),
                "currency": request.POST.get("currency"),
                "description": request.POST.get("description"),
                "customer_id": request.POST.get("customer_id"),
                "merchant_id": request.POST.get("merchant_id"),
                "firstName": request.POST.get("firstName"),
                "lastName": request.POST.get("lastName"),
                "address": request.POST.get("address"),
                "country": request.POST.get("country"),
                "city": request.POST.get("city"),
                "zip": request.POST.get("zip"),
                "email": request.POST.get("email"),
                "phone": request.POST.get("phone"),
                "ip": request.POST.get("ip"),
                "redirectUrl": request.POST.get("redirectUrl"),
                "pass": request.POST.get("pass"),
                "req_token": request.POST.get("req_token"),
            }
            response = requests.post(
                "http://localhost:8000/payment_gateways/charge", json=payload
            )
            if response.status_code == 200:
                return render(
                    request, "ui_test/success.html", {"message": "Charge successful!"}
                )
            else:
                return render(
                    request, "ui_test/failure.html", {"message": "Charge failed!"}
                )

    return render(request, "ui_test/charge_form.html")


def retrieve_charge_operation(request):
    if request.method == "POST":
        # Extract form data
        form = RetrieveChargeForm(request.POST)
        if form.is_valid():
            charge_id = form.cleaned_data.get("charge_id")
            # Prepare payload
            payload = {
                "charge_id": charge_id,
                "serviceProvider": "Tap",
            }

            # Send POST request
            response = requests.post(
                "http://localhost:8000/payment_gateways/retrieve_payment", json=payload
            )

            # Handle response
            if response.status_code == 200:
                return render(
                    request, "ui_test/success.html", {"message": "Retrieve successful!"}
                )
            elif response.status_code == 400:
                return render(
                    request, "ui_test/failure.html", {"message": "Retrieve failed!"}
                )

    else:
        form = RetrieveChargeForm()

    return render(request, "ui_test/retrieve_payment_form.html", {"form": form})


def initiate_merchant(request):
    if request.method == "POST":
        payment_gateway = request.POST.get("payment_gateway")
        if payment_gateway == "EdfaPay":
            return render(
                request,
                "ui_test/initiate_merchant.html",
                {"message": "There's no details about this operation from Edfa yet."},
            )
        elif payment_gateway == "Tap":
            # Handle the Tap payment gateway form submission here
            form_data = request.POST
            return render(
                request,
                "ui_test/success.html",
                {
                    "message": "Tap merchant details submitted successfully!",
                    "data": form_data,
                },
            )
    return render(request, "ui_test/initiate_merchant.html")


def card_demo(request):
    context = {
        "public_key": "pk_test_...",  # Replace with your actual public key
        "merchant_id": "merchant_id",  # Replace with your merchant ID
        "customer_id": "customer_id",  # Replace with your customer ID
        "customer_email": "test@gmail.com",
        "customer_phone_country_code": "20",
        "customer_phone_number": "1000000000",
    }
    return render(request, "ui_test/card_sdk.html", context)
