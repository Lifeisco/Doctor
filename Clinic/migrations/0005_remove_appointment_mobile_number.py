# Generated by Django 3.2.25 on 2024-09-11 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Clinic', '0004_userphone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='mobile_number',
        ),
    ]
