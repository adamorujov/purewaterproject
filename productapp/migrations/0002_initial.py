# Generated by Django 5.1.4 on 2024-12-09 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('productapp', '0001_initial'),
        ('registrationapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountmodel',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='registrationapp.clientmodel', verbose_name='Satış'),
        ),
        migrations.AddField(
            model_name='districtmodel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='productapp.citymodel', verbose_name='Şəhər'),
        ),
        migrations.AddField(
            model_name='villagemodel',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_villages', to='productapp.citymodel', verbose_name='Şəhər'),
        ),
        migrations.AddField(
            model_name='villagemodel',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='district_villages', to='productapp.districtmodel', verbose_name='Rayon'),
        ),
    ]
