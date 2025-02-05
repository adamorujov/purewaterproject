from django.contrib import admin
from registrationapp.models import (ClientModel, PaymentModel, SellerModel, RegistrationModel, InstallmentInfoModel, InstallmentModel,
FilterChangerModel, ChangeFilterModel, ServicerModel, ShuttleServiceModel, ExtraPaymentModel, CreditorModel
)


admin.site.register(ClientModel)
admin.site.register(PaymentModel)
admin.site.register(SellerModel)
admin.site.register(RegistrationModel)
admin.site.register(InstallmentInfoModel)
admin.site.register(InstallmentModel)
admin.site.register(ExtraPaymentModel)
admin.site.register(FilterChangerModel)
admin.site.register(ChangeFilterModel)
admin.site.register(ServicerModel)
admin.site.register(ShuttleServiceModel)
admin.site.register(CreditorModel)