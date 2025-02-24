from rest_framework.generics import (
    ListAPIView, ListCreateAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from registrationapp.models import (
    ClientModel, SellerModel, PaymentModel, RegistrationModel, InstallmentInfoModel, 
    InstallmentModel, ChangeFilterModel, FilterChangerModel, ServicerModel, ShuttleServiceModel, ExtraPaymentModel, CreditorModel
)
from registrationapp.api.serializers import (
    ClientCreateSerializer, PaymentCreateSerializer, SellerSerializer, SellerCreateSerializer, RegistrationSerializer, RegistrationCreateSerializer,
    InstallmentInfoSerializer, InstallmentInfoUpdateSerializer, InstallmentInfoInstallmentSerializer, 
    InstallmentSerializer, InstallmentUpdateSerializer, InstallmentDestroySerializer,
    DailyPaymentSerializer, DailyPaymentCreateSerializer, ChangeFilterSerializer, ChangeFilterUpdateSerializer, FilterChangerSerializer,
    ServicerSerializer, ShuttleServiceSerializer, ShuttleServiceCreateSerializer, 
    ExtraPaymentSerializer, PersonaDailyPaymentSerializer, PersonaDailyPaymentCreateSerializer, CreditorSerializer
)
from accounting.models import DailyPaymentModel, PersonaDailyPaymentModel
from datetime import date
from django.utils import timezone
from django.db.models import Q, F, Case, When, IntegerField
from django.shortcuts import get_object_or_404
from registrationapp.api.corrected_num2words import corrected_num2words

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

class SellerDataRetrieveAPIView(RetrieveAPIView):
    queryset = SellerModel.objects.all()
    serializer_class = SellerSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        start_date = request.query_params.get('start_date', None).split("-")
        end_date = request.query_params.get('end_date', None).split("-")

        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))

        if start_date <= end_date:
            all_registrations = instance.seller_registrations.all()
            result_data = []
            m_count = (end_date.year - start_date.year) * 12 + end_date.month - start_date.month
            all_months = []
            x, y= start_date.month, start_date.year
            for m in range(m_count + 1):
                all_months.append([x, y])
                if x < 12:
                    x += 1
                else:
                    x = 1
                    y += 1
            
            for d in all_months:
                e = []
                e.append(d)
                l, t, z = [], [], []
                for reg in all_registrations:
                    if reg.refusal_date and reg.refusal_date.year == d[1] and reg.refusal_date.month == d[0]:
                        t.append(reg.client.name)
                    if reg.end_date and reg.end_date.year == d[1] and reg.end_date.month == d[0]:
                        z.append(reg.client.name)
                    if (reg.client.date.year < d[1] or (reg.client.date.year == d[1] and reg.client.date.month <= d[0])) and (not reg.refusal_date or reg.refusal_date.year > d[1] or (reg.refusal_date.year == d[1] and reg.refusal_date.month > d[0])) and (not reg.end_date or reg.end_date.year > d[1] or (reg.end_date.year == d[1] and reg.end_date.month > d[0])):
                        l.append(reg.client.name)
                    
                e.append(l)
                e.append(t)
                e.append(z)
                e.append([len(l), len(t), len(z)])
                result_data.append(e)

            response_data = {
                "result_data": result_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response({"errors": "Başlanğıc tarix son tarixdən böyükdür."}, status=status.HTTP_400_BAD_REQUEST)


class SellerRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = SellerModel.objects.all()
    serializer_class = SellerCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "payment":
            payment_data = {
                "seller": instance.id,
                "month": request.data.get("month"),
                "date": request.data.get("date")
            }
            dp_serializer = PersonaDailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors": "Invalid action specified!"}, status=status.HTTP_400_BAD_REQUEST)

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
class InstallmentInfoListAPIView(ListAPIView):
    def get_queryset(self):
        return InstallmentInfoModel.objects.filter(registration__status="A")
    serializer_class = InstallmentInfoSerializer
    permission_classes = (IsAdminUser,)


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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "refund":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                instance.registration.status = "IO"
                instance.registration.refusal_date = timezone.now().date
                instance.registration.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "delete":
            instance.installments.all().delete()
            return Response({"success": "Taksitlər silindi."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action specified"}, status=status.HTTP_400_BAD_REQUEST)
            


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
                debt_payments = instance.installmentinfo.installments.filter(debt_amount__gt=0)
                x = instance.payment_amount
                for debt in debt_payments:
                    print(debt.installment_date)
                    y = debt.debt_amount
                    debt.debt_amount = y - x if x < y else 0
                    x -= y
                    debt.status = "O"
                    debt.message_status = False
                    debt.payment_type = instance.payment_type
                    debt.save()
                    if x <= 0:
                        break
                instance.installmentinfo.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        elif action == "whatsapp":
            phone_number = request.data.get("phone_number")
            client = instance.installmentinfo.registration.client
            message = "%s %s\n\n%s\n%s\n\nÖdəniş %0.2f azn\n\nÖdəniş tarixi %s\n\nQalıq %0.2f\n" % (
                client.name, client.father_name, client.phone_number1, client.phone_number2, 
                instance.payment_amount, instance.payment_date, instance.installmentinfo.remaining_amount
            ) if client.phone_number2 else "%s %s\n\n%s\n\nÖdəniş %0.2f azn\n\nÖdəniş tarixi %s\n\nQalıq %0.2f\n" % (
                client.name, client.father_name, client.phone_number1,
                instance.payment_amount, instance.payment_date, instance.installmentinfo.remaining_amount
            )
            message += client.city.city_name + " ş. " if client.city else ""
            message += client.district.district_name + " r. " if client.district else ""
            message += client.village.village_name + " k. " if client.village else ""

            instance.message_status = True
            instance.save()
            if phone_number:
                return Response({"phone_number": phone_number, "message": message}, status=status.HTTP_200_OK)
            else:
                return Response({"errors": "Kreditorun nömrəsi təyin edilməyib."}, status=status.HTTP_400_BAD_REQUEST)
        elif action == "check":
            client = instance.installmentinfo.registration.client
            client_address = ""
            client_address += client.city.city_name + " ş. " if client.city else ""
            client_address += client.district.district_name + " r. " if client.district else ""
            client_address += client.village.village_name + " k. " if client.village else ""
            # next_payment = InstallmentModel.objects.filter(installmentinfo=instance.installmentinfo, debt_amount=F('installment_amount'))[0]
            next_payment = instance.installmentinfo.installments.filter(debt_amount=F('installment_amount'))[0]
            print(instance.installmentinfo.installments.filter(debt_amount=F('installment_amount')))
            print(next_payment)

            check_data = {
                "name": client.name.split(" ")[0],
                "surname": client.name.split(" ")[1] or " ",
                "father_name": client.father_name or " ",
                "address": client_address,
                "payment_amount_with_digit": instance.payment_amount,
                "payment_amount_with_word": corrected_num2words(instance.payment_amount),
                "installment_date": instance.installment_date,
                "payment_date": instance.payment_date,
                "overdue_amount": instance.debt_amount,
                "overdue_date": instance.installment_date,
                "remaining_amount": instance.installmentinfo.remaining_amount,
                "next_payment_amount": next_payment.debt_amount,
                "next_payment_date": next_payment.installment_date
            }
            return Response(check_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)
        
class InstallmentDestroyAPIView(DestroyAPIView):
    queryset = InstallmentModel.objects.all()
    serializer_class = InstallmentDestroySerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ----------- ExtraPayment APIs ------------
class InstallmentInfoExtraPaymentListAPIView(ListAPIView):
    def get_queryset(self):
        id = self.kwargs.get("id")
        installmentinfo = get_object_or_404(InstallmentInfoModel, registration__id=id)
        return ExtraPaymentModel.objects.filter(installmentinfo=installmentinfo)
    serializer_class = ExtraPaymentSerializer
    permission_classes = (IsAdminUser,)

class ExtraPaymentCreateAPIView(CreateAPIView):
    queryset = ExtraPaymentModel.objects.all()
    serializer_class = ExtraPaymentSerializer
    permission_classes = (IsAdminUser,)

class ExtraPaymentRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = ExtraPaymentModel.objects.all()
    serializer_class = ExtraPaymentSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "payment":
            payment_data = {
                "installmentinfo": instance.installmentinfo.id,
                "date": instance.payment_date
            }
            dp_serializer = DailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                debt_installments = instance.installmentinfo.installments.filter(debt_amount__gt=0)
                x = instance.payment_amount
                for debt in debt_installments:
                    y = debt.debt_amount
                    debt.debt_amount = y - x if x < y else 0
                    x -= y
                    debt.status = "O"
                    debt.payment_type = instance.payment_type
                    debt.save()
                    if x <= 0:
                        break
                instance.status = "O"
                instance.save()
                instance.installmentinfo.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        elif action == "check":
            client = instance.installmentinfo.registration.client
            client_address = ""
            client_address += client.city.city_name + " ş. " if client.city else ""
            client_address += client.district.district_name + " r. " if client.district else ""
            client_address += client.village.village_name + " k. " if client.village else ""
            next_payment = instance.installmentinfo.installments.filter(debt_amount=F('installment_amount'))[0]
            check_data = {
                "name": client.name.split(" ")[0],
                "surname": client.name.split(" ")[1] or " ",
                "father_name": client.father_name or " ",
                "address": client_address,
                "payment_amount_with_digit": instance.payment_amount,
                "payment_amount_with_word": corrected_num2words(instance.payment_amount),
                "payment_date": instance.payment_date,
                "overdue_amount": instance.installmentinfo.overdue_amount,
                "remaining_amount": instance.installmentinfo.remaining_amount,
                "next_payment_amount": next_payment.debt_amount,
                "next_payment_date": next_payment.installment_date
            }
            return Response(check_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)

class ExtraPaymentDestroyAPIView(DestroyAPIView):
    queryset = ExtraPaymentModel.objects.all()
    serializer_class = ExtraPaymentSerializer
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

# ---------- Persona DailyPayment APIs -----------------
class PersonaDailyPaymentListAPIView(ListAPIView):
    queryset = PersonaDailyPaymentModel.objects.all()
    serializer_class = PersonaDailyPaymentSerializer
    permission_classes = (IsAdminUser,)

class PersonaDailyPaymentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = PersonaDailyPaymentModel.objects.all()
    serializer_class = PersonaDailyPaymentCreateSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

# ---------- OverduePayment APIs ------------
class OverduePaymentListAPIView(ListAPIView):
    def get_queryset(self):
        return InstallmentModel.objects.filter(debt_amount__gt=0, installment_date__lte = timezone.now())
    serializer_class = InstallmentSerializer
    permission_classes = (IsAdminUser,)

class AllPaymentListAPIView(ListAPIView):
    def get_queryset(self):
        return InstallmentModel.objects.order_by("installment_date")
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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "payment":
            payment_data = {
                "changer": instance.id,
                "month": request.data.get("month"),
                "date": request.data.get("date")
            }
            dp_serializer = PersonaDailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)

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

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "payment":
            payment_data = {
                "servicer": instance.id,
                "month": request.data.get("month"),
                "date": request.data.get("date")
            }
            dp_serializer = PersonaDailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)

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

# ------------ Creditor APIs ------------
class CreditorListCreateAPIView(ListCreateAPIView):
    queryset = CreditorModel.objects.all()
    serializer_class = CreditorSerializer
    permission_classes = (IsAdminUser,)

class CreditorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = CreditorModel.objects.all()
    serializer_class = CreditorSerializer
    permission_classes = (IsAdminUser,)
    lookup_field = "id"

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        action = request.data.get("action")

        if action == "update":
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif action == "payment":
            payment_data = {
                "creditor": instance.id,
                "month": request.data.get("month"),
                "date": request.data.get("date")
            }
            dp_serializer = PersonaDailyPaymentCreateSerializer(data=payment_data)
            if dp_serializer.is_valid():
                dp_serializer.save()
                return Response(payment_data, status=status.HTTP_200_OK)
            return Response({"errors": "Error! Sent data was not correct."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"errors": "Invalid action specified."}, status=status.HTTP_400_BAD_REQUEST)
        


