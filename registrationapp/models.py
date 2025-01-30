from django.db import models
from productapp.models import ProductModel, CityModel, VillageModel, GiftModel, DistrictModel
from django.utils import timezone
from datetime import date, datetime, timedelta

from django.db.models.signals import pre_save
from django.dispatch import receiver
from registrationapp.get_date import get_date

class ClientModel(models.Model):
    name = models.CharField("Ad, Soyad", max_length=50)
    father_name = models.CharField("Ata adı", max_length=20)
    phone_number1 = models.CharField("Telefon nömrəsi", max_length=20)
    phone_number2 = models.CharField("Əlavə telefon nömrəsi", max_length=20, blank=True, null=True)
    home_number = models.CharField("Ev nömrəsi", max_length=20, blank=True, null=True)
    identification = models.CharField("Şəxsiyyət vəsiqəsinin seriya nömrəsi", max_length=20)
    client_product = models.ForeignKey(ProductModel, verbose_name="Məhsul", on_delete=models.SET_NULL, related_name="product_clients", blank=True, null=True)
    client_gifts = models.ManyToManyField(GiftModel, verbose_name="Hədiyyələr", related_name="gift_clients", blank=True)
    address = models.TextField("Ünvan")
    city = models.ForeignKey(CityModel, verbose_name="Şəhər", on_delete=models.SET_NULL, related_name="city_clients", blank=True, null=True)
    district = models.ForeignKey(DistrictModel, verbose_name="Rayon", on_delete=models.SET_NULL, related_name='district_clients', blank=True, null=True)
    village = models.ForeignKey(VillageModel, verbose_name="Kənd", on_delete=models.SET_NULL, related_name="village_clients", blank=True, null=True)
    note = models.TextField("Qeyd", blank=True, null=True)
    date = models.DateField("Satış tarixi", auto_now_add=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Müştəri"
        verbose_name_plural = "Müştərilər"
    
    def __str__(self):
        return self.name
    
class PaymentModel(models.Model):
    discount_type = models.CharField("Endirimin tipi", max_length=100, blank=True, null=True)
    discount_percentage = models.FloatField("Endirim faizi", blank=True, null=True)
    discount_amount = models.FloatField("Endirim miqdarı", blank=True, null=True)
    total_amount = models.FloatField("Cəmi ödəniş")

    class Meta:
        verbose_name = "Ödəniş"
        verbose_name_plural = "Ödəniş məlumatları"

    def __str__(self):
        return self.discount_type

class SellerModel(models.Model):
    SALARY_TYPES = (
        ("N", "Net"),
        ("G", "Gross")
    )
    name = models.CharField("Ad, Soyad", max_length=50)
    phone_number1 = models.CharField("Telefon nömrəsi 1", max_length=20, blank=True, null=True)
    phone_number2 = models.CharField("Telefon nömrəsi 2", max_length=20, blank=True, null=True)
    salary = models.FloatField("Maaş", blank=True, null=True)
    salary_type = models.CharField("Maaş növü", choices=SALARY_TYPES, max_length=1, blank=True, null=True)
    premier = models.FloatField("Premyera", blank=True, null=True)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Satıcı"
        verbose_name_plural = "Satıcılar"

    def __str__(self):
        return self.name

class RegistrationModel(models.Model):
    STATUS = (
        ("A", "Aktiv"),
        ("OT", "Ödəniş tamamlanıb"),
        ("IO", "İmtina olunan")
    )
    client = models.OneToOneField(ClientModel, verbose_name="Müştəri", on_delete=models.CASCADE, related_name="client_registration")
    payment = models.OneToOneField(PaymentModel, verbose_name="Ödəniş", on_delete=models.CASCADE, related_name="payment_registration")
    sellers = models.ManyToManyField(SellerModel, verbose_name="Satıcılar", related_name="seller_registrations")
    status = models.CharField("Status", choices=STATUS, max_length=2, default="A")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Qeydiyyat"
        verbose_name_plural = "Qeydiyyatlar"

    def save(self, *args, **kwargs):
        if self.id and not InstallmentInfoModel.objects.filter(registration=self).exists():
            InstallmentInfoModel.objects.create(
                registration = self,
                total_amount = self.payment.total_amount,
                paid_amount = 0,
                remaining_amount = self.payment.total_amount,
                overdue_amount = 0,
                refund_amount = 0,
                payment_amount = 0,
                installment_count = 1,
                start_date = timezone.now()
            )
            ChangeFilterModel.objects.create(
                registration = self,
                category = "F",
                period = 0.5,
                date = get_date(self.client.date, 0.5),
                change_status = "DM",
            )
            ChangeFilterModel.objects.create(
                registration = self,
                category = "S",
                period = 1,
                date = get_date(self.client.date, 1),
                change_status = "DM",
            )
            ChangeFilterModel.objects.create(
                registration = self,
                category = "T",
                period = 1.5,
                date = get_date(self.client.date, 1.5),
                change_status = "DM",
            )
            ChangeFilterModel.objects.create(
                registration = self,
                category = "FT",
                period = 2,
                date = get_date(self.client.date, 2),
                change_status = "DM",
            )
            
        return super(RegistrationModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.client.name

class InstallmentInfoModel(models.Model):
    registration = models.OneToOneField(RegistrationModel, verbose_name="Qeydiyyat", on_delete=models.CASCADE, related_name="installmentinfo")
    total_amount = models.FloatField("İlkin məbləğ")
    paid_amount = models.FloatField("Ödənilən məbləğ")
    remaining_amount = models.FloatField("Qalan məbləğ")
    overdue_amount = models.FloatField("Gecikən məbləğ")
    refund_amount = models.FloatField("Geri ödənilən məbləğ")

    payment_amount = models.FloatField("Ödəniş miqdarı")
    installment_count = models.IntegerField("Taksit sayı")
    start_date = models.DateField(default=timezone.now)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Taksit məlumatı"
        verbose_name_plural = "Taksit məlumatları"

    def save(self, *args, **kwargs):
        if self.id:
            if not InstallmentModel.objects.filter(installmentinfo=self).exists():
                day = self.start_date.day
                month = self.start_date.month
                year = self.start_date.year
                InstallmentModel.objects.create(
                    installmentinfo = self,
                    installment_date = date(year, month, day),
                    installment_amount = self.total_amount - self.payment_amount,
                    payment_amount = 0,
                    debt_amount = 0
                )
                for i in range(self.installment_count):
                    month = month + 1
                    if month == 13:
                        month = 1
                        year = year + 1
                    elif month in (4, 6, 9, 11) and day == 31:
                        day = 30
                    elif month == 2 and day > 28:
                        day = 28
                    remainder = 0
                    if i < self.installment_count - 1:
                        InstallmentModel.objects.create(
                            installmentinfo = self,
                            installment_date = date(year, month, day),
                            installment_amount = round(self.payment_amount / self.installment_count),
                            payment_amount = 0,
                            debt_amount = self.payment_amount / self.installment_count,
                        )
                        remainder += self.payment_amount / self.installment_count - round(self.payment_amount / self.installment_count)
                    else:
                        InstallmentModel.objects.create(
                            installmentinfo = self,
                            installment_date = date(year, month, day),
                            installment_amount = self.payment_amount / self.installment_count + remainder,
                            payment_amount = 0,
                            debt_amount = self.payment_amount / self.installment_count,
                        )
            paid_amounts = [installment.payment_amount for installment in self.installments.all()]
            overdue_amounts = [installment.debt_amount for installment in self.installments.filter(status="OM") if installment.installment_date < datetime.now().date()]
            self.paid_amount = sum(paid_amounts)
            self.remaining_amount = self.total_amount - self.paid_amount
            self.overdue_amount = sum(overdue_amounts)
        return super(InstallmentInfoModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.registration.client.name

class InstallmentModel(models.Model):
    PAYMENT_TYPES = (
        ("N", "Nağd"),
        ("NS", "Nağdsız")
    )
    STATUS = (
        ('O', 'Ödənilib'),
        ('OM', 'Ödənilməyib')
    )
    installmentinfo = models.ForeignKey(InstallmentInfoModel, verbose_name="Taksit məlumatları", on_delete=models.CASCADE, related_name="installments")
    installment_date = models.DateField("Plan üzrə tarix")
    installment_amount = models.FloatField("Plan üzrə məbləğ")
    payment_date = models.DateField("Ödəniş tarixi", blank=True, null=True)
    payment_amount = models.FloatField("Ödəniş miqdarı")
    debt_amount = models.FloatField("Qalıq borc")
    payment_type = models.CharField("Ödəniş növü", max_length=2, choices=PAYMENT_TYPES, default="N")
    status = models.CharField("Status", max_length=2, choices=STATUS, default="OM")
    message_status = models.BooleanField("Mesaj statusu", default=False)

    class Meta:
        verbose_name = "Taksit"
        verbose_name_plural = "Taksitlər"

    def save(self, *args, **kwargs):
        self.debt_amount = self.installment_amount - self.payment_amount
        if ExtraPaymentModel.objects.filter(installment=self).exists():
            sum_extra_payments = sum([extra_payment.payment_amount for extra_payment in self.extra_payments.all()])
            self.debt_amount -= sum_extra_payments
        return super(InstallmentModel, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.installmentinfo.installment_count -= 1
        self.installmentinfo.save()
        return super(InstallmentModel, self).delete(*args, **kwargs)

    def __str__(self):
        return self.installmentinfo.registration.client.name
    
class ExtraPaymentModel(models.Model):
    PAYMENT_TYPES = (
        ("N", "Nağd"),
        ("NS", "Nağdsız")
    )
    installment = models.ForeignKey(InstallmentModel, verbose_name="Taksit", on_delete=models.SET_NULL, related_name="extra_payments", blank=True, null=True)
    payment_date = models.DateTimeField("Ödəniş tarixi")
    payment_amount = models.FloatField("Ödəniş miqdarı")
    payment_type = models.CharField("Ödəniş növü", max_length=2, choices=PAYMENT_TYPES, default="N")

    def save(self, *args, **kwargs):
        self.installment.save()
        self.installment.installmentinfo.save()
        return super(ExtraPaymentModel, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.installment.installmentinfo.registration.client.name + " | " + self.installment.installment_date.month
    
class FilterChangerModel(models.Model):
    name = models.CharField("Ad, Soyad", max_length=100)
    phone_number1 = models.CharField("Telefon nömrəsi 1", max_length=20, blank=True, null=True)
    phone_number2 = models.CharField("Telefon nömrəsi 2", max_length=20, blank=True, null=True)
    salary = models.FloatField("Maaş", default=0)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Filter dəyişdirən"
        verbose_name_plural = "Filter dəyişdirənlər"

    def __str__(self):
        return self.name

class ChangeFilterModel(models.Model):
    CHANGE_STATUS = (
        ("D", "Dəyişdirilib"),
        ("DM", "Dəyişdirilməyib")
    )
    CATEGORIES = (
        ("F", "Birinci kateqoriya"),
        ("S", "İkinci kateqoriya"),
        ("T", "Üçüncü kateqoriya"),
        ("FT", "Dördüncü kateqoriya")
    )
    PAYMENT_STATUS = (
        ("O", "Ödənişli"),
        ("OS", "Ödənişsiz")
    )
    registration = models.ForeignKey(RegistrationModel, verbose_name="Qeydiyyat", on_delete=models.CASCADE, related_name="changefilters")
    change_count = models.IntegerField("Dəyişim sayı", default=0)
    category = models.CharField("Kateqoriya", choices=CATEGORIES, max_length=2)
    period = models.FloatField("Period", editable=False)
    change_status = models.CharField("Dəyişim statusu", choices=CHANGE_STATUS, max_length=2)
    changers = models.ManyToManyField(FilterChangerModel, verbose_name="Filter Dəyişdirənlər", related_name="changer_changes", blank=True)
    date = models.DateField("Dəyişim tarixi")
    payment_status = models.CharField("Ödəniş statusu", choices=PAYMENT_STATUS, max_length=2, default="OS")
    payment_amount = models.FloatField("Ödəniş miqdarı", default=0)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Filtir dəyişimi"
        verbose_name_plural = "Filtir dəyişimləri"

    def save(self, *args, **kwargs):
        if self.id and not ChangeFilterModel.objects.filter(registration=self.registration, change_count=self.change_count+1, category=self.category).exists():
            ChangeFilterModel.objects.create(
                registration = self.registration,
                change_count = self.change_count + 1,
                category = self.category,
                period = self.period,
                date = get_date(self.date, self.period),
                change_status = "DM"
            )
            self.change_status = "D"
        return super(ChangeFilterModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.registration.client.name + " / " + self.category
    
class ServicerModel(models.Model):
    name = models.CharField("Ad, soyad", max_length=100)
    phone_number1 = models.CharField("Telefon nömrəsi 1", max_length=20, blank=True, null=True)
    phone_number2 = models.CharField("Telefon nömrəsi 2", max_length=20, blank=True, null=True)
    salary = models.FloatField("Maaş", default=0)

    class Meta:
        ordering = ("-id",)
        verbose_name = "Servis edən şəxs"
        verbose_name_plural = "Servis edən şəxslər"

    def __str__(self):
        return self.name
    

class ShuttleServiceModel(models.Model):
    SERVICE_TYPES = (
        ("O", "Ödənişli"),
        ("OS", "Ödənişsiz")
    )
    SERVICE_STATUS = (
        ("O", "Servis olunub"),
        ("OM", "Servis olunmayıb")
    )
    registration = models.ForeignKey(RegistrationModel, verbose_name="Qeydiyyat", on_delete=models.CASCADE, related_name="shuttleservices")
    service = models.TextField("Servis xidməti", blank=True, null=True)
    date = models.DateField("Servis tarixi")
    servicers = models.ManyToManyField(ServicerModel, verbose_name="Servis edən şəxs", related_name="shuttleservices")
    type = models.CharField("Servis tipi", choices=SERVICE_TYPES, max_length=2, default="OS")
    price = models.FloatField("Servis qiyməti", default=0)
    note = models.TextField("Qeyd", blank=True, null=True)
    status = models.CharField("Status", choices=SERVICE_STATUS, max_length=2, default="OM")

    class Meta:
        ordering = ("-id",)
        verbose_name = "Servis xidməti"
        verbose_name_plural = "Servis xidmətləri"

    def __str__(self):
        return self.service
    
