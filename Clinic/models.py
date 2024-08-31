from django.db import models
from django.contrib.auth.models import User


class CathegoryOfDoctor(models.Model):
    name = models.CharField(max_length=32, blank=False)
    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=32, blank=False)
    mobile_number = models.CharField(max_length=16, blank=False)
    email = models.EmailField(blank=False)
    cathegory_id = models.ForeignKey(CathegoryOfDoctor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.TimeField(blank=False)
    date = models.DateField(max_length=16, blank=False)
    doctor_id = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=16, blank=False)

    def __str__(self):
        return f"time - {self.time} date - {self.date}"
