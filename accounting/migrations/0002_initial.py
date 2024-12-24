# Generated by Django 5.1.4 on 2024-12-09 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0001_initial'),
        ('registrationapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailypaymentmodel',
            name='intstallment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dailypayments', to='registrationapp.installmentmodel', verbose_name='Taksit'),
        ),
    ]
