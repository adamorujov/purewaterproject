from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from account.models import UserMoreInfoModel
from account.api.serializers import UserSerializer, UserCreateSerializer, UserMoreInfoCreateSerializer, UserMoreInfoSerializer
from account.api.permissions import IsSuperUser, IsOwner,  IsUserOwner
from django.shortcuts import get_object_or_404


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
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
    serializer_class = UserCreateSerializer
    permission_classes = (IsOwner,)
    lookup_field = "username"

class UserMoreInfoRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = UserMoreInfoModel.objects.all()
    serializer_class = UserMoreInfoCreateSerializer
    def get_object(self):
        username = self.kwargs.get("username")
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserMoreInfoModel, user=user)
    permission_classes = (IsUserOwner,)
    lookup_field = "username"
    