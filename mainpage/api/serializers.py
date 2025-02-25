from rest_framework import serializers
from mainpage.models import SettingsModel, SocialMediaModel, ServiceModel, CategoryModel, OurProductModel, TestimonialModel

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingsModel
        fields = "__all__"

class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaModel
        fields = "__all__" 

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceModel
        fields = "__all__" 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OurProductModel
        fields = "__all__"

class OurProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = OurProductModel
        fields = "__all__"

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestimonialModel
        fields = "__all__"

