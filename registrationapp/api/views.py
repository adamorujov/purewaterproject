from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from registrationapp.models import (
    ClientModel, SellerModel, PaymentModel, RegistrationModel, InstallmentInfoModel, 
    InstallmentModel, ChangeFilterModel, FilterChangerModel, ServicerModel, ShuttleServiceModel
)
from registrationapp.api.serializers import (
    ClientCreateSerializer, PaymentCreateSerializer, SellerSerializer, SellerCreateSerializer, RegistrationSerializer, RegistrationCreateSerializer,
    InstallmentInfoSerializer, InstallmentInfoUpdateSerializer, InstallmentInfoInstallmentSerializer, 
    InstallmentSerializer, InstallmentUpdateSerializer, InstallmentDestroySerializer,
    DailyPaymentSerializer, DailyPaymentCreateSerializer, ChangeFilterSerializer, ChangeFilterUpdateSerializer, FilterChangerSerializer,
    ServicerSerializer, ShuttleServiceSerializer, ShuttleServiceCreateSerializer
)
from accounting.models import DailyPaymentModel
from django.utils import timezone
from django.db.models import Q, F, Case, When, IntegerField
from django.shortcuts import get_object_or_404
import openpyxl

# ---------- Client APIs -------------
class ClientCreateAPIView(CreateAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = (IsAdminUser,)

class ClientRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ClientModel.objects.all()
    serializer_class = ClientCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ---------- Seller APIs --------------
class SellerListAPIView(ListAPIView):
    queryset = SellerModel.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAdminUser,)

class SellerCreateAPIView(CreateAPIView):
    queryset = SellerModel.objects.all()
    serializer_class = SellerCreateSerializer
    permission_classes = (IsAdminUser,)

class SellerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SellerModel.objects.all()
    serializer_class = SellerCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ----------- Payment APIs --------------
class PaymentCreateAPIView(CreateAPIView):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = (IsAdminUser,)

class PaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PaymentModel.objects.all()
    serializer_class = PaymentCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# --------- Registration APIs ------------
class RegistrationListAPIView(ListAPIView):
    queryset = RegistrationModel.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = (IsAdminUser,)

class RegistrationCreateAPIView(CreateAPIView):
    queryset = RegistrationModel.objects.all()
    serializer_class = RegistrationCreateSerializer
    permission_classes = (IsAdminUser,)

class RegistrationRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = RegistrationModel.objects.all()
    serializer_class = RegistrationCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# --------- InstallmentInfo APIs -----------
class RegistrationInstallmentInfoRetrieveAPIView(RetrieveAPIView):
    def get_object(self):
        id = self.kwargs.get("id")
        return InstallmentInfoModel.objects.get(registration__id=id)
    serializer_class = InstallmentInfoSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

class InstallmentInfoRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = InstallmentInfoModel.objects.all()
    serializer_class = InstallmentInfoUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"


# ----------- Installment APIs ------------
class InstallmentInfoInstallmentListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        installmentinfo = get_object_or_404(InstallmentInfoModel, registration__id=id)
        return InstallmentModel.objects.filter(installmentinfo=installmentinfo)
    serializer_class = InstallmentInfoInstallmentSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

## installment create-i yaz
class InstallmentCreateAPIView(CreateAPIView):
    queryset = InstallmentModel.objects.all()
    serializer_class = InstallmentDestroySerializer
    permission_classes = (IsAdminUser,)

class InstallmentUpdateAPIView(UpdateAPIView):
    queryset = InstallmentModel.objects.all()
    serializer_class = InstallmentUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get('action')

        if action == 'update':
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                instance.installmentinfo.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'payment':
            payment_data = {
                "installment": instance.id,
                "month": request.data.get('month'),
                "date": instance.payment_date
            }
            dp_serializer = DailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                instance.status = "O"
                instance.installmentinfo.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response(dp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Invalid action specified."},
                status=status.HTTP_400_BAD_REQUEST
            )

class InstallmentDestroyAPIView(DestroyAPIView):
    queryset = InstallmentModel.objects.all()
    serializer_class = InstallmentDestroySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ---------- DailyPayment APIs ------------
class DailyPaymentListAPIView(ListAPIView):
    queryset = DailyPaymentModel.objects.all()
    serializer_class = DailyPaymentSerializer
    permission_classes = (IsAdminUser,)

class DailyPaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DailyPaymentModel.objects.all()
    serializer_class = DailyPaymentCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ---------- OverduePayment APIs ------------
class OverduePaymentListAPIView(ListAPIView):
    def get_queryset(self):
        return InstallmentModel.objects.filter(
            Q(installment_date__lt = timezone.now()) | Q(installment_date__lt = F("payment_date"))
        ).annotate(
            status_order = Case(
                When(status="O", then=1),
                When(status="OM", then=0),
                output_field=IntegerField()
            )
        ).order_by('status_order')
    serializer_class = InstallmentSerializer
    permission_classes = (IsAdminUser,)

# ------------ ChangeFilter APIs --------------
class ChangeFilterListAPIView(ListAPIView):
    queryset = ChangeFilterModel.objects.all()
    serializer_class = ChangeFilterSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

class ChangeFilterRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ChangeFilterModel.objects.all()
    serializer_class = ChangeFilterUpdateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ------------ FilterChanger APIs -----------
class FilterChangerListCreateAPIView(ListCreateAPIView):
    queryset = FilterChangerModel.objects.all()
    serializer_class = FilterChangerSerializer
    permission_classes = (IsAdminUser,)

class FilterChangerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = FilterChangerModel.objects.all()
    serializer_class = FilterChangerSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ------------ Servicer APIs ---------------
class ServicerListCreateAPIView(ListCreateAPIView):
    queryset = ServicerModel.objects.all()
    serializer_class = ServicerSerializer
    permission_classes = (IsAdminUser,)

class ServicerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ServicerModel.objects.all()
    serializer_class = ServicerSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ----------- ShuttleService APIs -----------
class ShuttleServiceListAPIView(ListAPIView):
    queryset = ShuttleServiceModel.objects.all()
    serializer_class = ShuttleServiceSerializer
    permission_classes = (IsAdminUser,)

class ShuttleServiceCreateAPIView(CreateAPIView):
    queryset = ShuttleServiceModel.objects.all()
    serializer_class = ShuttleServiceCreateSerializer
    permission_classes = (IsAdminUser,)

class ShuttleServiceRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = ShuttleServiceModel.objects.all()
    serializer_class = ShuttleServiceCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"
