from django.contrib import admin
from Clinic.models import CathegoryOfDoctor, Doctor, Appointment, UserPhone

admin.site.register(CathegoryOfDoctor)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(UserPhone)
