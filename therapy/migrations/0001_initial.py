# Generated by Django 5.0.1 on 2024-02-26 04:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('therapists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TherapyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readable_name', models.CharField(max_length=100, unique=True)),
                ('code_name', models.IntegerField(default=0, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TherapyTypeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapists.therapist')),
                ('therapy_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='therapy.therapytype')),
            ],
        ),
    ]