# Generated by Django 5.1.4 on 2024-12-15 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dailypaymentmodel',
            old_name='intstallment',
            new_name='installment',
        ),
    ]