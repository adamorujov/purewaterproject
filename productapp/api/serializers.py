from rest_framework import serializers
from productapp.models import (CityModel, DistrictModel, VillageModel, ProductModel, GiftModel, DiscountModel)

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityModel
        fields = "__all__"

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistrictModel
        fields = "__all__"

class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VillageModel
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = "__all__"

class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftModel
        fields = "__all__"

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountModel
        fields = "__all__"