from django.db import models
from django.contrib.auth.models import User

class UserMoreInfoModel(models.Model):
    user = models.OneToOneField(User, verbose_name="İstifadəçi", on_delete=models.CASCADE, related_name="usermoreinfo")
    profile_photo = models.ImageField("Profil şəkli", upload_to='profile_photos/')

    class Meta:
        ordering = ("-id",)
        verbose_name = "Profil şəkli"
        verbose_name_plural = "Profil şəkilləri"

    def __str__(self):
        return self.user.username