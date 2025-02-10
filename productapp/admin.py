from django.contrib import admin
from productapp.models import ProductModel, DistrictModel, CityModel, VillageModel, GiftModel

@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'price')

@admin.register(DistrictModel)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'city')
    list_filter = ('city',)

@admin.register(VillageModel)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'district', 'city')
    list_filter = ('district', 'city')

admin.site.register(CityModel)
admin.site.register(GiftModel)