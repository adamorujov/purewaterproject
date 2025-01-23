from django.db import models
from registrationapp.models import InstallmentModel

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


