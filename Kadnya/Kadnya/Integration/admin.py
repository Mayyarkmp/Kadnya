from django.contrib import admin
from .models import Lead, License, Charge, File
# Register your models here.

admin.site.register(Lead)
admin.site.register(License)
admin.site.register(Charge)
admin.site.register(File)
