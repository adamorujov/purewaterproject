from django.db import models

class CityModel(models.Model):
    city_name = models.CharField("Şəhər", max_length=30)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Şəhər"
        verbose_name_plural = "Şəhərlər"

    def __str__(self):
        return self.city_name

class DistrictModel(models.Model):
    district_name = models.CharField("Rayon", max_length=30)
    city = models.ForeignKey(CityModel, verbose_name="Şəhər", on_delete=models.CASCADE, related_name="districts", blank=True, null=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Rayon"
        verbose_name_plural = "Rayonlar"

    def __str__(self):
        return self.district_name

class VillageModel(models.Model):
    village_name = models.CharField("Kənd", max_length=100)
    district = models.ForeignKey(DistrictModel, verbose_name="Rayon", on_delete=models.CASCADE, related_name="district_villages", blank=True, null=True)
    city = models.ForeignKey(CityModel, verbose_name="Şəhər", on_delete=models.CASCADE, related_name="city_villages", blank=True, null=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Kənd"
        verbose_name_plural = "Kəndlər"

    def __str__(self):
        return self.village_name

class ProductModel(models.Model):
    name = models.TextField("Məhsulun adı")
    price = models.FloatField("Məhsulun qiyməti", default=0)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Məhsul"
        verbose_name_plural = "Məhsullar"

    def __str__(self):
        return self.name

class GiftModel(models.Model):
    name = models.TextField("Hədiyyənin adı")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Hədiyyə"
        verbose_name_plural = "Hədiyyələr"

    def __str__(self):
        return self.name

class DiscountModel(models.Model):
    client = models.ForeignKey('registrationapp.ClientModel', verbose_name="Satış", on_delete=models.CASCADE, related_name='discounts')
    discount_type = models.TextField("Endirimin tipi", blank=True, null=True)
    percentage = models.FloatField("Endirim %", blank=True, null=True)
    amount = models.FloatField("Endirimin miqdarı", blank=True, null=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Endirim"
        verbose_name_plural = "Endirimlər"

    def __str__(self):
        return self.discount_type
