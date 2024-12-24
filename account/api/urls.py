from django.urls import path
from account.api import views

urlpatterns = [
    path('user-list/', views.UserListAPIView.as_view(), name="user-list"),
    path('user-create/', views.UserCreateAPIView.as_view(), name="user-create"),
    path('usermoreinfo-create/', views.UserMoreInfoCreateAPIView.as_view(), name="usermoreinfo-create"),
    path('user-retrieve-update-destroy/<int:id>/', views.UserRetrieveUpdateDestroyAPIView.as_view(), name="user-retrieve-update-destroy"),
    path('usermoreinfo-retrieve-update-destroy/<int:id>/', views.UserMoreInfoRetrieveUpdateDestroyAPIView.as_view(), name="usermoreinfo-retrieve-update-destroy"),
]