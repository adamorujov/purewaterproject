from rest_framework import serializers
from registrationapp.models import (
    ClientModel, SellerModel, PaymentModel, RegistrationModel,
    InstallmentInfoModel, InstallmentModel, ChangeFilterModel, FilterChangerModel,
    ServicerModel, ShuttleServiceModel, ExtraPaymentModel, CreditorModel                        
)
from accounting.models import DailyPaymentModel, PersonaDailyPaymentModel
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
    class Meta:
        model = SellerModel
        fields = "__all__"

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

# for extrapayment list
class ExtraPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraPaymentModel
        fields = "__all__"

# for dailypayment list
class DailyPaymentSerializer(serializers.ModelSerializer):
    installment = InstallmentSerializer()
    extrapayment = ExtraPaymentSerializer()
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

# for servicer list, create, update, destroy
class ServicerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicerModel
        fields = "__all__"

# for shuttle service list
class ShuttleServiceSerializer(serializers.ModelSerializer):
    registration = RegistrationSerializer()
    servicers = ServicerSerializer(many=True)
    class Meta:
        model = ShuttleServiceModel
        fields = "__all__"

# for shuttle service retrive, create, update, destroy
class ShuttleServiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShuttleServiceModel
        fields = "__all__"

# for creditor 
class CreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditorModel
        fields = "__all__"

# for personadailypayment list
class PersonaDailyPaymentSerializer(serializers.ModelSerializer):
    seller = SellerSerializer()
    changer = FilterChangerSerializer()
    servicer = ServicerSerializer()
    creditor = CreditorSerializer()
    class Meta:
        model = PersonaDailyPaymentModel
        fields = "__all__"

# for personadailypayment create, retrieve, update, destroy
class PersonaDailyPaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonaDailyPaymentModel
        fields = "__all__"

