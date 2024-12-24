from django.urls import path
from registrationapp.api import views

urlpatterns = [
    path('client-create/', views.ClientCreateAPIView.as_view(), name="client-create"),
    path('client-retrieve-update-destroy/<int:id>/', views.ClientRetrieveUpdateDestroyAPIView.as_view(), name="client-retrieve-update-destroy"),
    path('seller-create/', views.SellerCreateAPIView.as_view(), name="seller-create"),
    path('seller-retrieve-update-destroy/<int:id>/', views.SellerRetrieveUpdateDestroyAPIView.as_view(), name="seller-retrieve-update-destroy"),
    path('payment-create/', views.PaymentCreateAPIView.as_view(), name="payment-create"),
    path('payment-retrieve-update-destroy/<int:id>/', views.PaymentRetrieveUpdateDestroyAPIView.as_view(), name="payment-retrieve-update-destroy"),
    path('registration-list/', views.RegistrationListAPIView.as_view(), name="registration-list"),
    path('registration-create/', views.RegistrationCreateAPIView.as_view(), name="registration-create"),
    path('registration-retrieve-update-destroy/<int:id>/', views.RegistrationRetrieveUpdateDestroyAPIView.as_view(), name="registration-retrieve-update-destroy"),
    path('registration-installmentinfo-retrieve/<int:id>/', views.RegistrationInstallmentInfoRetrieveAPIView.as_view(), name="registration-installmentinfo-retrieve"),
    path('installmentinfo-retrieve-update/<int:id>/', views.InstallmentInfoRetrieveUpdateAPIView.as_view(), name="installmentinfo-retrieve-update"),
    path('installmentinfo-installment-list/<int:id>/', views.InstallmentInfoInstallmentListAPIView.as_view(), name="installmentinfo-installment-list"),
    path('installment-update/<int:id>/', views.InstallmentUpdateAPIView.as_view(), name="installment-update"),
    path('installment-destroy/<int:id>/', views.InstallmentDestroyAPIView.as_view(), name="installment-destroy"),
    path('dailypayment-list/', views.DailyPaymentListAPIView.as_view(), name="dailypayment-list"),
    path('dailypayment-retrieve-update-destroy/<int:id>/', views.DailyPaymentRetrieveUpdateDestroyAPIView.as_view(), name="dailypayment-retrieve-update-destroy"),
    path('overduepayment-list/', views.OverduePaymentListAPIView.as_view(), name="overduepayment-list"),
    path('changefilter-list/', views.ChangeFilterListAPIView.as_view(), name="changefilter-list"),
    path('changefilter-retrieve-update-destroy/<int:id>/', views.ChangeFilterRetrieveUpdateDestroyAPIView.as_view(), name="changefilter-retrieve-update-destroy"),
    path('seller-list/', views.SellerListAPIView.as_view(), name="seller-list"),
    path('filter-changer-list-create/', views.FilterChangerListCreateAPIView.as_view(), name="filter-changer-list-create"),
    path('servicer-list-create/', views.ServicerListCreateAPIView.as_view(), name="servicer-list-create"),
    path('servicer-retrieve-update-destroy/', views.ServicerRetrieveUpdateDestroyAPIView.as_view(), name="servicer-list-create"),
    path('shuttle-service-list/', views.ShuttleServiceListAPIView.as_view(), name="shuttle-service-list"),
    path('shuttle-service-create/', views.ShuttleServiceCreateAPIView.as_view(), name="shuttle-service-create"),
    path('shuttle-service-retrieve-update-destroy/', views.ShuttleServiceRetrieveUpdateDestroyAPIView.as_view(), name="shuttle-service-retrieve-update-destroy"),
]