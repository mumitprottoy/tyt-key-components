# Generated by Django 4.2.10 on 2024-03-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0003_promo_therapy_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ]
