# Generated by Django 4.2.10 on 2024-05-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_appointment_tracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='email_sent',
            field=models.BooleanField(default=False),
        ),
    ]