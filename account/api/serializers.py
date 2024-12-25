from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from account.models import UserMoreInfoModel
from rest_framework import serializers

class UserMoreInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserMoreInfoModel
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    usermoreinfo = UserMoreInfoSerializer()
    class Meta:
        model = User
        exclude = ("password",)

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password")

    def validate(self, data):
        validate_password(data["password"])
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            username = validated_data["username"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserMoreInfoCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field="username")
    class Meta:
        model = UserMoreInfoModel
        fields = "__all__"
