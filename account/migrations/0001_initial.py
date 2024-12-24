# Generated by Django 5.1.4 on 2024-12-09 16:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMoreInfoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(upload_to='profile_photos/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='usermoreinfo', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'İstifadəçi məlumatları',
                'verbose_name_plural': 'İstifadəçilərin məlumatları',
            },
        ),
    ]