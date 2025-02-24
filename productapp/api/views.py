from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from productapp.models import CityModel, DistrictModel, VillageModel, ProductModel, GiftModel
from productapp.api.serializers import CitySerializer, DistrictSerializer, VillageSerializer, ProductSerializer, GiftSerializer
from rest_framework.permissions import IsAdminUser
from productapp.api.az_sort_key import az_sort_key

# ----------- City APIs -----------
class CityListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return sorted(CityModel.objects.all(), key=lambda obj: az_sort_key(obj.city_name))
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)

class CityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ----------- District APIs -------------
class DistrictListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return sorted(DistrictModel.objects.all(), key=lambda obj: az_sort_key(obj.district_name))
    serializer_class = DistrictSerializer
    permission_classes = (IsAdminUser,)

class CityDistrictListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        return DistrictModel.objects.filter(city__id=id)
    serializer_class = DistrictSerializer
    permission_classes = (IsAdminUser,)
        
class DistrictRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DistrictModel.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

class DistrictCityRetrieveAPIView(RetrieveAPIView):
    def get_object(self):
        id = self.kwargs.get("id")
        district = DistrictModel.objects.get(id=id)
        return district.city
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ------------- Village APIs -------------
class VillageListCreateAPIView(ListCreateAPIView):
    def get_queryset(self):
        return sorted(VillageModel.objects.all(), key=lambda obj: az_sort_key(obj.village_name))
    serializer_class = VillageSerializer
    permission_classes = (IsAdminUser,)

class DistrictVillageListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        return VillageModel.objects.filter(district__id=id)
    serializer_class = VillageSerializer
    permission_classes = (IsAdminUser,)

class CityVillageListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        return VillageModel.objects.filter(city__id=id)
    serializer_class = VillageSerializer
    permission_classes = (IsAdminUser,)

class VillageRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = VillageModel.objects.all()
    serializer_class = VillageSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"


# -------------- Product APIs --------------
class ProductListCreateAPIView(ListCreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)

class ProductRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# -------------- Gift APIs ---------------
class GiftListCreateAPIView(ListCreateAPIView):
    queryset = GiftModel.objects.all()
    serializer_class = GiftSerializer
    permission_classes = (IsAdminUser,)

class GiftRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = GiftModel.objects.all()
    serializer_class = GiftSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

