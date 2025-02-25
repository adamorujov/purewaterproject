from django.contrib import admin
from registrationapp.models import (ClientModel, PaymentModel, SellerModel, RegistrationModel, InstallmentInfoModel, InstallmentModel,
FilterChangerModel, ChangeFilterModel, ServicerModel, ShuttleServiceModel, ExtraPaymentModel, CreditorModel
)


@admin.register(ClientModel)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone_number1', 'city', 'district', 'village', 'client_product', 'date')
    list_filter = ('date',)
    search_fields = ('name', 'father_name', 'city__city_name', 'district__district_name', 'village__village_name')


admin.site.register(PaymentModel)
admin.site.register(SellerModel)

@admin.register(RegistrationModel)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    list_filter = ('status',)
    search_fields = ('client__name', 'client__father_name', 'client__city__city_name', 'client__district__district_name', 'client__village__village_name')

@admin.register(InstallmentInfoModel)
class InstallmentInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total_amount', 'paid_amount', 'remaining_amount', 'overdue_amount', 'refund_amount', 'get_down_payment_amount', 'installment_count', 'start_date')
    ordering = ("-id",)

    def get_down_payment_amount(self, obj):
        return obj.total_amount - obj.payment_amount
    get_down_payment_amount.short_description = "İlkin ödənilən məbləğ"   

@admin.register(InstallmentModel)
class InstallmentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'installment_date', 'installment_amount', 'payment_date', 'payment_amount', 'debt_amount', 'payment_type', 'status', 'message_status')
    ordering = ("id",)
    search_fields = ('installmentinfo__registration__client__name', 'installmentinfo__registration__client__father_name')

@admin.register(ExtraPaymentModel)
class ExtraPaymentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'payment_date', 'payment_amount', 'payment_type', 'status')
    search_fields = ('installment__installmentinfo__registration__client__name', 'installment__installmentinfo__registration__client__father_name')

admin.site.register(FilterChangerModel)

@admin.register(ChangeFilterModel)
class ChangeFilterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'category', 'get_period', 'change_count', 'change_status', 'date')

    def get_period(self, obj):
        if obj.period == 0.5:
            return '6 ay'
        elif obj.period == 1.5:
            return '1 il 6 ay'
        else:
            return str(int(obj.period)) + " il"
    get_period.short_description = "Period"


admin.site.register(ServicerModel)

@admin.register(ShuttleServiceModel)
class ShuttleServiceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_registration_client', 'date', 'status')
    list_filter = ('status',)
    search_fields = ('registration__client__name', 'registration__client__father_name')

    def get_registration_client(self, obj):
        return obj.registration.client.name + " " + obj.registration.client.father_name if obj.registration.client.father_name else obj.registration.client.name
    get_registration_client.short_description = "Müştəri"

admin.site.register(CreditorModel)