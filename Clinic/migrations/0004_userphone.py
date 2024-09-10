# Generated by Django 3.2.25 on 2024-09-05 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Clinic', '0003_auto_20240827_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPhone',
            fields=[
                ('phone_number', models.TextField(max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
            ],
        ),
    ]
