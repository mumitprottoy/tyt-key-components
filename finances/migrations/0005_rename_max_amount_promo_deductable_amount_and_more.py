# Generated by Django 4.2.10 on 2024-03-10 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('finances', '0004_promo_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='promo',
            old_name='max_amount',
            new_name='deductable_amount',
        ),
        migrations.RenameField(
            model_name='promo',
            old_name='count',
            new_name='retrieval_limit',
        ),
        migrations.RemoveField(
            model_name='promo',
            name='is_counted',
        ),
        migrations.AddField(
            model_name='promo',
            name='retrieval_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='promo',
            name='user_retrieval_limit',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='PromoRetrievalCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('maxed_out', models.BooleanField(default=False)),
                ('promo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='finances.promo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]