from django.contrib import admin
from accounting.models import DailyPaymentModel, PersonaDailyPaymentModel

@admin.register(DailyPaymentModel)
class DailyPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_client_name', 'get_month', 'date')
    list_filter = ('date',)

    def get_client_name(self, obj):
        if obj.installment:
            return obj.installment.installmentinfo.registration.client.name
        elif obj.extrapayment:
            return obj.extrapayment.installmentinfo.registration.client.name
        else:
            return "---"

    get_client_name.short_description = "Müştəri"

    def get_month(self, obj):
        if not obj.month:
            return "İlkin ödəniş" if obj.month == 0 else "Əlavə ödəniş"
        return obj.month
    get_month.short_description = "Ödənilən ay"

    def has_add_permission(self, request):
        return False
    
@admin.register(PersonaDailyPaymentModel)
class PersonaDailyPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_persona_name', 'get_month', 'date')
    list_filter = ('date',)

    def get_persona_name(self, obj):
        return obj.seller.name or obj.changer.name or obj.servicer.name or obj.creditor.name
    get_persona_name.short_description = "Persona"

    def get_month(self, obj):
        month_names = ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'İyun', 'İyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr']
        return month_names[obj.month-1]
    get_month.short_description = "Ödənilən ay"

    def has_add_permission(self, request):
        return False