from django.contrib import admin
from productapp.models import ProductModel, DistrictModel, CityModel, VillageModel, GiftModel, DiscountModel

admin.site.register(ProductModel)
admin.site.register(DistrictModel)
admin.site.register(CityModel)
admin.site.register(VillageModel)
admin.site.register(GiftModel)
admin.site.register(DiscountModel)