from django.db import models
from django.contrib.auth.models import User

class UserMoreInfoModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="usermoreinfo")
    profile_photo = models.ImageField(upload_to='profile_photos/')

    class Meta:
        verbose_name = "İstifadəçi məlumatları"
        verbose_name_plural = "İstifadəçilərin məlumatları"

    def __str__(self):
        return self.user.username