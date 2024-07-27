# Generated by Django 4.2.10 on 2024-04-20 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('therapy', '0002_dass21questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='DASS21Statements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('label', models.CharField(choices=[('Depression', 'Depression'), ('Anxiety', 'Anxiety'), ('Stress', 'Stress')], max_length=20)),
            ],
            options={
                'verbose_name': 'DASS-21 Test Statement',
                'verbose_name_plural': 'DASS-21 Test Statements',
            },
        ),
        migrations.DeleteModel(
            name='DASS21Questions',
        ),
    ]
