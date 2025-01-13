from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from productapp.models import CityModel, DistrictModel, VillageModel, ProductModel, GiftModel, DiscountModel
from productapp.api.serializers import CitySerializer, DistrictSerializer, VillageSerializer, ProductSerializer, GiftSerializer, DiscountSerializer
from rest_framework.permissions import IsAdminUser

# ----------- City APIs -----------
class CityListCreateAPIView(ListCreateAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)

class CityRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CityModel.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ----------- District APIs -------------
class DistrictListCreateAPIView(ListCreateAPIView):
    queryset = DistrictModel.objects.all()
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
    queryset = VillageModel.objects.all()
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

# --------------- Discount APIs --------------
class DiscountListCreateAPIView(ListCreateAPIView):
    queryset = DiscountModel.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAdminUser,)

class DiscountRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DiscountModel.objects.all()
    serializer_class = DiscountSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

