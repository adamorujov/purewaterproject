from django.db import models
from registrationapp.models import InstallmentModel, SellerModel, FilterChangerModel, ServicerModel

class DailyPaymentModel(models.Model):
    installment = models.ForeignKey(InstallmentModel, verbose_name="Taksit", on_delete=models.CASCADE, related_name="dailypayments")
    month = models.IntegerField("Ödədiyi ay")
    date = models.DateField("Ödəniş tarixi")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Günlük ödəniş"
        verbose_name_plural = "Günlük ödənişlər"

    def __str__(self):
        try:
            return self.installment.installmentinfo.registration.client.name + " | " + self.installment.installmentinfo.registration.client.client_product.name + " | " + str(self.date) + " | " + str(self.month)
        except:
            return "Silinmiş məlumat" + " | " + str(self.date) + " | " + str(self.month)

class PersonaDailyPaymentModel(models.Model):
    seller = models.ForeignKey(SellerModel, verbose_name="Satıcı", on_delete=models.SET_NULL, related_name="seller_dailypayments", blank=True, null=True)
    changer = models.ForeignKey(FilterChangerModel, verbose_name="Filter Dəyişən", on_delete=models.SET_NULL, related_name="changer_dailypayments", blank=True, null=True)
    servicer = models.ForeignKey(ServicerModel, verbose_name="Servis xidməti edən", on_delete=models.SET_NULL, related_name="servicer_dailypayments", blank=True, null=True)
    month = models.IntegerField("Ödənilən ay")
    date = models.DateField("Ödənilən tarix")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Persona üçün günlük ödəniş"
        verbose_name_plural = "Persona üçün günlük ödənişlər"

    def __str__(self):
        name = ""
        if self.seller:
            name = self.seller.name
        elif self.changer:
            name = self.changer.name
        elif self.servicer:
            name = self.servicer.name
        else:
            name = ""
        return name + " | " + str(self.month) + " | " + str(self.date)
