# Generated by Django 5.1.4 on 2024-12-28 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registrationapp', '0005_filterchangermodel_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='changefiltermodel',
            name='payment_amount',
            field=models.FloatField(default=0, verbose_name='Ödəniş miqdarı'),
        ),
    ]
