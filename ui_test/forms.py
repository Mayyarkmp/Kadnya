from django import forms


class ChargeForm(forms.Form):
    amount = forms.DecimalField(label="Amount", max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=[("USD", "USD"), ("KWD", "KWD")])
    description = forms.CharField(label="Description", max_length=255)


class RetrieveChargeForm(forms.Form):
    charge_id = forms.CharField(label="Charge ID", max_length=255)
