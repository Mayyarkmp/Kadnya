from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
from .forms import ChargeForm, RetrieveChargeForm


def payment_options(request):
    return render(request, "ui_test/payment_options.html")


def charge_operation(request):
    if request.method == "POST":
        serviceProvider = request.POST.get("serviceProvider")
        print(
            f"Amount: {request.POST.get('amount')}, Currency: {request.POST.get('currency')}"
        )
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
            print("Payload ------ ", payload)
            response = requests.post(
                "http://localhost:8000/payment_gateways/charge", json=payload
            )
            print(response.json())
            if response.status_code == 200:
                return render(
                    request, "ui_test/success.html", {"message": "Charge successful!"}
                )
            else:
                return render(
                    request, "ui_test/failure.html", {"message": "Charge failed!"}
                )
        elif serviceProvider == "EdfaPay":
            payload = {
                "serviceProvider": "EdfaPay",
                "amount": request.POST.get("edfa_amount"),
                "order_id": request.POST.get("edfa_order_id"),
                "currency": request.POST.get("edfa_currency"),
                "description": request.POST.get("edfa_description"),
                "customer_id": request.POST.get("edfa_customer_id"),
                "merchant_id": request.POST.get("edfa_merchant_id"),
                "firstName": request.POST.get("edfa_firstName"),
                "lastName": request.POST.get("edfa_lastName"),
                "address": request.POST.get("edfa_address"),
                "country": request.POST.get("edfa_country"),
                "city": request.POST.get("edfa_city"),
                "zip": request.POST.get("edfa_zip"),
                "email": request.POST.get("edfa_email"),
                "phone": request.POST.get("edfa_phone"),
                "ip": request.POST.get("edfa_ip"),
                "redirectUrl": request.POST.get("edfa_redirectUrl"),
                "pass": request.POST.get("edfa_pass"),
                "req_token": request.POST.get("edfa_req_token"),
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
        form = RetrieveChargeForm(request.POST)
        if form.is_valid():
            charge_id = form.cleaned_data.get("charge_id")
            payload = {
                "charge_id": charge_id,
                "serviceProvider": "Tap",
            }

            response = requests.post(
                "http://localhost:8000/payment_gateways/retrieve_payment", json=payload
            )

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
