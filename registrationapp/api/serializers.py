from rest_framework import serializers
from registrationapp.models import (
    ClientModel, SellerModel, PaymentModel, RegistrationModel,
    InstallmentInfoModel, InstallmentModel, ChangeFilterModel, FilterChangerModel,
    ServicerModel, ShuttleServiceModel                         
)
from accounting.models import DailyPaymentModel
from productapp.api.serializers import ProductSerializer, CitySerializer, DistrictSerializer, VillageSerializer, GiftSerializer
from django.utils import timezone

# for client create, update, destroy
class ClientSerializer(serializers.ModelSerializer):
    client_product = ProductSerializer()
    city = CitySerializer()
    district = DistrictSerializer()
    village = VillageSerializer()
    client_gifts = GiftSerializer(many=True)

    class Meta:
        model = ClientModel
        fields = "__all__"

class ClientCreateSerializer(serializers.ModelSerializer): 
    class Meta:
        model = ClientModel
        fields = "__all__"

# for seller list
class SellerSerializer(serializers.ModelSerializer):
    total_salary = serializers.SerializerMethodField()
    sold_count = serializers.SerializerMethodField()
    rejected_count = serializers.SerializerMethodField()

    class Meta:
        model = SellerModel
        fields = "__all__"

    def get_total_salary(self, obj):
        return obj.salary + obj.premier * self.get_sold_count(obj) - obj.premier * self.get_rejected_count(obj) if obj.salary and obj.premier else 0

    def get_sold_count(self, obj):
        return obj.seller_registrations.filter(status="A").filter(client__date__month=timezone.now().date().month).count()
    
    def get_rejected_count(self, obj):
        return obj.seller_registrations.filter(status="IO").filter(client__date__month=timezone.now().date().month).count()

# for seller create, update, destroy
class SellerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerModel
        fields = "__all__"

# for payment create, update, destroy
class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentModel
        fields = "__all__"

# for registration list
class RegistrationSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    sellers = SellerSerializer(many=True)
    payment = PaymentCreateSerializer()
    class Meta:
        model = RegistrationModel
        fields = "__all__"

# for registration create, update, destroy
class RegistrationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationModel
        fields = "__all__"

# for installmentinfo retrieve
class InstallmentInfoSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer()
    class Meta:
        model = InstallmentInfoModel
        fields = "__all__"

# for installmentinfo update
class InstallmentInfoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentInfoModel
        fields = "__all__"

# for installment list
class InstallmentSerializer(serializers.ModelSerializer):
    installmentinfo = InstallmentInfoSerializer()
    class Meta:
        model = InstallmentModel
        fields = "__all__"

# for installment retrieve
class InstallmentInfoInstallmentSerializer(serializers.ModelSerializer):
    installmentinfo = InstallmentInfoSerializer()
    class Meta:
        model = InstallmentModel
        fields = "__all__"

# for installment update
class InstallmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentModel
        fields = ("installment_date", "installment_amount", "payment_date", "payment_amount", "payment_type")

# for installment destroy
class InstallmentDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = InstallmentModel
        fields = "__all__"

# for dailypayment list
class DailyPaymentSerializer(serializers.ModelSerializer):
    installment = InstallmentSerializer()
    class Meta:
        model = DailyPaymentModel
        fields = "__all__"

# for dailypayment create, retrieve, update, destroy
class DailyPaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyPaymentModel
        fields = "__all__"

# for changefilter retrieve, update, delete
class ChangeFilterUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeFilterModel
        fields = "__all__"

# for filterchanger list, create, update, destroy
class FilterChangerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilterChangerModel
        fields = "__all__"

# for changefilter list
class ChangeFilterSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer()
    changers = FilterChangerSerializer(many=True)
    class Meta:
        model = ChangeFilterModel
        fields = "__all__"

class ServicerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicerModel
        fields = "__all__"

class ShuttleServiceSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer()
    servicers = ServicerSerializer(many=True)
    class Meta:
        model = ShuttleServiceModel
        fields = "__all__"

class ShuttleServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShuttleServiceModel
        fields = "__all__"

