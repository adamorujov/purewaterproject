from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from account.models import UserMoreInfoModel
from account.api.serializers import UserSerializer, UserCreateSerializer, UserMoreInfoCreateSerializer, UserMoreInfoSerializer
from account.api.permissions import IsSuperUser, IsOwner,  IsUserOwner


class UserListAPIView(ListAPIView):
    queryset = UserMoreInfoModel.objects.all()
    serializer_class = UserMoreInfoSerializer
    permission_classes = (IsAdminUser,)

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (IsSuperUser,)

class UserMoreInfoCreateAPIView(CreateAPIView):
    queryset = UserMoreInfoModel.objects.all()
    serializer_class = UserMoreInfoCreateSerializer
    permission_classes = (IsSuperUser,)

class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserMoreInfoModel
    permission_classes = (IsOwner,)
    lookup_field = "id"

class UserMoreInfoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserMoreInfoModel.objects.all()
    serializer_class = UserMoreInfoSerializer
    permission_classes = (IsUserOwner,)
    lookup_field = "id"