from django.db import models

class SettingsModel(models.Model):
    # main
    logo = models.TextField("Loqo", blank=True, null=True)
    slogan = models.TextField("Sloqan", blank=True, null=True)
    favicon = models.ImageField("İkon", upload_to="settings_images/", blank=True, null=True)
    # meta
    keywords = models.TextField("Açar sözlər", blank=True, null=True)
    description = models.TextField("Kontent", blank=True, null=True)
    # contact
    contact_number = models.CharField("Əlaqə nömrəsi", max_length=20, blank=True, null=True)
    email = models.EmailField("Email", max_length=100, blank=True, null=True)
    address = models.TextField("Ünvan", blank=True, null=True)
    # banner
    banner_title = models.TextField("Başlıq", blank=True, null=True)
    banner_text = models.TextField("Mətn", blank=True, null=True)
    banner_image = models.ImageField("Şəkil", upload_to="settings_images/", blank=True, null=True)
    # about
    about_text = models.TextField("Məzmun", blank=True, null=True)
    about_image1 = models.ImageField("Şəkil 1", upload_to="settings_images/", blank=True, null=True)
    about_image2 = models.ImageField("Şəkil 2", upload_to="settings_images/", blank=True, null=True)

    class Meta:
        verbose_name = "Parametr"
        verbose_name_plural = "Parametrlər"

    def save(self, *args, **kwargs):
        if not self.id and SettingsModel.objects.exists():
            return None
        return super(SettingsModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return "Parametrlər"

class SocialMediaModel(models.Model):
    icon_text = models.TextField("İkon")
    link = models.TextField("Link")

    class Meta:
        verbose_name = "Sosial media"
        verbose_name_plural = "Sosial medialar"
        ordering = ("-id",)

    def __str__(self):
        return self.link

class ServiceModel(models.Model):
    icon_text = models.TextField("İkon")
    title = models.TextField("Başlıq")
    content = models.TextField("Məzmun")

    class Meta:
        verbose_name = "Xidmət"
        verbose_name_plural = "Xidmətlər"
        ordering = ("-id",)

    def __str__(self):
        return self.title

class CategoryModel(models.Model):
    name = models.CharField("Ad", max_length=200)

    class Meta:
        verbose_name = "Kateqoriya"
        verbose_name_plural = "Kateqoriyalar"
        ordering = ("-id",)

    def __str__(self):
        return self.name
    
class OurProductModel(models.Model):
    title = models.TextField("Başlıq")
    image = models.ImageField("Şəkil", upload_to="product_images/")
    price = models.FloatField("Qiymət", default=0)
    category = models.ForeignKey(CategoryModel, verbose_name="Kateqoriya", on_delete=models.CASCADE, related_name="ourproducts")

    class Meta:
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"
        ordering = ("-id",)

    def __str__(self):
        return self.title


class TestimonialModel(models.Model):
    name = models.CharField("Ad, Soyad", max_length=100)
    place = models.CharField("Məkan", max_length=150, blank=True, null=True)
    text = models.TextField("Məzmun")
    star = models.IntegerField("Ulduz", default=0)

    class Meta:
        verbose_name = "Müştəri rəyi"
        verbose_name_plural = "Müştəri rəyləri"
        ordering = ("-id",)

    def __str__(self):
        return self.name