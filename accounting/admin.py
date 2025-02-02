from django.contrib import admin
from accounting.models import DailyPaymentModel, PersonaDailyPaymentModel

admin.site.register(DailyPaymentModel)
admin.site.register(PersonaDailyPaymentModel)