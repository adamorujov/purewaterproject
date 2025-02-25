from rest_framework.generics import ListAPIView
from mainpage.models import SettingsModel, SocialMediaModel, ServiceModel, TestimonialModel
from mainpage.api.serializers import SettingsSerializer, SocialMediaSerializer, ServiceSerializer, TestimonialSerializer

class SettingsListAPIView(ListAPIView):
    queryset = SettingsModel.objects.all()
    serializer_class = SettingsSerializer

class SocialMediaListAPIView(ListAPIView):
    queryset = SocialMediaModel.objects.all()
    serializer_class = SocialMediaSerializer

class ServiceListAPIView(ListAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceSerializer

class TestimonialListAPIView(ListAPIView):
    queryset = TestimonialModel.objects.all()
    serializer_class = TestimonialSerializer

    