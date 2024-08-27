from django.contrib import admin
from Clinic.models import Client, CathegoryOfDoctor, Doctor, Appointment

admin.site.register(Client)
admin.site.register(CathegoryOfDoctor)
admin.site.register(Doctor)
admin.site.register(Appointment)
