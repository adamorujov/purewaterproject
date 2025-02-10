from django.db import models
from registrationapp.models import InstallmentModel, SellerModel, FilterChangerModel, ServicerModel, CreditorModel

class DailyPaymentModel(models.Model):
    installment = models.ForeignKey(InstallmentModel, verbose_name="Taksit", on_delete=models.CASCADE, related_name="dailypayments")
    month = models.IntegerField("Ödənilən ay", blank=True, null=True)
    date = models.DateField("Ödəniş tarixi")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Günlük ödəniş"
        verbose_name_plural = "Günlük ödənişlər"

    def __str__(self):
        return str(self.id)

class PersonaDailyPaymentModel(models.Model):
    seller = models.ForeignKey(SellerModel, verbose_name="Satıcı", on_delete=models.SET_NULL, related_name="seller_dailypayments", blank=True, null=True)
    changer = models.ForeignKey(FilterChangerModel, verbose_name="Filter Dəyişən", on_delete=models.SET_NULL, related_name="changer_dailypayments", blank=True, null=True)
    servicer = models.ForeignKey(ServicerModel, verbose_name="Servis xidməti edən", on_delete=models.SET_NULL, related_name="servicer_dailypayments", blank=True, null=True)
    creditor = models.ForeignKey(CreditorModel, verbose_name="Kreditor", on_delete=models.SET_NULL, related_name="creditor_dailypayments", blank=True, null=True)
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
        elif self.creditor:
            name = self.creditor.name
        else:
            name = ""
        return name + " | " + str(self.month) + " | " + str(self.date)
