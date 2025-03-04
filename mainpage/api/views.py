from rest_framework.generics import ListAPIView, RetrieveAPIView
from mainpage.models import SettingsModel, SocialMediaModel, ServiceModel, CategoryModel, OurProductModel, TestimonialModel
from mainpage.api.serializers import SettingsSerializer, SocialMediaSerializer, ServiceSerializer, CategorySerializer, OurProductSerializer, TestimonialSerializer

class SettingsListAPIView(ListAPIView):
    queryset = SettingsModel.objects.all()
    serializer_class = SettingsSerializer

class SocialMediaListAPIView(ListAPIView):
    queryset = SocialMediaModel.objects.all()
    serializer_class = SocialMediaSerializer

class ServiceListAPIView(ListAPIView):
    queryset = ServiceModel.objects.all()
    serializer_class = ServiceSerializer

class CategoryListAPIView(ListAPIView):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer

class CategoryOurProductListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        return OurProductModel.objects.filter(category__id=id)
    serializer_class = OurProductSerializer

class OurProductRetrieveAPIView(RetrieveAPIView):
    queryset = OurProductModel.objects.all()
    serializer_class = OurProductSerializer
    lookup_field = "id"

class TestimonialListAPIView(ListAPIView):
    queryset = TestimonialModel.objects.all()
    serializer_class = TestimonialSerializer

    