from django.db import models
# Create your models here.


# ------------------------------------Lead------------------------------------#
class Lead(models.Model):
    lead_id = models.CharField(max_length=70)
    en_name = models.CharField(max_length=30)
    ar_name = models.CharField(max_length=30)
    country = models.CharField(max_length=10)
    is_licensed = models.BooleanField()


TYPE_CHOICES = [
    ("commercial_registration", "commercial_registration"),
    ("freelancer", "freelancer"),
]


class License(models.Model):
    number = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    type = models.CharField(max_length=40, choices=TYPE_CHOICES)


class Wallet(models.Model):
    bankName = models.CharField(max_length=40)
    accountName = models.CharField(max_length=40)
    accountNumber = models.CharField(max_length=40)
    accountSwift = models.CharField(max_length=40)
    accountIban = models.CharField(max_length=40)


# class Document(models.Model):
# 	docType = models.CharField(max_length=30)
# 	number = models.CharField(max_length=50)
# 	issuingCountry = models.CharField(max_length=10)
# 	issuingDate = models.DateField()
# 	expiryDate = models.DateField()
# 	license = models.ForeignKey(License, on_delete=models.CASCADE, null=True, blank=True)
# 	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, null=True, blank=True)


# class Image(models.Model):
#     img = models.ImageField
#     document = models.ForeignKey(Document, on_delete=models.CASCADE)


# ------------------------------------File------------------------------------#
class File(models.Model):
    file_id = models.CharField(max_length=70)


# ------------------------------------Charge------------------------------------#
class Charge(models.Model):
    charge_id = models.CharField(max_length=70)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    url = models.CharField(max_length=100)
    timestamp = models.IntegerField(null=True)
